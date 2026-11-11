import random as r
import os
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

class HangmanApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Игра виселица")
        self.geometry("650x450")
        self.resizable(False, False)

        self.words = self.load_words()
        self.word_for_test = ""
        self.word_to_secret = []
        self.max_attempts = 0
        self.attempts = 0
        self.guessed_letters = set()

        self.grid_columnconfigure(0, weight=1, minsize=280)
        self.grid_columnconfigure(1, weight=1, minsize=350)
        self.grid_rowconfigure(0, weight=1)

        # Левый фрейм для картинки
        self.left_frame = ctk.CTkFrame(self, corner_radius=15)
        self.left_frame.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

        self.image_label = ctk.CTkLabel(self.left_frame, text="")
        self.image_label.pack(expand=True, padx=10, pady=10)

        # Правый фрейм для управления
        self.right_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.right_frame.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")

        # Слово (ваши звёздочки, но заменим на красивые прочерки для GUI)
        self.word_label = ctk.CTkLabel(self.right_frame, text="", font=("Arial", 28, "bold"))
        self.word_label.pack(pady=(20, 10))

        # Счётчик попыток
        self.info_label = ctk.CTkLabel(self.right_frame, text="", font=("Arial", 14), text_color="gray")
        self.info_label.pack(pady=5)

        # Использованные буквы
        self.used_letters_label = ctk.CTkLabel(self.right_frame, text="", font=("Arial", 12), wraplength=300)
        self.used_letters_label.pack(pady=10)

        # Зона ввода
        self.input_frame = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        self.input_frame.pack(pady=20)

        self.input_letter = ctk.CTkEntry(self.input_frame, placeholder_text="Буква", width=60, font=("Arial", 16), justify="center")
        self.input_letter.grid(row=0, column=0, padx=5)
        self.input_letter.bind("<Return>", lambda event: self.make_move())

        self.btn_guess = ctk.CTkButton(self.input_frame, text="Проверить", width=100, command=self.make_move)
        self.btn_guess.grid(row=0, column=1, padx=5)

        # Кнопка перезапуска
        self.btn_restart = ctk.CTkButton(self.right_frame, text="Новая игра", fg_color="#27AE60", hover_color="#219653", command=self.start_new_game)
        self.btn_restart.pack(side="bottom", pady=20)

        # Старт первой игры
        self.start_new_game()
    def load_words(self) -> list:
        try:
            file_path = os.path.join(os.path.dirname(__file__), "words.txt")
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read().split()
        except FileNotFoundError:
            # Подстраховка, если файла нет рядом
            return ["ПИТОН", "ИНТЕРФЕЙС", "ПРОГРАММА"]


    def attempts_by_word_length(self, word: str) -> int:
        if len(word) < 5:
            return 5
        elif len(word) >= 5 and len(word) <= 8:
            return 7
        else:
            return 9

    def find_all_indexes(self, word, char):
        return [i for i, c in enumerate(word.lower()) if c == char.lower()]


    def get_new_word_by_char(self, word_for_test, word_to_secret, char):
        for i in range(len(word_for_test)):
            if word_for_test[i].lower() == char.lower():
                word_to_secret[i] = word_for_test[i]
        return word_to_secret

    def start_new_game(self):
        """Инициализация нового раунда."""
        if not self.words:
            self.words = ["ОШИБКА"]
            
        self.word_for_test = r.choice(self.words)
        self.max_attempts = self.attempts_by_word_length(self.word_for_test)
        self.attempts = self.max_attempts
        self.word_to_secret = ["*"] * len(self.word_for_test)
        self.guessed_letters = set()

        # Разблокируем ввод
        self.input_letter.configure(state="normal")
        self.input_letter.delete(0, 'end')
        self.btn_guess.configure(state="normal")

        self.update_ui()
        self.input_letter.focus()

    def make_move(self):
        """Основной игровой цикл, реагирующий на ввод пользователя."""
        char = self.input_letter.get().strip().lower()
        self.input_letter.delete(0, 'end')

        if not char or len(char) > 1 or not char.isalpha():
            return

        if char in self.guessed_letters:
            messagebox.showinfo("Внимание", f"Вы уже вводили букву '{char.upper()}'!")
            return

        self.guessed_letters.add(char)
        indexes = self.find_all_indexes(self.word_for_test, char)

        if len(indexes) == 0:
            self.attempts -= 1
        else:
            self.word_to_secret = self.get_new_word_by_char(self.word_for_test, self.word_to_secret, char)

        self.update_ui()
        self.check_game_status()

    def update_ui(self):
        """Обновление интерфейса на основе текущего состояния."""
        # 1. Рассчитываем, какую картинку (от 0 до 6) показать
        # Пропорционально переводим оставшиеся шаги в индекс кадра виселицы
        errors_made = self.max_attempts - self.attempts
        # Формула плавно распределяет ошибки на 6 кадров виселицы
        image_number = int((errors_made / self.max_attempts) * 6)
        image_path = f"{image_number}.png"

        if os.path.exists(image_path):
            pil_image = Image.open(image_path)
            ctk_image = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(240, 280))
            self.image_label.configure(image=ctk_image, text="")
        else:
            # Если картинок пока нет, временно пишем текстом
            self.image_label.configure(image=None, text=f"[Виселица: шаг {image_number} из 6]")

        # 2. Показываем зашифрованное слово (заменяем звёздочки на подчеркивания для красоты)
        display_word = " ".join([l if l != "*" else "_" for l in self.word_to_secret])
        self.word_label.configure(text=display_word)

        # 3. Обновляем статус попыток
        self.info_label.configure(text=f"Осталось попыток: {self.attempts} из {self.max_attempts}")

        # 4. Обновляем список использованных букв
        used = ", ".join(sorted(list(self.guessed_letters))).upper()
        self.used_letters_label.configure(text=f"Использованные буквы:\n{used}" if used else "")

    def check_game_status(self):
        """Проверка условий конца игры."""
        if "*" not in self.word_to_secret:
            self.end_game(True)
        elif self.attempts <= 0:
            self.end_game(False)

    def end_game(self, is_win):
        """Конец игры: блокировка элементов и вывод окна сообщения."""
        self.input_letter.configure(state="disabled")
        self.btn_guess.configure(state="disabled")

        if is_win:
            messagebox.showinfo("Победа! 🎉", f"Поздравляем! Вы выиграли!\nСлово было: {self.word_for_test.upper()}")
        else:
            messagebox.showerror("Поражение 💀", f"Игра завершена, вы проиграли!\nСлово было: {self.word_for_test.upper()}")


if __name__ == "__main__":
    app = HangmanApp()
    app.mainloop()
# def game(): 
#     print("Добро пожаловать в игру виселица!")
#     file = open(os.path.dirname(__file__) + "/words.txt", "r", encoding="utf-8")
#     words = file.read().split()

#     word_for_test = r.choice(words)
#     attempts = attemptsByWordLenght(word_for_test)
    
#     word_to_secret = ["*"] * len(word_for_test)
#     enabled = True
    
#     print(f"Ваше слово состоит из {len(word_for_test)} букв: {''.join(word_to_secret)}, попробуйте угадать его буквы!")
    
#     while enabled:
#         print(f"\nСейчас ваше слово выглядит так: {''.join(word_to_secret)}")
        
#         char = input("Введите букву: ").lower()
        
#         if not char:
#             continue
            
#         indexes = findAllIndexes(word_for_test, char)
        
#         if len(indexes) == 0:
#             attempts -= 1
#             print(f"Вы не угадали букву! Осталось попыток: {attempts}")
            
#             if attempts == 0:
#                 print(f"\nИгра завершена, вы проиграли! Слово было: {word_for_test}")
#                 enabled = False
#         else:
#             word_to_secret = getNewWordByChar(word_for_test, word_to_secret, char)
#             print("Вы угадали букву!")
#             if "*" not in word_to_secret:
#                 print(f"\nПоздравляем! Вы выиграли! Слово было: {word_for_test}")
#                 enabled = False


# game()