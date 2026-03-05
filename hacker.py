import time
import os
from Algorithm_Winstons import WinstonCipher


def get_default_dictionary():
    """
    Вбудований словник для тестування, якщо файл не обрано.
    """
    words = [
        "Сервер", "Клієнт", "Трафік", "Шлюз", "Протокол",
        "Брандмауер", "Маршрут", "Вірус", "Система", "Пароль",
        "Ключ", "Шифр", "Алгоритм", "Дані", "Хакер",
        "Атака", "Загроза", "Вразливість", "Ризик", "Політика",
        "Код", "Секрет", "Логін", "Мережа", "Київ"
    ]
    return words


def load_dictionary_from_file(filepath):
    """
    Зчитує слова з текстового файлу, де кожне слово починається з нового рядка.
    """
    if not os.path.exists(filepath):
        print(f" Помилка: Файл словника '{filepath}' не знайдено!")
        return []

    words = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                word = line.strip()
                if word:
                    words.append(word)
        print(f" Словник '{filepath}' успішно завантажено. Кількість слів: {len(words)}")
        return words
    except Exception as e:
        print(f" Помилка під час читання файлу: {e}")
        return []


def crack_wheatstone(encrypted_file, marker_word, dictionary):
    if not os.path.exists(encrypted_file):
        print(f"[-] Файл {encrypted_file} не знайдено!")
        return

    with open(encrypted_file, 'r', encoding='utf-8') as f:
        ciphertext = f.read()

    total_combinations = len(dictionary) ** 2

    print("\n" + "-" * 25)
    print("Взлом шифру Уітстона ")
    print("-" * 25)
    print(f" Файл для взлому: {encrypted_file}")
    print(f"Розмір словника: {len(dictionary)} слів.")
    print(f"Можливих пар ключів для перевірки: {total_combinations}")
    print(f" Маркерне слово для перевірки успіху: '{marker_word}'")
    print("Перебір ключів...\n")

    start_time = time.time()
    attempts = 0

    for key1 in dictionary:
        for key2 in dictionary:
            attempts += 1

            cipher = WinstonCipher(key1, key2)

            decrypted = cipher.process_text(ciphertext, mode='decrypt')

            if marker_word.lower() in decrypted.lower():
                end_time = time.time()
                exec_time = end_time - start_time

                print(f"Шифр зламано!")
                print(f"Знайдено Ключ 1: {key1}")
                print(f"Знайдено Ключ 2: {key2}")
                print(f"Витрачено часу: {exec_time:.6f} секунд")
                print(f"Кількість спроб: {attempts}")
                print(f"\nРозшифрований текст:\n{decrypted[:2000]}")
                return

    end_time = time.time()
    exec_time = end_time - start_time
    print(f"Взлом не вдався. Перевірено {attempts} комбінацій за {exec_time:.4f} с.")
    print("Схоже, правильних ключів немає у нашому словнику.")


if __name__ == "__main__":
    file_to_crack = input("Введіть ім'я зашифрованого файлу(.txt): ")
    marker = input("Введіть слово, яке точно є у розшифрованому тексті : ")

    print("\nОберіть джерело словника:")
    print("1. Використати вбудований словник (25 слів)")
    print("2. Завантажити словник із текстового файлу")
    choice = input("Ваш вибір (1 або 2): ")

    dictionary = []
    if choice == '2':
        dict_file = input("Введіть ім'я файлу словника(.txt): ")
        dictionary = load_dictionary_from_file(dict_file)
        if not dictionary:
            print(" Повернення до вбудованого словника...")
            dictionary = get_default_dictionary()
    else:
        dictionary = get_default_dictionary()

    crack_wheatstone(file_to_crack, marker, dictionary)