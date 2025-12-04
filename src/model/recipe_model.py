import sqlite3
import os


class RecipeModel:
    # SQLite でレシピ・材料・手順を管理するモデル

    DB_PATH = "../src/data/recipe.db"

    def __init__(self):
        # DB フォルダが無ければ作成
        os.makedirs(os.path.dirname(self.DB_PATH), exist_ok=True)

        # DB 接続とテーブル作成
        self.conn = sqlite3.connect(self.DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()

    # テーブル作成
    def create_tables(self):
        cur = self.conn.cursor()

        # recipes テーブル
        cur.execute("""
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                image_path TEXT
            )
        """)

        # ingredients テーブル
        cur.execute("""
            CREATE TABLE IF NOT EXISTS ingredients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipe_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                amount TEXT,
                FOREIGN KEY(recipe_id) REFERENCES recipes(id)
            )
        """)

        # steps テーブル
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

    # レシピ登録（レシピ・材料・手順をまとめて保存）
    def insert(self, data):
        cur = self.conn.cursor()

        # レシピ本体を挿入
        cur.execute("""
            INSERT INTO recipes (title, image_path)
            VALUES (?, ?)
        """, (data["title"], data["image_path"]))

        recipe_id = cur.lastrowid

        # 材料を挿入
        for ing in data["ingredients"]:
            cur.execute("""
                INSERT INTO ingredients (recipe_id, name, amount)
                VALUES (?, ?, ?)
            """, (recipe_id, ing["name"], ing["amount"]))

        # 作り方を挿入（順序付き）
        for idx, step_text in enumerate(data["steps"], start=1):
            cur.execute("""
                INSERT INTO steps (recipe_id, step_no, text)
                VALUES (?, ?, ?)
            """, (recipe_id, idx, step_text))

        self.conn.commit()
        return recipe_id

    # 全レシピ一覧を返す（タイトルと画像だけ）
    def load_all(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM recipes ORDER BY id ASC")
        rows = cur.fetchall()
        return [dict(row) for row in rows]

    # 1レシピを詳細情報付きで返す
    def find_by_id(self, recipe_id):
        cur = self.conn.cursor()

        # レシピ本体取得
        cur.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
        recipe = cur.fetchone()
        if not recipe:
            return None

        recipe = dict(recipe)

        # 材料一覧を取得
        cur.execute("""
            SELECT name, amount
            FROM ingredients
            WHERE recipe_id = ?
        """, (recipe_id,))
        recipe["ingredients"] = [dict(row) for row in cur.fetchall()]

        # 手順一覧を取得（step_no 順）
        cur.execute("""
            SELECT step_no, text
            FROM steps
            WHERE recipe_id = ?
            ORDER BY step_no ASC
        """, (recipe_id,))
        recipe["steps"] = [dict(row) for row in cur.fetchall()]

        return recipe

    # レシピ削除（材料と手順も削除）
    def delete(self, recipe_id):
        cur = self.conn.cursor()

        cur.execute("DELETE FROM ingredients WHERE recipe_id = ?", (recipe_id,))
        cur.execute("DELETE FROM steps WHERE recipe_id = ?", (recipe_id,))
        cur.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))

        self.conn.commit()
