from pieces import Knight, Pawn, Bishop, Queen, King, Rook

class GameLogic:
    def __init__(self):
        # self.board — это "память" этого конкретного объекта игры
        self.board = [["." for _ in range(8)] for _ in range(8)]
        self.setup_board() 
        # переменная памяти очередности хода
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

        # 1. Проверка очереди хода
        if piece == "." or piece.color != self.current_turn:
            return False, f"Сейчас ход {self.current_turn}!"

        # 2. ЛОГИКА РОКИРОВКИ 
        if isinstance(piece, King) and abs(c2 - c1) == 2:
            is_kingside = c2 > c1  # Определяем сторону (вправо или влево)
            rook_col = 7 if is_kingside else 0
            rook_new_col = 5 if is_kingside else 3
            rook = self.board[r1][rook_col]

            # Проверяем, что ладья на месте и ни она, ни король еще не ходили
            if isinstance(rook, Rook) and not piece.has_moved and not rook.has_moved:
                # Двигаем Короля
                self.board[r1][c2] = piece
                self.board[r1][c1] = "."
                # Двигаем Ладью
                self.board[r1][rook_new_col] = rook
                self.board[r1][rook_col] = "."
                
                # Помечаем, что они совершили свой первый ход
                piece.has_moved = True
                rook.has_moved = True
                
                self.switch_turn() 
                return True, "Рокировка выполнена!"
            else:
                return False, "Рокировка невозможна (фигуры уже ходили)!"

        # 3. Ход
        if piece.is_valid_move(start, end, self.board):
            self.board[r2][c2] = piece
            self.board[r1][c1] = "."
            
            if hasattr(piece, 'has_moved'):
                piece.has_moved = True
            
            self.switch_turn() 
            return True, "Ход выполнен"

        return False, "Эта фигура так не ходит!"

    # Метод в класс GameLogic )
    def switch_turn(self):
        if self.current_turn == "White":
            self.current_turn = "Black"
        else:
            self.current_turn = "White"