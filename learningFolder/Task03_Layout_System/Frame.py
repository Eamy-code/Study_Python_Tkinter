import tkinter as tk

root = tk.Tk()
root.title("Frame 3分割の練習（固定サイズ）")

# ウィンドウサイズを固定
root.geometry("400x300")  # ← 400px × 300px のウィンドウ

# --- 上のエリア ---
top_frame = tk.Frame(root, bg="lightblue", height=50)
top_frame.pack(fill="x")

# --- 中央のエリア ---
middle_frame = tk.Frame(root, bg="lightgreen")
middle_frame.pack(fill="both", expand=True)

# --- 下のエリア ---
bottom_frame = tk.Frame(root, bg="lightyellow", height=30)
bottom_frame.pack(fill="x")

root.mainloop()




# --- ポイント ---
# geometry("400x300") は「横400px × 縦300px」のウィンドウを作る
# "," ではなく "x" で区切るのが Tkinter のルール
# fill="x" → 横いっぱい
# fill="both", expand=True → 余った領域を中央フレームが広がって埋める
# 今は色だけ付けて、3つの領域が見えるようにしている
