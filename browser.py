"""Модуль для работы с браузером.
Создание экземпляра драйвера.
"""
# pip install selenium-stealth
from selenium_stealth import stealth
# pip install selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# pip install fake-useragent
from fake_useragent import UserAgent

import logging # Импортируем библиотеку для безопасного хранения логов
# Установлены настройки логгера для текущего файла
# В переменной __name__ хранится имя пакета;
# Это же имя будет присвоено логгеру.
# Это имя будет передаваться в логи, в аргумент %(name)
logger = logging.getLogger(__name__)
import inspect  # Для имени функции

from txt_utils import read_parameters_from_txt_file_and_add_to_dict
PARAM_DICT = read_parameters_from_txt_file_and_add_to_dict(file_name = 'config.txt')


# - Подключение модулей -
from config import  USER_AGENT_MY_GOOGLE_CHROME, PATH_TO_FILE_DRIVER_CHROME,\
    PARAMETER_ANSWER_A_SECRET_QUESTION, SLOW_INTERNET,\
    LIST_WITH_COLUMNS_COMBINED, LIST_WITH_STATUS_ACC
    # HEADLESS, PARAMETER_CHANGE_PASSWORD


def init_driver() -> webdriver:
    """Создание браузера (драйвера).
    
    - Создание экземпляра UserAgent (с помощью библиотеки fake_user_agent);
    - Добавление аргументов в экземпляр Options для браузера (драйвера);
    - Создание браузера (экземпляра webdriver) с нужными опциями.
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name} - инициализация браузера.')
    # Создание экземпляра UserAgent
    ua = UserAgent()  # (browsers=['chrome',])
    fake_user_agent = ua.random # (с помощью библиотеки fake_user_agent)
    # Изменение случайного юзер агента на свой chrome mac os (для теста)
    fake_user_agent = USER_AGENT_MY_GOOGLE_CHROME
    logger.debug(f'Создан user agent: {fake_user_agent}')
    # Опции для браузера (драйвера)
    options = Options()
    options.add_argument(f'user-agent={fake_user_agent}')
    logger.debug('в options добавлен fake_user_agent')

    # Включение режима инкогнито (для chrome)
    # options.add_argument("--incognito")

    # Отключение режима Webdriver
    options.add_argument(f'--disable-blink-features=AutomationControlled')
    logger.debug('в options Отключен режима Webdriver')
    # Скрытый режим headless mode
    if PARAM_DICT['HEADLESS'] == 'True':  # Строка, так как из текстового конфига
        options.add_argument("--headless")
        logger.debug('в options включен скрытый режим браузера')

    # путь к chromedriver.exe (можно задать через service)
    # s = Service(PATH_TO_FILE_DRIVER_CHROME)

    # # ------ Отключение автоматизированного ПО -------
    # options.add_argument("--disable-blink-features=AutomationControlled")

    # ------ Отключение надписи автоматизированного ПО сверху -------
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # инициализируем драйвер с нужными опциями
    driver = webdriver.Chrome(
        options=options,
        # executable_path=PATH_TO_FILE_DRIVER_CHROME,
        # service=s,
        )
    
    # # ------ Отключение режима автоматизированного ПО -------
    stealth(driver=driver,
        user_agent=USER_AGENT_MY_GOOGLE_CHROME,
        languages=["ru-RU", "ru"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        run_on_insecure_origins=True,
        )
    # driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    #     'source': '''
    #         delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
    #         delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
    #         delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
    # '''
    # })

    driver.set_page_load_timeout(30)
    return driver


