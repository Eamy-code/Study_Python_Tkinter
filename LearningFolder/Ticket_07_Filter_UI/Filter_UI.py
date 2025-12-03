import tkinter as tk
from tkinter import filedialog, ttk
import csv

root = tk.Tk()
root.title("CSV フィルタUI")
root.geometry("600x400")

# Treeview の作成
tree = ttk.Treeview(root)
tree.pack(fill="both", expand=True)

# コンボボックスと Entry の配置エリア
filter_frame = tk.Frame(root)
filter_frame.pack(fill="x", pady=10)

# 列名選択用 Combobox
column_var = tk.StringVar()
column_box = ttk.Combobox(filter_frame, textvariable=column_var, state="readonly")
column_box.pack(side="left", padx=5)

# 条件入力 Entry
cond_var = tk.StringVar()
cond_entry = tk.Entry(filter_frame, textvariable=cond_var)
cond_entry.pack(side="left", padx=5)

# データ保持用
csv_data = []


def load_csv():
    global csv_data

    filepath = filedialog.askopenfilename(
        filetypes=[("CSV Files", "*.csv")]
    )
    if not filepath:
        print("ファイルが選択されませんでした")
        return

    print("読み込むファイル:", filepath)

    with open(filepath, encoding="utf-8") as f:
        reader = csv.reader(f)
        csv_data = list(reader)

    header = csv_data[0]
    rows = csv_data[1:]

    # Treeview の初期化
    tree.delete(*tree.get_children())
    tree["columns"] = header
    tree["show"] = "headings"

    for col in header:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    for row in rows:
        tree.insert("", "end", values=row)

    # Combobox に列名をセット
    column_box["values"] = header
    column_box.current(0)


def apply_filter():
    if not csv_data:
        print("データが読み込まれていません")
        return

    header = csv_data[0]
    rows = csv_data[1:]

    target_col = column_var.get()
    condition = cond_var.get()

    if not target_col or not condition:
        print("条件を入力してください")
        return

    col_index = header.index(target_col)

    # 部分一致フィルタ
    filtered = [row for row in rows if condition.lower() in row[col_index].lower()]

    # Treeview の再表示
    tree.delete(*tree.get_children())
    for row in filtered:
        tree.insert("", "end", values=row)


# フィルタボタン
filter_button = tk.Button(filter_frame, text="フィルタ", command=apply_filter)
filter_button.pack(side="left", padx=5)

# CSV読み込みボタン
load_button = tk.Button(root, text="CSVを読み込む", command=load_csv)
load_button.pack(pady=5)

root.mainloop()




# --- ポイント ---
# Combobox：列名を選択するドロップダウン
# Entry：フィルタ文字を入力する
# apply_filter()：選んだ列の値に condition を含む行だけ抽出する
# ツリー表示は "delete → insert" で更新できる
# フィルタは部分一致（lower() を使って大文字小文字を無視）
