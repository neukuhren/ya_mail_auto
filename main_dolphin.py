import requests #Модуль запросов
from selenium import webdriver #Модуль Selenium драйвера
from selenium.webdriver.chrome.service import Service #Модуль Selenium драйвера
import time #Модуль ожидания или сна
import json

import logging # Импортируем библиотеку для безопасного хранения логов
# Установлены настройки логгера для текущего файла
# В переменной __name__ хранится имя пакета;
# Это же имя будет присвоено логгеру.
# Это имя будет передаваться в логи, в аргумент %(name)
logger = logging.getLogger(__name__)

# enpoint_browser_profile = "https://dolphin-anty-api.com/browser_profiles"
# TOKEN_DOLPHIE = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiNDFiZDI5NjhiMmY1ZjUyNGJkY2NlNzAzNmVhYzJhYzA5MGYyYmY0NWNmODczMDgzOTFmMzdiZWExZmFjYzg2NjNiZjgxYzM0ZDkyOGJhNzMiLCJpYXQiOjE3MTY4ODAwNTYuODI2NDc2LCJuYmYiOjE3MTY4ODAwNTYuODI2NDc3LCJleHAiOjE3NDg0MTYwNTYuODE3Njc2LCJzdWIiOiIzNDIxNjYyIiwic2NvcGVzIjpbXX0.KOIcw0nZgLoWz1cuA4lYV_brYa_Sq1n3rsU2_dJQ2Ny-UVyWCBOTSQWhOwiUCYaWXANxsNyiBPQonwp2EadDHgA45nzcDXwYG896I_t7m1fBdDIM8aAPy94jDCUpcnEy3G77F9fIc7r8MsAGFm_-sWXGer0y_tC0z5OLv7R7HIvM3vPdejfQT2efiVmBZxbJ9bjXG8DNkZ3oLaipo2NV0kpODQUBTZJHzCzTn2f6be-04LQFpotfpkkDzcSYDUcB2_ASsI0Hy3nmoXO25NNJ_XwhsTG6WhoJGXhFzkZpI3ShjTUPWvt6vJRsaqZgpyliNQGyPTCg8n_6cslzJBL6cBPLjJkpZYA9nt6h0dfKvqjW-CDw7hAEenX0zEBd-BiMMXHp0kSKiiaea_but0QdWbbEqglLPYuIj66V1nOqK8cIc2yirf4BcrQLTteF1tXSZkFrnTr0iYT-qqsYJKmGT-oGfAEZ42Z2ExBu5qeMh7wKuv-Nolyd7roljIt7UpfUUnYylhkH2-kcdNipMwYmQhVpSUcpEwYPLFwq7TkzJ6GowbNa4JpNFU9ea0lp-knVy6-_CMWwghcEpLwXE1zbDsmGhNsf5WyVS7poAqvQpA6RtZN1DCEJKnCTPWltDHM8-6AMJlPsCK57vRd3hml0I5uYQE59gzFjHNxhJ587xXs'

# payload='name=&tags%5B%5D=&tabs=&platform=&mainWebsite=&useragent%5Bmode%5D=&useragent%5Bvalue%5D=&webrtc%5Bmode%5D=&webrtc%5BipAddress%5D=&canvas%5Bmode%5D=&webgl%5Bmode%5D=&webglInfo%5Bmode%5D=&webglInfo%5Bvendor%5D=&webglInfo%5Brenderer%5D=&webglInfo%5Bwebgl2Maximum%5D=%7B%5C%22MAX_SAMPLES%5C%22%3A%208%2C%20%5C%22MAX_DRAW_BUFFERS%5C%22%3A%208%2C%20%5C%22MAX_TEXTURE_SIZE%5C%22%3A%2016384%2C%20%5C%22MAX_ELEMENT_INDEX%5C%22%3A%204294967294%2C%20%5C%22MAX_VIEWPORT_DIMS%5C%22%3A%20%5B16384%2C%2016384%5D%2C%20%5C%22MAX_VERTEX_ATTRIBS%5C%22%3A%2016%2C%20%5C%22MAX_3D_TEXTURE_SIZE%5C%22%3A%202048%2C%20%5C%22MAX_VARYING_VECTORS%5C%22%3A%2030%2C%20%5C%22MAX_ELEMENTS_INDICES%5C%22%3A%202147483647%2C%20%5C%22MAX_TEXTURE_LOD_BIAS%5C%22%3A%2015%2C%20%5C%22MAX_COLOR_ATTACHMENTS%5C%22%3A%208%2C%20%5C%22MAX_ELEMENTS_VERTICES%5C%22%3A%202147483647%2C%20%5C%22MAX_RENDERBUFFER_SIZE%5C%22%3A%2016384%2C%20%5C%22MAX_UNIFORM_BLOCK_SIZE%5C%22%3A%2065536%2C%20%5C%22MAX_VARYING_COMPONENTS%5C%22%3A%20120%2C%20%5C%22MAX_TEXTURE_IMAGE_UNITS%5C%22%3A%2032%2C%20%5C%22MAX_ARRAY_TEXTURE_LAYERS%5C%22%3A%202048%2C%20%5C%22MAX_PROGRAM_TEXEL_OFFSET%5C%22%3A%207%2C%20%5C%22MIN_PROGRAM_TEXEL_OFFSET%5C%22%3A%20-8%2C%20%5C%22MAX_CUBE_MAP_TEXTURE_SIZE%5C%22%3A%2016384%2C%20%5C%22MAX_VERTEX_UNIFORM_BLOCKS%5C%22%3A%2013%2C%20%5C%22MAX_VERTEX_UNIFORM_VECTORS%5C%22%3A%204096%2C%20%5C%22MAX_COMBINED_UNIFORM_BLOCKS%5C%22%3A%2060%2C%20%5C%22MAX_FRAGMENT_UNIFORM_BLOCKS%5C%22%3A%2013%2C%20%5C%22MAX_UNIFORM_BUFFER_BINDINGS%5C%22%3A%2072%2C%20%5C%22MAX_FRAGMENT_UNIFORM_VECTORS%5C%22%3A%204096%2C%20%5C%22MAX_VERTEX_OUTPUT_COMPONENTS%5C%22%3A%20124%2C%20%5C%22MAX_FRAGMENT_INPUT_COMPONENTS%5C%22%3A%20124%2C%20%5C%22MAX_VERTEX_UNIFORM_COMPONENTS%5C%22%3A%2016384%2C%20%5C%22MAX_VERTEX_TEXTURE_IMAGE_UNITS%5C%22%3A%2032%2C%20%5C%22MAX_FRAGMENT_UNIFORM_COMPONENTS%5C%22%3A%2016384%2C%20%5C%22UNIFORM_BUFFER_OFFSET_ALIGNMENT%5C%22%3A%20256%2C%20%5C%22MAX_COMBINED_TEXTURE_IMAGE_UNITS%5C%22%3A%2064%2C%20%5C%22MAX_COMBINED_VERTEX_UNIFORM_COMPONENTS%5C%22%3A%20229376%2C%20%5C%22MAX_TRANSFORM_FEEDBACK_SEPARATE_ATTRIBS%5C%22%3A%204%2C%20%5C%22MAX_COMBINED_FRAGMENT_UNIFORM_COMPONENTS%5C%22%3A%20229376%2C%20%5C%22MAX_TRANSFORM_FEEDBACK_SEPARATE_COMPONENTS%5C%22%3A%204%2C%20%5C%22MAX_TRANSFORM_FEEDBACK_INTERLEAVED_COMPONENTS%5C%22%3A%20128%7D%22%0Awebrtc%3A%20%7Bmode%3A%20%22altered%22%2C%20ipAddress%3A%20null%7D&notes%5Bicon%5D=&notes%5Bcolor%5D=&notes%5Bstyle%5D=&notes%5Bcontent%5D=&timezone%5Bmode%5D=&timezone%5Bvalue%5D=&locale%5Bmode%5D=&locale%5Bvalue%5D=&statusId=&geolocation%5Bmode%5D=&geolocation%5Blatitude%5D=&geolocation%5Blongitude%5D=&cpu%5Bmode%5D=&cpu%5Bvalue%5D=&memory%5Bmode%5D=&memory%5Bvalue%5D=&doNotTrack=&browserType=&proxy%5Bid%5D=&proxy%5Btype%5D=&proxy%5Bhost%5D=&proxy%5Bport%5D=&proxy%5Blogin%5D=&proxy%5Bpassword%5D=&proxy%5Bname%5D=&proxy%5BchangeIpUrl%5D='
# headers = {
#     'Content-Type': 'application/json',
#     'Authorization': f'Bearer {TOKEN_DOLPHIE}',
# }

# response = requests.post(enpoint_browser_profile, data=payload, headers=headers)

# print(response.text)


#Указываем айди профиля в антике
profile_id = '386720399'

#Делаем запрос к антику и вызываем нужный профиль
mla_url = 'http://localhost:3001/v1.0/browser_profiles/'+profile_id+'/start?automation=1'
resp = requests.get(mla_url)

#Получаем ответ после запуска профиля
json = resp.json()
print(json)

#Парсим значение открытого порта профиля антика
port = str(json['automation']['port'])
print(port)

#Инициализируем путь к веб драйверу Dolphin Anti
# chrome_dolphin_driver_path = Service("C:/Users/duglas/Desktop/SELENIUM/chromedriver-windows-x64-dolphin.exe")

#Загружаем предварительные настройки в Selenium драйвер и подключаемся к порту запущенного профиля
options = webdriver.ChromeOptions()
options.debugger_address = "127.0.0.1:"+port
driver = webdriver.Chrome(options=options) # service=chrome_dolphin_driver_path,

#Загружаем страницы в ранее открытом профиле и автоматизируем любые действия
driver.get('https://google.com/')
print(driver.title)
time.sleep(5)
driver.get('https://vk.com/')
print(driver.title)
driver.delete_all_cookies()
driver.close()
driver.quit()
