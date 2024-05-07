"""Модуль для отправки сообщений.

Открывает в браузере страницу.
Авторизуется.
Отправляет сообщения.
"""

import json
import logging # Импортируем библиотеку для безопасного хранения логов
from datetime import datetime
import inspect  # Для имени функции
import pickle
import shutil  # для загрузки куки - реализует  алгоритм сериализации и десериализации объектов Python
# import re
# from openpyxl import load_workbook


from fake_useragent import UserAgent
# import requests
# # from bs4 import BeautifulSoup
import random
import sys


import requests

# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains  # Цепочка событий
from selenium.webdriver.common.keys import Keys




# pip install selenium-stealth
from selenium_stealth import stealth

from time import sleep
from time import time

from random import randint

# # - Подключение модулей -
from config import  USER_AGENT_MY_GOOGLE_CHROME, LIST_WITH_COLUMNS_LNK,\
    LIST_WITH_STATUS_MSG, LIST_WITH_COLUMNS_COMBINED
#     PARAMETER_ANSWER_A_SECRET_QUESTION, PATH_TO_FILE_DRIVER_CHROME,\
#     LIST_WITH_STATUS
#     # HEADLESS, PARAMETER_CHANGE_PASSWORD,

from utils import generate_random_password
from captcha_utils import decrypt_captcha_deform_text, hack_recaptcha_used_audio_file
from excel_utils import  open_xlsx_file_and_return_active_sheet, \
    read_xslx_with_filter_col1_col2 # write_to_excel

from txt_utils import write_in_end_row_file_txt, read_txt_file_and_lines_to_list, \
    read_txt_file_return_list_with_lines_text, read_parameters_from_txt_file_and_add_to_dict

from browser import USE_PROXY, USE_ELITE_PRIVATE_PROXY, init_driver
from work_sheet import next_available_row, write_cell

# Установлены настройки логгера для текущего файла
# В переменной __name__ хранится имя пакета;
# Это же имя будет присвоено логгеру.
# Это имя будет передаваться в логи, в аргумент %(name)
logger = logging.getLogger(__name__)

dict_with_result_lnk = {} # словарь для хранения результатов работы со ссылкой

PARAM_DICT = read_parameters_from_txt_file_and_add_to_dict()
"""Словарь с параметрами из файла config.txt"""

URL_YANDEX_RU = 'https://passport.yandex.ru'
URL_AUTO_LOGIN = 'https://auth.auto.ru/login/?r=https%3A%2F%2Fauto.ru%2F'


def get_web_page_in_browser(url: str) -> None:
    """Открывает переданный url в браузере.
    
    Args: url (str) - адрес страницы, которую нужно открыть
    Return: None
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        driver.get(url=url)  # Открытие страницы
        logger.debug(f'В браузере открыта страница {url}')
    except Exception as exc:  # Исключения
        print(exc)
    finally:  # Выполняется всегда
        pass


def find_and_click_captcha_iam_not_robot() -> None:
    """Проверяет есть ли каптча я не робот и кликает на нее.
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        el_captcha = driver.find_element(By.CLASS_NAME, "CheckboxCaptcha-Anchor")
        if el_captcha:
            logger.debug(f'На странице была найдена каптча. Кликаю')
            try:
                el_captcha.click()
            except:
                logger.error('Ошибка при клике на каптчу')
    except:
        logger.debug(f'Каптчи 1 не было, либо она не была найдена.')
    try:
        el_captcha = driver.find_element(By.CLASS_NAME, "CheckboxCaptcha-Checkbox")
        if el_captcha:
            logger.debug(f'На странице была найдена каптча. Кликаю')
            try:
                el_captcha.click()
            except:
                logger.error('Ошибка при клике на каптчу')
    except:
        logger.debug(f'Каптчи 2 не было, либо она не была найдена.')
    try:
        el_captcha = driver.find_element(By.CLASS_NAME, "CheckboxCaptcha-Button")
        if el_captcha:
            logger.debug(f'На странице была найдена каптча. Кликаю')
            try:
                el_captcha.click()
            except:
                logger.error('Ошибка при клике на каптчу')
    except:
        logger.debug(f'Каптчи 3 не было, либо она не была найдена.')
        

def find_and_click_btn_close_window() -> None:
    """Проверяет есть ли вслывающее окно и кликает на кнопку его закрытия.
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        el_btn_close_window = driver.find_element(By.CLASS_NAME, "modal__close")
        logger.debug(f'На странице было найдено всплывающее окна. Закрываю его.')
        try:
            el_btn_close_window.click()
        except:
            logger.error('Ошибка при клике на кнопку закрытия окна')
    except:
        # кнопка закрытия всплывающего окна не было
        pass


def find_add_favorite_and_click_btn_close_window() -> None:
    """Проверяет есть ли вслывающее окно "Добавить в избранное" и кликает на кнопку его закрытия.
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        el_btn_close_window = driver.find_element(By.CLASS_NAME, 'dist-favourites__close')
        logger.debug(f'Найдено всплывающее окно добавить в избранное. Закрываю его.')
        try:
            el_btn_close_window.click()
        except:
            logger.error('Ошибка при клике на кнопку закрытия окна')
    except:
        # кнопка закрытия всплывающего окна не было
        pass


def check_avatar_on_page() -> object:
    """Проверяет если есть аватар пользователя, то возвращает элемент автара на странице.
    Если аватар не найден, то возвращает None
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        el_avatar = driver.find_element(By.CLASS_NAME, "HeaderUserMenu__userPic")
        logger.debug(f'На странице был найден аватар.')
        return el_avatar
    except:
        logger.debug(f'Аватара нет на странице, либо он не был найден.')


def check_avatar2_on_page() -> object:
    """Проверяет если есть аватар пользователя, то возвращает элемент автара на странице.
    Если аватар не найден, то возвращает None
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        el_avatar = driver.find_element(By.CLASS_NAME, "UserID-Avatar")
        logger.debug(f'На странице был найден аватар.')
        return el_avatar
    except:
        logger.debug(f'Аватара нет на странице, либо он не был найден.')


def find_and_click_btn_write() -> None:
    """Проверяет есть ли кнопка и кликает на неё.
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        el_btn_signin = driver.find_element(By.CLASS_NAME, 'OpenChatByOfferButton__caption')
        if el_btn_signin:
            logger.debug(f'На странице была найдена кнопка "написать". Кликаю')
            el_btn_signin.click()
    except:
        try:
            el_btn_signin = driver.find_element(By.CLASS_NAME, 'OpenChatByOfferButton__content')
            if el_btn_signin:
                logger.debug(f'На странице была найдена кнопка "написать". Кликаю')
                el_btn_signin.click()
        except:
            pass


def find_field_and_insert_text_msg(text_msg: str) -> bool:
    """Проверяет есть ли поле для текста сообщения и вставляет текстовое значение сообщения.
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        el_field_login_passwd = driver.find_element(By.CLASS_NAME, "ChatInput__textarea")
        logger.debug(f'На странице было поле для текста сообщения')
        try:
            el_field_login_passwd.send_keys(text_msg, Keys.ENTER)
            return True
        except:
            logger.error('Ошибка при заполнении поля текста сообщения')
    except:
        logger.debug(f'Поле текста сообщения не найдено')
        return False


def check_messsage_send_ok(text_msg='no text') -> bool:
    """Проверяет отправлено ли сообщение. Возвращает bool.
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        el_chatmessage = driver.find_element(By.CLASS_NAME, "ChatMessage__text")
        logger.debug(f'el_chatmessage атрибут text имеет значение - {el_chatmessage.text}')
        logger.info(f'el_chatmessage_text - {el_chatmessage}\n')
        if el_chatmessage:
            return True
    except Exception as exc:
        logger.error(f'Сообщение не найдено. Исключение {exc}')
    return False



def send_messages_main():
    """Основная функция работы приложения. Отправка сообщений на auto.ru"""
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')

    # DICT_Y_OR_M_ACC = {'y': 'использовать yandex-аккаунты',
    #                    'm': 'использовать mailru-аккаунты',
    #                    'ym': 'использовать случайно yandex и mailru аккаунты',
    #                    }
    # print(f'Какие аккаунты использовать для рассылки сообщений?')
    # for key, mode in DICT_Y_OR_M_ACC.items():
    #     print(f'{key} - {mode}')
    #     yandex_or_mail_accs = int(input(f'Введите букву: '))
        
    # Если выбранный режим существует, то запускаем работу
    # if yandex_or_mail_accs not in DICT_Y_OR_M_ACC:
    #     logger.error('Выбранного режима не существует!')
    # else:
    # logger.info(f'Выбран режим {yandex_or_mail_accs} - {DICT_Y_OR_M_ACC[yandex_or_mail_accs]}')
    try:
        # Открываем xlsx книгу и активный лист
        wb_lnk, ws_lnk = open_xlsx_file_and_return_active_sheet(file_name='lnk.xlsx')
        if wb_lnk and ws_lnk:  # Если xlsx книга и активный лист получены
            current_row = 2  # С какой строки читать xlsx файл
            logger.debug(f'Из книги lnk.xlsx получен активный лист {ws_lnk}')

        # Пройтись со второй строки 
        cur_cell = ws_lnk.cell(row=current_row, column=1)  # столбец 1 - ссылка
        while cur_cell.value is not None:  # до первой пустой

            dict_with_result_lnk.clear()  # словарь для хранения данных о ссылке (строчке таблицы)
            
            # Прочитаем второй столбец - Message_status
            dict_with_result_lnk["Message_status"] = ws_lnk.cell(row=current_row, column=2).value
            
            # Если статус ссылки пустой, неизвестный (нет в словаре) или retry (зациклить)
            if (dict_with_result_lnk["Message_status"] is None or 
                dict_with_result_lnk["Message_status"] not in LIST_WITH_STATUS_MSG or
                dict_with_result_lnk["Message_status"] == 'retry' or
                # Или статус сообщения соответствует проверяемому (из файла config.txt)
                dict_with_result_lnk["Message_status"] == PARAM_DICT['CHECKED_LNK_MESSAGE_STATUS']):
                # то работаем со ссылкой (текущей строкой)

                # Избавимся от приставки '\ufeff' при чтении ссылки из excel
                dict_with_result_lnk["Lnk"] = cur_cell.value.replace('\ufeff', '')
                logger.debug(f'Работа со ссылкой: {dict_with_result_lnk["Lnk"]}') 
                
                try:
                    # по текущей ссылке будет выполнено 2 попытки отправки сообщения
                    number_retry = 1
                    while number_retry < 3:
                        # Начинаем переход по ссылке
                        global driver
                        try:
                            logger.debug('Запускается инициализация драйвера')
                            # pause = input('Нажмите клавишу Enter')
                            driver = init_driver()
                        except Exception as exc:
                            logger.error(f'Ошибка при инициализации экземпляра driver - {exc}')                        
                        
                        # в цикле перебираем рандомные аккаунты 
                        try:
                            avatar_ = None
                            while avatar_ is None:  # цикл до успешной авторизации
                                driver.delete_all_cookies() # удаляем cookies
                                # get_web_page_in_browser(url=URL_YANDEX_RU)
                                get_web_page_in_browser(url='https://id.yandex.ru/')
                                sleep(randint(5, 10))
                                find_and_click_captcha_iam_not_robot()
                                sleep(randint(1, 4))
                                find_and_click_btn_close_window()
                                # find_add_favorite_and_click_btn_close_window()
                                sleep(randint(1, 4))

                                # загрузить в список файлы из папки cookies_yandex
                                from os import listdir
                                from os.path import isfile, join
                                files_from_dir_cookies = [f for f in listdir('./cookies_yandex/') if isfile(join('./cookies_yandex/', f))]
                                # Выбираем файл pkl
                                random_file_cookies = random.choice(files_from_dir_cookies)
                                while random_file_cookies[-4: ] != '.pkl':
                                    random_file_cookies = random.choice(files_from_dir_cookies)
                                logger.info(f'Работаем с аккаунтом {random_file_cookies[: -4]}')
                                cookies = pickle.load(open(f"cookies_yandex/{random_file_cookies}", "rb"))
                                logger.debug(f'{cookies}')
                                if cookies is None:
                                    logger.error('Не удалось загрузить файл с куками')
                                for cookie in cookies[: -2]:
                                    try:
                                        driver.add_cookie(cookie)
                                    except Exception as exc:
                                        logger.error(f'Не удалось загрузить куки: {cookie}')
                                        print(exc)
                                sleep(randint(3, 5))              
                                # pause = input('Нажмите клавишу Enter')

                                get_web_page_in_browser(url=dict_with_result_lnk['Lnk'])
                                sleep(randint(4, 8))
                                find_and_click_captcha_iam_not_robot()
                                # hack_recaptcha_used_audio_file(driver=driver)
                                sleep(randint(5, 10))

                                # find_and_click_btn_close_window()
                                # find_add_favorite_and_click_btn_close_window()
                                # sleep(randint(1, 3))                                
                                # pause = input('Нажмите клавишу Enter')
                                # Проверяем успешность входа по аватарке HeaderUserMenu__userPic
                                avatar2 = check_avatar2_on_page()
                                if avatar2:
                                    get_web_page_in_browser(url=dict_with_result_lnk['Lnk'])
                                    sleep(5)
                                # Проверяем успешность входа по аватарке HeaderUserMenu__userPic
                                avatar_ = check_avatar_on_page()
                                if avatar_:  # Вход выполнен успешно
                                    logger.info(f'Вход с аккаунта {random_file_cookies[-4]} выполнен успешно.')
                                else:
                                    logger.info(f'Возможно вход с аккаунта {random_file_cookies[: -4]} не был успешным. Начата попытка использовать другой аккаунт...')
                                    driver.quit()
                                    sleep(3)
                                    driver = init_driver()

                                    # Меняем прокси 
                                    if USE_ELITE_PRIVATE_PROXY:
                                        r = requests.get('http://176.9.113.111:20005/?command=switch&api_key=gNMLTBja2JNqnZWZPcvi&m_key=fG4MdgHCh5&port=21285')
                                        sleep(5)
                            # pause = input('Нажмите клавишу Enter')
                            # Выполняем работу по отправке сообщения
                            find_and_click_btn_write()  # Ищем кнопку написать 2 типов и кликаем
                            logger.debug('Получение рандомного текста')
                            frases_list = read_txt_file_return_list_with_lines_text(file_name='messages.txt')
                            dict_with_result_lnk["Message_text"]=random.choice(frases_list)
                            sleep(randint(3, 5))
                            check_field_txt_msg_ = find_field_and_insert_text_msg(text_msg=dict_with_result_lnk["Message_text"])  # Ищем поле для сообщения и отправляем
                            # pause = input('Нажмите клавишу Enter')
                            if check_field_txt_msg_:
                                pause_ = 10
                                logger.info(f'Жду {pause_} секунд, до проверки сообщения.')
                                sleep(pause_)
                                # Проверка статуса отправленного сообщения
                                send_msg = check_messsage_send_ok()
                                if send_msg == True:
                                    logger.info('Сообщение было успешно отправлено.')
                                    # Если статус был 'retry' (на повторе), то статус не меняем
                                    if dict_with_result_lnk["Message_status"] != 'retry':
                                        dict_with_result_lnk["Message_status"] = 'send'
                                else:  # после неудачной отправки сообщения меняем пользователя
                                    dict_with_result_lnk['Message_status'] = 'no status'
                                    logger.info('Сообщение не отправлено.')
                            else:  # если не нашлось поля текст сообщения
                                dict_with_result_lnk["Message_status"] = 'skip'
                                number_retry = 3  # чтобы не совершать новых попыток отправки по данной ссылке
                                logger.info('Нет возможности отправки сообщения по данной ссылке (skip)')
                        except Exception as exc:
                            logger.error(f'Ошибка {exc} при авторизации или отправке сообщения. Повторнная попытка...')
                            dict_with_result_lnk["Message_status"] = 'error'
                        finally:
                            # Записать данные (новый статус, сообщение, дата, куки-автору)
                            # print(f'Получен словарь {dict_with_result_lnk}')
                            cur_cell = ws_lnk.cell(row=current_row, column=LIST_WITH_COLUMNS_LNK.index('Message_status')+1, value=dict_with_result_lnk['Message_status'])
                            cur_cell = ws_lnk.cell(row=current_row, column=LIST_WITH_COLUMNS_LNK.index('Message_text')+1, value=dict_with_result_lnk["Message_text"])
                            # находим текущую дату и время
                            cur_dt = datetime.now().strftime('%x %X')
                            dict_with_result_lnk["Message_date"] = cur_dt
                            cur_cell = ws_lnk.cell(row=current_row, column=LIST_WITH_COLUMNS_LNK.index('Message_date')+1, value=dict_with_result_lnk["Message_date"])

                            # получаем куки
                            current_cookies = driver.get_cookies()
                            logger.debug(f'Текущее значение current_cookies - {current_cookies}\n')
                            # pause = input('Нажмите клавишу Enter')

                            # сохраняем куки с помощью pickle
                            pickle.dump(driver.get_cookies(), open(f"system_files/cookies_autoru/{random_file_cookies}", "wb"))
                            logger.debug(f'Создан файл system_files/cookies_autoru/{random_file_cookies}')  

                            # сохраняем куки в json
                            with open(f'system_files/cookies_autoru/{random_file_cookies[: -4]}.json', 'w') as file:
                                json.dump(current_cookies, file)
                                logger.debug(f'Cookies аккаунта {random_file_cookies[: -4]} успешно сохранены в cookies_autoru')

                            dict_with_result_lnk['Cookies'] = current_cookies
                            if dict_with_result_lnk['Cookies']:
                                # print(dict_with_result_lnk['Cookies'])
                                cur_cell = ws_lnk.cell(row=current_row, column=LIST_WITH_COLUMNS_LNK.index('Cookies')+1, value=str(dict_with_result_lnk['Cookies']))
                                empty_row = next_available_row('lnk')
                                write_cell('lnk',
                                        [[dict_with_result_lnk["Lnk"], 1],
                                         [dict_with_result_lnk["Message_status"], 2],
                                         [dict_with_result_lnk["Message_text"], 3],
                                         [dict_with_result_lnk["Message_date"], 4],
                                         [dict_with_result_lnk["Cookies"], 5],
                                        ],
                                        target_row=empty_row,
                                        )
                            logger.info(f'Попытка сохранить книгу')
                            wb_lnk.save(filename='lnk.xlsx')  # сохранить xlsx файл
                            logger.info(f'Файл xlsx сохранен')
                            if current_row % 10 == 0:
                                shutil.copyfile('lnk.xlsx', f'backups/backup_lnk.xlsx')
                                logger.info(f'Создан backup файла combined.xlsx')
                            driver.close()  # Закрытие окна браузера
                            driver.quit()  # Выход
                            # Если работа успешна и переходим к следующей ссылке
                            if dict_with_result_lnk["Message_status"] == 'send':
                                number_retry = 3  # чтобы не совершать новых попыток отправки по данной ссылке
                            elif dict_with_result_lnk["Message_status"] == 'retry':
                                number_retry = 1  # Еще попытка отправки по данной ссылке
                            elif dict_with_result_lnk["Message_status"] == 'error':
                                number_retry += 1  
                except:
                    logger.error('При работе со ссылкой произошла ошибка. Переход к следующей ссылке.')
                finally:
                    if driver:
                        # driver.close()  # Закрытие окна браузера
                        driver.quit()  # Выход
                    # Меняем прокси вручную
                    if USE_ELITE_PRIVATE_PROXY:
                        r = requests.get('http://176.9.113.111:20005/?command=switch&api_key=gNMLTBja2JNqnZWZPcvi&m_key=fG4MdgHCh5&port=21285')
                        sleep(5)
                    elif USE_PROXY:  # или ждем пару минут до смены
                        sleep(random.randint(110, 130))
            current_row += 1
            cur_cell = ws_lnk.cell(row=current_row, column=1)  # Переход на следующую строку
            # pause = input('Нажмите клавишу Enter для продолжения работы: ')
            if cur_cell.value is None:
                logger.info(f'Обнаружена пустая строка - {current_row}.')
                need_retry_check = False  # нужна ли повторная отправка сообщений
                for r in range(2, current_row):
                    c = ws_lnk.cell(row=r, column=LIST_WITH_COLUMNS_LNK.index('Message_status')+1)
                    # если значение статуса не содержится в словаре со статусами исключая no status
                    if c.value not in LIST_WITH_STATUS_MSG[1: ] or c.value == 'retry':
                        need_retry_check = True
                if need_retry_check:
                    current_row = 2
                    logger.info(f'Начинаю повторную отправку со строки {current_row}.')
                    cur_cell = ws_lnk.cell(row=current_row, column=1)
                else:
                    print('Отправлены сообщения по всем ссылкам из списка.')
                    shutil.copyfile('lnk.xlsx', f'backups/backup_lnk.xlsx')
                    logger.info(f'Создан backup файла combined.xlsx')
                    break

        logger.info('Работа цикла отправки сообщений завершена.')

    except:
        logger.critical('КРИТИЧЕСКАЯ ОШИБКА: при выполнении главной функции. Требуется перезапуск программы.')



if __name__ == '__main__':
    start_time = time()
    # Здесь задана глобальная конфигурация для всех логгеров
    logging.basicConfig(
        handlers=[logging.StreamHandler()],
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        # filename='main.log',
        # filemode='w'
        # w — содержимое файла перезаписывается при каждом запуске программы;
        # x — создать файл и записывать логи в него; если файл с таким именем уже существует — возникнет ошибка;
        # a — дописывать новые логи в конец указанного файла.
    )
    
    send_messages_main()

    print('\n\n')
    print('Время работы программы составило: ')
    print("--- %s seconds ---" % round((time() - start_time), 0))
    print('[!] Программа выполнена.')
    
