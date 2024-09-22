import subprocess
import os
from termcolor import colored
import colorama

# Инициализируем colorama для корректного отображения цветов в Windows
colorama.init(autoreset=True)


# Функция для тестирования одного файла
def run_test(input_file: str, expected_output_file: str):
    # Нормализуем путь, чтобы слэши были в одном направлении
    input_file = os.path.normpath(input_file)
    expected_output_file = os.path.normpath(expected_output_file)

    # Чтение входных данных
    with open(input_file, 'r') as f_in:
        input_data = f_in.read()

    # Чтение ожидаемого результата
    with open(expected_output_file, 'r') as f_out:
        expected_output = f_out.read().strip()

    # Запуск task1.py с передачей данных через стандартный ввод
    result = subprocess.run(
        ['python', 'task4.py'],  # Команда для запуска
        input=input_data,  # Входные данные
        text=True,  # Для работы с текстовыми данными, а не байтами
        capture_output=True  # Захватить вывод программы
    )

    # Получаем результат программы (stdout) и удаляем лишние пробелы и символы новой строки
    program_output = result.stdout.strip()

    if expected_output == "IMPOSSIBLE":
        if program_output != "IMPOSSIBLE":
            print(colored(f"Test {input_file} failed.", "red"))
            print(colored(f"Expected: {expected_output}", "yellow"))
            print(colored(f"Got: {program_output}", "yellow"))
            return False
        else:
            print(colored(f"Test {input_file} passed.", "green"))
            return True

    if program_output == "IMPOSSIBLE" and expected_output != "IMPOSSIBLE":
        print(colored(f"Test {input_file} failed.", "red"))
        print(colored(f"Expected: {expected_output}", "yellow"))
        print(colored(f"Got: {program_output}", "yellow"))
        return False

    if len(program_output) != int(input_data):
        print(colored(f"Test {input_file} failed.", "red"))
        print(colored( "Your string has wrong number of signs.", "red"))
        return False

    pup_sum = 0
    for i in range(len(program_output)):
        if program_output[i] == '+':
            pup_sum += (i + 1)
        else:
            pup_sum -= (i + 1)

    if pup_sum != 0:
        print(colored(f"Test {input_file} failed.", "red"))
        print(colored( "Wrong sign sequence!", "red"))
        return False

    print(colored(f"Test {input_file} passed.", "green"))
    return True



# Функция для запуска всех тестов
def run_all_tests():
    test_dir = './tests'  # Директория с тестами
    test_cases = [f[:-2] for f in os.listdir(test_dir) if
                  f.endswith('.a')]  # Список всех тестов по именам файлов без .a

    total_tests = len(test_cases)
    passed_tests = 0

    # Прогоняем каждый тест
    for test_case in test_cases:
        input_file = os.path.join(test_dir, test_case)
        expected_output_file = os.path.join(test_dir, test_case + '.a')

        # Если тест пройден, увеличиваем счетчик
        if run_test(input_file, expected_output_file):
            passed_tests += 1

    # Выводим итоговый результат
    print("\n" + "-" * 40)
    print(f"Total tests: {total_tests}")
    print(colored(f"Passed tests: {passed_tests}", "green"))
    print(colored(f"Failed tests: {total_tests - passed_tests}", "red"))
    if passed_tests == total_tests:
        print(colored("All tests passed!", "green", attrs=["bold"]))
    else:
        print(colored("Some tests failed.", "red", attrs=["bold"]))


if __name__ == "__main__":
    run_all_tests()
