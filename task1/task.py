import pandas as pd
import sys

def task1(file_path, row_number, column_number):
    # Читаем CSV файл в DataFrame
    df = pd.read_csv(file_path)

    # Проверяем, что номера строк и колонок находятся в допустимых пределах
    if row_number < 0 or row_number >= len(df):
        print(f"Ошибка: Номер строки {row_number} вне диапазона.")
        return
    if column_number < 0 or column_number >= len(df.columns):
        print(f"Ошибка: Номер колонки {column_number} вне диапазона.")
        return

    # Получаем значение ячейки
    cell_value = df.iat[row_number, column_number]
    print(f"Значение ячейки в строке {row_number + 1}, колонке {column_number + 1}: {cell_value}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Использование: python script.py <путь_к_csv> <номер_строки> <номер_колонки>")
    else:
        file_path = sys.argv[1]
        row_number = int(sys.argv[2]) - 1  # Преобразуем к 0-индексации
        column_number = int(sys.argv[3]) - 1  # Преобразуем к 0-индексации
        task1(file_path, row_number, column_number)

