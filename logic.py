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

        # 1. Сначала рокировка (как исключение)
        if isinstance(piece, King) and abs(c2 - c1) == 2:
            if c2 > c1: # Короткая
                rook = self.board[r1][7]
                if isinstance(rook, Rook) and not piece.has_moved and not rook.has_moved:
                    if self.board[r1][5] == "." and self.board[r1][6] == ".":
                        self.board[r1][6], self.board[r1][5] = piece, rook
                        self.board[r1][c1], self.board[r1][7] = ".", "."
                        piece.has_moved, rook.has_moved = True, True
                        return True, "Рокировка выполнена!"
            elif c2 < c1: # Длинная
                rook = self.board[r1][0]
                if isinstance(rook, Rook) and not piece.has_moved and not rook.has_moved:
                    if all(self.board[r1][i] == "." for i in range(1, 4)):
                        self.board[r1][2], self.board[r1][3] = piece, rook
                        self.board[r1][c1], self.board[r1][0] = ".", "."
                        piece.has_moved, rook.has_moved = True, True
                        return True, "Длинная рокировка!"
            return False, "Рокировка невозможна"

        # --- ВОТ ЭТО МЕСТО "ПОСЛЕ РОКИРОВКИ" --- [cite: 2026-02-05]
        
        target = self.board[r2][c2]
        
        # Проверка: нельзя бить своих [cite: 2026-02-05]
        if target != "." and target.color == piece.color:
            return False, "Там стоит ваша фигура!"

        # 2. ПРОВЕРКА ОБЫЧНОГО ХОДА
        if piece.is_valid_move(start, end, self.board):
            self.board[r2][c2] = piece
            self.board[r1][c1] = "."
            
            if hasattr(piece, 'has_moved'):
                piece.has_moved = True
                
            return True, "Ход выполнен"

        # 3. ФИНАЛЬНЫЙ СТОПОР
        return False, "Эта фигура так не ходит!"