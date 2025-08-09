import time
from recognizer_base import RecognizerBase

class RecognizerDummy(RecognizerBase):
    # 실제 마이크 인식 없이 수동 진행을 위한 더미
    def _run(self) -> None:
        while self._running:
            time.sleep(0.1)
