import tkinter as tk
from tkinter import ttk


# 縦スクロール＋マウスホイール対応の共通スクロールコンテナ
class ScrollFrame(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        # Canvas（スクロール領域）
        self.canvas = tk.Canvas(self, highlightthickness=0, bg="#FFF8E7")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # inner Frame
        self.inner = ttk.Frame(self.canvas, style="Base.TFrame")
        self.window = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")

        # サイズ変更時のスクロール領域更新
        self.inner.bind("<Configure>", self._update_scrollregion)
        self.canvas.bind("<Configure>", self._resize_inner)

        # マウスホイール対応
        self.bind_events()

    # スクロール領域更新
    def _update_scrollregion(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # inner の幅を canvas に合わせる
    def _resize_inner(self, event):
        self.canvas.itemconfig(self.window, width=event.width)

    # マウスホイールイベントの紐付け
    def bind_events(self):
        # Windows / Linux
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        # Mac（ホイールイベント名が異なる）
        self.canvas.bind_all("<Button-4>", self._on_mousewheel_mac)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel_mac)

    # Windows / Linux 用スクロール
    def _on_mousewheel(self, event):
        # event.delta は Windows で120単位、Linuxは±1が来る
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # Mac 用スクロール
    def _on_mousewheel_mac(self, event):
        if event.num == 4:  # 上スクロール
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:  # 下スクロール
            self.canvas.yview_scroll(1, "units")
