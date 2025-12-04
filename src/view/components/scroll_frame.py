import tkinter as tk
from tkinter import ttk

# 任意の画面をスクロール可能にする共通コンポーネント
class ScrollFrame(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        # Canvas（スクロール領域）
        self.canvas = tk.Canvas(self, highlightthickness=0, bg="#FFF8E7")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        # Canvas と Scrollbar の紐付け
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # 内部フレーム
        self.inner = ttk.Frame(self, style="Base.TFrame")
        self.window = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")

        # 内部フレームのサイズに応じてスクロール領域更新
        self.inner.bind("<Configure>", self._update_scrollregion)

        # Canvas 自体のサイズ変更に応じて inner の幅を合わせる
        self.canvas.bind("<Configure>", self._resize_inner)

    # スクロール領域を更新
    def _update_scrollregion(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # inner の幅を Canvas に合わせる
    def _resize_inner(self, event):
        self.canvas.itemconfig(self.window, width=event.width)
