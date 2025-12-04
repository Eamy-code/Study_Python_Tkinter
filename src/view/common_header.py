import tkinter as tk
from tkinter import ttk

class CommonHeader(ttk.Frame):
    # 共通ヘッダー（RecipeDesk タイトル・画面遷移ボタン）

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)

        self.controller = controller

        # タイトルラベル
        self.title_label = ttk.Label(
            self,
            text="RecipeDesk",
            font=("Arial", 20, "bold")
        )
        self.title_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

        # ボタンをまとめるフレーム（右寄せ）
        self.button_frame = ttk.Frame(self)
        self.button_frame.grid(row=0, column=1, sticky="e", padx=10)

        # 一覧ページへ遷移するボタン
        self.list_button = ttk.Button(
            self.button_frame,
            text="一覧へ",
            command=self.controller.show_list_view
        )
        self.list_button.pack(side="left", padx=5)

        # 登録ページへ遷移するボタン
        self.create_button = ttk.Button(
            self.button_frame,
            text="登録へ",
            command=self.controller.show_create_view
        )
        self.create_button.pack(side="left", padx=5)

        # グリッド調整（左が可変幅、右は固定）
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
