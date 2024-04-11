import pickle
import pandas as pd
from sys import argv
import logging
logger = logging.getLogger(__name__)
# script, filename = argv

def convert_pkl_to_json_files_from_dir():
    # загрузить в список файлы из папки cookies_yandex
    from os import listdir
    from os.path import isfile, join
    target_dir = input('Введите имя директории (папки), файлы pkl из которой нужно конвертировать в json: ')
    files_from_dir = [f for f in listdir(f'./{target_dir}/') if isfile(join(f'./{target_dir}/', f))]
    # Выбираем файл pkl
    for file in files_from_dir:
        if file[-4: ] == '.pkl':
            logger.info(f'конвертация файла {file[: -4]}'+'.pkl')
            # Load the pickle format file
            input_file = open(f'./{target_dir}/{file}', 'rb')
            # new_dict = pickle.load(input_file)
            # loads the pickle file into a pandas DataFrame
            data = pd.read_pickle(input_file)
            print(data)

            # Create a Pandas DataFrame
            # df = pd.DataFrame.from_dict(new_dict, orient='index')
            # resets the index of the DataFrame
            data.reset_index(drop=True, inplace=True)

            # Copy DataFrame index as a column
            # df['index1'] = df.index

            # Move the new index column to the front of the DataFrame
            # index1 = df['index1']
            # df.drop(labels=['index1'], axis=1, inplace=True)
            # df.insert(0, 'index1', index1)

            # Convert to json values
            # json_df = df.to_json(orient='values', date_format='iso', date_unit='s')
            data_json = data.to_json('data.json', orient='columns')

            # Create and record the JSON data in a new .JSON file
            with open(f'./{target_dir}/{file[: -4]}.json', 'w') as js_file:
                js_file.write(data_json)
    logger.info(f'Работаем с файлами выполнена')

