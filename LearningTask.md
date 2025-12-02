# Tkinter 学習チケット一覧

---

## Ticket_01_Operation_Check
**目的**：Tkinter が利用できる環境を確認する  
**タスク**
- `python -c "import tkinter"` でエラーが出ないことを確認
- Python対話モードで `tkinter._test()` を実行してウィンドウ表示
- 必要であれば環境整備（例：Linux なら `sudo apt install python3-tk`）

---

## Ticket_02_Minimal_GUI
**目的**：Tkinter の基本構造を理解する  
**タスク**
- Tk ウィンドウを生成してタイトルをつける
- Label を1つ表示する
- Button を1つ置き、クリック時に print させる
- `mainloop()` の役割を理解する  
**Output**：最小の Tkinter アプリ

---

## Ticket_03_Layout_System
**目的**：UI構築に必要なレイアウトを理解する  
**タスク**
- Frame を使って画面を上下 or 左右に分割
- `pack` と `grid` のどちらかを練習
- 「自分が採用するレイアウト方針」を README にメモ

---

## Ticket_04_File_Dialog
**目的**：外部ファイルをGUIから扱う  
**タスク**
- `filedialog.askopenfilename()` でCSVファイルを選択
- 選択したパスを Label or Text に表示

---

## Ticket_05_CSV_Load
**目的**：GUIとロジック（処理）の接続  
**タスク**
- `csv` または `pandas` で CSV を読み込む
- データ構造（list, DataFrame）として保持する
- エラーハンドリング（読み込み失敗など）

---

## Ticket_06_Table_View
**目的**：GUI画面にテーブル表示を実装  
**タスク**
- `ttk.Treeview` を配置
- 読み込んだCSVのヘッダーをカラムとして設定
- 行データを `insert` で追加
- スクロールバーの設置  
**Output**：CSVビューア画面

---

## Ticket_07_Filter_UI
**目的**：ユーザー操作とデータ処理の連動を理解  
**タスク**
- Combobox（列名選択）を設置
- Entry（条件入力）を配置
- 「フィルタ」ボタンで部分一致フィルタを実装
- 絞り込み後のデータを Treeview に再表示

---

## Ticket_08_CSV_Save
**目的**：実務用ツールとして最低限の完成度にする  
**タスク**
- `asksaveasfilename()` で保存先を選択
- フィルタ後のデータを CSV に書き出し
- ステータスバーに保存完了を表示

---

## Ticket_09_Refactoring
**目的**：読みやすく保守性のあるコードにする  
**タスク**
- 関数化 or クラス化
- コメント・Docstring の追加
- 不要コードの削除

---