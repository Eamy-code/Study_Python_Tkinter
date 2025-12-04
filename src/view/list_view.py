import tkinter as tk
from tkinter import ttk
from PIL import ImageTk

from model.recipe_model import RecipeModel
from utils.image_manager import ImageManager
from view.common_header import CommonHeader


class ListView(ttk.Frame):
    # おしゃれなナチュラル系カードで一覧表示する画面

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)

        self.controller = controller
        self.model = RecipeModel()
        self.image_manager = ImageManager()

        # 背景色をクリーム色に統一
        self.configure(style="Base.TFrame")

        # ヘッダー表示
        self.header = CommonHeader(self, controller)
        self.header.pack(fill="x")

        # スクロール可能キャンバス
        self.canvas = tk.Canvas(self, bg="#FFF8E7", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)

        self.scrollable_frame = ttk.Frame(self.canvas, style="Base.TFrame")

        # Canvas に Frame を乗せる
        self.canvas_frame = self.canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw"
        )

        # スクロール設定
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # レシピ一覧の描画
        self.draw_recipe_cards()

    # レシピカードの描画
    def draw_recipe_cards(self):
        recipes = self.model.load_all()

        # 画像消失対策用
        self.thumbnail_images = []

        # カード配置設定
        col_count = 2
        row = 0
        col = 0

        if not recipes:
            ttk.Label(
                self.scrollable_frame,
                text="レシピがありません。",
                style="Heading.TLabel"
            ).grid(row=0, column=0, padx=20, pady=20)
            return

        for recipe in recipes:

            # カード全体（丸角風・影風）
            card = ttk.Frame(
                self.scrollable_frame,
                style="Card.TFrame",
                padding=15
            )
            card.grid(row=row, column=col, padx=20, pady=20, sticky="n")

            # 画像
            image = self.image_manager.get_thumbnail(recipe["image_path"])
            tk_img = ImageTk.PhotoImage(image)
            self.thumbnail_images.append(tk_img)

            img_label = tk.Label(
                card,
                image=tk_img,
                bg="#FFFFFF",
                bd=0,
                highlightthickness=0
            )
            img_label.pack()

            # タイトル
            title_btn = ttk.Button(
                card,
                text=recipe["title"],
                style="CardTitle.TButton",
                command=lambda rid=recipe["id"]: self.controller.show_detail_view(rid)
            )
            title_btn.pack(pady=10)

            # カードクリックで詳細へ（画像クリック対応）
            img_label.bind(
                "<Button-1>",
                lambda e, rid=recipe["id"]: self.controller.show_detail_view(rid)
            )

            # グリッド制御
            col += 1
            if col >= col_count:
                col = 0
                row += 1
