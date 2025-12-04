import tkinter as tk

from view.list_view import ListView
from view.detail_view import DetailView
from view.create_view import CreateView


class AppController:
    # 画面切替を管理するコントローラー

    def __init__(self, root):
        self.root = root
        self.current_view = None

        # 最初は一覧画面を表示
        self.show_list_view()

    # 現在の画面を削除する
    def clear_view(self):
        if self.current_view is not None:
            self.current_view.destroy()

    # 一覧画面を表示する
    def show_list_view(self):
        self.clear_view()
        self.current_view = ListView(self.root, self)
        self.current_view.pack(fill="both", expand=True)

    # 詳細画面を表示する
    def show_detail_view(self, recipe_id):
        self.clear_view()
        self.current_view = DetailView(self.root, self, recipe_id)
        self.current_view.pack(fill="both", expand=True)

    # 登録画面を表示する
    def show_create_view(self):
        self.clear_view()
        self.current_view = CreateView(self.root, self)
        self.current_view.pack(fill="both", expand=True)

    # 編集画面を表示する
    def show_edit_view(self, recipe_id):
        self.clear_view()
        from view.edit_view import EditView
        self.current_view = EditView(self.root, self, recipe_id)
        self.current_view.pack(fill="both", expand=True)
