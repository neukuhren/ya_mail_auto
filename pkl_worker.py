import tkinter as tk
from tkinter import filedialog

def read_file():
    filepath = filedialog.askopenfilename()
    try:
        with open(filepath, 'r') as file:
            content = file.read()
            print("Файл прочитан успешно")
            print("Содержимое файла:")
            print(content)
    except:
        print("Файл не удалось прочитать")

root = tk.Tk()
root.title("Чтение файлов pkl")

button = tk.Button(root, text="Выбрать файл...", command=read_file)
button.pack()

close_button = tk.Button(root, text="Выход", command=root.destroy)
close_button.pack()

root.mainloop()