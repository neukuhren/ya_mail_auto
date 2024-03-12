"""Модуль для работы с txt файлами"""


def read_txt_file_and_lines_to_list(file_name='combined.txt'):
    """Читает файл txt построчно, РАЗДЕЛЯЕТ СТРОКИ по ":" и возвращает результат в виде списка со списками .
    """
    with open(file_name) as file:
        user_data_list = []
        while line := file.readline():
            cur_line = line.rstrip()
            user_data = cur_line.split(':')
            user_data_list.append(user_data)
        return user_data_list


def read_txt_file_return_list_with_lines_text(file_name='messages.txt'):
    """Читает файл txt построчно и возвращает результат в виде списка.
    """
    with open(file_name, encoding='utf-8', errors='ignore') as file:
        list_with_lines_text = []
        while line := file.readline():
            list_with_lines_text.append(line.strip('\n'))
        return list_with_lines_text

    
def read_parameters_from_txt_file_and_add_to_dict(file_name='config.txt'):
    """Читает файл txt построчно и возвращает результат в виде словаря.
    """
    dict_parameter_value = {}
    with open(file_name) as file:
        while line := file.readline():
            cur_line = line.rstrip()
            list_parameter_value = cur_line.split(':')
            dict_parameter_value[list_parameter_value[0]] = list_parameter_value[1]
        return dict_parameter_value


def write_in_end_row_file_txt(file_name = 'entry_ok.txt', list_with_data = []):
    """Записывает данные в конец строки текстового файла.
    Args:
        Имя файла, в который производить запись;
        Данные в ивде строки или в виде списка, которые необходимо записать."""
    with open(file_name, 'a', encoding='utf-8') as file:
        for index, data in enumerate(list_with_data):
            if isinstance(data, str):  # Если данные приходят в виде строки, 
                file.write(data)  # пишем строку в файл
            elif isinstance(data, list):  # Если данные в виде списка, 
                # то записываем предварительно преобразовав в строку
                file.write(str(data))
            # Если текущие данные последние в списке, 
            if index == len(list_with_data) - 1:
                # То переносим строку
                file.write('\n')
            else:  # Если текущие данные не последние в списке,
                # То разделяем двоеточием 
                file.write(':')