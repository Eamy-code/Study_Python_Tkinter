import tkinter as tk

root = tk.Tk()
root.title("Frame の練習")

# 上のエリア（Frame）
top_frame = tk.Frame(root)
top_frame.pack()

# 下のエリア（Frame）
bottom_frame = tk.Frame(root)
bottom_frame.pack()

# 上のエリアにラベルを置く
label = tk.Label(top_frame, text="上のエリアです")
label.pack()

# 下のエリアにボタンを置く
button = tk.Button(bottom_frame, text="下のエリアのボタン")
button.pack()

root.mainloop()




# --- ポイント ---
# Frame は「部品を入れるための箱」のイメージ
# Label や Button を Frame に入れると、そのエリアにだけ配置される
# pack() を Frame に対して行うと、その枠ごと画面に表示される
