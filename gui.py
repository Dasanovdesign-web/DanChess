import tkinter as tk
from tkinter import messagebox # Чтобы выводить красивые окна с ошибками

class ChessGUI:
    def __init__(self, root, logic):
        self.root = root
        self.logic = logic
        self.selected_square = None  # Храним (r, c) первой нажатой клетки
        self.buttons = [[None for _ in range(8)] for _ in range(8)]
        
        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        """Создаем сетку кнопок 8x8, которая тянется"""
        # Разрешаем колонкам и строкам главного окна расширяться
        for i in range(8):
            self.root.grid_columnconfigure(i, weight=1)
            self.root.grid_rowconfigure(i, weight=1)

        for r in range(8):
            for c in range(8):
                color = "#eeeed2" if (r + c) % 2 == 0 else "#769656"
                
                btn = tk.Button(
                    self.root, 
                    bg=color, 
                    # Убираем фиксированные width и height или ставим 1
                    font=("Arial", 20),
                    command=lambda row=r, col=c: self.handle_click(row, col)
                )
                
                # Параметр sticky="nsew" заставляет кнопку растягиваться во все стороны
                btn.grid(row=r, column=c, sticky="nsew")
                self.buttons[r][c] = btn

    def update_display(self):
        """Синхронизируем текст на кнопках с объектами в logic.board"""
        for r in range(8):
            for c in range(8):
                piece = self.logic.board[r][c]
                # Если в клетке объект фигуры, берем его символ, иначе пустота
                symbol = piece.symbol if hasattr(piece, "symbol") else ""
                self.buttons[r][c].config(text=symbol)
        
        # Обновляем заголовок окна, показывая баланс сил
        balance = self.logic.get_balance()
        self.root.title(f"Шахматы | Перевес сил: {balance}")

    def handle_click(self, r, c):
        """Логика взаимодействия: первый клик - выбор, второй - ход"""
        if self.selected_square is None:
            # Выбираем фигуру
            if self.logic.board[r][c] != ".":
                self.selected_square = (r, c)
                self.buttons[r][c].config(bg="yellow") # Подсвечиваем выбор
        else:
            # Пытаемся сделать ход
            start = self.selected_square
            end = (r, c)
            
            # Вызываем твой метод из logic.py
            success, message = self.logic.move_piece(start, end)
            
            if success:
                self.update_display()
            else:
                # Если ход запрещен, показываем причину
                messagebox.showwarning("Внимание", message)
            
            # В любом случае сбрасываем выделение
            self.reset_colors()
            self.selected_square = None

    def reset_colors(self):
        """Возвращаем клеткам их исходный цвет"""
        for r in range(8):
            for c in range(8):
                color = "#eeeed2" if (r + c) % 2 == 0 else "#F38028"
                self.buttons[r][c].config(bg=color)