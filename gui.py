import tkinter as tk
import tksvg
import os
from tkinter import messagebox

class ChessGUI:
    def __init__(self, root, logic):
        self.root = root
        self.logic = logic
        
        # 1. Окно ткинтера фикс
        self.root.resizable(False, False)
        
        self.selected_square = None
        self.buttons = [[None for _ in range(8)] for _ in range(8)]
        self.images = {} # Словарь для хранения SVG

        self.load_images()   # Загружаем SVG перед созданием кнопок 
        self.create_widgets()
        self.update_display()

    def load_images(self):
        """Загрузка SVG из твоей папки pieces_ui"""
        base_path = os.path.dirname(__file__)
        pieces_dir = os.path.join(base_path, "pieces_ui")
        
        pieces = ["Pawn", "Rook", "Knight", "Bishop", "Queen", "King"]
        colors = ["White", "Black"]

        for p in pieces:
            for c in colors:
                name = f"{p}_{c}"
                path = os.path.join(pieces_dir, f"{name}.svg")
                if os.path.exists(path):
                    # Масштаб 0.8, чтобы фигурка не касалась краев клетки 
                    self.images[name] = tksvg.SvgImage(master=self.root, file=path, scale=0.8)

    def create_widgets(self):
        """Создаем сетку 8x8 Сстатичного размера"""
        # Создаем невидимый пиксель, чтобы размер кнопок был в пикселях, а не в буквах 
        self.pixel_virtual = tk.PhotoImage(width=1, height=1)

        for r in range(8):
            for c in range(8):
                # цвета доски
                color = "#eeeed2" if (r + c) % 2 == 0 else "#769656"
                
                btn = tk.Button(
                    self.root, 
                    bg=color, 
                    relief="flat",
                    image=self.pixel_virtual, # фиксации размера 
                    compound="center",
                    width=80, height=80, 
                    command=lambda row=r, col=c: self.handle_click(row, col)
                )
                btn.grid(row=r, column=c) 
                self.buttons[r][c] = btn

    def update_display(self):
        """Ставим SVG картинку на кнопку вместо текста"""
        for r in range(8):
            for c in range(8):
                piece = self.logic.board[r][c]
                btn = self.buttons[r][c]
                
                if piece != ".":
                    # Собираем имя (
                    piece_name = f"{piece.__class__.__name__}_{piece.color}"
                    if piece_name in self.images:
                        btn.config(image=self.images[piece_name], text="")
                    else:
                        # Если картинки нет оставим текст как запасной вариант
                        symbol = piece.symbol if hasattr(piece, "symbol") else "?"
                        btn.config(text=symbol, image=self.pixel_virtual)
                else:
                    btn.config(image=self.pixel_virtual, text="")
        
        balance = self.logic.get_balance()
        self.root.title(f"Шахматы | Перевес сил: {balance}")

    def handle_click(self, r, c):
        if self.selected_square is None:
            # первый клик: Выбираем фигуру 
            piece = self.logic.board[r][c]
            if piece != ".":
                if piece.color == self.logic.current_turn: 
                    self.selected_square = (r, c)
                    self.buttons[r][c].config(bg="yellow")
                else:
                    messagebox.showinfo("Очередь", f"Сейчас ходят {self.logic.current_turn}")
        else:
            # Второй клик: Пытаемся пойти ( Добавь отступ для всех строк ниже) 
            start = self.selected_square
            end = (r, c)
            
            success, message = self.logic.move_piece(start, end)
            
            if success:
                self.update_display()
            else:
                messagebox.showwarning("Внимание", message)
            
            # С
            self.reset_colors()        
            self.selected_square = None 

    def reset_colors(self):
        """Возвращаем клеткам их законный цвет"""
        for r in range(8):
            for c in range(8):
                color = "#eeeed2" if (r + c) % 2 == 0 else "#769656"
                self.buttons[r][c].config(bg=color)