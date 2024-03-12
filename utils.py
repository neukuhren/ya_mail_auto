"""Утилиты"""



def generate_random_password(number_symbols=12):
    """Генерирует случайный пароль из цифр и букв.
    Args:
    number_symbols : Int (число символов - длина пароля)
    Returns:
    random_password : str (сгенерированный пароль).
    """
    import secrets
    import string
    alphabet = string.ascii_letters + string.digits
    random_password = ''.join(secrets.choice(alphabet) for _ in range(number_symbols))
    return random_password



def timer_in_consol(seconds: int):
    """Запускает таймер в командной строке."""
    from time import sleep
    import sys

    for remaining in range(seconds, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("Ожидание получения письма {:2d} s".format(remaining))
        sys.stdout.flush()
        sleep(1)

    sys.stdout.write("\rПроверка получения письма            \n")




