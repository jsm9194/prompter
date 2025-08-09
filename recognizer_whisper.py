import queue
import numpy as np
from recognizer_base import RecognizerBase

try:
    from faster_whisper import WhisperModel  # type: ignore
    HAS_WHISPER = True
except Exception:
    HAS_WHISPER = False

try:
    import sounddevice as sd  # type: ignore
    HAS_SD = True
except Exception:
    HAS_SD = False

SAMPLE_RATE = 16000
BLOCK_SECONDS = 1.5
MODEL_SIZE = "small"  # base / small / medium

class RecognizerWhisper(RecognizerBase):
    def __init__(self) -> None:
        super().__init__()
        if not (HAS_WHISPER and HAS_SD):
            raise RuntimeError("faster-whisper 또는 sounddevice가 설치되지 않았습니다.")
        self._audio_q: "queue.Queue[np.ndarray]" = queue.Queue()
        # device='auto': GPU 있으면 cuda, 없으면 cpu
        self._model = WhisperModel(MODEL_SIZE, device="auto", compute_type="int8")

    def _audio_callback(self, indata, frames, time_, status):
        if not self._running:
            return
        data = indata.copy().reshape(-1)  # mono float32
        self._audio_q.put(data)

    def _run(self) -> None:
        stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="float32",
            blocksize=int(SAMPLE_RATE * BLOCK_SECONDS),
            callback=self._audio_callback,
        )
        stream.start()

        buffer = np.zeros(0, dtype=np.float32)

        try:
            while self._running:
                try:
                    chunk = self._audio_q.get(timeout=0.2)
                except queue.Empty:
                    continue

                buffer = np.concatenate([buffer, chunk])

                # 일정 길이 이상 모였을 때만 인식 (보수적)
                min_len = int(SAMPLE_RATE * 2.5)
                if len(buffer) < min_len:
                    continue

                segments, _ = self._model.transcribe(
                    buffer,
                    language="ko",
                    vad_filter=True
                )
                text = "".join(s.text for s in segments).strip()
                if text:
                    self._emit(text)

                # 버퍼는 최근 5초만 유지
                keep = int(SAMPLE_RATE * 5)
                if len(buffer) > keep:
                    buffer = buffer[-keep:]
        finally:
            stream.stop()
            stream.close()
