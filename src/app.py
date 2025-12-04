import tkinter as tk
from controller.app_controller import AppController

# アプリ起動
if __name__ == "__main__":
    root = tk.Tk()
    root.title("RecipeDesk")
    root.geometry("900x700")

    app = AppController(root)
    root.mainloop()
