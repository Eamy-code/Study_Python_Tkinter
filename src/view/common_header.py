import tkinter as tk
from tkinter import ttk


class CommonHeader(ttk.Frame):
    # ナチュラルで柔らかい印象の共通ヘッダー

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)

        self.controller = controller

        # 背景色（Header自身に設定）
        self.configure(style="Header.TFrame")

        # タイトルラベル
        title = ttk.Label(
            self,
            text="RecipeDesk",
            style="HeaderTitle.TLabel"
        )
        title.grid(row=0, column=0, sticky="w", padx=20, pady=15)

        # 右側ボタンまとめフレーム
        btn_frame = ttk.Frame(self, style="Header.TFrame")
        btn_frame.grid(row=0, column=1, sticky="e", padx=20)

        # 一覧へ
        list_btn = ttk.Button(
            btn_frame,
            text="一覧へ",
            style="Header.TButton",
            command=self.controller.show_list_view
        )
        list_btn.pack(side="left", padx=5)

        # 登録へ
        create_btn = ttk.Button(
            btn_frame,
            text="登録へ",
            style="Header.TButton",
            command=self.controller.show_create_view
        )
        create_btn.pack(side="left", padx=5)

        # グリッド調整
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
