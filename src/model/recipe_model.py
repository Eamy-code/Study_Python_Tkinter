import sqlite3
import os


# SQLite を使ったレシピデータ管理クラス
class RecipeModel:

    def __init__(self):
        # DBファイルのパス
        self.db_path = "../src/database/recipe.db"

        # ディレクトリが無ければ作成
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        # テーブル初期化
        self.init_db()

    # DB接続を取得する
    def get_connection(self):
        return sqlite3.connect(self.db_path)

    # レシピテーブルを作成（存在しなければ）
    def init_db(self):
        conn = self.get_connection()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                image_path TEXT,
                ingredient1 TEXT,
                ingredient2 TEXT,
                ingredient3 TEXT,
                ingredient4 TEXT,
                ingredient5 TEXT,
                ingredient6 TEXT,
                ingredient7 TEXT,
                ingredient8 TEXT,
                ingredient9 TEXT,
                step1 TEXT,
                step2 TEXT,
                step3 TEXT,
                step4 TEXT,
                step5 TEXT,
                step6 TEXT
            )
        """)

        conn.commit()
        conn.close()

    # 全件取得
    def load_all(self):
        conn = self.get_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM recipes ORDER BY id")
        rows = cur.fetchall()

        conn.close()

        # Dict化して返す（CSV版と互換性のため）
        dict_list = []
        for r in rows:
            dict_list.append({
                "id": str(r[0]),
                "title": r[1],
                "image_path": r[2],
                "ingredient1": r[3],
                "ingredient2": r[4],
                "ingredient3": r[5],
                "ingredient4": r[6],
                "ingredient5": r[7],
                "ingredient6": r[8],
                "ingredient7": r[9],
                "ingredient8": r[10],
                "ingredient9": r[11],
                "step1": r[12],
                "step2": r[13],
                "step3": r[14],
                "step4": r[15],
                "step5": r[16],
                "step6": r[17],
            })

        return dict_list

    # IDで1件取得
    def find_by_id(self, recipe_id):
        conn = self.get_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM recipes WHERE id=?", (recipe_id,))
        r = cur.fetchone()

        conn.close()

        if r is None:
            return None

        return {
            "id": str(r[0]),
            "title": r[1],
            "image_path": r[2],
            "ingredient1": r[3],
            "ingredient2": r[4],
            "ingredient3": r[5],
            "ingredient4": r[6],
            "ingredient5": r[7],
            "ingredient6": r[8],
            "ingredient7": r[9],
            "ingredient8": r[10],
            "ingredient9": r[11],
            "step1": r[12],
            "step2": r[13],
            "step3": r[14],
            "step4": r[15],
            "step5": r[16],
            "step6": r[17],
        }

    # 材料9個・手順6個を埋める
    def ensure_fields(self, data):
        for i in range(1, 10):
            key = f"ingredient{i}"
            if key not in data or data[key] is None:
                data[key] = ""

        for i in range(1, 7):
            key = f"step{i}"
            if key not in data or data[key] is None:
                data[key] = ""

        return data

    # 新規登録
    def insert(self, data):
        data = self.ensure_fields(data)

        conn = self.get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO recipes (
                title, image_path,
                ingredient1, ingredient2, ingredient3, ingredient4, ingredient5,
                ingredient6, ingredient7, ingredient8, ingredient9,
                step1, step2, step3, step4, step5, step6
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["title"],
            data["image_path"],
            data["ingredient1"], data["ingredient2"], data["ingredient3"],
            data["ingredient4"], data["ingredient5"], data["ingredient6"],
            data["ingredient7"], data["ingredient8"], data["ingredient9"],
            data["step1"], data["step2"], data["step3"],
            data["step4"], data["step5"], data["step6"],
        ))

        conn.commit()
        new_id = cur.lastrowid
        conn.close()

        return new_id
