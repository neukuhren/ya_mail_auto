"""Основной модуль - парсер.

Открывает в браузере страницу.
Авторизуется.
"""
import logging # Импортируем библиотеку для безопасного хранения логов
import inspect  # Для имени функции
import pickle  # для сохранения куки - реализует  алгоритм сериализации и десериализации объектов Python
import re
import shutil
import urllib  # понадобится для сохранения изображения
import json  # понадобится для сохранения cookies
from fake_useragent import UserAgent
import requests
# from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains  # Цепочка событий
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# pip install selenium-stealth
from selenium_stealth import stealth

from time import sleep
from time import time

from random import randint

# - Подключение модулей -
from config import  USER_AGENT_MY_GOOGLE_CHROME, PATH_TO_FILE_DRIVER_CHROME,\
    PARAMETER_ANSWER_A_SECRET_QUESTION, SLOW_INTERNET,\
    LIST_WITH_COLUMNS_COMBINED, LIST_WITH_STATUS_ACC
    # HEADLESS, PARAMETER_CHANGE_PASSWORD,
from browser import init_driver
from captcha_utils import decrypt_captcha_deform_text
from utils import  generate_random_password, timer_in_consol
from txt_utils import write_in_end_row_file_txt, read_txt_file_and_lines_to_list, \
    read_parameters_from_txt_file_and_add_to_dict
from excel_utils import open_xlsx_file_and_return_active_sheet
from captcha_utils import find_and_click_captcha_iam_not_robot, \
    decrypt_recaptcha_v2_iam_not_robot, decrypt_captcha_deform_text, \
    hack_recaptcha_used_audio_file
from vosk_simple import text_from_mp3

import logging # Импортируем библиотеку для безопасного хранения логов
# Установлены настройки логгера для текущего файла
# В переменной __name__ хранится имя пакета;
# Это же имя будет присвоено логгеру.
# Это имя будет передаваться в логи, в аргумент %(name)
logger = logging.getLogger(__name__)

PARAM_DICT = read_parameters_from_txt_file_and_add_to_dict()
"""Словарь с параметрами из файла config.txt"""

URL_YA = 'https://ya.ru'
URL_YA_AUTH = 'https://passport.yandex.ru/auth/'
URL_YA_DZEN = 'https://dzen.ru/'
URL_YA_ID = 'https://id.yandex.ru/'
URL_MAIL = 'https://trk.mail.ru/c/veoz41'
dict_with_data = {}
"""Cловарь для хранения данных об аккаунте (строчке таблицы)"""


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



def find_field_by_css_and_paste_text(field_css: str, text_for_field: str, press_key_enter=False) -> None:
    """Проверяет есть ли поле c переданным css и вставляет переданное текстовое значение.
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        el_field = driver.find_element(By.CSS_SELECTOR, field_css)
        logger.debug(f'Поле {field_css} найдено.')
        el_field.click()
        try:
            if press_key_enter:
                el_field.send_keys(text_for_field, Keys.ENTER)
            else:
                el_field.send_keys(text_for_field)
        except:
            logger.error(f'Ошибка при заполнении поля {field_css}')
    except:
        logger.error(f'Поле {field_css} не найдено.')


def find_field_by_css_and_paste_text_func2_for_many_css(field_css: str, text_for_field: str, press_key_enter=False) -> None:
    """Проверяет есть ли поле c переданным css и вставляет переданное текстовое значение.
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        for i in range(1, 100):
            try:
                el_field = driver.find_element(By.CSS_SELECTOR, f'{field_css}{i}')
                if el_field:
                    logger.debug(f'Поле {field_css} найдено.')
                    el_field.click()
                    if press_key_enter:
                        el_field.send_keys(text_for_field, Keys.ENTER)
                    else:
                        el_field.send_keys(text_for_field)
                    break
            except:
                pass
    except:
        logger.error(f'Поле {field_css} не найдено.')


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
    

def find_and_click_btn_signin() -> None:
    """Проверяет есть ли кнопка Войти с помощью и кликает на неё.
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        el_btn_signin = driver.find_element(By.CSS_SELECTOR, "#passp\:sign-in")
        logger.debug(f'На странице была найдена кнопка "Войти с помощью". Кликаю')
        try:
            el_btn_signin.click()
        except:
            logger.error('Ошибка при клике на кнопку "Войти с помощью"')
    except:
        logger.debug(f'Кнопка "Войти с помощью" не найдена')


def find_and_click_btn_with_mailru() -> None:
    """Проверяет есть ли кнопка Войти с помощью mailru и кликает на неё.
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        el_btn_signin = driver.find_element(By.CSS_SELECTOR, "body > div.Popup2.Popup2_visible.Popup2_direction_top-center.Popup2_target_anchor.Popup2_view_default > div > button:nth-child(2)")
        logger.debug(f'На странице была найдена кнопка "Войти с помощью mailru". Кликаю')
        try:
            el_btn_signin.click()
        except:
            logger.error('Ошибка при клике на кнопку "Войти с помощью mailru"')
    except:
        logger.debug(f'Кнопка "Войти с помощью mailru" не найдена')


def find_and_click_btn_accept_from_mailru() -> None:
    """Проверяет есть ли кнопка Разрешить доступ к данным mail.ru и кликает на неё.
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        el_btn_signin = driver.find_element(By.CLASS_NAME, "ui-button-main")
        logger.debug(f'На странице была найдена кнопка "Разрешить mailru". Кликаю')
        try:
            el_btn_signin.click()
        except:
            logger.error('Ошибка при клике на кнопку "Разрешить mailru"')
    except:
        logger.debug(f'Кнопка "Разрешить mailru" не найдена')


def find_and_click_btn_next() -> None:
    """Проверяет есть ли кнопка Далее и кликает на неё.
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        el_btn_signin = driver.find_element(By.CSS_SELECTOR, "#root > div > div.passp-page > div.passp-flex-wrapper > div > div > div.passp-auth-content > div.passp-route-forward > div > div > div > div > form > div.SocialSuggestRegisterLite-controls > button")
        logger.debug(f'На странице была найдена кнопка "Далее". Кликаю')
        try:
            el_btn_signin.click()
        except:
            logger.error('Ошибка при клике на кнопку "Далее"')
    except:
        logger.debug(f'Кнопка "Далее" не найдена')


def find_and_click_btn_psw() -> None:
    """Проверяет есть ли кнопка 2FA Пароль и кликает на неё.
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        el_btn_signin = driver.find_element(By.CSS_SELECTOR, "#root > div > div.passp-page > div.passp-flex-wrapper > div > div > div.passp-auth-content > div.passp-route-forward > div > div > div.Image2FA-tabs > span > label:nth-child(3) > input")
        logger.debug(f'На странице была найдена кнопка "Пароль". Кликаю')
        try:
            el_btn_signin.click()
        except:
            logger.error('Ошибка при клике на кнопку "Пароль"')
    except:
        logger.debug(f'Кнопка "Пароль" не найдена')


def find_and_click_btn_email() -> None:
    """Проверяет есть ли кнопка Почта и кликает на неё.
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        el_btn_email = driver.find_element(By.CSS_SELECTOR, "#root > div > div.passp-page > div.passp-flex-wrapper > div > div > div.passp-auth-content > div:nth-child(3) > div > div > div > div > form > div > div.layout_content > div.AuthLoginInputToggle-wrapper.AuthLoginInputToggle-wrapper_theme_contrast > div:nth-child(1) > button")
        logger.debug(f'На странице была найдена кнопка "Почта". Кликаю')
        try:
            el_btn_email.click()
        except:
            logger.error('Ошибка при клике на кнопку "Почта"')
    except:
        logger.debug(f'Кнопка "Почта" не найдена')


def find_field_and_insert_email_text_on_page_mail(login_email: str) -> None:
    """Проверяет есть ли поле "Имя аккаунта" и вставляет текстовое значение email.
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        el_field_login_email = driver.find_element(By.CSS_SELECTOR, "#root > div:nth-child(2) > div > div > div > div > div > form > div:nth-child(2) > div:nth-child(2) > div.login-row.username > div > div > div > div > div > div.base-0-2-64.first-0-2-70 > div > input")
        logger.debug(f'На странице было найдено поле login-email')
        try:
            el_field_login_email.send_keys(login_email)  # , Keys.ENTER
        except:
            logger.error('Ошибка при заполнении поля login-email')
    except:
        logger.debug(f'Поле login-email не найдено')


def find_field_and_insert_email_text_on_page_yandex(login_email: str) -> None:
    """Проверяет есть ли поле "Логин или email" на странице passport.yandex.ru и вставляет текстовое значение email.
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        el_field_login_email = driver.find_element(By.CSS_SELECTOR, "#passp-field-login")
        logger.debug(f'На странице было найдено поле login-email')
        el_field_login_email.click()
        try:
            el_field_login_email.send_keys(login_email, Keys.ENTER) 
        except:
            logger.error('Ошибка при заполнении поля login-email')
    except:
        logger.debug(f'Поле login-email не найдено')


def find_and_click_btn_input_psw() -> None:
    """Проверяет есть ли кнопка "Ввести пароль" и кликает на неё.
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        el_btn_signin = driver.find_element(By.CSS_SELECTOR, "#root > div:nth-child(2) > div > div > div > div > div > form > div:nth-child(2) > div:nth-child(2) > div:nth-child(3) > div > div > div.submit-button-wrap > button")
        logger.debug(f'На странице была найдена кнопка "Ввести пароль". Кликаю')
        try:
            el_btn_signin.click()
        except:
            logger.error('Ошибка при клике на кнопку "Ввести пароль"')
    except:
        logger.debug(f'Кнопка "Ввести пароль" не найдена')


def find_label_account_not_exist() -> bool:
    """Проверяет есть ли сообщение "Такой аккаунт не зарегистрирован".
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        el_find_label_account_not_exist = driver.find_element(By.CSS_SELECTOR, '#root > div:nth-child(2) > div > div > div > div > div > form > div:nth-child(2) > div:nth-child(2) > div.login-row.username.login-row_error > div > div > div > div.error-0-2-59 > small')
        # Логин введен некорректно или удален
        if el_find_label_account_not_exist.text == 'Такой аккаунт не зарегистрирован':
            logger.info(f'На странице было найдено поле "Такой аккаунт не зарегистрирован"')
            dict_with_data['Status'] = 'invalid'
            return True
    except:
        logger.debug(f'Метка "Такой аккаунт не зарегистрирован" не найдена')
        return False


def find_field_and_insert_passwd_text(passwd: str) -> None:
    """Проверяет есть ли поле passwd и вставляет текстовое значение пароля.
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        el_field_login_passwd = driver.find_element(By.CSS_SELECTOR, "#root > div:nth-child(2) > div > div > div > div > div > form > div:nth-child(2) > div > div.login-row.password.fill-icon > div > div > div > div > div > input")
        logger.debug(f'На странице было найдено поле passwd')
        try:
            el_field_login_passwd.send_keys(passwd , Keys.ENTER)
        except:
            logger.error('Ошибка при заполнении поле passwd')
    except:
        logger.debug(f'Поле passwd не найдено')


def find_field_retry_psw_and_insert_passwd_text(passwd: str) -> None:
    """Проверяет есть ли поле passwd и вставляет текстовое значение пароля.
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        el_field_login_passwd = driver.find_element(By.CSS_SELECTOR, "#root > div:nth-child(2) > div > div > div > div > div > form > div:nth-child(2) > div > div.login-row.password.fill-icon > div > div > div > div > div > input")
        logger.debug(f'На странице было найдено поле passwd')
        try:
            el_field_login_passwd.send_keys(passwd)  # , Keys.ENTER
        except:
            logger.error('Ошибка при заполнении поле passwd')
    except:
        logger.debug(f'Поле passwd не найдено')


def find_label_invalid_login(driver :object) -> None:
    """Проверяет есть ли сообщение passwd и вставляет текстовое значение пароля.
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        el_field_invalid_login = driver.find_element(By.ID, 'field:input-login:hint')
        # Логин введен некорректно или удален
        logger.info(f'На странице было найдено поле неверный логин')
        dict_with_data['Status'] = 'invalid'
    except:
        logger.debug(f'Поле неверный логин не найдено')



def find_el_first_email_and_click(driver :object) -> None:
    """Находит первое входящее письмо, кликает на него.
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        el_first_mail = driver.find_element(By.XPATH, '//*[@id="app-canvas"]/div/div[1]/div[1]/div/div[2]/span/div[2]/div/div/div/div/div/div[3]/div/div/div/div[1]/div/div/a[1]')
        logger.info(f'Входящее письмо найдено. Открытие...')
        try:
            el_first_mail.click()
        except:
            logger.error(f'ошибка при клике на письмо')
        # href = el_first_mail.get_attribute('href')
        # get_web_page_in_browser(url=href)
    except:
        logger.debug(f'Поле неверный логин не найдено')


def find_field_invalid_password(driver :object) -> None:
    """Проверяет есть ли поле passwd и вставляет текстовое значение пароля.
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        el_field_invalid_passwd = driver.find_element(By.ID, 'field:input-passwd:hint')
        logger.info(f'На странице было поле неверный пароль')
        dict_with_data['Status'] = 'invalid'
    except:
        logger.debug(f'Поле неверный пароль не найдено')


def find_image2fa_entertype(el_class='Image2FA-enterType') -> bool:
    """Проверяет есть ли advanced каптча формата Yandex Smart Captcha 
    по наличию надписи "Способы входа Ключом"
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        el_image2fa_entertype = driver.find_element(By.CLASS_NAME, el_class)
        if el_image2fa_entertype:
            logger.info(f'Элемент Способы входа Ключом {el_class} найден.')
            dict_with_data['Status'] = '2FA'
            return True
    except:
        logger.debug(f'Элемент Способы входа Ключом {el_class} не найден.')
        return False


def check_security_question_and_insert_answer_text(security_answer: str) -> None:
    """Проверяет есть ли поле security_question и вставляет текстовое значение ответа.
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        el_security_question = driver.find_element(By.ID, "passp-field-question")
        if el_security_question:
            logger.info(f'Требуется вход по секретному вопросу. Обрабатывается...')
            # symbol = input('Войти по секретному вопросу? (y, n): ')
            # if symbol == 'y':
            if PARAMETER_ANSWER_A_SECRET_QUESTION:
                try:
                    el_security_question.send_keys(security_answer, Keys.ENTER)
                    if PARAM_DICT['NEED_PAUSE_BEFORE_ANSWER_QUESTION'] == True:
                        pause = input('Пауза. Нажмите любую клавишу для продолжения')
                    sleep(randint(1, 3))  # задержка, перед дальнейшей проверкой аватара
                except:
                    logger.error('Ошибка при заполнении поле passwd')
            else:
                logger.debug('Вход по секретному вопросу производиться не будет.')
    except:
        logger.debug(f'Поле security_question не найдено')


def check_entry_only_sms(driver :object) -> bool:
    """Проверяет если вход возможен только по смс возвращает true.
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        el_entry_sms = driver.find_element(By.ID, "passp-field-phoneCode")
        if el_entry_sms:
            logger.info(f'Требуется вход по смс.')
            return True
    except:
        logger.debug(f'Элемента Вход по смс (типа 1) не найдено.')
    try:
        el_entry_sms2 = driver.find_element(By.CLASS_NAME, "Button2-Text")
        if el_entry_sms2.text == 'Подтвердить':
            logger.info(f'Требуется вход по смс.')
            return True
    except:
        logger.debug(f'Элемента Вход по смс (типа 2) не найдено.')


def check_entry_only_email_code() -> bool:
    """Проверяет если вход возможен только по коду с почты, то возвращает true.
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        el_entry_code = driver.find_element(By.CLASS_NAME, "Field-label")
        print(el_entry_code.text)
        # el_entry_code = driver.find_element(By.CSS_SELECTOR, "#passp-field-confirmation-code")
        # if 'код из письма' in el_entry_code.text:
        #     print('фраза код из письма найдена')
        if el_entry_code:
            logger.info(f'Требуется вход по коду с почты.')
            return True
    except:
        logger.debug(f'Элемента Вход по коду с почты не найдено.')


def check_need_recovery(driver :object) -> bool:
    """Проверяет, требует ли сайт восстановить доступ к аккаунту.
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        el_btn_recovery = driver.find_element(By.CLASS_NAME, "Button2-Text")
        if el_btn_recovery.text == 'Восстановить доступ':
            logger.debug(f'На странице необходимо восстановить доступ к аккаунту.')
            return True
    except:
        logger.debug(f'Восстановить доступ нет на странице, либо он не был найден.')


def check_avatar1_mail_on_page_and_click(driver :object) -> object:
    """Проверяет если есть аватар пользователя, то возвращает элемент автара на странице.
    Если аватар не найден, то возвращает None
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        el_avatar = driver.find_element(By.CSS_SELECTOR, "#ph-whiteline > div > div.ph-auth.svelte-1osmzf1 > div.ph-project.ph-project__account.svelte-1osmzf1 > span > div > img")
        logger.debug(f'На странице был найден аватар типа 1.')
        return el_avatar
    except:
        logger.debug(f'Аватара нет на странице, либо он не был найден.')


def check_avatar1_yandex_on_page_and_click(driver :object) -> object:
    """Проверяет если есть аватар пользователя, то возвращает элемент автара на странице.
    Если аватар не найден, то возвращает None
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        el_avatar = driver.find_element(By.CLASS_NAME, "avatar__image-wrapper")
        logger.debug(f'На странице был найден аватар.')
        return el_avatar
    except:
        logger.debug(f'Аватара нет на странице, либо он не был найден.')


def check_avatar2_on_page_and_click(driver :object) -> object:
    """Проверяет если есть аватар пользователя, то возвращает элемент автара на странице.
    Если аватар не найден, то возвращает None
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        el_avatar = driver.find_element(By.CSS_SELECTOR, "#__next > div > header > div.Header_user__1Whuh > div > button > div > div.UserID-Avatar")
        logger.debug(f'На странице был найден аватар.')
        return el_avatar
    except:
        logger.debug(f'Аватара нет на странице, либо он не был найден.')


def check_avatar3_on_page_and_click(driver :object) -> object:
    """Проверяет если есть аватар пользователя, то возвращает элемент автара на странице.
    Если аватар не найден, то возвращает None
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        el_avatar = driver.find_element(By.CLASS_NAME, "UserID-Account")
        logger.debug(f'На странице был найден аватар.')
        return el_avatar
    except:
        logger.debug(f'Аватара нет на странице, либо он не был найден.')


def check_avatar4_on_page_and_click(driver :object) -> object:
    """Проверяет если есть аватар пользователя, то возвращает элемент автара на странице.
    Если аватар не найден, то возвращает None
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        el_avatar = driver.find_element(By.CSS_SELECTOR, "#ph-whiteline > div > div.ph-auth.svelte-1og5bwk")
        logger.debug(f'На странице был найден аватар.')
        return el_avatar
    except:
        logger.debug(f'Аватара нет на странице, либо он не был найден.')


def check_avatar5_on_page_and_click(driver :object) -> object:
    """Проверяет если есть аватар пользователя, то возвращает элемент автара на странице.
    Если аватар не найден, то возвращает None
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        el_avatar = driver.find_element(By.CSS_SELECTOR, "#ph-whiteline > div > div.ph-auth.svelte-1au561b > div.ph-project.ph-project__account.svelte-1au561b > span > div > img")
        logger.debug(f'На странице был найден аватар.')
        return el_avatar
    except:
        logger.debug(f'Аватара нет на странице, либо он не был найден.')


def check_account_for_signin(driver :object) -> object:
    """Проверяет если есть ли элемент выбрать аккаунт для входа, кликает на него.
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        # el_check_account = driver.find_element(By.CLASS_NAME, "AuthAccountListItem-block")
        el_check_account = driver.find_element(By.CSS_SELECTOR, "#root > div > div.passp-page > div.passp-flex-wrapper > div > div > div.passp-auth-content > div:nth-child(3) > div > div > div > div.layout_content > div > ul > li > div > a")
        logger.debug(f'На странице был найден аккаунт для входа.')
        # el_check_account_href = el_check_account.href
        try:
            el_check_account.click()
            # get_web_page_in_browser(url=el_check_account_href)
        except:
            logger.error('Ошибка при клике на аккаунт для входа"')
    except:
        logger.debug(f'Аккаунта для входа нет на странице, либо он не был найден.')


def find_magicpromopage_title_qr_code(driver :object, el_class='MagicPromoPage-title'):
    """Проверяет есть ли MagicPromoPage-title по наличию элемента изображения qr-кода.
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        el_magicpromopage_title = driver.find_element(By.CLASS_NAME, el_class)
        if el_magicpromopage_title.text == 'Откройте приложение Яндекс.Ключ и наведите камеру на QR-код':
            logger.info(f'Элемент MagicPromoPage-title {el_class} найден.')
            dict_with_data['Status'] = 'qr code'
    except:
        logger.debug(f'Элемент MagicPromoPage-title {el_class} не найден.')


def find_advanced_captcha(driver :object, el_class='AdvancedCaptcha-SilhouetteTask'):
    """Проверяет есть ли advanced каптча формата Yandex Smart Captcha 
    по наличию надписи "Нажмите в таком порядке:"
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        el_advanced_сaptcha = driver.find_element(By.CLASS_NAME, el_class)
        if el_advanced_сaptcha:
            logger.info(f'Элемент advanced каптча {el_class} найден.')
            dict_with_data['Status'] = 'adv captcha'
            pause = 10
            logger.info(f'Ждем {pause} сек для автоматического решения через расширение браузера.')
            sleep(pause)
    except:
        logger.debug(f'Элемент advanced каптча {el_class} не найдена.')


def navigate_menu_and_change_password(el_avatar, dict_with_data) -> str:
    """Переходит через аватар или по ссылке по меню для изменения пароля.
    """
    # try:
    #     el_avatar.click()
    # except:
    #     logger.error('Ошибка при клике на аватар')
    
    get_web_page_in_browser(url='https://id.yandex.ru/security/')
    sleep(randint(1, 10)/10+2.5)  # от 0.6 до 1.4 секунды
    
    get_web_page_in_browser(url='https://id.yandex.ru/profile/password?backpath=https%3A%2F%2Fid.yandex.ru%2Fsecurity')
    sleep(randint(1, 10)/10+2.5)  # от 0.6 до 1.4 секунды
    find_field_by_css_and_paste_text(field_css='currentPassword', text_for_field=dict_with_data['Password'])
    sleep(randint(1, 10)/10+2.5)  # от 0.6 до 1.4 секунды
    
    new_psw = generate_random_password(number_symbols=12) # генерируем новый пароль
    print(f'Был сгенерирован пароль {new_psw}')
    find_field_by_css_and_paste_text(field_css='newPassword', text_for_field=new_psw)
    sleep(randint(1, 10)/10+0.5)  # от 0.6 до 1.4 секунды
    find_field_by_css_and_paste_text(field_css='repeatPassword', text_for_field=new_psw)
    try:
        image_captcha_content = find_captcha_on_css_and_save_img(el_css='captcha-image')
    except:
        logger.error(f'Каптча не найдена на странице')
    if image_captcha_content:
        captcha_code = decrypt_captcha_deform_text(PARAM_DICT['API_KEY_FOR_RUCAPTCHA'], file_name='image_captcha.png')
        if captcha_code:
            logger.info(f'Каптча расшифрована. Кодовая фраза: {captcha_code}')
            # Заполнить поле каптча
            find_field_by_css_and_paste_text(field_css='#app > div > div > form > div.b-panel__content > div > div > input', text_for_field=captcha_code, press_key_enter=True)
            sleep(randint(4, 6))
    # Если каптча во второй раз не была найдена, считаем результат успешным
    try:
        image_captcha_content = find_captcha_on_css_and_save_img(el_css='captcha-image')
        # возвращаем новый пароль
        return new_psw
    except:
        # Остается старый пароль, ничего не возвращаем
        return  None


def find_captcha_on_css_and_save_img(el_css: str, driver: object):
    """Проверяет есть ли каптча формата Изображение (простая) и сохраняет изображение для последующей отправки
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        el_сaptcha = driver.find_element(By.CSS_SELECTOR, el_css)
        if el_сaptcha:
            logger.info(f'Элемент каптча найдена через css.')
        # url_for_image_captcha = el_сaptcha.get_attribute('src')
        # print(f'url_for_image_captcha -- {url_for_image_captcha}')
        # image_captcha = requests.get(url_for_image_captcha)
        # sleep(2)
        with open('image_captcha.png', 'wb') as f:
            f.write(el_сaptcha.screenshot_as_png)
        return el_сaptcha.screenshot_as_png
    except:
        logger.debug(f'Элемент каптча {el_css} не найдена.')


def check_and_hack_captcha(driver :object, el_css: str):
    """Проверяет есть ли каптча формата Изображение и решает ее
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        image_el_сaptcha_screenshot = find_captcha_on_css_and_save_img(el_css=el_css, driver=driver)
    except:
        logger.error(f'Каптча не найдена на странице')
    if image_el_сaptcha_screenshot:
            captcha_code = decrypt_captcha_deform_text(PARAM_DICT['API_KEY_FOR_RUCAPTCHA'], file_name='image_captcha.png')
            if captcha_code:
                logger.info(f'Каптча расшифрована. Кодовая фраза: {captcha_code}')
                # Заполнить поле каптча
                find_field_by_css_and_paste_text(field_css='#app > div > div > form > div.b-panel__content > div > div > input', text_for_field=captcha_code, press_key_enter=True)
                sleep(randint(4, 6))
    # Если каптча во второй раз не была найдена, считаем результат успешным
    try:
        image_el_сaptcha_screenshot = find_captcha_on_css_and_save_img(el_css=el_css, driver=driver)
        logger.debug(f'После попытки расшифровки повторно каптча не найдена.')
        return 
    except:
        return


def find_and_click_btn_more(driver: object) -> None:
    """Проверяет есть ли кнопка Еще (чтобы войти другим способом) и кликает на нее.
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        el_btn_more = driver.find_element(By.CSS_SELECTOR, "#root > div > div.passp-page > div.passp-flex-wrapper > div > div > div.passp-auth-content > div:nth-child(3) > div > div > div > div > form > div > div.layout_controls > div.AuthSocialBlock > div > div:nth-child(2) > button")
        if el_btn_more:
            logger.debug(f'На странице была найдена кнопка Еще. Кликаю')
            try:
                el_btn_more.click()
            except:
                logger.error('Ошибка при клике на кнопку Еще')
    except:
        logger.debug(f'Кнопки Еще не было, либо она не была найдена.')


def find_and_click_btn_log_in_another_way(driver :object) -> None:
    """Проверяет есть ли кнопка Войти другим способом и кликает на нее.
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        el_btn_log_in_another_way = driver.find_element(By.CSS_SELECTOR, "#root > div > div.passp-page > div.passp-flex-wrapper > div > div > div.passp-auth-content > div.passp-route-forward > div > div > button.Button2.Button2_size_xxl.Button2_view_contrast-pseudo.Button2_width_max")
        if el_btn_log_in_another_way:
            logger.debug(f'На странице была найдена кнопка Войти другим способом. Кликаю')
            try:
                el_btn_log_in_another_way.click()
            except:
                logger.error('Ошибка при клике на кнопку Войти другим способом')
    except:
        logger.debug(f'Кнопки Войти другим способом не было, либо она не была найдена.')


def find_and_click_btn_sent_mail_for_login(driver :object) -> None:
    """Проверяет есть ли кнопка отправить письмо для входа.
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        el_btn_sent_mail_for_login = driver.find_element(By.CSS_SELECTOR, "#root > div > div.passp-page > div.passp-flex-wrapper > div > div > div.passp-auth-content > div.passp-route-forward > div > div > form > div > div.layout_controls > div > button")
        if el_btn_sent_mail_for_login:
            logger.debug(f'На странице была найдена кнопка отправить письмо для входа. Кликаю')
            try:
                el_btn_sent_mail_for_login.click()
            except:
                logger.error('Ошибка при клике на кнопку отправить письмо для входа')
    except:
        logger.debug(f'Кнопки отправить письмо для входа не было, либо она не была найдена.')


def auth_yandex_with_mailru_acc(driver :object):
    """Авторизация на passport.yandex.ru. Изменяет словарь с данными аккаунта."""
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    get_web_page_in_browser(url=URL_YA_AUTH)
    sleep(2)
    # find_and_click_btn_more(driver=driver)
    # sleep(1)
    # find_and_click_btn_log_in_another_way(driver=driver)
    find_and_click_captcha_iam_not_robot(driver=driver)
    sleep(0.5)
    find_and_click_btn_close_window()
    sleep(0.5)
    find_add_favorite_and_click_btn_close_window()
    sleep(0.5)
    # find_and_click_btn_signin()  # AuthSocialBlock-provider  Для активации текстового поля email
    find_field_and_insert_email_text_on_page_yandex(dict_with_data['Login'])
    sleep(randint(1, 3))
    # Провериить если надпись Письмо со ссылкой придёт на почту honwerve@mail.ru. Откройте его на любом устройстве
    # Нажать кнопку отправить письмо для входа
    # Открыть в новой вкладке https://e.mail.ru/inbox/ 
    # Достать пароль из письма

    # find_and_click_btn_with_mailru()
    # sleep(randint(5, 10))
    # Ожидаем загрузку нового окна разрешить доступ через mail.ru
    # Setup wait for later
    # wait = WebDriverWait(driver, 10)
    # Store the ID of the original window
    original_window = driver.current_window_handle
    # wait.until(EC.number_of_windows_to_be(2))
    # Loop through until we find a new window handle
    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break
    # Wait for the new tab to finish loading content
    # wait.until(EC.title_is("SeleniumHQ Browser Automation"))
    # Если вход возможен только по коду из смс
    if check_entry_only_email_code():
        dict_with_data['Status'] = 'only mail ok'
    # elif check_entry_only_sms():
    #     dict_with_data['Status'] = 'only mail ok'
    # elif check_need_recovery():
    #     dict_with_data['Status'] = 'only mail ok'
    else:
        # Нажимаем разрешить ui-button-main
        find_and_click_btn_accept_from_mailru()
        sleep(randint(1, 3))
        # Loop through until we find a new window handle
        for window_handle in driver.window_handles:
            if window_handle != None:
                driver.switch_to.window(window_handle)
                break
        find_and_click_btn_next()
        sleep(randint(1, 3))
        cur_avatar_obj = None
        # print('Проверяю аватар')
        el_avatar1 = check_avatar1_yandex_on_page_and_click()  # аватар 1 вида
        el_avatar2 = check_avatar2_on_page_and_click()  # аватар 2 вида
        el_avatar3 = check_avatar3_on_page_and_click()  # аватар 3 вида
        el_avatar4 = check_avatar4_on_page_and_click()  # аватар 4 вида
        if el_avatar1 or el_avatar2 or el_avatar3 or el_avatar4:
            logger.info(f'Вход выполнен успешно')
            dict_with_data['Status'] = 'ok'
            if el_avatar1: 
                cur_avatar_obj = el_avatar1
            elif el_avatar2:
                cur_avatar_obj = el_avatar2
            elif el_avatar3:
                cur_avatar_obj = el_avatar3
            elif el_avatar4:
                cur_avatar_obj = el_avatar4
            if PARAM_DICT['PARAMETER_CHANGE_PASSWORD_USE_PSW'] == 'True':
                new_psw = navigate_menu_and_change_password(el_avatar=cur_avatar_obj, dict_with_data=dict_with_data)
                if new_psw:
                    dict_with_data['Password'] = new_psw
            # получаем cookies yandex.ru
            current_cookies = driver.get_cookies()
            # print(f'\n\n{current_cookies}\n\n')
            # сохраняем cookies yandex.ru в словарь
            dict_with_data['Cookies'] = current_cookies
            #получаем и сохраняем куки mail с помощью pickle
            pickle.dump(driver.get_cookies(), open(f"cookies_mailru/{dict_with_data['Login']}.pkl", "wb"))
        else:
            logger.error(f'Авторизация в yandex не выполнена')
            dict_with_data['Status'] = 'only mail ok'


def find_window_enable_push_in_browser_and_click_cancel(driver :object) -> None:
    """Проверяет есть ли вслывающее окно "Уведомления в браузере" и нажимает кнопку Отмена.
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:  # selector окна
        el_window_enable_push = driver.find_element(By.CSS_SELECTOR, "body > div.flexContainer-0-2-187 > div:nth-child(2) > div")
        logger.debug(f'На странице было найдено всплывающее окна. Закрываю его.')
    except:
        logger.debug(f'Всплывающее окно Включить уведомления не найдено.')
    try:  # селектор кнопки включить
        el_btn_enable_in_push_window = driver.find_element(By.CSS_SELECTOR, "body > div.flexContainer-0-2-187 > div:nth-child(2) > div > div > div.wrapper-0-2-167 > div.buttonsBlock-0-2-197 > div:nth-child(1) > button")
        logger.debug(f'На странице была найдена кнопка Включить.')
    except:
        logger.debug(f'Кнопки Включить уведомления не найдено.')
    try:  # селектор кнопки отмена
        el_btn_cancel_in_push_window = driver.find_element(By.CSS_SELECTOR, "body > div.flexContainer-0-2-187 > div:nth-child(2) > div > div > div.wrapper-0-2-167 > div.buttonsBlock-0-2-197 > div:nth-child(3) > button")
        logger.debug(f'На странице была найдена кнопка Отмена.')
        try:
            el_btn_cancel_in_push_window.click()
        except:
            logger.error('Ошибка при клике на кнопку Отмена')
    except:
        logger.debug(f'Кнопки Отмена уведомлений не найдено.')


def find_window_make_its_you_and_click_its_me(driver: object) -> None:
    """Проверяет есть ли вслывающее окно "Хотим убедиться что это Вы" и нажимает кнопку Это я.
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    # try:  # selector окна
    #     el_window_make_its_you = driver.find_element(By.CSS_SELECTOR, "body > div.flexContainer-0-2-187 > div:nth-child(2) > div")
    #     logger.debug(f'На странице было найдено всплывающее окна. Закрываю его.')
    # except:
    #     logger.debug(f'Всплывающее окно Включить уведомления не найдено.')
    # try:  # селектор кнопки Назад
    #     el_btn_enable_in_push_window = driver.find_element(By.CSS_SELECTOR, "body > div.flexContainer-0-2-187 > div:nth-child(2) > div > div > div.wrapper-0-2-167 > div.buttonsBlock-0-2-197 > div:nth-child(1) > button")
    #     logger.debug(f'На странице была найдена кнопка Включить.')
    # except:
    #     logger.debug(f'Кнопки Включить уведомления не найдено.')
    try:  # селектор кнопки Это я
        el_btn_its_me_in_push_window = driver.find_element(By.CSS_SELECTOR, "#root > div:nth-child(2) > div > div > div > div > div > button.base-0-2-62.primary-0-2-76.auto-0-2-88")
        logger.debug(f'На странице была найдена кнопка Это я".')
        try:
            el_btn_its_me_in_push_window.click()
        except:
            logger.error('Ошибка при клике на кнопку Это я')
    except:
        logger.debug(f'Кнопки Это я уведомлений не найдено.')
        return
    # Если кнопка Это я кликнута успешно, то
    # Повторно ввести пароль
    find_field_retry_psw_and_insert_passwd_text(passwd=dict_with_data['Password'])
    # Нажать кнопку я не робот
    find_and_click_captcha_iam_not_robot(driver=driver)
    # !!!!!!!!!!!!! ПОПРАВИТЬ Здесь возникает проблема с поиском чекбокса я не робот


def find_window_add_phone_number_and_click_cancel(driver :object) -> None:
    """Проверяет есть ли вслывающее окно "Добавление номера телефона" и нажимает кнопку Отмена.
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:  # selector окна
        el_btn_cancel = driver.find_element(By.CSS_SELECTOR, "body > div.flexContainer-0-2-9 > div:nth-child(2) > div > div > div > div.wrapper-0-2-21 > form > button:nth-child(10) > span")
        logger.debug(f'На странице было найдено всплывающее окно. Закрываю его.')
        try:
            el_btn_cancel.click()
        except:
            logger.error('Ошибка при клике на кнопку Отмена')
    except:
        logger.debug(f'Всплывающее окно "Добавление номера телефона" не найдено.')


def check_account_mailru():
    """Начинает проверку акаунта @mail.ru. Изменяет словарь с данными аккаунта.
    В случае успеха сохраняет cookies mail.ru"""
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    logger.debug(f'\nТекущее значение dict_with_data:\n{dict_with_data}')
    global driver
    if len(dict_with_data) != 0:
        try:
            logger.debug('Запускается инициализация драйвера')
            driver = init_driver()
        except:
            logger.critical('Ошибка при инициализации экземпляра driver')

        get_web_page_in_browser(url=URL_MAIL)
        sleep(2)
        # find_and_click_captcha_iam_not_robot()
        # sleep(0.5)
        # find_and_click_btn_close_window()
        # sleep(0.5)
        # find_add_favorite_and_click_btn_close_window()
        # sleep(0.5)
        # find_and_click_btn_signin()
        # pause = 10 if SLOW_INTERNET else randint(1, 3)
        # sleep(pause)
        # find_and_click_btn_email()
        # sleep(randint(1, 3))
        find_field_and_insert_email_text_on_page_mail(login_email=dict_with_data['Login'])
        sleep(1)
        find_and_click_btn_input_psw()
        sleep(randint(1, 3))
        account_not_exist = find_label_account_not_exist()
        if account_not_exist:
            dict_with_data['Status'] = 'not exist'
        else:
            find_field_and_insert_passwd_text(passwd=dict_with_data['Password'])
            sleep(3)
            find_window_make_its_you_and_click_its_me(driver=driver)
            sleep(2)
            # find_and_click_captcha_iam_not_robot(driver=driver)
            hack_recaptcha_used_audio_file(driver=driver)
            find_label_invalid_login(driver=driver)
            # if find_image2fa_entertype():
            #     find_and_click_btn_psw()
            #     sleep(1)
            #     find_field_and_insert_passwd_text(passwd=dict_with_data['Password'])
            find_field_invalid_password(driver=driver)
            find_advanced_captcha(driver=driver)
            find_magicpromopage_title_qr_code(driver=driver)

            # Ищем и решаем каптчу картинку два раза
            check_and_hack_captcha(driver=driver, el_css='#app > div > div > form > div.b-panel__content > div > img')
            sleep(2)
            check_and_hack_captcha(driver=driver, el_css='#app > div > div > form > div.b-panel__content > div > img')
            
            # check_security_question_and_insert_answer_text(security_answer=dict_with_data['Answer'])
            sleep(2)
            find_window_enable_push_in_browser_and_click_cancel(driver=driver)
            cur_avatar_obj = None
            # Если вход возможен только по коду из смс
            if check_entry_only_sms(driver=driver):
                dict_with_data['Status'] = 'sms'
            
            elif check_need_recovery(driver=driver):
                dict_with_data['Status'] = 'recovery'

            else:
                # print('Проверяю аватар')
                el_avatar1 = check_avatar1_mail_on_page_and_click(driver=driver)  # аватар 1 вида
                el_avatar2 = check_avatar2_on_page_and_click(driver=driver)  # аватар 2 вида
                el_avatar3 = check_avatar3_on_page_and_click(driver=driver)  # аватар 3 вида
                el_avatar4 = check_avatar4_on_page_and_click(driver=driver)  # аватар 4 вида
                el_avatar5 = check_avatar5_on_page_and_click(driver=driver)  # аватар 4 вида
                if el_avatar1 or el_avatar2 or el_avatar3 or el_avatar4 or el_avatar5:
                    logger.info(f'Вход в mail.ru выполнен успешно')
                    dict_with_data['Status'] = 'ok'

                    # Сохраняем объект текущего аватара (если в дальнейшем понадобится для клика по нему)
                    if el_avatar1: 
                        cur_avatar_obj = el_avatar1
                    elif el_avatar2:
                        cur_avatar_obj = el_avatar2
                    elif el_avatar3:
                        cur_avatar_obj = el_avatar3
                    elif el_avatar4:
                        cur_avatar_obj = el_avatar4
                    elif el_avatar5:
                        cur_avatar_obj = el_avatar5
                    
                    find_window_add_phone_number_and_click_cancel(driver=driver)

                    # получаем cookies
                    current_cookies = driver.get_cookies()
                    # logger.debug(f'\n\n{current_cookies}\n\n')
                    # сохраняем cookies в словарь
                    dict_with_data["Cookies_mailru"] = current_cookies
                    #получаем и сохраняем куки с помощью pickle
                    pickle.dump(driver.get_cookies(), open(f"cookies_mailru/{dict_with_data['Login']}.pkl", "wb"))
                    # Получаем и сохраняем куки в json
                    with open(f'cookies_mailru/{dict_with_data["Login"]}.json', 'w') as file:
                        json.dump(current_cookies, file)

                    if PARAM_DICT['PARAMETER_CHANGE_PASSWORD_USE_PSW'] == 'True':
                        new_psw = navigate_menu_and_change_password(el_avatar=cur_avatar_obj, dict_with_data=dict_with_data)
                        if new_psw:
                            dict_with_data['Password'] = new_psw
                else:
                    dict_with_data['Status'] = 'unknow'

            # Если статус аккаунта ок, то получим личные данные из профиля (Имя и Фамилия)
            if dict_with_data['Status'] == 'ok':
                if  PARAM_DICT["USED_NAME_FROM_MAILRU"] == 'True':
                    try:
                        get_web_page_in_browser(url='https://id.mail.ru/profile?utm_campaign=mailid&utm_medium=ph&from=headline')
                        sleep(5)
                        el_full_name = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div[1]/div/div[4]/h4')
                        first_name = el_full_name.text.split()[0]
                        last_name = el_full_name.text.split()[1]
                        dict_with_data["first_name"] = first_name
                        dict_with_data["last_name"] = last_name
                        logger.info(f'Извлечены личные данные: {first_name} {last_name}')
                    except:
                        pass
                    finally:
                        get_web_page_in_browser(url='https://trk.mail.ru/c/veoz41')
                        sleep(3)
            # Если статус аккаунта не ок, то закрываем брузер (переход к следующему аккаунту)
            else:
            # print(user_data)
            # forward_to_next_account = input('Перейти к следующему аккаунту? (y/n): ')
            # if forward_to_next_account == 'y':
                # удаляем cookies
                driver.delete_all_cookies()
                # sleep(0.5)
                if PARAM_DICT['NEED_PAUSE_BEFORE_CLOSED_BROWSER']  == 'True':  # Строка, так как из текстового конфига
                    pause = input('нажмите любую клавишу для продолжения')
                driver.close()  # Закрытие окна браузера
                driver.quit()  # Выход
            # print(f'Обновленные данные {dict_with_data}')


def create_on_mailru_psw_for_external_apps(driver :object) -> None:
    """Производит на странице mail.ru действия по получению пароля для приложений 
    для аккаунтов со статусом ok.
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    get_web_page_in_browser(url='https://account.mail.ru/user/2-step-auth/passwords?back_url=https%3A%2F%2Fid.mail.ru%2Fsecurity')
    sleep(2)
    get_web_page_in_browser(url='https://account.mail.ru/user/2-step-auth/passwords/add')
    sleep(2)
    find_field_by_css_and_paste_text_func2_for_many_css(field_css='#name_',
                                     text_for_field='Psw_mailru_for_app',
                                     press_key_enter=True
                                     )
    # decrypt_recaptcha_v2_iam_not_robot(driver=driver,
                                    #    api_key_for_rucaptcha=PARAM_DICT["API_KEY_FOR_RUCAPTCHA"])
    sleep(1)
    hack_recaptcha_used_audio_file(driver=driver)
    

    # получаем cookies
    current_cookies = driver.get_cookies()
    # logger.debug(f'\n\n{current_cookies}\n\n')
    # сохраняем cookies в словарь
    dict_with_data['Cookies'] = current_cookies
    #получаем и сохраняем куки с помощью pickle
    pickle.dump(driver.get_cookies(), open(f"cookies_mailru/{dict_with_data['Login']}.pkl", "wb"))
    # Получаем и сохраняем куки в json
    with open(f'cookies_mailru/{dict_with_data["Login"]}.json', 'w') as file:
        json.dump(current_cookies, file)
# print(user_data)
# forward_to_next_account = input('Перейти к следующему аккаунту? (y/n): ')
# if forward_to_next_account == 'y':
    # удаляем cookies
    driver.delete_all_cookies()
    # sleep(0.5)
    if PARAM_DICT['NEED_PAUSE_BEFORE_CLOSED_BROWSER']  == 'True':  # Строка, так как из текстового конфига
        pause = input('нажмите любую клавишу для продолжения')
    driver.close()  # Закрытие окна браузера
    driver.quit()  # Выход
    # print(f'Обновленные данные {dict_with_data}')


def click_smart_captcha():
    """Кликает на смарт каптчу"""
    try:  # если появляется smart captcha
        # находим надпись smart captcha (если ее нет, то попадаем в except)
        driver.find_element(By.CSS_SELECTOR, "#checkbox-captcha-form > div.Spacer.Spacer_auto-gap_bottom > div > div.Text.Text_color_ghost.Text_weight_regular.Text_typography_control-s.CaptchaLinks.CheckboxCaptcha-Links > div > a")
        driver.find_element(By.CSS_SELECTOR, "#js-button").click()
        try:
            text_captcha = driver.find_element(By.CSS_SELECTOR, "#advanced-captcha-form > div > div > div.AdvancedCaptcha-SilhouetteTask > span")
            if text_captcha:
                logger.info('Обнаружена smart captcha - решить не удется')
                dict_with_data["Status"] = 'no yandex status'
        except:
            logger.info('Вероятно, smart captcha решена успешно. Ожидание загрузки страницы...')
            sleep(10)
    except:
        logger.debug('Возможно, smart captcha не найдена')


def auth_on_yandexru_with_email_verify(driver :object) -> None:
    """Производит авторизацию в passpot.yandex.ru с запросом кода подтверждения на эл почту.
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')

    # Open a new window
    driver.execute_script("window.open('');")
    # Switch to the new window in new Tab
    driver.switch_to.window(driver.window_handles[1])
    get_web_page_in_browser(url=URL_YA_AUTH)
    click_smart_captcha()
    sleep(2)
    hack_recaptcha_used_audio_file(driver=driver)
    sleep(2)
    try:
        find_field_and_insert_email_text_on_page_yandex(login_email=dict_with_data["Login"])
    except:
        dict_with_data["Status"] = 'no yandex status'
        return
    sleep(2)
    find_and_click_captcha_iam_not_robot(driver=driver)
    sleep(5)
    hack_recaptcha_used_audio_file(driver=driver)
    sleep(3)
    find_field_by_css_and_paste_text(field_css='#passp-field-passwd',
                                     text_for_field=dict_with_data["Password"],
                                     press_key_enter=True)
    sleep(1)
    find_and_click_btn_sent_mail_for_login(driver=driver)
    # Входите по лицу или отпечатку пальца - Не сейчас
    try:
        driver.find_element(By.CSS_SELECTOR, '#root > div > div.passp-page > div.passp-flex-wrapper > div > div > div.passp-auth-content > div.passp-route-forward > div > div > div > div:nth-child(5) > button').click()
    except:
        pass
    sleep(5)

    # Проверяем - авторизация по коду из письма?
    is_auth_with_code_from_email = None
    try:
        is_auth_with_code_from_email = driver.find_element(By.ID, 'passp-field-phoneCode')
        logger.info(f'Яндекс требует авторизации по коду из письма')
    except:
        pass
    # Switch back to the first tab
    driver.switch_to.window(driver.window_handles[0])
    timer_in_consol(10)
    driver.refresh()
    # driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'r')
    sleep(5)
    find_el_first_email_and_click(driver=driver)
    sleep(4)
    if is_auth_with_code_from_email:  # если авторизация по коду из письма
        secret_code = None
        try:
            el_code = driver.find_element(By.CSS_SELECTOR, '#style_17101535751861182055_BODY > div > table > tbody > tr > td > table:nth-child(2) > tbody > tr > td > p:nth-child(3)')
            if int(el_code.text) in range(0, 1000000):
                secret_code = el_code.text
                logger.info(f'Код найден по css_selector. Значение {secret_code}')
            else:
                secret_code = None
        except:
            logger.debug(f'Элемент с кодом не найден по css_selector')
        if secret_code == None:  # Если значение кода не найдено, то пробуем найти через тег b
            try:
                elements = driver.find_elements(By.TAG_NAME, "p")
                for el in elements:
                    try:
                        if int(el.text) in range(0, 1000000):
                            secret_code = el.text
                            logger.info(f'Код найден по тегу. Значение {secret_code}')
                            break
                    except:
                        pass
            except:
                logger.debug(f'Элемент с кодом не найден по тегу')
        if secret_code:
            try:
                driver.switch_to.window(driver.window_handles[-1])
                el_field = driver.find_element(By.ID, 'passp-field-phoneCode')
                el_field.click()
                try:
                    el_field.send_keys(secret_code, Keys.ENTER)
                except:
                    logger.error(f'Ошибка при заполнении поля код')







                    # !!!!!!!!!!!!!!!!
                # find_field_by_css_and_paste_text(field_css=)
            except:
                logger.error(f'Не удалось найти поле код')
    else:  # иначе авторизация по кнопке
        elements = driver.find_elements(By.TAG_NAME, "a")
        url_login_yandex = ''
        for el in elements:
            try:
                link = el.get_attribute("href")
                if 'https://passport.yandex.ru/auth' in link:
                    url_login_yandex = link
                    logger.info(f'Секретная ссылка извлечена успешно:\n{url_login_yandex}')
                    break
            except:
                pass
        get_web_page_in_browser(url=url_login_yandex)
        sleep(3)
        click_smart_captcha()
        # Клик по кнопке войти
        driver.find_element(By.CSS_SELECTOR, "#root > div > div.passp-page > div.passp-flex-wrapper > div > div > div.passp-auth-content > div:nth-child(3) > div > div > div.auth_letter_action-buttons > div:nth-child(2) > button").click()
        sleep(2)
    driver.switch_to.window(driver.window_handles[-1])
    sleep(2)
    try:
        # Если имя и фамилия не были получены с личных данных mail.ru
        # проверим по наличию ключа в словаре
        if ("first_name" in dict_with_data) and ("last_name" in dict_with_data):
            pass
        else:
            # то сгенерировать русские имя и фамилию
            from russian_names import RussianNames
            rn = RussianNames(count=1, patronymic=False, transliterate=False)
            for person in rn:
                first_name = person.split()[0]
                last_name = person.split()[1]
        # Ввод имени и фамилии при необходимости
        find_field_by_css_and_paste_text(field_css='#passp-field-firstname',
                                        #  dict_with_data['Login'].split('@')[0]
                                        text_for_field=first_name,
                                        press_key_enter=False
                                        )
        find_field_by_css_and_paste_text(field_css='#passp-field-lastname',
                                        #  Фамилия - реверс имени
                                        # dict_with_data['Login'].split('@')[0][::-1]
                                        text_for_field=last_name,
                                        press_key_enter=True)
        sleep(2)
        # Пароль
        find_field_by_css_and_paste_text(field_css='#passp-field-password',
                                         text_for_field=dict_with_data['Password'],
                                         press_key_enter=False)
        sleep(2)
        # Далее
        driver.find_element(By.CSS_SELECTOR, '#root > div > div.passp-page > div.passp-flex-wrapper > div > div > div.passp-auth-content > div.passp-route-forward > div > div > form > div > div > div.passp-button.passp-lite__password-submit > button').click()
        sleep(2)
        # Зарегистрироваться
        driver.find_element(By.CSS_SELECTOR, '#root > div > div.passp-page > div.passp-flex-wrapper > div > div > div.passp-auth-content > div.passp-route-forward > div > div > form > div.passp-button.passp-lite__password-submit > button').click()
        dict_with_data["first_name"] = first_name
        dict_with_data["last_name"] = last_name
        sleep(2)
        # Email
        find_field_by_css_and_paste_text(field_css='#passp-field-email',
                                         text_for_field=dict_with_data["Login"],
                                         press_key_enter=False)
        # Продолжить
        driver.find_element(By.CSS_SELECTOR, '#passp\:email\:controls\:next').click()
        sleep(2)
    except:
        pass
    sleep(7)
    driver.refresh()
    sleep(3)
    # Подписаться на дзен
    get_web_page_in_browser(url=URL_YA_DZEN)
    sleep(5)
    try:
        ava = driver.find_element(By.CSS_SELECTOR, '#dzen-header > div.desktop-base-header__controls-3o.desktop-base-header__isMorda-mX > div.desktop-base-header__profileButton-bf.desktop-base-header__isMorda-mX.desktop-base-header__isAuthorized-Yz')
        if ava:
            ava.click()
            sleep(2)
            try:
                btn_create_post = driver.find_element(By.CLASS_NAME, "menu-items__createPublication-2b")
                if btn_create_post:  # Если есть кнопка создать публикацию есть, значит акк уже привязан к дзен
                    dict_with_data["Dzen_status"] = 'ok'
                    logger.info(f'Аккаунт {dict_with_data["Login"]} уже подключен к Дзен.')
            except:
                logger.debug('кнопка создать пост не найдена')
                try:
                    # Кнопки Это мой аккаунт и Разрешить доступ
                    allow_access = driver.find_element(By.CSS_SELECTOR, '#dzen-header > div.desktop-base-header__controls-3o.desktop-base-header__isMorda-mX > div.desktop-base-header__profileButton-bf.desktop-base-header__isMorda-mX.desktop-base-header__isAuthorized-Yz > div.Popup2.Popup2_visible.Popup2_target_anchor.Popup2_view_default.Popup2_hasCloseButton > div > button.base-button__rootElement-12.base-button__isFluid-Cq.base-button__xl-UC.base-button__accentPrimary-3e')
                    if allow_access:
                        allow_access.click()
                        sleep(2)
                        driver.switch_to.window(driver.window_handles[-1])
                        driver.find_element(By.CSS_SELECTOR, '#root > div > div > div.Approval-card > div.Approval-controls > div > button.Button2.Button2_size_l.Button2_view_action.Button2_width_max.ApprovalControls-item').click()
                        sleep(2)
                        dict_with_data["Dzen_status"] = 'ok'
                        logger.info(f'Подключение к Дзен аккаунта {dict_with_data["Login"]} успешно выполнено.')
                except:
                    dict_with_data["Dzen_status"] = 'fail'
                    logger.info(f'Подключение к Дзен аккаунта {dict_with_data["Login"]} успешно выполнено.')
    except:
        dict_with_data["Dzen_status"] = 'no status'
        logger.debug(f'Статус подключения к Дзен не установлен')
    driver.switch_to.window(driver.window_handles[-1])
    sleep(2)
    # Сохранить куки
    get_web_page_in_browser(URL_YA_ID)
    sleep(5)
    # получаем cookies
    current_cookies = driver.get_cookies()
    # logger.debug(f'\n\n{current_cookies}\n\n')
    # сохраняем cookies в словарь
    dict_with_data["Cookies"] = current_cookies
    #получаем и сохраняем куки с помощью pickle
    pickle.dump(driver.get_cookies(), open(f"cookies_yandex/{dict_with_data['Login']}.pkl", "wb"))
    sleep(3)
    # Получаем и сохраняем куки в json
    with open(f'cookies_yandex/{dict_with_data["Login"]}.json', 'w') as file:
        json.dump(current_cookies, file)
    logger.info(f'Cookies yandexru аккаунта {dict_with_data["Login"]} успешно сохранены')


def check_mailru_accounts_main():
    """Основная функция работы приложения check_mailru_accounts"""
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')    
    # Открываем xlsx книгу и активный лист
    workbook, worksheet = open_xlsx_file_and_return_active_sheet(file_name='combined_mailru.xlsx')    
    if workbook and worksheet:  # Если xlsx книга и активный лист получены
        current_row = 2  # С какой строки читать xlsx файл
        # Пройтись со второй строки до первой пустой
        try: 
            cur_cell = worksheet.cell(row=current_row, column=1)
            # while cur_cell.value is not None:
            while True:
                dict_with_data.clear()  # словарь для хранения данных об аккаунте (строчке таблицы)
                for index_, cur_col_name in enumerate(LIST_WITH_COLUMNS_COMBINED):
                    cur_cell = worksheet.cell(row=current_row, column=index_+1)
                    # Записать значение ячейки в словарь
                    dict_with_data[cur_col_name] = cur_cell.value
                print(f'Из xlsx файла получены данные: {dict_with_data["Login"]}')
                try: 
                    if len(dict_with_data) != 0:  # если словарь не пустой (был заполнен данными из файла)
                        # если статус аккаунта соответствует проверяемому (из файла config.txt), None или неизвестный
                        if (dict_with_data['Status'] == PARAM_DICT['CHECKED_STATUS']) or (dict_with_data['Status'] == None) or (dict_with_data['Status'] not in LIST_WITH_STATUS_ACC):
                            # Начинаем проверку аккаунта, получаем после проверки обновленные данные
                            check_account_mailru()

                            # Записать данные (новый пароль, статус, куки) в xlsx файл
                            logger.debug(f'Получен словарь {dict_with_data}')
                            cur_cell = worksheet.cell(row=current_row, column=2, value=dict_with_data['Password'])
                            logger.debug(f'В ячейку записан пароль {cur_cell.value}')
                            cur_cell = worksheet.cell(row=current_row, column=4, value=dict_with_data["Status"])
                            logger.info(f'Статус проверяемого аккаунта - {cur_cell.value}')
                            # cur_cell = worksheet.cell(row=current_row, column=5, value=dict_with_data["Cookies"])

                            if dict_with_data["Cookies_mailru"]:  # Если есть cookies mailru, то сохраняем их в excel
                                # print(dict_with_data['Cookies'])
                                cur_cell = worksheet.cell(row=current_row, column=7, value=str(dict_with_data["Cookies_mailru"]))
                            
                            # ----------Работает только с аккаунтами, у которых подтвержден телефон -----------
                            # # Для аккаунтов со статусом ok - создаем пароль mailru для приложений
                            # if dict_with_data["Status"] == 'ok' and dict_with_data["Psw_mailru_for_app"] is None:
                            #     create_on_mailru_psw_for_external_apps(driver=driver)
                            #     cur_cell = worksheet.cell(row=current_row, column=6, value=dict_with_data["Psw_mailru_for_app"])
                            #     if dict_with_data["Psw_mailru_for_app"]:
                            #         logger.info(f'Успешно создан пароль для внешних приложений {cur_cell.value}')
                            
                            logger.info(f'Попытка сохранить книгу excel')
                            workbook.save(filename='combined_mailru.xlsx')  # сохранить xlsx файл

                            if dict_with_data["Status"] == 'ok':
                                auth_on_yandexru_with_email_verify(driver=driver)
                                logger.debug(f'Получен словарь {dict_with_data}')
                                # Записать данные (куки яндекс) в xlsx файл
                                if dict_with_data["Dzen_status"] == 'ok':
                                    cur_cell = worksheet.cell(row=current_row, column=8, value=dict_with_data["Dzen_status"])
                                if dict_with_data["Cookies"]:
                                    cur_cell = worksheet.cell(row=current_row, column=5, value=str(dict_with_data["Cookies"]))
                                if dict_with_data["first_name"]:
                                    cur_cell = worksheet.cell(row=current_row, column=9, value=str(dict_with_data["first_name"]))
                                if dict_with_data["last_name"]:
                                    cur_cell = worksheet.cell(row=current_row, column=10, value=str(dict_with_data["last_name"]))
                            
                            logger.info(f'Попытка сохранить книгу excel')
                            workbook.save(filename='combined_mailru.xlsx')  # сохранить xlsx файл
                            if current_row % 10 == 0:
                                shutil.copyfile('combined_mailru.xlsx', f'backups/backup_combined_mailru.xlsx')
                                logger.info(f'Создан backup файла combined_mailru.xlsx')
                            logger.debug(f'файл xlsx сохранен')

                            # удаляем cookies
                            driver.delete_all_cookies()
                            # sleep(0.5)
                            if PARAM_DICT['NEED_PAUSE_BEFORE_CLOSED_BROWSER']  == 'True':  # Строка, так как из текстового конфига
                                pause = input('Нажмите любую клавишу для продолжения')
                            driver.close()  # Закрытие окна браузера
                            driver.quit()  # Выход
                            # print(f'Обновленные данные {dict_with_data}')

                        # если статус аккаунта ok, переходим к следующему
                        if (dict_with_data['Status'] == 'ok') and  (PARAM_DICT['CHECKED_STATUS'] != 'ok'):
                            logger.info('Аккаунт со статусом "ok". Переход к следующему.')
                except:
                    logger.error(f'При проверке {dict_with_data["Login"]} возникла непредвиденная ошибка')
                    try:
                        driver.close()  # Закрытие окна браузера
                        driver.quit()  # Выход
                    except:
                        pass
                finally:
                    # Переход на следующую строку
                    current_row += 1
                    cur_cell = worksheet.cell(row=current_row, column=1)  
                    # pause = input('Нажмите любую клавишу для продолжения работы: ')
                    if cur_cell.value is None:
                        logger.info(f'Обнаружена пустая строка - {current_row}.')
                        need_retry_check = False  # нужна ли повторная проверка
                        for r in range(2, current_row):
                            c = worksheet.cell(row=r, column=LIST_WITH_COLUMNS_COMBINED.index('Status')+1)
                            # если значение статуса не содержится в словаре со статусами исключая no status
                            if c.value not in LIST_WITH_STATUS_ACC[1: ]:
                                need_retry_check = True
                        if need_retry_check:
                            current_row = 2
                            logger.info(f'Начинаю повторную проверку со строки {current_row}.')
                            cur_cell = worksheet.cell(row=current_row, column=1)
                        else:
                            print('Проверены все аккаунты из списка.')
                            shutil.copyfile('combined_mailru.xlsx', f'backups/backup_combined_mailru.xlsx')
                            logger.info(f'Создан backup файла combined_mailru.xlsx')
                            break
            logger.info('Выход из цикла проверки')
        except:
            logger.critical(f'КРИТИЧЕСКАЯ ОШИБКА: при выполнении функции {inspect.currentframe().f_code.co_name}. Требуется перезапуск программы.')


def start_change_password():
    """Начинает изменение пароля для аккаунта, который хранится в глобальной переменной."""
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    # logger.debug(f'\nТекущее значение dict_with_data:\n{dict_with_data}')
    global driver
    if len(dict_with_data) != 0:
        try:
            logger.debug('Запускается инициализация драйвера')
            driver = init_driver()
        except:
            logger.error('Ошибка при инициализации экземпляра driver')

        get_web_page_in_browser(url='https://passport.yandex.ru/')
        sleep(randint(1, 3))
        find_and_click_captcha_iam_not_robot()
        sleep(randint(1, 3))
        find_and_click_btn_close_window()
        find_add_favorite_and_click_btn_close_window()
        sleep(randint(1, 3))
        if PARAM_DICT['NEED_PAUSE_BEFORE_PRESS_SIGNIN']  == 'True':  # Строка, так как из текстового конфига
            pause = input('нажмите любую клавишу для продолжения')
        
        # Авторизация по куки текущего пользователя
        if PARAM_DICT['PARAMETER_CHANGE_PASSWORD_USE_COOKIES'] == 'True':
            # загрузить куки текущего пользователя
            logger.debug(f'Работаем с аккаунтом {dict_with_data["Login"]}')
            try:
                cookies = pickle.load(open(f'cookies_mailru/{dict_with_data["Login"]}.pkl', "rb"))
            except:
                pass
            if cookies is None:
                logger.error(f'При попытке чтения куки для пользователя {dict_with_data["Login"]} не были найдены в папке.')
            for cookie in cookies:
                try:
                    driver.add_cookie(cookie)
                except Exception as exc:
                    logger.error(f'Не удалось загрузить куки: {cookie}')
                    print(exc)
            sleep(1)
            driver.refresh()
            sleep(3)
            check_account_for_signin()
            sleep(5)
            # Проверяем результат авторизации
            cur_avatar_obj = None
            el_avatar1 = check_avatar1_mail_on_page_and_click()  # аватар 1 вида
            el_avatar2 = check_avatar2_on_page_and_click()  # аватар 2 вида
            el_avatar3 = check_avatar3_on_page_and_click()  # аватар 2 вида
            if el_avatar1 or el_avatar2 or el_avatar3:
                logger.info(f'Вход выполнен успешно')
                dict_with_data['Status'] = 'ok'
                if el_avatar1: 
                    cur_avatar_obj = el_avatar1
                elif el_avatar2:
                    cur_avatar_obj = el_avatar2
                elif el_avatar3:
                    cur_avatar_obj = el_avatar2
                sleep(3)
                # Изменяем пароль
                new_psw = navigate_menu_and_change_password(el_avatar=cur_avatar_obj, dict_with_data=dict_with_data)
                if new_psw:
                    dict_with_data['Password'] = new_psw
                    dict_with_data['Status'] = 'ok_psw_changed'

                # получаем cookies
                current_cookies = driver.get_cookies()
                # print(f'\n\n{current_cookies}\n\n')
                # сохраняем cookies в словарь
                dict_with_data['Cookies'] = current_cookies

                #получаем и сохраняем куки с помощью pickle
                pickle.dump(driver.get_cookies(), open(f"cookies_mailru/{dict_with_data['Login']}.pkl", "wb"))

        else:
            logger.error(f'В файле config.txt установлено неверное значение параметра PARAMETER_CHANGE_PASSWORD_USE_COOKIES, установите True')
    else:
        logger.error(f'словарь dict_with_data с данными текущего аккаунта пуст')        
    # print(user_data)
    # forward_to_next_account = input('Перейти к следующему аккаунту? (y/n): ')
    # if forward_to_next_account == 'y':

    # удаляем cookies
    driver.delete_all_cookies()
    # sleep(0.5)
    if PARAM_DICT['NEED_PAUSE_BEFORE_CLOSED_BROWSER']  == 'True':  # Строка, так как из текстового конфига
        pause = input('нажмите любую клавишу для продолжения')
    driver.close()  # Закрытие окна браузера
    driver.quit()  # Выход
    # print(f'Обновленные данные {dict_with_data}')


def change_password_for_ok_accs_main():
    """Основная функция в режиме смена пароля для успешных аккаунтов.
    Построчно читает xlsx файл и вызывает для каждого валидного аккаунта функцию смены пароля."""
    # ------------------------- Работа с xlsx файлом -----------------------------
    # try:
    #     # Читаем файл с данными юзеров в список [Login, Password, Answer]
    #     list_user_data = read_xlsx_file_and_lines_to_list(file_name='combined_mailru.xlsx')
    # except:
    #     logger.critical(f'КРИТИЧЕСКАЯ ОШИБКА: при чтении xlsx файла с аккаунтами.')
    
    # Открываем xlsx книгу и активный лист
    workbook, worksheet = open_xlsx_file_and_return_active_sheet(file_name='combined_mailru.xlsx')

    if workbook and worksheet:  # Если xlsx книга и активный лист получены
        current_row = 2  # С какой строки читать xlsx файл
        # list_with_data = []  # список со словарями все аккаунты

        # Пройтись со второй строки до первой пустой
        try: 
            cur_cell = worksheet.cell(row=current_row, column=1)
            # while cur_cell.value is not None:
            while True:
                dict_with_data.clear()  # словарь для хранения данных об аккаунте (строчке таблицы)
                for index_, cur_col_name in enumerate(LIST_WITH_COLUMNS_COMBINED):
                    cur_cell = worksheet.cell(row=current_row, column=index_+1)
                    # Записать значение ячейки в словарь
                    dict_with_data[cur_col_name] = cur_cell.value
                print(f'Из xlsx файла получены данные: {dict_with_data["Login"]}')
                try: 
                    if len(dict_with_data) != 0:  # если словарь не пустой (был заполнен данными из файла)
                        # если статус аккаунта ok
                        if dict_with_data['Status'] == 'ok':
                            # Начинаем смену пароля, получаем после проверки обновленные данные
                            start_change_password()
                            # Записать данные (новый пароль, статус, куки) в xlsx файл
                            # logger.debug(f'Получен словарь {dict_with_data}')
                            cur_cell = worksheet.cell(row=current_row, column=2, value=dict_with_data['Password'])
                            print(f'В ячейку записан пароль {cur_cell.value}')
                            cur_cell = worksheet.cell(row=current_row, column=4, value=dict_with_data['Status'])
                            print(f'В ячейку записан статус {dict_with_data["Status"]}')
                            logger.info(f'Статус проверяемого аккаунта - {cur_cell.value}')
                        
                            if dict_with_data['Cookies']:
                                # print(dict_with_data['Cookies'])
                                cur_cell = worksheet.cell(row=current_row, column=5, value=str(dict_with_data['Cookies']))
                            
                            print(f'Попытка сохранить книгу')
                            workbook.save(filename='combined_mailru.xlsx')  # сохранить xlsx файл
                            if current_row % 10 == 0:
                                shutil.copyfile('combined_mailru.xlsx', f'backups/backup_combined_mailru.xlsx')
                                logger.info(f'Создан backup файла combined_mailru.xlsx')
                            logger.debug(f'файл xlsx сохранен')

                        else: # если статус аккаунта не ok
                            logger.info('Аккаунт не имеет статус "ok". Переход к следующему.')
                except:
                    logger.error(f'При проверке {dict_with_data["Login"]} возникла непредвиденная ошибка')
                finally:
                    current_row += 1
                    cur_cell = worksheet.cell(row=current_row, column=1)  # Переход на следующую строку
                    # pause = input('Нажмите любую клавишу для продолжения работы: ')
                    if cur_cell.value is None:
                        logger.info(f'Обнаружена пустая строка - {current_row}.')
                        need_retry_check = False  # нужна ли повторная проверка
                        # for r in range(2, current_row):
                        #     c = worksheet.cell(row=r, column=LIST_WITH_COLUMNS_COMBINED.index('Status')+1)
                        #     # если значение статуса не содержится в словаре со статусами исключая no status
                        #     if c.value not in LIST_WITH_STATUS_ACC[1: ]:
                        #         need_retry_check = True
                        if need_retry_check:
                            current_row = 2
                            logger.info(f'Начинаю повторную проверку со строки {current_row}.')
                            cur_cell = worksheet.cell(row=current_row, column=1)
                        else:
                            print('Проверены все аккаунты из списка.')
                            shutil.copyfile('combined_mailru.xlsx', f'backups/backup_combined_mailru.xlsx')
                            logger.info(f'Создан backup файла combined_mailru.xlsx')
                            break
            logger.info('Выход из цикла проверки')
        except:
            logger.critical('КРИТИЧЕСКАЯ ОШИБКА: при выполнении главной функции. Требуется перезапуск программы.')


def delete_unvalid_accounts_from_xlsx():
    """Основная функция работы приложения check_accounts"""
    # ------------------------- Работа с xlsx файлом -----------------------------
    # try:
    #     # Читаем файл с данными юзеров в список [Login, Password, Answer]
    #     list_user_data = read_xlsx_file_and_lines_to_list(file_name='combined_mailru.xlsx')
    # except:
    #     logger.critical(f'КРИТИЧЕСКАЯ ОШИБКА: при чтении xlsx файла с аккаунтами.')
    
    target_status_accs_for_deleted = input(f'Аккаунты с каким статусом удалить из файла combined_mailru.xlsx?\n'\
                                           f'{LIST_WITH_STATUS_ACC}\n'\
                                           f'Введите здесь: ')
    # Открываем xlsx книгу и активный лист
    workbook, worksheet = open_xlsx_file_and_return_active_sheet(file_name='combined_mailru.xlsx')
    
    if workbook and worksheet:  # Если xlsx книга и активный лист получены
        current_row = 2  # С какой строки читать xlsx файл
        # list_with_data = []  # список со словарями все аккаунты

        # Пройтись со второй строки до первой пустой
        try: 
            cur_cell = worksheet.cell(row=current_row, column=1)
            # while cur_cell.value is not None:
            while True:
                dict_with_data.clear()  # словарь для хранения данных об аккаунте (строчке таблицы)
                for index_, cur_col_name in enumerate(LIST_WITH_COLUMNS_COMBINED):
                    cur_cell = worksheet.cell(row=current_row, column=index_+1)
                    # Записать значение ячейки в словарь
                    dict_with_data[cur_col_name] = cur_cell.value
                logger.debug(f'Из xlsx файла получены данные: {dict_with_data["Login"]}')
                try: 
                    if len(dict_with_data) != 0:  # если словарь не пустой (был заполнен данными из файла)
                        # если статус аккаунта соответствует проверяемому (из файла config.txt)
                        if dict_with_data['Status'] == target_status_accs_for_deleted:
                            try:
                                # Удалить текущую строку из файла
                                worksheet.delete_rows(current_row, 1)  # индекс, кол-во
                                logger.info(f'Данные аккаунта {dict_with_data["Login"]} удалены')
                            except Exception as exc:
                                logger.error(f'При попытке удаления аккаунта {dict_with_data["Login"]} (строки - {current_row}) возникла ошибка {exc}')
                            logger.debug(f'Попытка сохранить книгу')
                            workbook.save(filename='combined_mailru.xlsx')  # сохранить xlsx файл
                            if current_row % 10 == 0:
                                shutil.copyfile('combined_mailru.xlsx', f'backups/backup_combined_mailru.xlsx')
                                logger.info(f'Создан backup файла combined_mailru.xlsx')
                            logger.debug(f'файл xlsx сохранен')
                        else:
                            # logger.debug(f'Аккаунт со статусом {dict_with_data["Status"]}. Переход к следующему.')
                            pass
                except:
                    logger.error(f'При проверке {dict_with_data["Login"]} возникла непредвиденная ошибка')
                finally:
                    current_row += 1
                    cur_cell = worksheet.cell(row=current_row, column=1)  # Переход на следующую строку
                    # pause = input('Нажмите любую клавишу для продолжения работы: ')
                    if cur_cell.value is None:
                        logger.info(f'Обнаружена пустая строка - {current_row}.')
                        need_retry_check = False  # нужна ли повторная проверка
                        for r in range(2, current_row):
                            c = worksheet.cell(row=r, column=LIST_WITH_COLUMNS_COMBINED.index('Status')+1)
                            # если значение статуса не содержится в словаре со статусами исключая no status
                            if c.value == target_status_accs_for_deleted:
                                need_retry_check = True
                        if need_retry_check:
                            current_row = 2
                            logger.info(f'Начинаю повторную проверку со строки {current_row}.')
                            cur_cell = worksheet.cell(row=current_row, column=1)
                        else:
                            print('Проверены все аккаунты из списка.')
                            shutil.copyfile('combined_mailru.xlsx', f'backups/backup_combined_mailru.xlsx')
                            logger.info(f'Создан backup файла combined_mailru.xlsx')
                            break
            logger.info('Выход из цикла проверки')
        except:
            logger.critical('КРИТИЧЕСКАЯ ОШИБКА: при выполнении главной функции. Требуется перезапуск программы.')


def start_set_password_app():
    """Функция установки пароля приложений, в качестве логина использует секретку.
    Сначала запускает такую же функцию изменения пароля, затем уходит в ответвление,
    выходит через break
    выполняет свои функции по установке пароля приложения"""
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    # logger.debug(f'\nТекущее значение dict_with_data:\n{dict_with_data}')
    global driver
    if len(dict_with_data) != 0:
        try:
            logger.debug('Запускается инициализация драйвера')
            driver = init_driver()
        except:
            logger.error('Ошибка при инициализации экземпляра driver')

        get_web_page_in_browser(url='https://passport.yandex.ru/')
        sleep(2)
        find_and_click_captcha_iam_not_robot()
        sleep(0.5)
        find_and_click_btn_close_window()
        sleep(0.5)
        find_add_favorite_and_click_btn_close_window()
        sleep(0.5)
        if PARAM_DICT['NEED_PAUSE_BEFORE_PRESS_SIGNIN']  == 'True':  # Строка, так как из текстового конфига
            pause = input('нажмите любую клавишу для продолжения')
        
        # Авторизация по куки текущего пользователя
        if PARAM_DICT['PARAMETER_CHANGE_PASSWORD_USE_COOKIES'] == 'True':
            # загрузить куки текущего пользователя
            logger.debug(f'Работаем с аккаунтом {dict_with_data["Login"]}')
            try:
                cookies = pickle.load(open(f'cookies_mailru/{dict_with_data["Login"]}.pkl', "rb"))
            except:
                pass
            if cookies is None:
                logger.error(f'При попытке чтения куки для пользователя {dict_with_data["Login"]} не были найдены в папке.')
            else:
                for cookie in cookies:
                    try:
                        driver.add_cookie(cookie)
                    except Exception as exc:
                        logger.error(f'Не удалось загрузить куки: {cookie}')
                        print(exc)
                sleep(1)
                driver.refresh()
                sleep(1)
                check_account_for_signin()
                # Проверяем результат авторизации
                el_avatar = check_avatar1_mail_on_page_and_click()  # аватар 1 вида
                el_avatar2 = check_avatar2_on_page_and_click()  # аватар 2 вида
                if el_avatar or el_avatar2:
                    logger.info(f'Вход выполнен успешно')
                    dict_with_data['Status'] = 'ok'
                    # get_web_page_in_browser(url='https://id.yandex.ru/security')  # безопасность
                    # sleep(2)
                    get_web_page_in_browser(url='https://id.yandex.ru/security/app-passwords')  # пароли приложений
                    sleep(2)
                    try:
                        el_mail = driver.find_element(By.CSS_SELECTOR, '#__next > div > main > div > section:nth-child(2) > div > div.List_root__CuPfW > div:nth-child(1)')
                        el_mail.click()
                    except Exception as exc:
                        logger.error(f'Ошибка при переходе в элемент "Создать пароль приложения Почта" {exc}')
                    try:
                        el_name_label = driver.find_element(By.CLASS_NAME, 'MaterialTextField_label__HE8cz')
                        if el_name_label.text == 'Придумайте имя пароля':
                                # el_name_psw_field.click()
                                # gen_name_psw = dict_with_data['Login'].split('@')[0]+'_mail_psw'
                                el_name_psw_field = driver.find_element(By.CLASS_NAME, 'MaterialTextField_input__94X76')
                                el_name_psw_field.send_keys(dict_with_data['Answer'], Keys.ENTER)
                                # dict_with_data['name_psw_for_mail'] = gen_name_psw
                    except Exception as exc:
                        logger.error(f'Ошибка при заполнении поля Имя пароля {exc}')
                    sleep(0.5)
                    try:
                        el_psw = driver.find_element(By.CSS_SELECTOR, 'body > div.Modal.Modal_visible.Modal_hasAnimation.Modal_root__smA6R.Modal_insets_none__tCHaA.app-password-wizzard_wizzard__u1u8J > div.Modal-Wrapper > div > div > div > section.Section_root__zl60G.app-password_section__AYoA5 > div > div.List_root__yESwN.variant-filled_root__baqI4.list-style-compact_root__m8IfF.size-normal_root__GrEvW.app-password_list__60lwa > div > div.UnstyledListItem_inner__Td3gb > div.Slot_root__jYlNI.Slot_content__XYDYF.alignment-center_root__ndulA.color-inherit_root__OQmPQ.Slot_direction_vertical__I3MEt > span')
                        dict_with_data['Psw_mailru_for_app'] = el_psw.text
                        if dict_with_data['Psw_mailru_for_app']:
                            logger.info(f'Для пользователя {dict_with_data["Login"]} получен пароль {dict_with_data["Psw_mailru_for_app"]}')
                        el_btn_close = driver.find_element(By.CSS_SELECTOR, 'body > div.Modal.Modal_visible.Modal_hasAnimation.Modal_root__smA6R.Modal_insets_none__tCHaA.app-password-wizzard_wizzard__u1u8J > div.Modal-Wrapper > div > div > div > section:nth-child(4) > div > button > span')
                        el_btn_close.click()
                    except Exception as exc:
                        logger.error(f'Ошибка при получении пароля для почты" {exc}')
                        dict_with_data["Psw_mailru_for_app"] = None
        else:
            logger.error(f'В файле config.txt установлено неверное значение параметра PARAMETER_CHANGE_PASSWORD_USE_COOKIES, установите True')
    else:
        logger.error(f'словарь dict_with_data с данными текущего аккаунта пуст')        
    # print(user_data)
    # forward_to_next_account = input('Перейти к следующему аккаунту? (y/n): ')
    # if forward_to_next_account == 'y':

    # удаляем cookies
    driver.delete_all_cookies()
    # sleep(0.5)
    if PARAM_DICT['NEED_PAUSE_BEFORE_CLOSED_BROWSER']  == 'True':  # Строка, так как из текстового конфига
        pause = input('нажмите любую клавишу для продолжения')
    driver.close()  # Закрытие окна браузера
    driver.quit()  # Выход
    # print(f'Обновленные данные {dict_with_data}')
    

def set_password_app_main():
    """Основная функция в режиме получения пароля приложения почта для успешных аккаунтов.
    Построчно читает xlsx файл и вызывает для каждого валидного аккаунта функцию смены пароля."""
    
    # Открываем xlsx книгу и активный лист
    workbook, worksheet = open_xlsx_file_and_return_active_sheet(file_name='combined_mailru.xlsx')

    if workbook and worksheet:  # Если xlsx книга и активный лист получены
        current_row = 2  # С какой строки читать xlsx файл
        # list_with_data = []  # список со словарями все аккаунты

        # Пройтись со второй строки до первой пустой
        try: 
            cur_cell = worksheet.cell(row=current_row, column=1)
            # while cur_cell.value is not None:
            while True:
                dict_with_data.clear()  # словарь для хранения данных об аккаунте (строчке таблицы)
                for index_, cur_col_name in enumerate(LIST_WITH_COLUMNS_COMBINED):
                    cur_cell = worksheet.cell(row=current_row, column=index_+1)
                    # Записать значение ячейки в словарь
                    dict_with_data[cur_col_name] = cur_cell.value
                print(f'Из xlsx файла получены данные: {dict_with_data["Login"]}')
                try: 
                    if len(dict_with_data) != 0:  # если словарь не пустой (был заполнен данными из файла)
                        # если статус аккаунта ok 
                        if (dict_with_data["Status"] == 'ok') and (dict_with_data["Psw_mailru_for_app"] == None):
                            # Начинаем получение пароля, получаем после проверки обновленные данные
                            start_set_password_app()
                            # Записать данные (пароль для приложения почта) в xlsx файл
                            if dict_with_data["Psw_mailru_for_app"]:
                                cur_cell = worksheet.cell(row=current_row, column=6, value=str(dict_with_data["Psw_mailru_for_app"]))
                            
                            logger.info(f'Попытка сохранить книгу')
                            workbook.save(filename='combined_mailru.xlsx')  # сохранить xlsx файл
                            if current_row % 10 == 0:
                                shutil.copyfile('combined_mailru.xlsx', f'backups/backup_combined_mailru.xlsx')
                                logger.info(f'Создан backup файла combined_mailru.xlsx')
                            logger.info(f'файл xlsx сохранен')

                        else: # если статус аккаунта не ok
                            logger.info('Аккаунт не имеет статус "ok". Переход к следующему.')
                except:
                    logger.error(f'При проверке {dict_with_data["Login"]} возникла непредвиденная ошибка')
                finally:
                    current_row += 1
                    cur_cell = worksheet.cell(row=current_row, column=1)  # Переход на следующую строку
                    # pause = input('Нажмите любую клавишу для продолжения работы: ')
                    if cur_cell.value is None:
                        logger.info(f'Обнаружена пустая строка - {current_row}.')
                        need_retry_check = False  # нужна ли повторная проверка
                        for r in range(2, current_row):
                            c_status = worksheet.cell(row=r, column=LIST_WITH_COLUMNS_COMBINED.index("Status")+1)
                            c_Psw_mailru_for_app = worksheet.cell(row=r, column=LIST_WITH_COLUMNS_COMBINED.index("Psw_mailru_for_app")+1)
                            # если значение статуса ok не содержится в словаре со статусами исключая no status
                            if (c_status.value == 'ok') and (c_Psw_mailru_for_app.value == None):
                                need_retry_check = True
                        if need_retry_check:
                            current_row = 2
                            logger.info(f'Начинаю повторную проверку со строки {current_row}.')
                            cur_cell = worksheet.cell(row=current_row, column=1)
                        else:
                            print('Получены пароли для всех успешных аккаунтов.')
                            shutil.copyfile('combined_mailru.xlsx', f'backups/backup_combined_mailru.xlsx')
                            logger.info(f'Создан backup файла combined_mailru.xlsx')
                            break
            logger.info('Выход из цикла проверки')
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
    
    check_mailru_accounts_main()

    print('\n\n')
    print('Время работы программы составило: ')
    print("--- %s seconds ---" % round((time() - start_time), 0))
    print('[!] Программа выполнена.')
    
