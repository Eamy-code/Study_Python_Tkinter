import tkinter as tk
from tkinter import ttk
from PIL import ImageTk

from model.recipe_model import RecipeModel
from utils.image_manager import ImageManager
from view.common_header import CommonHeader
from view.components.scroll_frame import ScrollFrame


class ListView(ttk.Frame):
    # レシピ一覧画面（おしゃれ UI + スクロール対応 + ヘッダー固定）

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)

        self.controller = controller
        self.model = RecipeModel()
        self.image_manager = ImageManager()

        self.configure(style="Base.TFrame")

        # ヘッダー（固定）
        header = CommonHeader(self, controller)
        header.pack(fill="x")

        # ScrollFrame（中身のみスクロール）
        scroll = ScrollFrame(self)
        scroll.pack(fill="both", expand=True)

        content = scroll.inner

        recipes = self.model.load_all()

        self.images = []

        col_count = 2
        row = 0
        col = 0

        for r in recipes:
            card = ttk.Frame(content, style="Card.TFrame", padding=12)
            card.grid(row=row, column=col, padx=20, pady=20, sticky="n")

            img = self.image_manager.get_thumbnail(r["image_path"])
            tk_img = ImageTk.PhotoImage(img)
            self.images.append(tk_img)

            img_label = ttk.Label(card, image=tk_img)
            img_label.pack()

            title_btn = ttk.Button(
                card,
                text=r["title"],
                style="CardTitle.TButton",
                command=lambda rid=r["id"]: controller.show_detail_view(rid)
            )
            title_btn.pack(pady=8)

            img_label.bind(
                "<Button-1>",
                lambda e, rid=r["id"]: controller.show_detail_view(rid)
            )

            col += 1
            if col >= col_count:
                col = 0
                row += 1
