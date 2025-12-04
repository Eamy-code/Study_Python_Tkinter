# --- Content from app.py ---
import tkinter as tk
from controller.app_controller import AppController
from style.theme import apply_theme

if __name__ == "__main__":
    root = tk.Tk()
    root.title("RecipeDesk")
    root.geometry("900x700")

    # テーマ適用
    apply_theme(root)

    app = AppController(root)
    root.mainloop()

# --- Content from requirement.txt ---
pillow>=10.0.0
