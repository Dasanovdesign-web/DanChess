from pieces import Knight, Pawn, Bishop, Queen, King, Rook

class GameLogic:
    def __init__(self):
        # self.board — это "память" этого конкретного объекта игры
        self.board = [["." for _ in range(8)] for _ in range(8)]
        self.setup_board() 

    def setup_board(self):
        # Расставляем пешки
        for i in range(8):
            self.board[1][i] = Pawn("White")
            self.board[6][i] = Pawn("Black")
        
        # Расставляем тяжелые фигуры
        main_lineup = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for i in range(8):
            self.board[0][i] = main_lineup[i]("White")
            self.board[7][i] = main_lineup[i]("Black")

    def get_balance(self):
        # Считаем разницу очков: белые в плюс, черные в минус
        score = 0
        for row in self.board:
            for cell in row:
                if hasattr(cell, "value"):
                    # Если фигура белая — прибавляем, если черная — отнимаем
                    score += cell.value if cell.color == "White" else -cell.value
        return score

    def move_piece(self, start, end):
        r1, c1 = start
        r2, c2 = end
        piece = self.board[r1][c1]
        
        # 0. Проверка: а выбрали ли мы вообще фигуру?
        if piece == ".":
            return False, "Там нет фигуры"

        # Определяем, стоит ли на целевой клетке враг
        target = self.board[r2][c2]
        is_enemy = hasattr(target, "color") and target.color != piece.color

        # 1. Проверка валидности хода (с учетом особенностей пешки)
        if isinstance(piece, Pawn):
            # Тут мы передаем target_is_enemy, так как у пешки это важно
            if not piece.is_valid_move(start, end, target_is_enemy=is_enemy):
                return False, "Пешка так не ходит"
        else:
            # Для всех остальных фигур вызываем обычный метод
            if not piece.is_valid_move(start, end):
                return False, "Так ходить нельзя"
        
        # 2. Проверка на "дружественный огонь"
        if hasattr(target, "color") and target.color == piece.color:
            return False, "Нельзя бить своих"

        # 3. Сама логика перемещения в массиве
        self.board[r2][c2] = piece
        self.board[r1][c1] = "."
        return True, "Успешно"