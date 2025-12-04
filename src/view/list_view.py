import tkinter as tk
from tkinter import ttk
from PIL import ImageTk

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

    # レシピカード一覧を描画する
    def draw_recipe_cards(self):
        recipes = self.model.load_all()

        # レシピが1件もない場合
        if not recipes:
            empty_label = ttk.Label(self.scrollable_frame, text="レシピがありません。", font=("Arial", 14))
            empty_label.grid(row=0, column=0, pady=20)
            return

        # カード用の画像保持（GC対策）
        self.thumbnail_images = []

        # レイアウト設定
        col_count = 2
        row = 0
        col = 0

        for recipe in recipes:
            card = ttk.Frame(self.scrollable_frame, padding=10)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="n")

            # 画像の準備
            image = self.image_manager.get_thumbnail(recipe["image_path"])
            tk_image = ImageTk.PhotoImage(image)
            self.thumbnail_images.append(tk_image)

            # 画像ボタン（クリックで詳細へ）
            img_button = tk.Button(
                card,
                image=tk_image,
                command=lambda rid=recipe["id"]: self.controller.show_detail_view(rid),
                borderwidth=0
            )
            img_button.pack()

            # タイトル（クリックでも詳細へ）
            title_button = ttk.Button(
                card,
                text=recipe["title"],
                command=lambda rid=recipe["id"]: self.controller.show_detail_view(rid)
            )
            title_button.pack(pady=5)

            # 2列レイアウト制御
            col += 1
            if col >= col_count:
                col = 0
                row += 1
