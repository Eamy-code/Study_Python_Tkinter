import os

# 画像管理クラス（コピー・リサイズ・ロード）
class ImageManager:


    def __init__(self):
        # 画像保存先フォルダのパス
        self.image_dir = "src/images"

        # デフォルト画像のパス
        self.default_image_path = os.path.join(self.image_dir, "default.png")

        # フォルダが無ければ作成
        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir, exist_ok=True)
