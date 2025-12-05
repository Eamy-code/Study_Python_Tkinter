import tkinter as tk

root = tk.Tk()
root.title("ラベルの練習")

# ラベル（文字）を作る
label = tk.Label(root, text="ここに書いてね")

# 画面に配置する
label.pack()

root.mainloop()




# --- ポイント ---
# Label(...) で「ラベル（文字の表示部品）」を作る
# text="●●●" が画面に表示される文字
# pack() は「画面に配置する」ための命令
