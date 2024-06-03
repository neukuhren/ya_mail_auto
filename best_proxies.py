"""Модуль для получения списка прокси серверов с сайта best-proxies.ru
"""
import inspect  # Для имени функции
import requests
from time import sleep
from time import time

import logging # Импортируем библиотеку для безопасного хранения логов
# Установлены настройки логгера для текущего файла
# В переменной __name__ хранится имя пакета;
# Это же имя будет присвоено логгеру.
# Это имя будет передаваться в логи, в аргумент %(name)
logger = logging.getLogger(__name__)

import os
from dotenv import load_dotenv # pip install python-dotenv
load_dotenv()
# Теперь переменные (TOKEN и др.), описанные в файле .env,
# доступны в пространстве переменных окружения
# API_KEY_BEST_PROXY = os.getenv('API_KEY_BEST_PROXY')
API_KEY_BEST_PROXY = ''

# from utils import timer_in_consol

proxies = []
proxy = ''


def get_proxies_list() -> list:
    """Получает список прокси через api.best-proxies.ru"""
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        url = f'https://api.best-proxies.ru/proxylist.txt?key={API_KEY_BEST_PROXY}&type=https&level=1&speed=1,2&country=ru&limit=0'
        # url = f'https://api.best-proxies.ru/proxylist.txt?key={API_KEY_BEST_PROXY}&type=https&level=1&speed=1&uptime=1&country=us&limit=0'
        response = requests.get(url)
        proxies = response.text.strip().replace('\r', '').split('\n')
        logger.info(f'Получен список из {len(proxies)} прокси:\n {proxies}')
        return proxies
    except Exception as exc:
        logger.error(f'При получении прокси листа возникла ошибка: {exc}. Подготовка к повторному запросу.')
        sleep(20)
        get_proxies_list()


def rotate_proxy() -> str:
    """Возвращает адрес прокси сервера в формате 3.127.203.145:80"""
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    global proxies
    if len(proxies) != 0:
        proxy = proxies.pop(0)
    else:
        proxies = get_proxies_list()
        sleep(1)
        proxy = rotate_proxy()
    # seleniumwire_options = {
    #     'proxy': {
    #     'http': f'{proxy_server_url}',
    #     'https': f'{proxy_server_url}',
    #     'verify_ssl': False,
    #     },
    # }
    return proxy


def best_proxies_main():
    """Основная функция работы приложения"""
    global proxies
    if len(proxies) == 0:
        proxies = get_proxies_list()


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
    best_proxies_main()

    print('\n\n')
    print('Время работы программы составило: ')
    print("--- %s seconds ---" % round((time() - start_time), 0))
    print('[!] Программа выполнена.')