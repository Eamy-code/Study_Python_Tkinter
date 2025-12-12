import tkinter as tk
from tkinter import ttk


# ナチュラル系のアプリ共通テーマを設定する関数
def apply_theme(root):
    style = ttk.Style()

    # 全体背景色
    root.configure(bg="#FFF8E7")

    # ttk 共通設定
    style.configure(
        ".",                     # 全要素共通
        background="#FFF8E7",
        foreground="#5B4636",
        font=("Helvetica", 12)
    )

    # ラベル
    style.configure(
        "TLabel",
        background="#FFF8E7",
        foreground="#5B4636",
        font=("Helvetica", 12)
    )

    # 見出しラベル
    style.configure(
        "Heading.TLabel",
        background="#FFF8E7",
        foreground="#5B4636",
        font=("Helvetica", 14, "bold")
    )

    # タイトル
    style.configure(
        "Title.TLabel",
        background="#FFF8E7",
        foreground="#5B4636",
        font=("Helvetica", 18, "bold")
    )

    # ボタン
    style.configure(
        "TButton",
        background="#D8B892",
        foreground="#5B4636",
        relief="flat",
        padding=8
    )

    style.map(
        "TButton",
        background=[("active", "#C9A77E")]
    )

    # Entry
    style.configure(
        "TEntry",
        fieldbackground="#FFFFFF",
        bordercolor="#E6DCCD",
        relief="solid",
        padding=5
    )

    # カード用の Frame 風スタイル（丸角は疑似的）
    style.configure(
        "Card.TFrame",
        background="#FFFFFF",
        borderwidth=1,
        relief="solid"
    )
    # ヘッダーフレーム
    style.configure(
        "Header.TFrame",
        background="#FFF3D8",      # 一段濃いクリーム色
        relief="flat"
    )

    # ヘッダータイトル
    style.configure(
        "HeaderTitle.TLabel",
        background="#FFF3D8",
        foreground="#5B4636",
        font=("Helvetica", 20, "bold")
    )

    # ヘッダーボタン
    style.configure(
        "Header.TButton",
        background="#D8B892",
        foreground="#5B4636",
        padding=10,
        relief="flat"
    )

    style.map(
        "Header.TButton",
        background=[("active", "#C9A77E")]
    )
    # ベース背景（クリーム色）
    style.configure(
        "Base.TFrame",
        background="#FFF8E7"
    )

    # カードフレーム（白い四角）
    style.configure(
        "Card.TFrame",
        background="#FFFFFF",
        borderwidth=1,
        relief="solid",
        bordercolor="#E6DCCD"
    )

    # カードタイトル
    style.configure(
        "CardTitle.TButton",
        background="#FFFFFF",
        foreground="#5B4636",
        font=("Helvetica", 12, "bold"),
        padding=5,
        relief="flat"
    )

    style.map(
        "CardTitle.TButton",
        background=[("active", "#F4E9D8")]
    )
    # タイトル（大見出し）
    style.configure(
        "Title.TLabel",
        background="#FFF8E7",
        foreground="#5B4636",
        font=("Helvetica", 18, "bold")
    )

    # カード内の見出し
    style.configure(
        "Heading.TLabel",
        background="#FFFFFF",
        foreground="#5B4636",
        font=("Helvetica", 14, "bold")
    )

    # 画像カード
    style.configure(
        "ImageCard.TFrame",
        background="#FFFFFF",
        borderwidth=1,
        relief="solid",
        bordercolor="#E6DCCD",
        padding=10
    )
    # Entry フィールド（白背景）
    style.configure(
        "TEntry",
        fieldbackground="#FFFFFF",
        bordercolor="#E6DCCD",
        foreground="#5B4636",
        padding=6
    )

    # プレビュー用ラベル背景
    style.configure(
        "ImagePreview.TLabel",
        background="#FFFFFF"
    )
