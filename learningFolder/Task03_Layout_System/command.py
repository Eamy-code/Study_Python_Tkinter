import tkinter as tk

root = tk.Tk()
root.title("ボタンの練習")

# ラベルを作る
label = tk.Label(root, text="最初の文字")
label.pack()

# ボタンを押した時の動作
def change_text():
    label.config(text="ボタンが押されたよ！")

# ボタンを作る
button = tk.Button(root, text="押してみて", command=change_text)
button.pack()

root.mainloop()




# --- ポイント ---
# command=change_text の "change_text" は () をつけない
# ボタンが押された時に change_text() が自動で呼ばれる
# label.config(...) は「ラベルの内容を変更する」メソッド
