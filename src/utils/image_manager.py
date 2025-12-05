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
