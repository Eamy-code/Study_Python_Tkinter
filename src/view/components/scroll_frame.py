import tkinter as tk
from tkinter import ttk


class ScrollFrame(ttk.Frame):
    # 安全なスクロール管理（複数フレーム競合対策済み）

    def __init__(self, parent):
        super().__init__(parent)

        self.canvas = tk.Canvas(self, highlightthickness=0, bg="#FFF8E7")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(self, orient="vertical",
                                       command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.inner = ttk.Frame(self.canvas, style="Base.TFrame")
        self.window = self.canvas.create_window((0, 0),
                                                window=self.inner,
                                                anchor="nw")

        self.inner.bind("<Configure>", self._update_scrollregion)
        self.canvas.bind("<Configure>", self._resize_inner)

        self.bind_events()

    # スクロール領域更新
    def _update_scrollregion(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # inner の幅を canvas に合わせる
    def _resize_inner(self, event):
        self.canvas.itemconfig(self.window, width=event.width)

    # イベントバインド
    def bind_events(self):
        self.canvas.bind("<Enter>", lambda e: self._bind_wheel())
        self.canvas.bind("<Leave>", lambda e: self._unbind_wheel())

    def _bind_wheel(self):
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind("<Button-4>", self._on_mousewheel_mac)
        self.canvas.bind("<Button-5>", self._on_mousewheel_mac)

    def _unbind_wheel(self):
        self.canvas.unbind("<MouseWheel>")
        self.canvas.unbind("<Button-4>")
        self.canvas.unbind("<Button-5>")

    # Windows / Linux
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # macOS
    def _on_mousewheel_mac(self, event):
        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")
