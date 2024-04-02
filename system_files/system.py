#  pip install gspread
# https://dvsemenov.ru/google-tablicy-i-python-podrobnoe-rukovodstvo-s-primerami/
import gspread
import logging
import inspect

logger = logging.getLogger(__name__)

# Указываем путь к JSON
gc = gspread.service_account(filename='pricespy-398516-bafaee30d4c9.json')


def read_google_sheets(file_name : str = "pricespy", worksheet_name : str = 'urls') -> list:
    """Читает гугл таблицу и возвращет все ячейки в виде списка со словарями"""
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    # Открытие электронной таблицы
    sh = gc.open(file_name)
    # Выбор рабочего листа
    worksheet = sh.worksheet(worksheet_name)
    # Получение всех значений из рабочего листа в виде списка словарей
    list_of_dicts = worksheet.get_all_records()
    for dict in list_of_dicts:
        logger.info(dict)
    return list_of_dicts
    # Выводим значение ячейки A1
    # print(sh.sheet1.get('B3'))


def write_cell_on_google_sheets(file_name : str = "pricespy",
                                worksheet_name : str = 'urls',
                                target_row : int = 1,
                                target_col : int = 1,
                                value : any = 'pos'
                                ):
    """Записывает в гугл таблицу в целевую ячейку нужное значение"""
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    # Открытие электронной таблицы
    sh = gc.open(file_name)
    # Выбор рабочего листа
    worksheet = sh.worksheet(worksheet_name)
    worksheet.update_cell(row=target_row, col=target_col, value=value)
