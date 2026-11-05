def findAllIndexes(word, char):
    return [i for i, c in enumerate(word.lower()) if c == char.lower()]


def getNewWordByChar(word_for_test, word_to_secret, char):
    for i in range(len(word_for_test)):
        if word_for_test[i].lower() == char.lower():
            word_to_secret[i] = word_for_test[i]
    return word_to_secret


def game():
    attempts = 5
    print("Добро пожаловать в игру виселица!")
    word_for_test = "Получатель"
    
    word_to_secret = ["*"] * len(word_for_test)
    enabled = True
    
    print(f"Ваше слово состоит из {len(word_for_test)} букв: {''.join(word_to_secret)}, попробуйте угадать его буквы!")
    
    while enabled:
        print(f"\nСейчас ваше слово выглядит так: {''.join(word_to_secret)}")
        
        char = input("Введите букву: ").lower()
        
        if not char:
            continue
            
        indexes = findAllIndexes(word_for_test, char)
        
        if len(indexes) == 0:
            attempts -= 1
            print(f"Вы не угадали букву! Осталось попыток: {attempts}")
            
            if attempts == 0:
                print(f"\nИгра завершена, вы проиграли! Слово было: {word_for_test}")
                enabled = False
        else:
            word_to_secret = getNewWordByChar(word_for_test, word_to_secret, char)
            print("Вы угадали букву!")
            if "*" not in word_to_secret:
                print(f"\nПоздравляем! Вы выиграли! Слово было: {word_for_test}")
                enabled = False


game()