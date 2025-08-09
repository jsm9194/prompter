import tkinter as tk
from utils import similarity

HIGHLIGHT_THRESHOLD = 0.72  # 보수적 진행

class PrompterUI:
    def __init__(self, root: tk.Tk, lines: list[str], on_prev, on_next, on_quit):
        self.root = root
        self.lines = lines
        self.idx = 0

        root.title("Prompt Demo")
        root.geometry("900x360")
        root.configure(bg="#111111")

        self.curr_label = tk.Label(root, text="", font=("맑은 고딕", 32, "bold"),
                                   fg="#FFFFFF", bg="#111111", wraplength=840, justify="center")
        self.next_label = tk.Label(root, text="", font=("맑은 고딕", 22),
                                   fg="#AAAAAA", bg="#111111", wraplength=840, justify="center")
        # 유사도/최근 인식 텍스트 표기 영역
        self.info_label = tk.Label(root, text="유사도: - / 인식: -", font=("맑은 고딕", 14),
                                   fg="#888888", bg="#111111", wraplength=840, justify="center")

        self.curr_label.pack(pady=(30, 10))
        self.next_label.pack(pady=(0, 10))
        self.info_label.pack(pady=(0, 10))

        root.bind("<Escape>", lambda e: on_quit())
        root.bind("<F11>", self.toggle_fullscreen)
        root.bind("<space>", lambda e: on_next())
        root.bind("<Return>", lambda e: on_next())
        root.bind("<Down>", lambda e: on_next())
        root.bind("<Up>", lambda e: on_prev())

        self.is_fullscreen = False
        self.update_labels()

    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes("-fullscreen", self.is_fullscreen)

    def update_labels(self):
        curr = self.lines[self.idx] if self.idx < len(self.lines) else ""
        nxt  = self.lines[self.idx + 1] if self.idx + 1 < len(self.lines) else ""
        self.curr_label.config(text=curr)
        self.next_label.config(text=nxt)
        self.curr_label.config(fg="#FFFFFF")
        self.info_label.config(text="유사도: - / 인식: -")

    def try_advance_with_text(self, recognized_text: str):
        if self.idx >= len(self.lines):
            return
        target = self.lines[self.idx]
        sim = similarity(recognized_text, target)

        # 하이라이트 컬러
        if   sim >= 0.90: fg = "#7CFC00"
        elif sim >= 0.75: fg = "#ADFF2F"
        elif sim >= 0.60: fg = "#FFD700"
        else:             fg = "#FFFFFF"
        self.curr_label.config(fg=fg)

        # 유사도/인식 텍스트 출력 (길면 잘라서)
        short_rec = (recognized_text[:60] + "…") if len(recognized_text) > 60 else recognized_text
        self.info_label.config(text=f"유사도: {int(sim*100)}% / 인식: {short_rec}")

        if sim >= HIGHLIGHT_THRESHOLD:
            self.idx += 1
            self.update_labels()

    def manual_prev(self):
        if self.idx > 0:
            self.idx -= 1
            self.update_labels()

    def manual_next(self):
        if self.idx < len(self.lines):
            self.idx += 1
            self.update_labels()
