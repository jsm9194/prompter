import threading
from typing import Callable, Optional

class RecognizerBase:
    # STT 결과를 콜백으로 전달하는 공통 인터페이스
    def __init__(self) -> None:
        self._on_text: Optional[Callable[[str], None]] = None
        self._running = False
        self._thread: Optional[threading.Thread] = None

    def start(self, on_text: Callable[[str], None]) -> None:
        self._on_text = on_text
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._running = False

    def _emit(self, text: str) -> None:
        if self._on_text:
            self._on_text(text)

    def _run(self) -> None:
        raise NotImplementedError
