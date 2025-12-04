import tkinter as tk
from tkinter import ttk, filedialog
from PIL import ImageTk

from model.recipe_model import RecipeModel
from utils.image_manager import ImageManager
from view.common_header import CommonHeader
from view.components.scroll_frame import ScrollFrame


class CreateView(ttk.Frame):
    # レシピ登録画面（スクロール対応＋レスポンシブ）

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)

        self.controller = controller
        self.model = RecipeModel()
        self.image_manager = ImageManager()

        self.selected_image_path = ""
        self.preview_image = None

        self.configure(style="Base.TFrame")

        # ScrollFrame（縦スクロール）
        scroll = ScrollFrame(self)
        scroll.pack(fill="both", expand=True)

        content = scroll.inner

        # ヘッダー
        header = CommonHeader(content, controller)
        header.pack(fill="x")

        # フォームカード（レスポンシブ）
        form_card = ttk.Frame(content, style="Card.TFrame", padding=20)
        form_card.pack(fill="x", padx=30, pady=20)

        # タイトル
        ttk.Label(form_card, text="タイトル", style="Heading.TLabel").pack(anchor="w")
        self.title_entry = ttk.Entry(form_card)
        self.title_entry.pack(anchor="w", fill="x", pady=(0, 15))

        # 材料
        ttk.Label(form_card, text="材料（1〜9）", style="Heading.TLabel").pack(anchor="w", pady=(0, 5))
        self.ingredient_entries = []
        for i in range(1, 10):
            entry = ttk.Entry(form_card)
            entry.pack(anchor="w", fill="x", pady=3)
            self.ingredient_entries.append(entry)

        # 作り方
        ttk.Label(form_card, text="作り方（1〜6）", style="Heading.TLabel").pack(anchor="w", pady=(20, 5))
        self.step_entries = []
        for i in range(1, 6 + 1):
            entry = ttk.Entry(form_card)
            entry.pack(anchor="w", fill="x", pady=3)
            self.step_entries.append(entry)

        # 画像カード
        ttk.Label(form_card, text="画像", style="Heading.TLabel").pack(anchor="w", pady=(20, 10))

        img_card = ttk.Frame(form_card, style="Card.TFrame", padding=10)
        img_card.pack(anchor="w", fill="x")

        ttk.Button(
            img_card,
            text="画像を選択",
            style="Header.TButton",
            command=self.select_image
        ).pack(anchor="w")

        self.preview_label = ttk.Label(img_card, background="#FFFFFF")
        self.preview_label.pack(pady=10)

        # Submit ボタン（中央寄せ）
        ttk.Button(
            content,
            text="登録（Submit）",
            style="Header.TButton",
            command=self.submit
        ).pack(pady=20)

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

    # DB保存
    def submit(self):
        title = self.title_entry.get()

        if not title:
            tk.messagebox.showerror("エラー", "タイトルは必須です。")
            return

        ingredients = [e.get() for e in self.ingredient_entries]
        steps = [e.get() for e in self.step_entries]

        img_path = ""
        if self.selected_image_path:
            img_path = self.image_manager.copy_image(self.selected_image_path)

        data = {
            "title": title,
            "image_path": img_path
        }

        for i in range(1, 10):
            data[f"ingredient{i}"] = ingredients[i - 1]

        for i in range(1, 7):
            data[f"step{i}"] = steps[i - 1]

        self.model.insert(data)

        tk.messagebox.showinfo("完了", "レシピを登録しました")
        self.controller.show_list_view()
