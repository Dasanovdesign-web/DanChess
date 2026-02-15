from pieces import Knight, Pawn, Bishop, Queen, King, Rook

class GameLogic:
    def __init__(self):
        self.board = [["." for _ in range(8)] for _ in range(8)]
        self.setup_board() 
        self.current_turn = "White"

    def setup_board(self):
        # 1. Расставляем пешки
        for i in range(8):
            self.board[1][i] = Pawn("Black")  # Черные пешки сверху
            self.board[6][i] = Pawn("White")  # Белые пешки снизу
        
        # 2. Тяжелые фигуры
        main_lineup = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for i in range(8):
            self.board[0][i] = main_lineup[i]("Black") # Черный тыл
            self.board[7][i] = main_lineup[i]("White") # Белый тыл

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
                    if isinstance(p, Pawn):
                        # ВАЖНО: Если белые внизу (ряд 7), они бьют ВВЕРХ (-1)
                        # Если черные вверху (ряд 0), они бьют ВНИЗ (+1)
                        direction = -1 if p.color == "White" else 1
                        if king_pos[0] == r + direction and abs(king_pos[1] - c) == 1:
                            return True
                    elif p.is_valid_move((r, c), king_pos, self.board):
                        return True
        return False

    def move_piece(self, start, end):
        r1, c1 = start
        r2, c2 = end
        piece = self.board[r1][c1]
        target = self.board[r2][c2]

        if piece == "." or piece.color != self.current_turn:
            return False, "Не ваш ход!"

        # Рокировка
        if isinstance(piece, King) and abs(c2 - c1) == 2:
            return self.handle_castling(piece, r1, c1, c2) # Вынеси в отдельный метод для чистоты

        # Обычный ход
        if target != "." and target.color == piece.color:
            return False, "Нельзя бить своих!"

        if piece.is_valid_move(start, end, self.board):
            original_target = self.board[r2][c2]
            # Временный ход
            self.board[r2][c2] = piece
            self.board[r1][c1] = "."
            
            # Проверка: остался ли шах после хода?
            if self.is_in_check(piece.color):
                self.board[r1][c1] = piece
                self.board[r2][c2] = original_target
                return False, "Ход не спасает короля!"

            piece.has_moved = True
            self.switch_turn() 
            return True, "Ход выполнен"
        
    def handle_castling(self, king, r, c1, c2):
        # Определяем, в какую сторону рокировка
        is_long = (c2 < c1)
        rook_col = 0 if is_long else 7
        rook_target_col = 3 if is_long else 5
        
        rook = self.board[r][rook_col]
        
        # 1. Проверки: не ходили ли фигуры и есть ли там ладья
        if not isinstance(rook, Rook) or king.has_moved or rook.has_moved:
            return False, "Рокировка невозможна (фигуры уже ходили)"

        # 2. Проверка: свободен ли путь для короля и ладьи
        check_cols = [1, 2, 3] if is_long else [5, 6]
        for col in check_cols:
            if self.board[r][col] != ".":
                return False, "Путь для рокировки занят"

        # 3. Проверка: не находится ли король под шахом и не проходит ли через шах
        # Король проходит через c1, d1 (для длинной) или f1 (для короткой)
        pass_cols = [2, 3, 4] if is_long else [4, 5, 6]
        for col in pass_cols:
            # Временный прыжок короля для проверки шаха на клетке
            original_pos = self.board[r][col]
            self.board[r][col] = king
            self.board[r][c1] = "." # Убираем с исходной
            
            under_attack = self.is_in_check(king.color)
            
            # Возвращаем как было
            self.board[r][c1] = king
            self.board[r][col] = original_pos
            
            if under_attack:
                return False, "Нельзя рокироваться через битое поле!"

        # Если всё ок — двигаем короля и ладью
        self.board[r][c2] = king
        self.board[r][c1] = "."
        self.board[r][rook_target_col] = rook
        self.board[r][rook_col] = "."
        
        king.has_moved = True
        rook.has_moved = True
        self.switch_turn()
        return True, "Рокировка выполнена"

    def switch_turn(self):
        """Переключает очередь хода"""
        self.current_turn = "Black" if self.current_turn == "White" else "White"

    def is_checkmate(self, color):
        """Проверяет, наступил ли мат для указанного цвета"""
        # 1. Если нет шаха, то это точно не мат
        if not self.is_in_check(color):
            return False
        
        # 2. Перебираем все фигуры этого цвета на доске
        for r1 in range(8):
            for c1 in range(8):
                piece = self.board[r1][c1]
                if piece != "." and piece.color == color:
                    # Пробуем пойти на любую клетку
                    for r2 in range(8):
                        for c2 in range(8):
                            if piece.is_valid_move((r1, c1), (r2, c2), self.board):
                                # Делаем временный мнимый ход
                                original_target = self.board[r2][c2]
                                self.board[r2][c2] = piece
                                self.board[r1][c1] = "."
                                
                                still_in_check = self.is_in_check(color)
                                
                                # Возвращаем всё назад
                                self.board[r1][c1] = piece
                                self.board[r2][c2] = original_target
                                
                                # Если хоть один ход убирает шах - мата нет!
                                if not still_in_check:
                                    return False
        # Если ни один ход не спас - это МАТ
        return True