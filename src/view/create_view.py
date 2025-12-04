import tkinter as tk
from tkinter import ttk, filedialog
from PIL import ImageTk

from model.recipe_model import RecipeModel
from utils.image_manager import ImageManager
from view.common_header import CommonHeader


class CreateView(ttk.Frame):
    # レシピ登録画面（タイトル・材料・手順・画像アップロード）

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)

        self.controller = controller
        self.model = RecipeModel()
        self.image_manager = ImageManager()

        self.selected_image_path = ""  # 選択された元画像パス
        self.preview_image = None      # プレビュー保持用（GC防止）

        # ヘッダー表示
        self.header = CommonHeader(self, controller)
        self.header.pack(fill="x")

        # メインフォームフレーム
        form = ttk.Frame(self)
        form.pack(fill="x", padx=20, pady=10)

        # タイトル
        ttk.Label(form, text="タイトル", font=("Arial", 14, "bold")).pack(anchor="w")
        self.title_entry = ttk.Entry(form, width=40)
        self.title_entry.pack(anchor="w", pady=5)

        # 材料入力
        ttk.Label(form, text="材料（1～9）", font=("Arial", 14, "bold")).pack(anchor="w", pady=(10, 0))

        self.ingredient_entries = []
        for i in range(1, 10):
            entry = ttk.Entry(form, width=40)
            entry.pack(anchor="w", pady=2)
            self.ingredient_entries.append(entry)

        # 作り方入力
        ttk.Label(form, text="作り方（1～6）", font=("Arial", 14, "bold")).pack(anchor="w", pady=(15, 0))

        self.step_entries = []
        for i in range(1, 7):
            entry = ttk.Entry(form, width=60)
            entry.pack(anchor="w", pady=2)
            self.step_entries.append(entry)

        # 画像アップロード部分
        ttk.Label(form, text="画像", font=("Arial", 14, "bold")).pack(anchor="w", pady=(15, 0))

        img_frame = ttk.Frame(form)
        img_frame.pack(anchor="w", pady=5)

        # ファイル選択ボタン
        select_button = ttk.Button(img_frame, text="ファイルを選択", command=self.select_image)
        select_button.pack(side="left")

        # プレビューラベル
        self.preview_label = ttk.Label(form)
        self.preview_label.pack(anchor="w", pady=10)

        # Submit ボタン
        submit_button = ttk.Button(self, text="登録（Submit）", command=self.submit)
        submit_button.pack(pady=20)

    # 画像を選択しプレビューを表示する
    def select_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("画像ファイル", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        if not file_path:
            return

        self.selected_image_path = file_path

        # プレビュー表示用画像
        img = self.image_manager.get_thumbnail(file_path, size=(200, 200))
        self.preview_image = ImageTk.PhotoImage(img)
        self.preview_label.config(image=self.preview_image)

    # 入力内容を CSV に保存する
    def submit(self):
        title = self.title_entry.get()

        # タイトルは必須
        if not title:
            tk.messagebox.showerror("エラー", "タイトルは必須です。")
            return

        # 材料・手順の収集
        ingredients = [e.get() for e in self.ingredient_entries]
        steps = [e.get() for e in self.step_entries]

        # 画像のコピー処理
        saved_image_path = ""
        if self.selected_image_path:
            saved_image_path = self.image_manager.copy_image(self.selected_image_path)

        # CSV に渡すデータ作成
        data = {
            "title": title,
            "image_path": saved_image_path
        }

        # 材料をセット
        for i, v in enumerate(ingredients, start=1):
            data[f"ingredient{i}"] = v

        # 手順をセット
        for i, v in enumerate(steps, start=1):
            data[f"step{i}"] = v

        # 登録処理
        self.model.insert(data)

        # 登録完了 → 一覧へ
        tk.messagebox.showinfo("登録完了", "レシピを登録しました。")
        self.controller.show_list_view()
