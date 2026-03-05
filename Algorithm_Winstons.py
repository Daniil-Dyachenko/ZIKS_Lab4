import time
import os


class WinstonCipher:
    def __init__(self, key1, key2):
        ua_lower = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"
        ua_upper = ua_lower.upper()
        punctuation = " 0123456789.,!?-:;()\n'\"/[]{}<>@#$"
        self.alphabet = ua_lower + ua_upper + punctuation

        self.n = 10
        self.m = 10
        self.matrix1 = self._generate_matrix(key1)
        self.matrix2 = self._generate_matrix(key2)

    def _generate_matrix(self, keyword):
        keyword_clean = ""
        for char in keyword:
            if char in self.alphabet and char not in keyword_clean:
                keyword_clean += char

        remaining = "".join([c for c in self.alphabet if c not in keyword_clean])
        full_key = keyword_clean + remaining

        return [list(full_key[i:i + self.m]) for i in range(0, len(full_key), self.m)]

    def _find_pos(self, matrix, char):
        for r in range(self.n):
            for c in range(self.m):
                if matrix[r][c] == char:
                    return r, c
        return None, None

    def process_text(self, text, mode='encrypt'):
        clean_text = "".join([c if c in self.alphabet else " " for c in text])

        if len(clean_text) % 2 != 0:
            clean_text += " "

        result = ""
        for i in range(0, len(clean_text), 2):
            m1, m2 = clean_text[i], clean_text[i + 1]

            if mode == 'encrypt':
                r1, c1 = self._find_pos(self.matrix1, m1)
                r2, c2 = self._find_pos(self.matrix2, m2)

                if r1 == r2:
                    result += self.matrix2[r1][c1] + self.matrix1[r2][c2]
                else:
                    result += self.matrix2[r1][c2] + self.matrix1[r2][c1]

            elif mode == 'decrypt':
                r1, c1 = self._find_pos(self.matrix2, m1)
                r2, c2 = self._find_pos(self.matrix1, m2)

                if r1 == r2:
                    result += self.matrix1[r1][c1] + self.matrix2[r2][c2]
                else:
                    result += self.matrix1[r1][c2] + self.matrix2[r2][c1]

        return result


def main():
    print("Шифр Уітстона")
    key1 = input("Введіть перший ключ: ")
    key2 = input("Введіть другий ключ: ")

    cipher = WheatstoneCipher(key1, key2)

    while True:
        print("\nМЕНЮ: ")
        print("1. Зашифрувати файл")
        print("2. Розшифрувати файл")
        print("3. Вийти")
        choice = input("Оберіть дію: ")

        if choice == '3':
            print("Роботу завершено.")
            break

        if choice not in ['1', '2']:
            print("Невірний вибір, спробуйте ще раз.")
            continue

        mode = 'encrypt' if choice == '1' else 'decrypt'
        action_name = "Шифрування" if mode == 'encrypt' else "Дешифрування"

        input_file = input(f"Введіть ім'я вхідного файлу (.txt): ")
        output_file = input(f"Введіть ім'я файлу для збереження результату (.txt): ")

        if not os.path.exists(input_file):
            print(f"Помилка: Файл '{input_file}' не знайдено!")
            continue

        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()

        print(f"\n{action_name.lower()}...")
        start_time = time.time()

        result_text = cipher.process_text(text, mode=mode)

        end_time = time.time()
        exec_time = end_time - start_time

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result_text)

        print(f"Успішно! Результат збережено у '{output_file}'")
        print(f"Час виконання: {exec_time:.6f} секунд")
        print(f"Оброблено символів: {len(result_text)}")


if __name__ == "__main__":
    main()