import os
import time
from pieces import Knight, Pawn, Bishop, Queen, King, Rook

#Блок знакомства с пользователем
print("Давайте познакомимся!")
user_name = input("Как вас зовут?") #Используем username чтобы не запутаться
print (f"Добрый день, {user_name}!")
# 1. ПЕРЕВОДЧИК КООРДИНАТ
def parse_coords(input_str):
    letters = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    try:
        input_str = input_str.strip().lower()
        if len(input_str) < 2: return None
        col = letters[input_str[0]]
        row = 8 - int(input_str[1:])
        if 0 <= row <= 7 and 0 <= col <= 7:
            return row, col
        return None
    except:
        return None

# 2. ПОЛНАЯ РАССТАНОВКА
board = [["." for _ in range(8)] for _ in range(8)]

def setup_board(board):
    for i in range(8):
        board[1][i] = Pawn("White")
        board[6][i] = Pawn("Black")
    main_lineup = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
    for i in range(8):
        board[0][i] = main_lineup[i]("White")
        board[7][i] = main_lineup[i]("Black")

setup_board(board)

# 3. ГЛАВНЫЙ ЦИКЛ (Тут вся чистота)
while True:
    # ПОЛНАЯ ОЧИСТКА ЭКРАНА
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # ОТРИСОВКА (Только один раз за цикл!)
    print("\n      A   B   C   D   E   F   G   H")
    print("    " + "-" * 31) 

    for i, row in enumerate(board):
        display_row = [cell.symbol if hasattr(cell, "symbol") else cell for cell in row]
        print(f" {8 - i} | " + " | ".join(display_row) + f" | {8 - i}")
    
    print("    " + "-" * 31)
    print("      A   B   C   D   E   F   G   H")

    try:
        # ВЫБОР ФИГУРЫ
        start_pos = input("\nКакую фигуру берем? (напр. b1): ")
        start_coords = parse_coords(start_pos)
        
        if not start_coords:
            print("Неверный ввод!"); time.sleep(1); continue
            
        r1, c1 = start_coords
        piece = board[r1][c1]

        if not hasattr(piece, "symbol"):
            print("Там пусто!"); time.sleep(1); continue

        # ВЫБОР ЦЕЛИ
        end_pos = input(f"Куда двигаем {piece.symbol}? (напр. c3): ")
        end_coords = parse_coords(end_pos)

        if not end_coords:
            print("Неверная цель!"); time.sleep(1); continue

        r2, c2 = end_coords

        # ПРОВЕРКА ЛОГИКИ
        can_move = True
        if hasattr(piece, "is_valid_move"):
            can_move = piece.is_valid_move((r1, c1), (r2, c2))

        if can_move:
            board[r1][c1] = "."
            board[r2][c2] = piece
            print("Ход выполнен!"); time.sleep(0.5)
        else:
            print(f"Ошибка! {piece.symbol} так не ходит."); time.sleep(1.5)
            
    except Exception as e:
        print(f"Ошибка: {e}"); time.sleep(2)