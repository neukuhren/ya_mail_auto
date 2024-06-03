"""Модуль для cозданиz экземпляра веб драйвера.
"""
import inspect  # Для имени функции
import random
import requests

# pip install selenium-stealth
from selenium_stealth import stealth

# pip install selenium
from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service as ChromeService
# from selenium.webdriver.chrome.options import Options 

# pip install webdriver-manager
# from webdriver_manager.chrome import ChromeDriverManager

# pip install selenium-wire
# from seleniumwire import webdriver

# pip install undetected-chromedriver
import undetected_chromedriver as uc

# pip install fake-useragent
from fake_useragent import UserAgent

import logging
# Установлены настройки логгера для текущего файла
# В переменной __name__ хранится имя пакета;
# Это же имя будет присвоено логгеру.
# Это имя будет передаваться в логи, в аргумент %(name)
logger = logging.getLogger(__name__)

# from best_proxies import rotate_proxy
from config import POTOK 
from config_dolphin import IDS_PROFILE_DOLPHY

# --------------------- Конфигурация браузера-------------------------
USE_RANDOM_FAKE_USER_AGENT = True
# """Использовать случайный UserAgent из библиотеки fake-useragent"""
USER_AGENT_MY_GOOGLE_CHROME = "Mozilla/5.0 (Macintosh; \
    Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, \
    like Gecko) Chrome/114.0.0.0 Safari/537.36"
HEADLESS = False
"""Использование браузера в скрытом (свернутом) режиме."""
USE_SELENIUM_STEALTH = True
"""Использовать браузер под управлением библиотеки selenium-stealth"""
DISABLE_AUTO_OPTIONS_SELENIUM = True
"""Для обхода проверки браузера на использование автоматизированного ПО
    возможно отключение некоторых опций, браузера под управлением Selenium."""
USE_MY_HEADERS = False
"""Передавать ли мои заголовки в браузере"""
USE_PROXY = False
"""Использовать ли прокси-сервер"""
USE_ELITE_PRIVATE_PROXY = False
"""Использовать ли элитные прокси с ручной ротацией"""
USE_UNDETECTED_CHROMEDRIVER = False
"""Использовать браузер под управлением библиотеки undetected-chromedriver"""
USE_DOLPHIN_ANTY = False
"""Использовать ли антидетекст браузер dolphin anty"""
# ---------------------------------------------------------------------


def init_driver() -> webdriver:
    """Создание браузера (экземпляра веб драйвера).
    
    - Создание экземпляра UserAgent (с помощью библиотеки fake_user_agent);
    - Добавление аргументов в экземпляр Options для браузера (драйвера);
    - Создание браузера (экземпляра webdriver) с нужными опциями.
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name} - инициализация браузера.')
    try:
        # -------------------- Опции для браузера (драйвера) --------------------
        if USE_UNDETECTED_CHROMEDRIVER:
            options = uc.ChromeOptions()
        else:
            options = webdriver.ChromeOptions()
        
        # Создание экземпляра UserAgent
        ua = UserAgent()  # (browsers=['chrome',])
        if USE_RANDOM_FAKE_USER_AGENT:
            fake_user_agent = ua.random # (с помощью библиотеки fake_user_agent)
        else:
            # Изменение случайного юзер агента на свой chrome mac os (для теста)
            fake_user_agent = USER_AGENT_MY_GOOGLE_CHROME
        logger.debug(f'Создан user agent: {fake_user_agent}')
        options.add_argument(f'--user-agent={fake_user_agent}')
        logger.debug('в options добавлен fake_user_agent')

        # Включение режима инкогнито (для chrome)
        # options.add_argument("--incognito")
        # Отключение всплывающих окон chrome
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-notifications")
        # options.add_argument("--disable-extensions")
        options.add_argument('--ignore-certificate-errors')
        
        # WebDriver ожидает, пока не будет возвращен запуск события DOMContentLoaded.
        options.page_load_strategy = 'eager'

        # Pass the argument 1 to allow and 2 to block
        options.add_experimental_option(
            "prefs", {"profile.default_content_setting_values.notifications": 1}
            )
        
        # ------ Отключение автоматизированного ПО -------
        options.add_argument("--disable-blink-features=AutomationControlled")

        # Список распространённых разрешений экрана
        screen_res = [(1366, 768), (1920, 1080), (1024, 768)]
        # Список распространённых семейств шрифтов
        font_families = ["Arial", "Times New Roman", "Verdana"]
        #Выбор случайного разрешения
        width, height = random.choice(screen_res)

        #Создание опций chrome
        # opts = webdriver.ChromeOptions()
        # Установка случайного разрешения экрана
        options.add_argument(f"--window-size={width},{height}")
        # Установка случайного списка шрифтов
        random_fonts = random.choices(font_families, k=2)
        options.add_argument(f'--font-list="{random_fonts[0]};{random_fonts[1]}"')

        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-renderer-backgrounding")
        options.add_argument("--disable-background-timer-throttling")
        options.add_argument("--disable-backgrounding-occluded-windows")
        options.add_argument("--disable-client-side-phishing-detection")
        options.add_argument("--disable-crash-reporter")
        options.add_argument("--disable-oopr-debug-crash-dump")
        options.add_argument("--no-crash-upload")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-low-res-tiling")
        options.add_argument("--log-level=3")
        options.add_argument("--silent")

        options.add_argument('--disable-popup-blocking')
        
        # путь к chromedriver.exe (можно задать через service)
        # s = Service('chromedriver/')

        if HEADLESS:
            options.headless = True
            # options.add_argument("--headless")
            logger.debug('в options включен скрытый режим браузера')
        else: 
            options.headless = False

        # ------ Отключение надписи автоматизированного ПО сверху ------
        if not USE_UNDETECTED_CHROMEDRIVER and not USE_DOLPHIN_ANTY:
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)

        list_proxy_port_user_psw = [
            [],
            ['65.109.79.176:30035', 'R9DShEZhZM:ZzV5QifvGj'],  # мой lteboost
        ]
        """Список прокси, портов логинов и паролей"""
        
        if USE_PROXY:
            # Selenium configuration to use a proxy
            options.add_argument(f'--proxy={list_proxy_port_user_psw[POTOK][0]}')
            options.add_argument(f'--proxy-auth={list_proxy_port_user_psw[POTOK][1]}')

        if USE_ELITE_PRIVATE_PROXY:
            # Selenium configuration to use a proxy
            options.add_argument(f'--proxy=65.109.79.176:30035')
            options.add_argument(f'--proxy-auth=KlY7AUbMk77g:TSaV9gpByq') 
        
        if USE_UNDETECTED_CHROMEDRIVER:
            driver = uc.Chrome(headless=HEADLESS, use_subprocess=False, options=options)

        elif USE_DOLPHIN_ANTY:
            # Делаем запрос к антику и получаем его параметры нужного профиля
            url_dolphin_profiles = 'http://localhost:3001/v1.0/browser_profiles/'+ IDS_PROFILE_DOLPHY[POTOK] + '/start?automation=1'
            r = requests.get(url_dolphin_profiles)

            # Получаем ответ после запуска профиля
            json = r.json()
            logger.info(r.text)
            # Парсим значение открытого порта профиля антика
            port = str(json['automation']['port'])
            logger.debug(port)

            # Инициализируем путь к веб драйверу Dolphin Anti
            # chrome_dolphin_driver_path = Service("C:/Users/duglas/Desktop/SELENIUM/chromedriver-windows-x64-dolphin.exe")

            # Загружаем предварительные настройки в Selenium драйвер и подключаемся к порту запущенного профиля
            options = webdriver.ChromeOptions()
            options.debugger_address = "127.0.0.1:" + port
            driver = webdriver.Chrome(options=options) # service=chrome_dolphin_driver_path,
        
        else:  # Обычный хром драйвер
            driver = webdriver.Chrome(options=options) 

        if USE_SELENIUM_STEALTH:
            # надстройка selenium-stealth, предназначенная для скрытия следов автоматизации
            stealth(driver=driver,
                user_agent=fake_user_agent,
                languages=["ru-RU", "ru"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                run_on_insecure_origins=True,
                )
        
        if USE_MY_HEADERS:
            my_headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "ru,en;q=0.9",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive",
                "Referrer": "https://id.yandex.ru/",
                # "Cookie": 'gdpr=0; my=YwA=; yandexuid=8141904171647094482; yuidss=8141904171647094482; _ym_uid=1695714279610629334; yashr=314850291696346721; yandex_login=michael.mois3enko; amcuid=4380050701704445531; ymex=2027094028.yrts.1711734028; yandex_gid=21647; is_gdpr=0; is_gdpr_b=CK/lARC3+AEoAg==; font_loaded=YSv1; i=JR7OZiHnqIGMBa8NgbDsOcNfBF1IWFKVFxGM7DPEpwh1/Kdt4Ukdoh0YgcY9UcAnNv0xFs0nQ5T6buaTTqAY2tEAfdk=; Session_id=3:1714759241.5.0.1643623968279:_mXZsg:28.1.2:1|347656226.-1.2.1:62865718.2:57|1926234700.59014021.2.2:59014021.3:1702637989|3:10287363.676009.NvgXs5vou5FPZcid5pkZWMNZz94; sessar=1.1189.CiBa3gxH0-gfjEe_a5V9dAWClGcUfgoyWbvj_H1hUv18-A.Ml3D3miyH0H6Izr06M1S9YZx-TcdATt4fCnEh15bjXw; sessionid2=3:1714759241.5.0.1643623968279:_mXZsg:28.1.2:1|347656226.-1.2.1:62865718.2:57|1926234700.59014021.2.2:59014021.3:1702637989|3:10287363.676009.fakesign0000000000000000000; isa=TegYUzCmxsJtShgRPZBJ6wLJRuoyn6V9sE/4q3H1mK18r9FEXyKCL7JcvXgXhZv/gxTPip+jbu16QCi3EMAEQIRR5jk=; sae=0:39D1E83C-D796-4095-88D2-8EB68A59D482:p:24.1.5.827:m:d:RU:20220312; _ym_isad=2; cycada=KnoDiH8/pNMUd+BR0oKYeOEBAjnSuynI+nbLKo8Iz0g=; _yasc=gmtybSUyP2YIoeW2JkqqbG1hS5AHtfqpwZpYc2WIBvYANxCGMs1QpfPK/SIwwHNHuudaeVzfNHzGXpEH330W7M6vIeA=; ys=svt.1#def_bro.1#wprid.1714987194760596-13561191211747633818-balancer-l7leveler-kubr-yp-vla-133-BAL#ybzcc.ru#newsca.native_cache; _ym_d=1714987195; yp=1715032059.uc.ru#1715032059.duc.ru#1734173990.cld.1955450#1717656961.csc.1#1717146962.hdrc.1#1996605021.hks.0#2017997989.multib.1#2030347195.pcs.1#2018352306.sp.family:1#1726400080.stltp.serp_bk-map_1_1694864080#1730010749.szm.2:1440x900:1440x800#2018352306.udn.cDrQnNC40YXQsNC40Lsg0JzQvtC40YHQtdC10L3QutC%2B#1715799101.ygu.1#1714994422.gpauto.55_600506:37_042492:100000:3:1714987222; bh=EkwiTm90X0EgQnJhbmQiO3Y9IjgiLCJDaHJvbWl1bSI7dj0iMTIwIiwiWWFCcm93c2VyIjt2PSIyNC4xIiwiWW93c2VyIjt2PSIyLjUiGgUiYXJtIiIMIjI0LjEuNS44MjciKgI/MDoHIm1hY09TIkIIIjEyLjIuMCJKBCI2NCJSZCJOb3RfQSBCcmFuZCI7dj0iOC4wLjAuMCIsIkNocm9taXVtIjt2PSIxMjAuMC42MDk5LjI5MSIsIllhQnJvd3NlciI7dj0iMjQuMS41LjgyNyIsIllvd3NlciI7dj0iMi41IiJaAj8w; yabs-vdrf=OPZTc7G1xLvG1IJDcDG2HZhK1IYfcJG3wOw0142LcJW1JTG00WHzc1G2_hG40vn1cWW1jKcm1E11cF0DxdCC1k0zcGG3t4Rq1k0zcYm3nUC01jWzcIW1Plxe1d0zcJG0EKsy1VVvb2W7Jfem1YVnbCG27lnK0vVjb903Emum10',
                # "Host": "id.yandex.ru",
                # "Sec-Fetch-Dest": "document",
                # "Sec-Fetch-Mode": "navigate",
                # "Sec-Fetch-Site": "none",
                # "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": 1,
                # "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36",
                # "sec-ch-prefers-color-scheme": "dark",
                # "sec-ch-ua": f'"Not_A Brand";v="8", "Chromium";v="120", "YaBrowser";v="24.1", "Yowser";v="2.5"',
                # "sec-ch-ua-arch": "arm",
                # "sec-ch-ua-bitness": "64",
                # "sec-ch-ua-full-version-list": '"Not_A Brand";v="8.0.0.0", "Chromium";v="120.0.6099.291", "YaBrowser";v="24.1.5.827", "Yowser";v="2.5"',
                # "sec-ch-ua-mobile": "?0",
                # "sec-ch-ua-platform": "macOS",
                # "sec-ch-ua-platform-version": "12.2.0",
                # "sec-ch-ua-wow64": "?0",
            }
            # Create a request interceptor
            def interceptor(request):
                for key, val in my_headers.items():
                    request.headers[key] = val

            # Set the interceptor on the driver
            driver.request_interceptor = interceptor
        
        # Для того, чтобы обойти защиту проверки браузера на использование автоматизированного ПО,
        # Отключение некоторых опций, которые присутствуют в браузере под управлением Selenium
        if DISABLE_AUTO_OPTIONS_SELENIUM:
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                'source': '''
                    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
            '''
            })

        driver.set_page_load_timeout(30)
        # driver.maximize_window()

        return driver
    except Exception as exc:
        logger.error(f'Ошибка при инициализации драйвера {exc}')
    
    

