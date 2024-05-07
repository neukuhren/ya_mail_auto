#  pip install gspread
import gspread
import logging
import inspect

logger = logging.getLogger(__name__)

sa = gspread.service_account(filename='./system_files/ya-mail-auto.json')


def read_sheet(ws_name : str, file_name = 'ya_mail_auto') -> list:
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    sh = sa.open(file_name)
    ws = sh.worksheet(ws_name)
    return sh.sheet1.get_all_values()


def next_available_row(ws_name = 'lnk', file_name = "ya_mail_auto"):
    sh = sa.open(file_name)
    ws = sh.worksheet(ws_name)
    str_list = list(filter(None, ws.col_values(1)))
    return int(str(len(str_list)+1))


def write_cell(ws_name :str,
               val_col :list,
               target_row :int,
               file_name = "ya_mail_auto"
               ):
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    sh = sa.open(file_name)
    ws = sh.worksheet(ws_name)
    try:
        for pair in val_col:
            # print(pair)
            ws.update_cell(row=target_row, col=pair[1], value=str(pair[0]))
    except Exception as exc:
        logger.error(f'Незначительная ошибка при записи')
