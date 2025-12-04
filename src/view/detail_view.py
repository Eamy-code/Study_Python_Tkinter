import tkinter as tk
from tkinter import ttk
from PIL import ImageTk

from model.recipe_model import RecipeModel
from utils.image_manager import ImageManager
from view.common_header import CommonHeader


class DetailView(ttk.Frame):
    # 詳細画面（画像・材料・ステップ・次へ戻る）

    def __init__(self, parent, controller, recipe_id):
        ttk.Frame.__init__(self, parent)

        self.controller = controller
        self.model = RecipeModel()
        self.image_manager = ImageManager()

        # 現在のレシピ ID とインデックス管理
        self.recipes = self.model.load_all()
        self.current_index = self._get_recipe_index(recipe_id)

        # ヘッダー表示
        self.header = CommonHeader(self, controller)
        self.header.pack(fill="x")

        # タイトル表示用ラベル
        self.title_label = ttk.Label(self, text="", font=("Arial", 18, "bold"))
        self.title_label.pack(pady=10)

        # メインコンテンツフレーム（画像＋材料）
        content_frame = ttk.Frame(self)
        content_frame.pack(fill="x", pady=10)

        # 左：画像フレーム
        self.image_label = ttk.Label(content_frame)
        self.image_label.grid(row=0, column=0, padx=20)

        # 右：材料一覧フレーム
        self.ingredients_frame = ttk.Frame(content_frame)
        self.ingredients_frame.grid(row=0, column=1, padx=20)

        # 下：作り方フレーム
        self.steps_frame = ttk.Frame(self)
        self.steps_frame.pack(fill="x", padx=20, pady=20)

        # 最下段：戻る / 次へ ボタン
        nav_frame = ttk.Frame(self)
        nav_frame.pack(pady=10)

        self.prev_button = ttk.Button(
            nav_frame,
            text="戻る",
            command=self.show_prev
        )
        self.prev_button.pack(side="left", padx=20)

        self.next_button = ttk.Button(
            nav_frame,
            text="次へ",
            command=self.show_next
        )
        self.next_button.pack(side="left", padx=20)

        # レシピ内容を初回表示
        self.update_view()

    # 指定 ID のレシピインデックスを取得する
    def _get_recipe_index(self, recipe_id):
        for i, r in enumerate(self.recipes):
            if r["id"] == str(recipe_id):
                return i
        return 0

    # 画面表示を更新する
    def update_view(self):
        recipe = self.recipes[self.current_index]

        # タイトル
        self.title_label.config(text=recipe["title"])

        # 画像表示
        image = self.image_manager.get_detail_image(recipe["image_path"])
        self.tk_image = ImageTk.PhotoImage(image)  # 保存しないとGCで消える
        self.image_label.config(image=self.tk_image)

        # 材料一覧をクリアして再描画
        for widget in self.ingredients_frame.winfo_children():
            widget.destroy()

        ttk.Label(self.ingredients_frame, text="材料", font=("Arial", 14, "bold")).pack(anchor="w")

        for i in range(1, 10):
            ing = recipe.get(f"ingredient{i}", "")
            ttk.Label(self.ingredients_frame, text=f"{i}. {ing}").pack(anchor="w")

        # 作り方一覧をクリアして再描画
        for widget in self.steps_frame.winfo_children():
            widget.destroy()

        ttk.Label(self.steps_frame, text="作り方", font=("Arial", 14, "bold")).pack(anchor="w")

        for i in range(1, 7):
            step = recipe.get(f"step{i}", "")
            ttk.Label(self.steps_frame, text=f"{i}. {step}").pack(anchor="w", pady=2)

    # 前のレシピへ移動（ループ式）
    def show_prev(self):
        self.current_index = (self.current_index - 1) % len(self.recipes)
        self.update_view()

    # 次のレシピへ移動（ループ式）
    def show_next(self):
        self.current_index = (self.current_index + 1) % len(self.recipes)
        self.update_view()
