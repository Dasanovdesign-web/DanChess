class Knight:
    def __init__(self, color):
        self.color = color
        self.is_alive = True
        self.value = 3 #Ценность фигуры
        #Беый конь ♘, черный ♞
        self.symbol = "♘" if color == "White" else "♞" 
        self.material = "porcelain" # По умолчаю сдесь будет стандартный скин клетки, в будущем тутможно менять скины доски 

    def is_valid_move(self, start_pos, end_pos):
            #рассчитываем насколько клеток мы сдвинулись
            row_diff = abs(start_pos[0] - end_pos[0])
            col_diff = abs(start_pos[1] - end_pos[1])

            #Правило буквы Г: (2 и 1) или (1 и 2)
            return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)
    

class Pawn:
    def __init__(self, color):
        self.color = color
        self.is_alive = True
        self.value = 1 #Ценность фигуры
        #Белая пешка ♙, черный ♟
        self.symbol = "♙" if color == "White" else "♟"

    def is_valid_move(self, start_pos, end_pos):
         row_diff = abs(start_pos[0] - end_pos[0])
         col_diff = abs(start_pos[1] - end_pos[1])

         if col_diff !=0:
              return False
         
         return row_diff == 1 or row_diff == 2

        
class Bishop:
    def __init__(self, color):
        self.color = color
        self.is_alive = True
        self.value = 3 #Ценность фигуры
        #Белый слон на ♗, черный ♝
        self.symbol = "♗" if color == "White" else "♝"
        pass
           
    def is_valid_move(self, start_pos, end_pos):
              #1 Считаем разницу между начальной и конечной точкой
              row_diff = abs(start_pos[0] - end_pos[0])
              col_diff = abs(start_pos[1]- end_pos[1])

              #2 Правило слона разница строк должна быть равна разнице столбцов
              # И мы добавляем row_diff > 0, чтобы нельзя было "сходить" в ту же самую клетку 
              return row_diff == col_diff and row_diff > 0
        



class Rook:
    def __init__(self, color):
        self.color = color
        self.is_alive = True 
        self.value = 5 #Ценность фигуры
        #Белая ладья ♖, черный ♜
        self.symbol = "♖" if color == "White" else "♜"
     
    def is_valid_move(self, start_pos, end_pos):
            # 1. Считаем разницу, используя правильные индексы [0] и [1]
            row_diff = abs(start_pos[0] - end_pos[0])
            col_diff = abs(start_pos[1] - end_pos[1])
            
            # 2. Правило ладьи: одна из разниц ОБЯЗАТЕЛЬНО должна быть 0, 
            # а другая больше 0(чтоб не стоять на месте)
            return (row_diff > 0 and col_diff == 0) or (row_diff == 0 and col_diff > 0)

            
         

        
class Queen:
    def __init__(self, color):
        self.color = color
        self.is_alive = True
        self.value = 9 #Ценность фигуры
        #Белый ферзь  ♕, черный ♛
        self.symbol = "♕" if color == "White" else "♛"

    def is_valid_move(self, start_pos, end_pos):
         row_diff = abs(start_pos[0] - end_pos[0])
         col_diff = abs(start_pos[1] - end_pos[1])
         #Логика ладьи (прямо) и логика слона (диагональ)
         is_rook = (row_diff > 0 and col_diff == 0) or (row_diff == 0 and col_diff > 0)
         is_bishop = (row_diff == col_diff and row_diff > 0)
         return is_rook or is_bishop




class King:
    def __init__(self, color):
        self.color = color
        self.is_alive = True
        #Белый король  ♔, черный ♚
        self.symbol = "♔" if color == "White" else "♚"
    