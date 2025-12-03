import csv
import os

# RecipeDesk の CSV データ管理クラス
class RecipeModel:


    CSV_PATH = "src/data/recipes.csv"
    FIELDNAMES = [
        "id",
        "title",
        "image_path",
    ] + [f"ingredient{i}" for i in range(1, 10)] \
      + [f"step{i}" for i in range(1, 7)]

    def __init__(self):
        # CSV が存在しない場合は新規作成する
        if not os.path.exists(self.CSV_PATH):
            os.makedirs(os.path.dirname(self.CSV_PATH), exist_ok=True)
            with open(self.CSV_PATH, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=self.FIELDNAMES)
                writer.writeheader()

   # CSV 全件読み込み
    def load_all(self):
        recipes = []
        with open(self.CSV_PATH, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                recipes.append(row)
        return recipes

    # CSV 全件保存（上書き）
    def save_all(self, recipes):
        with open(self.CSV_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.FIELDNAMES)
            writer.writeheader()
            writer.writerows(recipes)