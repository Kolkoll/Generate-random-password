from pynput.mouse import Controller
import time
import math


def main_function():
    print("Введите длину пароля")
    # Ввод длины пароля и проверка введенного значения
    length_password = ""
    alphabet = "0123456789abcdefghigklmnopqrstyvwxyzQWERTYUIOPZXCVBNMLKJHGFDSA_"
    amount_of_signs = math.ceil(math.log(len(alphabet), 2))
    while True:
        length_password = input()
        try:
            length_password = int(length_password)
            break
        except ValueError:
            print("Недопустимое значение длины пароля")
    if length_password >= 174848:
        print("Ничего не введено или длина пароля больше максимально возможной")
        print("Завершение работы")
        return
    random_data = []
    while True:
        create_entropy(random_data, length_password, amount_of_signs)
        count_0 = check_entropy(random_data)
        count_1 = length_password * amount_of_signs - count_0
        if count_1 / count_0 < 0.8 and (count_1 / count_0) > 1.3:
            print("Попробуйте поводить мышкой еще раз")
            random_data = []
            continue
        password = create_password(random_data, length_password, amount_of_signs, alphabet)
        if password is None:
            print("В пароле много повторений, сгенерируем снова")
            random_data = []
            continue
        else:
            print(password)
            print("Работа программы завершена")
            break


# Берем от пользователя источник энтропии - мышь
def create_entropy(random_data, length_password, amount_of_signs):
    amount_of_entropy = length_password * amount_of_signs / 2
    mouse = Controller()
    random_data_format = []
    print("Через 5 секунд начинайте водить мышкой по экрану")
    time.sleep(5)
    print("Начинайте")
    while amount_of_entropy > 0:
        random_data_format.append(mouse.position)
        amount_of_entropy -= 1
        time.sleep(0.2)
    print("Закончили водить мышкой")
    # Конвертируем список кортежей в список данных в двоичной СС
    for i in range(len(random_data_format)):
        random_data_format[i] = list(random_data_format[i])
    for pair in range(len(random_data_format)):
        for coordinate in range(len(random_data_format[pair])):
            random_data.append(random_data_format[pair][coordinate])
    for i in range(len(random_data)):
        random_data[i] = bin(random_data[i])


# Смотрим соотношение четных и нечетных битов
def check_entropy(random_data):
    count_0 = 0
    for i in range(len(random_data)):
        if random_data[i][len(random_data[i]) - 1] == '0':
            count_0 += 1
    return count_0


# Создаем пароль
def create_password(random_data, length_password, amount_of_signs, alphabet):
    binary_password = []
    for character in range(length_password):
        binary_string = ""
        start_of_character_code = character * amount_of_signs
        for i in range(amount_of_signs):
            binary_string = binary_string + \
                            random_data[i + start_of_character_code][len(random_data[i + start_of_character_code]) - 1]
        binary_password.append(binary_string)
    for character in range(len(binary_password)):
        binary_password[character] = int(binary_password[character], 2) % len(alphabet)
    quality = confirm_quality_password(binary_password, length_password)
    if quality is False:
        print("Пароль содержит недопустимое количество повторений")
        return None
    else:
        password = ""
        for character in range(len(binary_password)):
            password += alphabet[binary_password[character]]
        return password


# Проверяем пароль на количество повторяющихся символов
def confirm_quality_password(binary_password, length_password):
    characters_of_password = dict()
    for i in range(len(binary_password)):
        if characters_of_password.get(binary_password[i]) is None:
            characters_of_password[binary_password[i]] = 1
        else:
            characters_of_password[binary_password[i]] += 1
    for value in characters_of_password.values():
        if value > length_password / 10:
            return False
        else:
            return True


# Запуск программы
main_function()
