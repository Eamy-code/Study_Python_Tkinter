#================================================================================
# image_manager.py
#================================================================================

import os
import shutil
from PIL import Image


class ImageManager:
    # 画像管理クラス（コピー・リサイズ・ロード）

    def __init__(self):
        # このファイルの絶対パス
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # images フォルダの絶対パス
        self.image_dir = os.path.join(base_dir, "../src/images")

        # デフォルト画像の絶対パス
        self.default_image_path = os.path.join(self.image_dir, "default.png")

        # フォルダが無ければ作成
        os.makedirs(self.image_dir, exist_ok=True)

    # パスを正規化して返す
    def normalize_path(self, path):
        return os.path.normpath(path)

    # 画像を /src/images にコピー
    def copy_image(self, src_path):
        if not src_path:
            return ""

        filename = os.path.basename(src_path)
        dest_path = os.path.join(self.image_dir, filename)

        # 同名ファイルなら連番付与
        if os.path.exists(dest_path):
            base, ext = os.path.splitext(filename)
            count = 1
            while True:
                new_name = f"{base}_{count}{ext}"
                dest_path = os.path.join(self.image_dir, new_name)
                if not os.path.exists(dest_path):
                    break
                count += 1

        try:
            shutil.copy(src_path, dest_path)
        except Exception:
            return ""

        return self.normalize_path(dest_path)

    # 画像ロード（失敗したらデフォルト）
    def load_image(self, path):
        if not path or not os.path.exists(path):
            return Image.open(self.default_image_path)

        try:
            return Image.open(path)
        except:
            return Image.open(self.default_image_path)

    # リサイズ
    def resize_image(self, image, width, height):
        return image.resize((width, height), Image.Resampling.LANCZOS)

    # サムネイル取得
    def get_thumbnail(self, path, size=(150, 150)):
        image = self.load_image(path)
        return self.resize_image(image, size[0], size[1])

    # 詳細画面用
    def get_detail_image(self, path, size=(300, 200)):
        image = self.load_image(path)
        return self.resize_image(image, size[0], size[1])


#================================================================================
# app.py
#================================================================================

import tkinter as tk
from controller.app_controller import AppController
from style.theme import apply_theme

if __name__ == "__main__":
    root = tk.Tk()
    root.title("RecipeDesk")
    root.geometry("900x700")

    # テーマ適用
    apply_theme(root)

    app = AppController(root)
    root.mainloop()


#================================================================================
# app_controller.py
#================================================================================

import tkinter as tk

from view.list_view import ListView
from view.detail_view import DetailView
from view.create_view import CreateView


class AppController:
    # 画面切替を管理するコントローラー

    def __init__(self, root):
        self.root = root
        self.current_view = None

        # 最初は一覧画面を表示
        self.show_list_view()

    # 現在の画面を削除する
    def clear_view(self):
        if self.current_view is not None:
            self.current_view.destroy()

    # 一覧画面を表示する
    def show_list_view(self):
        self.clear_view()
        self.current_view = ListView(self.root, self)
        self.current_view.pack(fill="both", expand=True)

    # 詳細画面を表示する
    def show_detail_view(self, recipe_id):
        self.clear_view()
        self.current_view = DetailView(self.root, self, recipe_id)
        self.current_view.pack(fill="both", expand=True)

    # 登録画面を表示する
    def show_create_view(self):
        self.clear_view()
        self.current_view = CreateView(self.root, self)
        self.current_view.pack(fill="both", expand=True)

    # 編集画面を表示する
    def show_edit_view(self, recipe_id):
        self.clear_view()
        from view.edit_view import EditView
        self.current_view = EditView(self.root, self, recipe_id)
        self.current_view.pack(fill="both", expand=True)


#================================================================================
# edit_view.py
#================================================================================

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


#================================================================================
# recipe_model.py
#================================================================================

import sqlite3
import os


class RecipeModel:
    # SQLite でレシピ・材料・手順を管理するモデル

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "../data/recipe.db")

    def __init__(self):
        # DB フォルダが無ければ作成
        os.makedirs(os.path.dirname(self.DB_PATH), exist_ok=True)

        # DB 接続
        self.conn = sqlite3.connect(self.DB_PATH)
        self.conn.row_factory = sqlite3.Row

        # テーブル作成
        self.create_tables()

    # テーブル作成
    def create_tables(self):
        cur = self.conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                image_path TEXT
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS ingredients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipe_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                amount TEXT,
                FOREIGN KEY(recipe_id) REFERENCES recipes(id)
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS steps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipe_id INTEGER NOT NULL,
                step_no INTEGER NOT NULL,
                text TEXT NOT NULL,
                FOREIGN KEY(recipe_id) REFERENCES recipes(id)
            )
        """)

        self.conn.commit()

    # レシピ登録
    def insert(self, data):
        cur = self.conn.cursor()

        cur.execute("""
            INSERT INTO recipes (title, image_path)
            VALUES (?, ?)
        """, (data["title"], data["image_path"]))

        recipe_id = cur.lastrowid

        for ing in data["ingredients"]:
            cur.execute("""
                INSERT INTO ingredients (recipe_id, name, amount)
                VALUES (?, ?, ?)
            """, (recipe_id, ing["name"], ing["amount"]))

        for idx, step_text in enumerate(data["steps"], start=1):
            cur.execute("""
                INSERT INTO steps (recipe_id, step_no, text)
                VALUES (?, ?, ?)
            """, (recipe_id, idx, step_text))

        self.conn.commit()
        return recipe_id

    # レシピ更新
    def update(self, recipe_id, data):
        cur = self.conn.cursor()

        cur.execute("""
            UPDATE recipes
            SET title = ?, image_path = ?
            WHERE id = ?
        """, (data["title"], data["image_path"], recipe_id))

        cur.execute("DELETE FROM ingredients WHERE recipe_id = ?", (recipe_id,))
        for ing in data["ingredients"]:
            cur.execute("""
                INSERT INTO ingredients (recipe_id, name, amount)
                VALUES (?, ?, ?)
            """, (recipe_id, ing["name"], ing["amount"]))

        cur.execute("DELETE FROM steps WHERE recipe_id = ?", (recipe_id,))
        for idx, step_text in enumerate(data["steps"], start=1):
            cur.execute("""
                INSERT INTO steps (recipe_id, step_no, text)
                VALUES (?, ?, ?)
            """, (recipe_id, idx, step_text))

        self.conn.commit()

    # レシピ一覧取得
    def load_all(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM recipes ORDER BY id ASC")
        rows = cur.fetchall()
        return [dict(row) for row in rows]

    # レシピ詳細取得
    def find_by_id(self, recipe_id):
        cur = self.conn.cursor()

        cur.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
        recipe = cur.fetchone()
        if not recipe:
            return None

        recipe = dict(recipe)

        cur.execute("""
            SELECT name, amount
            FROM ingredients
            WHERE recipe_id = ?
        """, (recipe_id,))
        recipe["ingredients"] = [dict(row) for row in cur.fetchall()]

        cur.execute("""
            SELECT step_no, text
            FROM steps
            WHERE recipe_id = ?
            ORDER BY step_no ASC
        """, (recipe_id,))
        recipe["steps"] = [dict(row) for row in cur.fetchall()]

        return recipe

    # レシピ削除
    def delete(self, recipe_id):
        cur = self.conn.cursor()

        cur.execute("DELETE FROM ingredients WHERE recipe_id = ?", (recipe_id,))
        cur.execute("DELETE FROM steps WHERE recipe_id = ?", (recipe_id,))
        cur.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))

        self.conn.commit()


#================================================================================
# create_view.py
#================================================================================

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import ImageTk

from model.recipe_model import RecipeModel
from utils.image_manager import ImageManager
from view.common_header import CommonHeader
from view.components.scroll_frame import ScrollFrame


class CreateView(ttk.Frame):
    # レシピ登録画面（動的材料・動的手順＋スクロール安定＋ヘッダー固定）

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)

        self.controller = controller
        self.model = RecipeModel()
        self.image_manager = ImageManager()

        self.selected_image_path = ""
        self.preview_image = None

        self.configure(style="Base.TFrame")

        # ヘッダー（固定）
        header = CommonHeader(self, controller)
        header.pack(fill="x")

        # ScrollFrame（中身のみスクロール）
        scroll = ScrollFrame(self)
        scroll.pack(fill="both", expand=True)

        content = scroll.inner

        form = ttk.Frame(content, style="Card.TFrame", padding=20)
        form.pack(fill="x", padx=30, pady=20)

        ttk.Label(form, text="タイトル", style="Heading.TLabel").pack(anchor="w")
        self.title_entry = ttk.Entry(form)
        self.title_entry.pack(fill="x", pady=(0, 15))


        ttk.Label(form, text="材料（材料名 ＋ 量）", style="Heading.TLabel").pack(anchor="w", pady=(10, 5))
        self.ingredients_frame = ttk.Frame(form, style="Base.TFrame")
        self.ingredients_frame.pack(fill="x")
        self.ingredient_rows = []
        self.add_ingredient_row()

        ttk.Button(
            form, text="+ 材料を追加", style="Header.TButton",
            command=self.add_ingredient_row
        ).pack(anchor="w", pady=10)


        ttk.Label(form, text="作り方", style="Heading.TLabel").pack(anchor="w", pady=(20, 5))
        self.steps_frame = ttk.Frame(form, style="Base.TFrame")
        self.steps_frame.pack(fill="x")
        self.step_rows = []
        self.add_step_row()

        ttk.Button(
            form, text="+ 作り方を追加", style="Header.TButton",
            command=self.add_step_row
        ).pack(anchor="w", pady=10)


        ttk.Label(form, text="画像", style="Heading.TLabel").pack(anchor="w", pady=(20, 10))

        img_card = ttk.Frame(form, style="Card.TFrame", padding=10)
        img_card.pack(fill="x")

        ttk.Button(
            img_card, text="画像を選択", style="Header.TButton",
            command=self.select_image
        ).pack(anchor="w")

        self.preview_label = ttk.Label(img_card, background="#FFFFFF")
        self.preview_label.pack(pady=10)


        ttk.Button(
            content, text="登録（Submit）", style="Header.TButton",
            command=self.submit
        ).pack(pady=20)


    # 材料行追加
    def add_ingredient_row(self):
        row = ttk.Frame(self.ingredients_frame, style="Base.TFrame")
        row.pack(fill="x", pady=3)

        name = ttk.Entry(row)
        name.pack(side="left", fill="x", expand=True, padx=(0, 5))

        amount = ttk.Entry(row, width=15)
        amount.pack(side="left", padx=(0, 5))

        del_btn = ttk.Button(
            row, text="−", width=2,
            command=lambda rf=row: self.remove_ingredient_row(rf)
        )
        del_btn.pack(side="left")

        self.ingredient_rows.append((row, name, amount))

    # 材料削除
    def remove_ingredient_row(self, row):
        if len(self.ingredient_rows) <= 1:
            messagebox.showwarning("注意", "材料は最低 1 行必要です。")
            return

        self.ingredient_rows = [r for r in self.ingredient_rows if r[0] != row]
        row.destroy()

    # 手順行追加
    def add_step_row(self):
        row = ttk.Frame(self.steps_frame, style="Base.TFrame")
        row.pack(fill="x", pady=3)

        entry = ttk.Entry(row)
        entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

        del_btn = ttk.Button(
            row, text="−", width=2,
            command=lambda rf=row: self.remove_step_row(rf)
        )
        del_btn.pack(side="left")

        self.step_rows.append((row, entry))

    # 手順削除
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

    # Submit
    def submit(self):
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

        img_path = ""
        if self.selected_image_path:
            img_path = self.image_manager.copy_image(self.selected_image_path)

        data = {
            "title": title,
            "image_path": img_path,
            "ingredients": ingredients,
            "steps": steps
        }

        self.model.insert(data)

        messagebox.showinfo("完了", "レシピを登録しました")
        self.controller.show_list_view()


#================================================================================
# detail_view.py
#================================================================================

import tkinter as tk
from tkinter import ttk
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

        self.configure(style="Base.TFrame")

        recipe = self.model.find_by_id(recipe_id)
        if not recipe:
            return
        self.recipe = recipe

        # ヘッダー（固定）
        header = CommonHeader(self, controller)
        header.pack(fill="x")

        # ScrollFrame（中身のみスクロール）
        scroll = ScrollFrame(self)
        scroll.pack(fill="both", expand=True)

        content = scroll.inner

        title_label = ttk.Label(content, text=recipe["title"], style="Title.TLabel")
        title_label.pack(pady=15)

        mid = ttk.Frame(content, style="Base.TFrame")
        mid.pack(fill="x", padx=20, pady=10)

        img_card = ttk.Frame(mid, style="Card.TFrame", padding=10)
        img_card.grid(row=0, column=0, padx=20, pady=5)

        img = self.image_manager.get_detail_image(recipe["image_path"])
        self.tk_img = ImageTk.PhotoImage(img)

        ttk.Label(img_card, image=self.tk_img, background="#FFFFFF").pack()

        ing_card = ttk.Frame(mid, style="Card.TFrame", padding=15)
        ing_card.grid(row=0, column=1, padx=20, pady=5, sticky="n")

        ttk.Label(ing_card, text="材料", style="Heading.TLabel").pack(anchor="w", pady=(0, 10))

        for ing in recipe["ingredients"]:
            line = f"{ing['name']} … {ing['amount']}"
            ttk.Label(ing_card, text=line, style="TLabel").pack(anchor="w", pady=2)

        steps_card = ttk.Frame(content, style="Card.TFrame", padding=15)
        steps_card.pack(fill="x", padx=20, pady=20)

        ttk.Label(steps_card, text="作り方", style="Heading.TLabel").pack(anchor="w", pady=(0, 10))

        for step in recipe["steps"]:
            s = f"{step['step_no']}. {step['text']}"
            ttk.Label(steps_card, text=s, style="TLabel").pack(anchor="w", pady=3)


#================================================================================
# list_view.py
#================================================================================

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


#================================================================================
# scroll_frame.py
#================================================================================

import tkinter as tk
from tkinter import ttk


# 縦スクロール＋マウスホイール対応の共通スクロールコンテナ
class ScrollFrame(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        # Canvas（スクロール領域）
        self.canvas = tk.Canvas(self, highlightthickness=0, bg="#FFF8E7")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # inner Frame
        self.inner = ttk.Frame(self.canvas, style="Base.TFrame")
        self.window = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")

        # サイズ変更時のスクロール領域更新
        self.inner.bind("<Configure>", self._update_scrollregion)
        self.canvas.bind("<Configure>", self._resize_inner)

        # マウスホイール対応
        self.bind_events()

    # スクロール領域更新
    def _update_scrollregion(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # inner の幅を canvas に合わせる
    def _resize_inner(self, event):
        self.canvas.itemconfig(self.window, width=event.width)

    # マウスホイールイベントの紐付け
    def bind_events(self):
        # Windows / Linux
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        # Mac（ホイールイベント名が異なる）
        self.canvas.bind_all("<Button-4>", self._on_mousewheel_mac)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel_mac)

    # Windows / Linux 用スクロール
    def _on_mousewheel(self, event):
        # event.delta は Windows で120単位、Linuxは±1が来る
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # Mac 用スクロール
    def _on_mousewheel_mac(self, event):
        if event.num == 4:  # 上スクロール
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:  # 下スクロール
            self.canvas.yview_scroll(1, "units")


#================================================================================
# theme.py
#================================================================================

import tkinter as tk
from tkinter import ttk


# ナチュラル系のアプリ共通テーマを設定する関数
def apply_theme(root):
    style = ttk.Style()

    # 全体背景色
    root.configure(bg="#FFF8E7")

    # ttk 共通設定
    style.configure(
        ".",                     # 全要素共通
        background="#FFF8E7",
        foreground="#5B4636",
        font=("Helvetica", 12)
    )

    # ラベル
    style.configure(
        "TLabel",
        background="#FFF8E7",
        foreground="#5B4636",
        font=("Helvetica", 12)
    )

    # 見出しラベル
    style.configure(
        "Heading.TLabel",
        background="#FFF8E7",
        foreground="#5B4636",
        font=("Helvetica", 14, "bold")
    )

    # タイトル
    style.configure(
        "Title.TLabel",
        background="#FFF8E7",
        foreground="#5B4636",
        font=("Helvetica", 18, "bold")
    )

    # ボタン
    style.configure(
        "TButton",
        background="#D8B892",
        foreground="#5B4636",
        relief="flat",
        padding=8
    )

    style.map(
        "TButton",
        background=[("active", "#C9A77E")]
    )

    # Entry
    style.configure(
        "TEntry",
        fieldbackground="#FFFFFF",
        bordercolor="#E6DCCD",
        relief="solid",
        padding=5
    )

    # カード用の Frame 風スタイル（丸角は疑似的）
    style.configure(
        "Card.TFrame",
        background="#FFFFFF",
        borderwidth=1,
        relief="solid"
    )
    # ヘッダーフレーム
    style.configure(
        "Header.TFrame",
        background="#FFF3D8",      # 一段濃いクリーム色
        relief="flat"
    )

    # ヘッダータイトル
    style.configure(
        "HeaderTitle.TLabel",
        background="#FFF3D8",
        foreground="#5B4636",
        font=("Helvetica", 20, "bold")
    )

    # ヘッダーボタン
    style.configure(
        "Header.TButton",
        background="#D8B892",
        foreground="#5B4636",
        padding=10,
        relief="flat"
    )

    style.map(
        "Header.TButton",
        background=[("active", "#C9A77E")]
    )
    # ベース背景（クリーム色）
    style.configure(
        "Base.TFrame",
        background="#FFF8E7"
    )

    # カードフレーム（白い四角）
    style.configure(
        "Card.TFrame",
        background="#FFFFFF",
        borderwidth=1,
        relief="solid",
        bordercolor="#E6DCCD"
    )

    # カードタイトル
    style.configure(
        "CardTitle.TButton",
        background="#FFFFFF",
        foreground="#5B4636",
        font=("Helvetica", 12, "bold"),
        padding=5,
        relief="flat"
    )

    style.map(
        "CardTitle.TButton",
        background=[("active", "#F4E9D8")]
    )
    # タイトル（大見出し）
    style.configure(
        "Title.TLabel",
        background="#FFF8E7",
        foreground="#5B4636",
        font=("Helvetica", 18, "bold")
    )

    # カード内の見出し
    style.configure(
        "Heading.TLabel",
        background="#FFFFFF",
        foreground="#5B4636",
        font=("Helvetica", 14, "bold")
    )

    # 画像カード
    style.configure(
        "ImageCard.TFrame",
        background="#FFFFFF",
        borderwidth=1,
        relief="solid",
        bordercolor="#E6DCCD",
        padding=10
    )
    # Entry フィールド（白背景）
    style.configure(
        "TEntry",
        fieldbackground="#FFFFFF",
        bordercolor="#E6DCCD",
        foreground="#5B4636",
        padding=6
    )

    # プレビュー用ラベル背景
    style.configure(
        "ImagePreview.TLabel",
        background="#FFFFFF"
    )


#================================================================================
# common_header.py
#================================================================================

import tkinter as tk
from tkinter import ttk


class CommonHeader(ttk.Frame):
    # ナチュラルで柔らかい印象の共通ヘッダー

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)

        self.controller = controller

        # 背景色（Header自身に設定）
        self.configure(style="Header.TFrame")

        # タイトルラベル
        title = ttk.Label(
            self,
            text="RecipeDesk",
            style="HeaderTitle.TLabel"
        )
        title.grid(row=0, column=0, sticky="w", padx=20, pady=15)

        # 右側ボタンまとめフレーム
        btn_frame = ttk.Frame(self, style="Header.TFrame")
        btn_frame.grid(row=0, column=1, sticky="e", padx=20)

        # 一覧へ
        list_btn = ttk.Button(
            btn_frame,
            text="一覧へ",
            style="Header.TButton",
            command=self.controller.show_list_view
        )
        list_btn.pack(side="left", padx=5)

        # 登録へ
        create_btn = ttk.Button(
            btn_frame,
            text="登録へ",
            style="Header.TButton",
            command=self.controller.show_create_view
        )
        create_btn.pack(side="left", padx=5)

        # グリッド調整
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)


