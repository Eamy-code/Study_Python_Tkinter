import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import ImageTk

from model.recipe_model import RecipeModel
from utils.image_manager import ImageManager
from view.common_header import CommonHeader
from view.components.scroll_frame import ScrollFrame


class EditView(ttk.Frame):
    # レシピ編集画面（CreateView の機能 + 初期値セット + update 呼び出し）

    def __init__(self, parent, controller, recipe_id):
        ttk.Frame.__init__(self, parent)

        self.controller = controller
        self.model = RecipeModel()
        self.image_manager = ImageManager()

        self.recipe_id = recipe_id
        self.recipe = self.model.find_by_id(recipe_id)

        self.selected_image_path = self.recipe["image_path"]
        self.preview_image = None

        self.configure(style="Base.TFrame")

        # ヘッダー固定
        header = CommonHeader(self, controller)
        header.pack(fill="x")

        # スクロール
        scroll = ScrollFrame(self)
        scroll.pack(fill="both", expand=True)
        content = scroll.inner

        # フォームカード
        form = ttk.Frame(content, style="Card.TFrame", padding=20)
        form.pack(fill="x", padx=30, pady=20)

        # タイトル
        ttk.Label(form, text="タイトル", style="Heading.TLabel").pack(anchor="w")
        self.title_entry = ttk.Entry(form)
        self.title_entry.pack(fill="x", pady=(0, 15))
        self.title_entry.insert(0, self.recipe["title"])

        # 材料
        ttk.Label(form, text="材料（材料名 + 量）", style="Heading.TLabel").pack(anchor="w")

        self.ingredients_frame = ttk.Frame(form, style="Base.TFrame")
        self.ingredients_frame.pack(fill="x")

        self.ingredient_rows = []
        for ing in self.recipe["ingredients"]:
            self.add_ingredient_row(name=ing["name"], amount=ing["amount"])

        ttk.Button(
            form, text="+ 材料を追加", style="Header.TButton",
            command=self.add_ingredient_row
        ).pack(anchor="w", pady=10)

        # 作り方
        ttk.Label(form, text="作り方", style="Heading.TLabel").pack(anchor="w", pady=(20, 5))

        self.steps_frame = ttk.Frame(form, style="Base.TFrame")
        self.steps_frame.pack(fill="x")

        self.step_rows = []
        for step in self.recipe["steps"]:
            self.add_step_row(text=step["text"])

        ttk.Button(
            form, text="+ 作り方を追加", style="Header.TButton",
            command=self.add_step_row
        ).pack(anchor="w", pady=10)

        # 画像
        ttk.Label(form, text="画像", style="Heading.TLabel").pack(anchor="w", pady=(20, 10))
        img_card = ttk.Frame(form, style="Card.TFrame", padding=10)
        img_card.pack(fill="x")

        ttk.Button(
            img_card, text="画像を選択", style="Header.TButton",
            command=self.select_image
        ).pack(anchor="w")

        img = self.image_manager.get_thumbnail(self.selected_image_path, size=(200, 200))
        self.preview_image = ImageTk.PhotoImage(img)
        self.preview_label = ttk.Label(img_card, image=self.preview_image)
        self.preview_label.pack()

        # Submit
        ttk.Button(
            content, text="更新（Update）", style="Header.TButton",
            command=self.update_recipe
        ).pack(pady=20)

    # 材料行追加
    def add_ingredient_row(self, name="", amount=""):
        row = ttk.Frame(self.ingredients_frame, style="Base.TFrame")
        row.pack(fill="x", pady=3)

        name_entry = ttk.Entry(row)
        name_entry.insert(0, name)
        name_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

        amount_entry = ttk.Entry(row, width=15)
        amount_entry.insert(0, amount)
        amount_entry.pack(side="left", padx=(0, 5))

        del_btn = ttk.Button(
            row, text="−", width=2,
            command=lambda rf=row: self.remove_ingredient_row(rf)
        )
        del_btn.pack(side="left")

        self.ingredient_rows.append((row, name_entry, amount_entry))

    def remove_ingredient_row(self, row):
        if len(self.ingredient_rows) <= 1:
            messagebox.showwarning("注意", "材料は最低 1 行必要です。")
            return

        self.ingredient_rows = [r for r in self.ingredient_rows if r[0] != row]
        row.destroy()

    # 作り方行追加
    def add_step_row(self, text=""):
        row = ttk.Frame(self.steps_frame, style="Base.TFrame")
        row.pack(fill="x", pady=3)

        entry = ttk.Entry(row)
        entry.insert(0, text)
        entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

        del_btn = ttk.Button(
            row, text="−", width=2,
            command=lambda rf=row: self.remove_step_row(rf)
        )
        del_btn.pack(side="left")

        self.step_rows.append((row, entry))

    def remove_step_row(self, row):
        if len(self.step_rows) <= 1:
            messagebox.showwarning("注意", "作り方は最低 1 行必要です。")
            return

        self.step_rows = [r for r in self.step_rows if r[0] != row]
        row.destroy()

    # 画像選択
    def select_image(self):
        path = filedialog.askopenfilename(
            filetypes=[("画像ファイル", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if not path:
            return

        self.selected_image_path = path
        img = self.image_manager.get_thumbnail(path, size=(200, 200))
        self.preview_image = ImageTk.PhotoImage(img)
        self.preview_label.config(image=self.preview_image)

    # 更新ボタン押下
    def update_recipe(self):
        title = self.title_entry.get()
        if not title:
            messagebox.showerror("エラー", "タイトルは必須です。")
            return

        ingredients = []
        for frame, name_entry, amount_entry in self.ingredient_rows:
            name = name_entry.get().strip()
            amount = amount_entry.get().strip()
            if name:
                ingredients.append({"name": name, "amount": amount})

        steps = []
        for frame, entry in self.step_rows:
            text = entry.get().strip()
            if text:
                steps.append(text)

        img_path = self.selected_image_path

        data = {
            "title": title,
            "image_path": img_path,
            "ingredients": ingredients,
            "steps": steps
        }

        self.model.update(self.recipe_id, data)

        messagebox.showinfo("完了", "レシピを更新しました")
        self.controller.show_detail_view(self.recipe_id)
