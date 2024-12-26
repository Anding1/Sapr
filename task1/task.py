import pandas as pd
import sys

def get_cell_value(file_path, row_number, column_number):
    # Читаем CSV файл в DataFrame
    df = pd.read_csv(file_path)

    # Проверяем, что номера строк и колонок находятся в допустимых пределах
    if row_number < 0 or row_number >= len(df):
        print(f"Ошибка: Номер строки {row_number + 1} вне диапазона.")
        return None
    if column_number < 0 or column_number >= len(df.columns):
        print(f"Ошибка: Номер колонки {column_number + 1} вне диапазона.")
        return None

    # Получаем значение ячейки
    cell_value = df.iat[row_number, column_number]
    return cell_value

def main():
    if len(sys.argv) != 4:
        print("Использование: python task.py <путь_к_csv> <номер_строки> <номер_колонки>")
        return

    file_path = sys.argv[1]
    try:
        row_number = int(sys.argv[2]) - 1  # Преобразуем к 0-индексации
        column_number = int(sys.argv[3]) - 1  # Преобразуем к 0-индексации
    except ValueError:
        print("Ошибка: Номера строки и колонки должны быть целыми числами.")
        return

    cell_value = get_cell_value(file_path, row_number, column_number)
    if cell_value is not None:
        print(f"Значение ячейки в строке {row_number + 1}, колонке {column_number + 1}: {cell_value}")

if __name__ == "__main__":
    main()
