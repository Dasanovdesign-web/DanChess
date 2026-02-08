class Piece:
    """Родительский класс для всех фигур"""
    def __init__(self, color, value, symbol):
        self.color = color
        self.value = value
        self.symbol = symbol
        self.is_alive = True
        self.material = "porcelain" # Твоя идея со скинами [cite: 2026-02-02]

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, 3, "♘" if color == "White" else "♞")

    def is_valid_move(self, start_pos, end_pos):
        row_diff = abs(start_pos[0] - end_pos[0])
        col_diff = abs(start_pos[1] - end_pos[1])
        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, 1, "♙" if color == "White" else "♟")

    def is_valid_move(self, start_pos, end_pos, target_is_enemy=False):
        direction = 1 if self.color == "White" else -1
        row_diff = end_pos[0] - start_pos[0]
        col_diff = abs(end_pos[1] - start_pos[1])

        # Атака
        if col_diff == 1 and row_diff == direction:
            return target_is_enemy
        # Ход прямо
        if col_diff == 0 and not target_is_enemy:
            if row_diff == direction: return True
            if (start_pos[0] == 1 or start_pos[0] == 6) and row_diff == 2 * direction:
                return True
        return False

class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color, 3, "♗" if color == "White" else "♝")

    def is_valid_move(self, start_pos, end_pos):
        row_diff = abs(start_pos[0] - end_pos[0])
        col_diff = abs(start_pos[1] - end_pos[1])  
        return row_diff == col_diff and row_diff > 0

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, 5, "♖" if color == "White" else "♜")

    def is_valid_move(self, start_pos, end_pos):
        row_diff = abs(start_pos[0] - end_pos[0])
        col_diff = abs(start_pos[1] - end_pos[1])
        return (row_diff > 0 and col_diff == 0) or (row_diff == 0 and col_diff > 0)

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, 9, "♕" if color == "White" else "♛")

    def is_valid_move(self, start_pos, end_pos):
        row_diff = abs(start_pos[0] - end_pos[0])
        col_diff = abs(start_pos[1] - end_pos[1])
        is_rook = (row_diff > 0 and col_diff == 0) or (row_diff == 0 and col_diff > 0)
        is_bishop = (row_diff == col_diff and row_diff > 0)
        return is_rook or is_bishop

class King(Piece):
    def __init__(self, color):
        super().__init__(color, 100, "♔" if color == "White" else "♚")

    def is_valid_move(self, start_pos, end_pos):
        row_diff = abs(start_pos[0] - end_pos[0])
        col_diff = abs(start_pos[1] - end_pos[1])
        return row_diff <= 1 and col_diff <= 1 and (row_diff > 0 or col_diff > 0)