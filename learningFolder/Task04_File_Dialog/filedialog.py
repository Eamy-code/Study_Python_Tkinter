import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.title("ファイルダイアログの練習")
root.geometry("400x200")

# ファイルを開く動作
def open_file():
    filepath = filedialog.askopenfilename()
    print("選択されたファイル:", filepath)

# ボタン作成
button = tk.Button(root, text="ファイルを選ぶ", command=open_file)
button.pack(pady=20)

root.mainloop()




# --- ポイント ---
# filedialog.askopenfilename() が OSの「ファイルを開く」画面を表示する
# 戻り値は選んだファイルのパス（例: C:/user/.../xxx.csv）
# キャンセルすると空文字 "" が返る
# 今は print() に表示して動作確認している
