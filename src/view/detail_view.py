import tkinter as tk
from tkinter import ttk
from PIL import ImageTk

from model.recipe_model import RecipeModel
from utils.image_manager import ImageManager
from view.common_header import CommonHeader
from view.components.scroll_frame import ScrollFrame


class DetailView(ttk.Frame):
    # 詳細画面（スクロール対応・ナチュラルデザイン）

    def __init__(self, parent, controller, recipe_id):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.model = RecipeModel()
        self.image_manager = ImageManager()

        self.configure(style="Base.TFrame")

        # ScrollFrame で全体を包む
        scroll = ScrollFrame(self)
        scroll.pack(fill="both", expand=True)

        content = scroll.inner

        # レシピ全件読み込み
        self.recipes = self.model.load_all()
        self.current_index = self.get_recipe_index(recipe_id)

        # ヘッダー
        header = CommonHeader(content, controller)
        header.pack(fill="x")

        # タイトル
        self.title_label = ttk.Label(content, text="", style="Title.TLabel")
        self.title_label.pack(pady=15)

        # 画像 + 材料エリア
        mid_frame = ttk.Frame(content, style="Base.TFrame")
        mid_frame.pack(fill="x", padx=20, pady=10)

        # 画像カード
        self.image_frame = ttk.Frame(mid_frame, style="Card.TFrame", padding=10)
        self.image_frame.grid(row=0, column=0, padx=20, pady=5)

        self.image_label = ttk.Label(self.image_frame, background="#FFFFFF")
        self.image_label.pack()

        # 材料カード
        self.ingredients_frame = ttk.Frame(mid_frame, style="Card.TFrame", padding=15)
        self.ingredients_frame.grid(row=0, column=1, padx=20, pady=5, sticky="n")

        # 作り方カード
        self.steps_frame = ttk.Frame(content, style="Card.TFrame", padding=15)
        self.steps_frame.pack(fill="x", padx=20, pady=20)

        # 戻る/次へ
        nav_frame = ttk.Frame(content, style="Base.TFrame")
        nav_frame.pack(pady=10)

        ttk.Button(
            nav_frame,
            text="戻る",
            style="Header.TButton",
            command=self.show_prev
        ).pack(side="left", padx=20)

        ttk.Button(
            nav_frame,
            text="次へ",
            style="Header.TButton",
            command=self.show_next
        ).pack(side="left", padx=20)

        # 初回表示
        self.update_view()

    # レシピIDのインデックス取得
    def get_recipe_index(self, recipe_id):
        for i, r in enumerate(self.recipes):
            if r["id"] == str(recipe_id):
                return i
        return 0

    # 表示更新
    def update_view(self):
        recipe = self.recipes[self.current_index]

        self.title_label.config(text=recipe["title"])

        # 画像
        img = self.image_manager.get_detail_image(recipe["image_path"])
        self.tk_img = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.tk_img)

        # 材料
        for w in self.ingredients_frame.winfo_children():
            w.destroy()

        ttk.Label(self.ingredients_frame, text="材料", style="Heading.TLabel").pack(anchor="w", pady=(0, 10))

        for i in range(1, 10):
            ttk.Label(
                self.ingredients_frame,
                text=f"{i}. {recipe.get(f'ingredient{i}', '')}",
                style="TLabel"
            ).pack(anchor="w", pady=2)

        # 作り方
        for w in self.steps_frame.winfo_children():
            w.destroy()

        ttk.Label(self.steps_frame, text="作り方", style="Heading.TLabel").pack(anchor="w", pady=(0, 10))

        for i in range(1, 7):
            ttk.Label(
                self.steps_frame,
                text=f"{i}. {recipe.get(f'step{i}', '')}",
                style="TLabel"
            ).pack(anchor="w", pady=3)

    def show_prev(self):
        self.current_index = (self.current_index - 1) % len(self.recipes)
        self.update_view()

    def show_next(self):
        self.current_index = (self.current_index + 1) % len(self.recipes)
        self.update_view()
