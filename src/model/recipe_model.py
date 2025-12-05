import sqlite3
import os


class RecipeModel:
    # SQLite でレシピ・材料・手順を管理するモデル

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "../data/recipe.db")

    def __init__(self):
        os.makedirs(os.path.dirname(self.DB_PATH), exist_ok=True)

        self.conn = sqlite3.connect(self.DB_PATH)
        self.conn.row_factory = sqlite3.Row

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

        for idx, step in enumerate(data["steps"], start=1):
            cur.execute("""
                INSERT INTO steps (recipe_id, step_no, text)
                VALUES (?, ?, ?)
            """, (recipe_id, idx, step["text"]))

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
        for idx, step in enumerate(data["steps"], start=1):
            cur.execute("""
                INSERT INTO steps (recipe_id, step_no, text)
                VALUES (?, ?, ?)
            """, (recipe_id, idx, step["text"]))

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
