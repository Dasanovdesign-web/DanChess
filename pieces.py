class Piece:
    def __init__(self, color, value, symbol):
        self.color = color
        self.value = value
        self.symbol = symbol
        self.is_alive = True

    def is_path_clear(self, start_pos, end_pos, board):
        r1, c1 = start_pos
        r2, c2 = end_pos
        
        # Определяем направление шага (-1, 0 или 1)
        row_step = 0 if r1 == r2 else (1 if r2 > r1 else -1)
        col_step = 0 if c1 == c2 else (1 if c2 > c1 else -1)
        
        curr_r, curr_c = r1 + row_step, c1 + col_step
        
        # Идем до конечной клетки (не включая её)
        while (curr_r, curr_c) != (r2, c2):
            if board[curr_r][curr_c] != ".":
                return False # Путь прегражден!
            curr_r += row_step
            curr_c += col_step
        return True

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, 3, "♘" if color == "White" else "♞")

    def is_valid_move(self, start_pos, end_pos, board=None):
        row_diff = abs(start_pos[0] - end_pos[0])
        col_diff = abs(start_pos[1] - end_pos[1])
        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, 1, "♙" if color == "White" else "♟")

    def is_valid_move(self, start_pos, end_pos, board):
        direction = -1 if self.color == "White" else 1 
        row_diff = end_pos[0] - start_pos[0]
        col_diff = abs(end_pos[1] - start_pos[1])
        
        target = board[end_pos[0]][end_pos[1]]
        is_empty = (target == ".")
        is_enemy = (target != "." and target.color != self.color)

        # Ход на 2 клетки
        if col_diff == 0 and is_empty:
            if row_diff == direction: 
                return True
            
            # Проверяем начальный ряд для каждого цвета
            is_initial_row = (self.color == "White" and start_pos[0] == 6) or \
                             (self.color == "Black" and start_pos[0] == 1)
            
            if is_initial_row and row_diff == 2 * direction:
                # Важно: пешка не может прыгать ЧЕРЕЗ фигуру
                mid_row = start_pos[0] + direction
                if board[mid_row][start_pos[1]] == ".":
                    return True              
        # Атака
        if col_diff == 1 and row_diff == direction and is_enemy:
            return True
        return False

class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color, 3, "♗" if color == "White" else "♝")

    def is_valid_move(self, start_pos, end_pos, board):
        row_diff = abs(start_pos[0] - end_pos[0])
        col_diff = abs(start_pos[1] - end_pos[1])  
        # Проверяем: диагональ ли это И свободен ли путь
        if row_diff == col_diff and row_diff > 0:
            return self.is_path_clear(start_pos, end_pos, board)
        return False

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, 5, "♖" if color == "White" else "♜")
        self.has_moved = False 

    def is_valid_move(self, start_pos, end_pos, board):
        row_diff = abs(start_pos[0] - end_pos[0])
        col_diff = abs(start_pos[1] - end_pos[1])
        # Проверяем: прямая ли это И свободен ли путь
        if (row_diff > 0 and col_diff == 0) or (row_diff == 0 and col_diff > 0):
            return self.is_path_clear(start_pos, end_pos, board)
        return False

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, 9, "♕" if color == "White" else "♛")

    def is_valid_move(self, start_pos, end_pos, board):
        row_diff = abs(start_pos[0] - end_pos[0])
        col_diff = abs(start_pos[1] - end_pos[1])
        is_rook = (row_diff > 0 and col_diff == 0) or (row_diff == 0 and col_diff > 0)
        is_bishop = (row_diff == col_diff and row_diff > 0)
        # Если ход похож на ход ладьи или слона — проверяем путь
        if is_rook or is_bishop:
            return self.is_path_clear(start_pos, end_pos, board)
        return False

class King(Piece):
    def __init__(self, color):
        super().__init__(color, 100, "♔" if color == "White" else "♚")
        self.has_moved = False 

    def is_valid_move(self, start_pos, end_pos, board=None):
        row_diff = abs(start_pos[0] - end_pos[0])
        col_diff = abs(start_pos[1] - end_pos[1])
        return row_diff <= 1 and col_diff <= 1 and (row_diff > 0 or col_diff > 0)