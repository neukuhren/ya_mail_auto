## ------------ Системные требования: ----------------
Наличие браузера Google Chrome https://www.google.com/intl/ru/chrome/
Наличие интерпретатора python  https://www.python.org/downloads/
- обязательно: не ниже версии 3.8 (windows 7 last python version)
- рекомендуется: не ниже версии 3.11.4

## -------------------Установка ----------------------
### Создать папки:
cookies_yandex
cookies_mailru
cookies_autoru
backups
extensions

## Запустить терминал и выполнить следующие команды:
### на Windows:
python -m venv venv
. venv/scripts/activate
python -m pip install --upgrade pip
pip install -r req.txt

### на Mac OS:
python3 -m venv venv
. venv/bin/activate
python3 -m pip3 install --upgrade pip
pip3 install -r req.txt


## ------------- Подготовка к запуску: ----------------
1. ### Ранее сохраненные cookies-файлы формата .pkl
поместить в соответствующие папки cookies_yandex и cookies_mailru
2. ### Ранее сохраненные сведения об аккаунтах в формате xlsx-файлов
- combined.xlsx (данные аккаунтов yandex)
- combined_mailru.xlsx (данные аккаунтов mail.ru)
поместить в корневую папку проекта (ya_mail_auto)
3. ### Исходные данные об аккаунтах в формате txt-файлов 
- combined.txt (данные аккаунтов yandex)
- combined_mailru.txt (данные аккаунтов mail.ru)
поместить в корневую папку проекта (ya_mail_auto)
4. ### Шаблоны текстовых сообщений для рассылки в файле text.txt
поместить в корневую папку проекта (ya_mail_auto)
5. ### Для обхода каптчи
В файле config.txt в строке API_KEY_FOR_RUCAPTCHA: 
указать после двоеточия значение ключа с сайта https://2captcha.com/enterpage
например, 
API_KEY_FOR_RUCAPTCHA:9ac02c9ggg1dd9bbb27t87b65c85rec378
6. ### При необходимости работы программы в скрытом режиме браузера
В файле config.txt в строке HEADLESS: 
указать после двоеточия значение True
например, 
HEADLESS:True
7. ### Чтобы при регистрации в яндекс использовать имея и фамилию, указанные в аккаунте mailru
В файле config.txt в строке USED_NAME_FROM_MAILRU: 
указать после двоеточия значение True
например, 
USED_NAME_FROM_MAILRU:True
Внимание! Очень часто в аккаунтах mailru в качестве имени используются просто набор 
латинских букв. Возможно, лучше использовать генерацию русских имени и фамилии.
Для этого параметр изменить на
USED_NAME_FROM_MAILRU:False

## --------------------- Запуск ------------------------
### Запустить терминал и выполнить следующие команды:
### на Windows:
. venv/scripts/activate
python main.py
### на Mac OS:
. venv/bin/activate
python3 main.py
