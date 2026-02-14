from pieces import Knight, Pawn, Bishop, Queen, King, Rook

class GameLogic:
    def __init__(self):
        self.board = [["." for _ in range(8)] for _ in range(8)]
        self.setup_board() 
        self.current_turn = "White"

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
        score = 0
        for row in self.board:
            for cell in row:
                if hasattr(cell, "value"):
                    score += cell.value if cell.color == "White" else -cell.value
        return score

    def is_in_check(self, color):
        king_pos = None
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if isinstance(p, King) and p.color == color:
                    king_pos = (r, c)
                    break
            if king_pos: break

        if not king_pos: return False

        enemy_color = "Black" if color == "White" else "White"
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p != "." and p.color == enemy_color:
                    # Специальная проверка для пешки: она бьет только по диагонали
                    if isinstance(p, Pawn):
                        direction = 1 if p.color == "White" else -1
                        if king_pos[0] == r + direction and abs(king_pos[1] - c) == 1:
                            return True
                    # Остальные фигуры проверяем как обычно
                    elif p.is_valid_move((r, c), king_pos, self.board):
                        return True
        return False

    def move_piece(self, start, end):
        r1, c1 = start
        r2, c2 = end
        piece = self.board[r1][c1]

        # 1. Проверка очереди хода
        if piece == "." or piece.color != self.current_turn:
            return False, f"Сейчас ход {self.current_turn}!"

        # 2. ЛОГИКА РОКИРОВКИ 
        if isinstance(piece, King) and abs(c2 - c1) == 2:
            if self.is_in_check(piece.color):
                return False, "Нельзя делать рокировку: король под шахом!"

            is_kingside = c2 > c1
            # Клетка, через которую проходит король (f1/f8 или d1/d8)
            step = 1 if is_kingside else -1
            passed_col = c1 + step
            
            # ПРОВЕРКА: Проходит ли король через битое поле?
            # Временно ставим короля на соседнюю клетку и проверяем шах
            self.board[r1][passed_col] = piece
            self.board[r1][c1] = "."
            if self.is_in_check(piece.color):
                self.board[r1][c1] = piece # Возвращаем назад
                self.board[r1][passed_col] = "."
                return False, "Нельзя рокироваться через битое поле!"
            self.board[r1][c1] = piece # Возвращаем назад для финального хода
            self.board[r1][passed_col] = "."

            rook_col = 7 if is_kingside else 0
            rook_new_col = 5 if is_kingside else 3
            rook = self.board[r1][rook_col]

            if isinstance(rook, Rook) and not piece.has_moved and not rook.has_moved:
                # Финальное перемещение
                self.board[r1][c2] = piece
                self.board[r1][c1] = "."
                self.board[r1][rook_new_col] = rook
                self.board[r1][rook_col] = "."
                piece.has_moved = True
                rook.has_moved = True
                self.switch_turn() 
                return True, "Рокировка выполнена!"
            return False, "Рокировка невозможна!"

               
        # 3. ОБЫЧНЫЙ ХОД
        if piece.is_valid_move(start, end, self.board):
            self.board[r2][c2] = piece
            self.board[r1][c1] = "."
            
            if hasattr(piece, 'has_moved'):
                piece.has_moved = True
            
            self.switch_turn() 
            return True, "Ход выполнен"

        return False, "Эта фигура так не ходит!"

    def switch_turn(self):
        self.current_turn = "Black" if self.current_turn == "White" else "White"