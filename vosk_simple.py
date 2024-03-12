"""Модуль для распознавания аудио с использованием нейросети Vosk."""

import subprocess
import wave
import sys
from vosk import Model, KaldiRecognizer, SetLogLevel
import json

from pydub import AudioSegment  # pip install pydub - для конвертации mp3 в wav

from time import sleep
import inspect
import logging # Импортируем библиотеку для безопасного хранения логов
# Установлены настройки логгера для текущего файла
# В переменной __name__ хранится имя пакета;
# Это же имя будет присвоено логгеру.
# Это имя будет передаваться в логи, в аргумент %(name)
logger = logging.getLogger(__name__)

from config import PATH_VOSK_MODEL  # Имя папки, в которой находится модель Vosk


def convert_mp3_to_wav(path_audio_mp3 :str) -> str:
    """Конвертирует аудиофайл формата mp3 в wav.
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        audio_mp3 = AudioSegment.from_mp3(path_audio_mp3)
        audio_mp3.set_channels(1)
        path_audio_wav = f'{path_audio_mp3[:-4]}.wav'
        audio_mp3.export(path_audio_wav, format='wav')  # format='s16le' для pcm
        audio_wav = AudioSegment.from_wav(file=path_audio_wav)
        audio_wav = audio_wav.set_channels(1)
        audio_wav.export(path_audio_wav, format='wav')
        
        # import soundfile  # pip install soundfile
        # # Читаем и перезаписываем файл как soundfile
        # data, samplerate = soundfile.read(path_audio_wav)
        # soundfile.write(path_audio_wav, data, samplerate)
        # # Now try to open the file with wave
        # with wave.open(path_audio_wav) as file:
        #     print('File opened!')

        logger.info('Конвертация аудио в формат wav выполнена успешно')
        return path_audio_wav
    except:
        logger.error('Ошибка при конвертации аудио файла')


def get_text_from_wav(path_audio_wav :str):
    """Транскрибация текста из аудио файла wav
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    try:
        # При необходимости получения debug сообщений можно установить значение 0
        SetLogLevel(-1)

        wf = wave.open(f=path_audio_wav, mode='rb')
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
            print("Audio file must be WAV format mono PCM.")
            sys.exit(1)

        logger.info(f'Запуск нейросети...')
        sleep(2)
        # You can also init model by name or with a folder path
        model = Model(PATH_VOSK_MODEL)

        rec = KaldiRecognizer(model, wf.getframerate())
        rec.SetWords(True)
        rec.SetPartialWords(True)

        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                # print(rec.Result())
                pass
            else:
                # print(rec.PartialResult())
                pass
        
        result = json.loads(rec.FinalResult())
        return result["text"]
    except:
        return


def text_from_mp3(path_audio_mp3 :str) -> str:
    """Транскрибация текста из аудио файла mp3
    """
    logger.debug(f'Запуск функции {inspect.currentframe().f_code.co_name}')
    path_audio_wav = convert_mp3_to_wav(path_audio_mp3=path_audio_mp3)
    logger.debug(f'Перекодирование mp3 --> wav')
    return get_text_from_wav(path_audio_wav=path_audio_wav)


if __name__ == '__main__':
    print(text_from_mp3(path_audio_mp3='/Users/me/Downloads/audio.mp3'))
