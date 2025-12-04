import tkinter as tk
from tkinter import ttk
from model.recipe_model import RecipeModel
from utils.image_manager import ImageManager
from view.common_header import CommonHeader


class ListView(ttk.Frame):
    # 一覧画面（2列グリッドのカードビュー）

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)

        self.controller = controller
        self.model = RecipeModel()
        self.image_manager = ImageManager()

        # ヘッダーの表示
        self.header = CommonHeader(self, controller)
        self.header.pack(fill="x")

        # スクロール可能エリアの作成
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        # スクロール設定
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # レシピ一覧の描画
        self.draw_recipe_cards()

  