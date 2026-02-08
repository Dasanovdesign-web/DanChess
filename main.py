import tkinter as tk
from logic import GameLogic
from gui import ChessGUI

def start_game():
    print("--- ТЕСТ ЗАПУСКА ---")
    user_name = input("Как вас зовут? ")
    print(f"Добрый день, {user_name}!")

    print("1. Создаю объект окна (root)...")
    root = tk.Tk()
    
    print("2. Инициализирую GameLogic...")
    # Если зависнет здесь — значит проблема в logic.py или pieces.py
    game_logic = GameLogic() 
    
    print("3. Инициализирую ChessGUI...")
    # Если зависнет здесь — значит проблема в gui.py
    app = ChessGUI(root, game_logic)
    
    print("4. Запускаю mainloop (сейчас должно появиться окно)...")
    root.mainloop()

if __name__ == "__main__":
    start_game()