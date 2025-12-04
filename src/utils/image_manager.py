import os
import shutil
from PIL import Image

class ImageManager:
    # 画像管理クラス（コピー・リサイズ・ロード）

    def __init__(self):
        # 画像保存先フォルダのパス
        self.image_dir = "src/images"

        # デフォルト画像のパス
        self.default_image_path = os.path.join(self.image_dir, "default.png")

        # フォルダが無ければ作成
        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir, exist_ok=True)

    # パスを正規化して返す
    def normalize_path(self, path):
        return os.path.normpath(path)

    # 画像を /src/images にコピーして保存パスを返す
    def copy_image(self, src_path):
        # パスが空の場合 → 空文字を返す（画像なし扱い）
        if not src_path:
            return ""

        # ファイル名だけ取り出す
        filename = os.path.basename(src_path)

        # 保存先パス
        dest_path = os.path.join(self.image_dir, filename)

        # 同名ファイル回避（既にある場合は連番にする）
        if os.path.exists(dest_path):
            base, ext = os.path.splitext(filename)
            count = 1
            while True:
                new_name = f"{base}_{count}{ext}"
                dest_path = os.path.join(self.image_dir, new_name)
                if not os.path.exists(dest_path):
                    break
                count += 1

        # コピーの実行
        try:
            shutil.copy(src_path, dest_path)
        except Exception:
            # コピーエラー時 → 空文字（画像なし扱い）
            return ""

        return self.normalize_path(dest_path)

    # 画像を読み込む（失敗したらデフォルト画像）
    def load_image(self, path):
        # パスが無い場合 → デフォルト
        if not path or not os.path.exists(path):
            return Image.open(self.default_image_path)

        try:
            return Image.open(path)
        except:
            # 壊れた画像など例外時もデフォルト
            return Image.open(self.default_image_path)

    # 指定サイズにリサイズして返す
    def resize_image(self, image, width, height):
        return image.resize((width, height), Image.Resampling.LANCZOS)

    # サムネイル画像を生成（一覧画面用）
    def get_thumbnail(self, path, size=(150, 150)):
        image = self.load_image(path)
        return self.resize_image(image, size[0], size[1])

    # 詳細画面用の大きめ画像を返す
    def get_detail_image(self, path, size=(300, 200)):
        image = self.load_image(path)
        return self.resize_image(image, size[0], size[1])
