import tkinter as tk
from pathlib import Path

from ui import PrompterUI

# 설정: "dummy" 또는 "whisper"
recognizer_backend = "whisper"  # whisper로 바꾸면 실제 STT 사용

SCRIPT_PATH = Path(__file__).with_name("script.txt")

def load_lines() -> list[str]:
    if not SCRIPT_PATH.exists():
        return []
    raw = SCRIPT_PATH.read_text(encoding="utf-8")
    lines = [ln.strip() for ln in raw.splitlines() if ln.strip()]
    if not lines:
        lines = [
            "script.txt에 한 줄당 한 문장씩 입력하세요.",
            "스페이스/엔터 키로 다음 문장으로 이동합니다.",
            "F11로 전체화면 토글, ESC로 종료합니다.",
            "whisper 모드로 전환하면 마이크 인식에 따라 자동 진행됩니다.",
        ]
    return lines

def run_app():
    root = tk.Tk()
    lines = load_lines()

    def on_prev():
        ui.manual_prev()

    def on_next():
        ui.manual_next()

    def on_quit():
        try:
            recognizer.stop()
        except Exception:
            pass
        root.destroy()

    ui = PrompterUI(root, lines, on_prev, on_next, on_quit)

    # STT 백엔드 로드
    global recognizer
    if recognizer_backend == "whisper":
        try:
            from recognizer_whisper import RecognizerWhisper
            recognizer = RecognizerWhisper()
        except Exception as e:
            print("[whisper] 백엔드 로드 실패:", e)
            print("dummy 백엔드로 대체합니다.")
            from recognizer_dummy import RecognizerDummy
            recognizer = RecognizerDummy()
    else:
        from recognizer_dummy import RecognizerDummy
        recognizer = RecognizerDummy()

    def on_text(text: str):
        ui.try_advance_with_text(text)

    recognizer.start(on_text)

    root.mainloop()

if __name__ == "__main__":
    run_app()
