import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk

from model.recipe_model import RecipeModel
from utils.image_manager import ImageManager
from view.common_header import CommonHeader
from view.components.scroll_frame import ScrollFrame


class DetailView(ttk.Frame):
    # レシピ詳細画面（動的材料・動的手順＋スクロール安定＋ヘッダー固定）

    def __init__(self, parent, controller, recipe_id):
        ttk.Frame.__init__(self, parent)

        self.controller = controller
        self.model = RecipeModel()
        self.image_manager = ImageManager()
        self.recipe_id = recipe_id

        self.configure(style="Base.TFrame")

        recipe = self.model.find_by_id(recipe_id)
        if not recipe:
            messagebox.showerror("エラー", "レシピが見つかりません。")
            controller.show_list_view()
            return
        self.recipe = recipe

        # ヘッダー（固定）
        header = CommonHeader(self, controller)
        header.pack(fill="x")

        # ScrollFrame（中身のみスクロール）
        scroll = ScrollFrame(self)
        scroll.pack(fill="both", expand=True)

        content = scroll.inner

        # タイトル
        title_label = ttk.Label(content, text=recipe["title"], style="Title.TLabel")
        title_label.pack(pady=15)

        # 上段（画像＋材料）
        mid = ttk.Frame(content, style="Base.TFrame")
        mid.pack(fill="x", padx=20, pady=10)

        # 画像
        img_card = ttk.Frame(mid, style="Card.TFrame", padding=10)
        img_card.grid(row=0, column=0, padx=20, pady=5)

        img = self.image_manager.get_detail_image(recipe["image_path"])
        self.tk_img = ImageTk.PhotoImage(img)

        ttk.Label(img_card, image=self.tk_img, background="#FFFFFF").pack()

        # 材料
        ing_card = ttk.Frame(mid, style="Card.TFrame", padding=15)
        ing_card.grid(row=0, column=1, padx=20, pady=5, sticky="n")

        ttk.Label(ing_card, text="材料", style="Heading.TLabel").pack(anchor="w", pady=(0, 10))

        for ing in recipe["ingredients"]:
            line = f"{ing['name']} … {ing['amount']}"
            ttk.Label(ing_card, text=line, style="TLabel").pack(anchor="w", pady=2)

        # 作り方
        steps_card = ttk.Frame(content, style="Card.TFrame", padding=15)
        steps_card.pack(fill="x", padx=20, pady=20)

        ttk.Label(steps_card, text="作り方", style="Heading.TLabel").pack(anchor="w", pady=(0, 10))

        for step in recipe["steps"]:
            s = f"{step['step_no']}. {step['text']}"
            ttk.Label(steps_card, text=s, style="TLabel").pack(anchor="w", pady=3)

        # 編集＆削除ボタン
        btn_area = ttk.Frame(content, style="Base.TFrame")
        btn_area.pack(pady=20)

        edit_btn = ttk.Button(
            btn_area,
            text="編集する",
            style="Header.TButton",
            command=lambda: controller.show_edit_view(self.recipe_id)
        )
        edit_btn.pack(side="left", padx=10)

        delete_btn = ttk.Button(
            btn_area,
            text="削除する",
            style="Header.TButton",
            command=self.delete_recipe
        )
        delete_btn.pack(side="left", padx=10)

    # 削除処理
    def delete_recipe(self):
        ok = messagebox.askyesno("確認", "本当に削除しますか？")
        if not ok:
            return

        self.model.delete(self.recipe_id)
        messagebox.showinfo("完了", "レシピを削除しました。")

        # 一覧へ戻る
        self.controller.show_list_view()
