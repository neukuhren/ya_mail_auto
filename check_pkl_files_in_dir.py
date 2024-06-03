# import pickle
# import pandas as pd
# from sys import argv
import pickle
import json
import os
import tkinter as tk
from tkinter import filedialog

import logging
logger = logging.getLogger(__name__)
# script, filename = argv

from time import time


def convert_pkl_to_json_files_from_dir():
    root = tk.Tk()
    root.withdraw()  # Скрываем основное окно

    # Открываем диалоговое окно для выбора директорий
    input_directory = filedialog.askdirectory(title="Выберите папку с pkl файлами")
    output_directory = filedialog.askdirectory(title="Выберите папку для json файлов")

    input_directory, output_directory
    all, good, bad = 0, 0, 0
    for filename in os.listdir(input_directory):
        if filename.endswith(".pkl"):
            all += 1
            with open(os.path.join(input_directory, filename), 'rb') as file:
                cookies_data = pickle.load(file)
                if cookies_data:
                    good +=1
                    print(cookies_data)
                else: bad += 1
            # with open(os.path.join(output_directory, filename.replace('.pkl', '.json')), 'w') as file:
            #     json.dump({"cookies": cookies_data}, file)
    logger.info(f'Работаем с файлами завершена')
    print(f'Всего pkl файлов - {all}, прочитанных - {good}, битых - {bad}')


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
    
    convert_pkl_to_json_files_from_dir()

    print('\n\n')
    print('Время работы программы составило: ')
    print("--- %s seconds ---" % round((time() - start_time), 0))
    print('[!] Программа выполнена.')

# def convert_pkl_to_json():
#     # загрузить в список файлы из папки cookies_yandex
#     from os import listdir
#     from os.path import isfile, join
#     target_dir = input('Введите имя директории (папки), файлы pkl из которой нужно конвертировать в json: ')
#     files_from_dir = [f for f in listdir(f'./{target_dir}/') if isfile(join(f'./{target_dir}/', f))]
#     # Выбираем файл pkl
#     for file in files_from_dir:
#         if file[-4: ] == '.pkl':
#             logger.info(f'конвертация файла {file[: -4]}'+'.pkl')
#             # Load the pickle format file
#             input_file = open(f'./{target_dir}/{file}', 'rb')
#             # new_dict = pickle.load(input_file)
#             # loads the pickle file into a pandas DataFrame
#             data = pd.read_pickle(input_file)
#             print(data)

#             # Create a Pandas DataFrame
#             # df = pd.DataFrame.from_dict(new_dict, orient='index')
#             # resets the index of the DataFrame
#             data.reset_index(drop=True, inplace=True)

#             # Copy DataFrame index as a column
#             # df['index1'] = df.index

#             # Move the new index column to the front of the DataFrame
#             # index1 = df['index1']
#             # df.drop(labels=['index1'], axis=1, inplace=True)
#             # df.insert(0, 'index1', index1)

#             # Convert to json values
#             # json_df = df.to_json(orient='values', date_format='iso', date_unit='s')
#             data_json = data.to_json('data.json', orient='columns')

#             # Create and record the JSON data in a new .JSON file
#             with open(f'./{target_dir}/{file[: -4]}.json', 'w') as js_file:
#                 js_file.write(data_json)

