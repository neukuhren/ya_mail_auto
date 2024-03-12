"""Модуль для поиска и решения каптч."""
import inspect  # Для имени функции
import logging

# Импортируем библиотеку для безопасного хранения логов
# Установлены настройки логгера для текущего файла
# В переменной __name__ хранится имя пакета;
# Это же имя будет присвоено логгеру.
# Это имя будет передаваться в логи, в аргумент %(name)
logger = logging.getLogger(__name__)

from selenium.webdriver.common.by import By


def find_and_click_captcha_iam_not_robot(driver: object) -> None:
    """Проверяет есть ли каптча (тип 1 и 2) я не робот и кликает на нее.
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')

    try:
        el_captcha = driver.find_element(By.ID, "recaptcha-anchor")
        if el_captcha:
            logger.debug(f'На странице была найдена каптча по id. Кликаю')
            try:
                el_captcha.click()
            except:
                logger.error('Ошибка при клике на каптчу')
    except:
        logger.debug(f'Каптчи не было, либо она не была найдена по id.')

    # поиск по class_name
    list_on_class_name = [
        "recaptcha-checkbox-checkmark"
        "CheckboxCaptcha-Anchor",
        "recaptcha-checkbox-border",
    ]
    for class_name in list_on_class_name:
        try:
            el_captcha = driver.find_element(By.CLASS_NAME, class_name)
            if el_captcha:
                logger.debug(f'На странице была найдена каптча по class_name. Кликаю')
                try:
                    el_captcha.click()
                    break
                except:
                    logger.error('Ошибка при клике на каптчу')
        except:
            logger.debug(f'Каптчи не было, либо она не была найдена по class_name.')
    
    # поиск по css_selector
        list_on_css_selectors = [
        "#root > div:nth-child(2) > div > div > div > div > div > form > div:nth-child(2) > div > div.login-row.captcha > div > div > div > div.widget > div > div > div > iframe"
        "#recaptcha-anchor-label"
        "#recaptcha-anchor",
        "#rc-anchor-container",
        "#rc-anchor-container > div.rc-anchor-content > div:nth-child(1)",
        "#rc-anchor-container > div.rc-anchor-content > div:nth-child(1) > div",
        "#rc-anchor-container > div.rc-anchor-content > div:nth-child(1) > div > div",
        "#recaptcha-anchor",
        "#recaptcha-anchor > div.recaptcha-checkbox-border",
        "#recaptcha-anchor > div.recaptcha-checkbox-borderAnimation",
        "#recaptcha-anchor > div.recaptcha-checkbox-checkmark",
    ]
    for css_selector in list_on_css_selectors:
        try:
            el_captcha2 = driver.find_element(By.CSS_SELECTOR, css_selector)
            if el_captcha2:
                logger.debug(f'На странице была найдена каптча по css_selector. Кликаю')
                try:
                    el_captcha2.click()
                    break
                except:
                    logger.error('Ошибка при клике на каптчу')
        except:
            logger.debug(f'Каптчи не было, либо она не была найдена по css_selector.')

    # поиск по xpath
    list_on_xpath = [
        '//*[@id="recaptcha-anchor"]/div[4]',
        '//*[@id="recaptcha-anchor"]',
    ]
    for xpath in list_on_xpath:
        try:
            el_captcha4 = driver.find_element(By.XPATH, xpath)
            
            if el_captcha4:
                logger.debug(f'На странице была найдена каптча по xpath. Кликаю')
                try:
                    el_captcha4.click()
                    break
                except:
                    logger.error('Ошибка при клике на каптчу')
        except:
            logger.debug(f'Каптчи не было, либо она не была найдена по xpath.')


# import os 
# from dotenv import load_dotenv # Импортируем для безопасного хранения токенов
# load_dotenv()
# доступны в пространстве переменных окружения
# API_KEY_FOR_RUCAPTCHA = os.getenv('API_KEY_FOR_RUCAPTCHA')

def decrypt_recaptcha_v2_iam_not_robot(driver :object, api_key_for_rucaptcha :str) -> None:
    """Решает recaptcha V2 я не робот.
    Args:
    api_key_for_rucaptcha : str - ключ для работы с API rucaptcha
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    # https://github.com/2captcha/2captcha-python
    import sys
    import os
    # sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    from twocaptcha import TwoCaptcha  # для использования сервиса rucaptcha.ru
    # api_key = os.getenv('APIKEY_2CAPTCHA', 'YOUR_API_KEY')
    solver = TwoCaptcha(api_key_for_rucaptcha)
    try:
        result = solver.recaptcha(
            sitekey='6LfD3PIbAAAAAJs_eEHvoOl75_83eXSqpPSRFJ_u',
            url='https://2captcha.com/demo/recaptcha-v2')
    except Exception as e:
        logger.error(e)
        # sys.exit(e)
    # else:
    #     sys.exit('solved: ' + str(result))



# import os 
# from dotenv import load_dotenv # Импортируем для безопасного хранения токенов
# load_dotenv()
# доступны в пространстве переменных окружения
# API_KEY_FOR_RUCAPTCHA = os.getenv('API_KEY_FOR_RUCAPTCHA')
from twocaptcha import TwoCaptcha  # для использования сервиса rucaptcha.ru
from time import sleep
def decrypt_captcha_deform_text(api_key_for_rucaptcha :str, file_name: str):
    """Отправляет изображение каптчи на rucaptcha для расшифровки.
    Args:
    api_key_for_rucaptcha : str - ключ для работы с API rucaptcha
    Returns:
    code : str - текстовая строка с расшифрованными символами."""
    try:
        solver = TwoCaptcha(api_key_for_rucaptcha)
        id = solver.send(file=file_name)
        sleep(12)
        code = solver.get_result(id)
        return code
    except Exception as exc:
        logger.error(f'Ошибка при расшифровке каптчи {exc}')



def find_and_click_btn_audiotest(driver :object) -> None:
    """Проверяет есть ли кнопка "Пройти аудиотест" и кликает на неё.
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        el_btn_signin = driver.find_element(By.CSS_SELECTOR, "#recaptcha-audio-button")
        logger.info(f'Обнаружена recaptcha. Попытка обойти через аудио...')
        logger.debug(f'На странице была найдена кнопка "Пройти аудиотест". Кликаю')
        try:
            el_btn_signin.click()
        except:
            logger.error('Ошибка при клике на кнопку "Пройти аудиотест"')
    except:
        logger.debug(f'Кнопка "Пройти аудиотест" не найдена')


# def find_and_click_btn_next(driver :object) -> None:
#     """Проверяет есть ли кнопка "Скачать mp-3 файл" и кликает на неё.
#     """
#     logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
#     try:
#         el_btn_download = driver.find_element(By.CSS_SELECTOR, "#rc-audio > div.rc-audiochallenge-tdownload > a")
#         logger.debug(f'На странице была найдена кнопка "Скачать mp-3 файл". Кликаю')
#         try:
#             el_btn_download.click()
#         except:
#             logger.error('Ошибка при клике на кнопку "Скачать mp-3 файл"')
#     except:
#         logger.debug(f'Кнопка "Скачать mp-3 файл" не найдена')


def get_url_src_audio_file_from_btn(driver :object) -> str:
    """Проверяет есть ли кнопка "Прослушать" и кликает на неё.
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        el_btn_listen = driver.find_element(By.CSS_SELECTOR, "#audio-source")
        logger.debug(f'На странице была найдена кнопка "Прослушать". Ищу источник аудио.')
        try:
            el = driver.find_element(By.ID, "audio-source")
            src = el.get_attribute("src")
            return src
        except:
            logger.error('Ошибка при поиске источника аудиофайла"')
    except:
        logger.debug(f'Кнопка "Прослушать" не найдена')


def hack_recaptcha_used_audio_file(driver :object):
    """Скачивает аудио файл из recaptcha.
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        # Switch back to the first tab
        # driver.switch_to.window(driver.window_handles[0])
        find_and_click_captcha_iam_not_robot(driver=driver)  # кликаем я не робот
        sleep(1)
        find_and_click_btn_audiotest(driver=driver)
        sleep(1)
        src = get_url_src_audio_file_from_btn(driver=driver)
        # Скачиваем и сохраняем файл
        import urllib.request
        urllib.request.urlretrieve(src, "audio.mp3")
        from txt_utils import read_parameters_from_txt_file_and_add_to_dict
        # PARAM_DICT = read_parameters_from_txt_file_and_add_to_dict()
        # """Словарь с параметрами из файла config.txt"""
        from vosk_simple import text_from_mp3
        text_from_audio_captcha = text_from_mp3(path_audio_mp3='audio.mp3') # PARAM_DICT["PATH_TO_DIR_DOWNLOADS"]+'audio.mp3'
        if text_from_audio_captcha:
            logger.info(f'Расшифрованная кодовая фраза: {text_from_audio_captcha}')
    except:
        logger.debug(f'При обходе каптчи возникла ошибка, либо каптчи не было.')