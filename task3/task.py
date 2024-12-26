import numpy as np
import csv
import io
import math

def task(csv_data: str) -> float:
    """
    Вычисление энтропии структуры графа из CSV строки.
    csv_data: строка с матрицей экстенсиональных длин узлов графа.
    Возвращает значение энтропии, округленное до одного знака после запятой.
    """
    # Преобразование CSV-строки в матрицу
    matrix = []
    csv_reader = csv.reader(io.StringIO(csv_data), delimiter=' ')
    
    for row in csv_reader:
        matrix.append(list(map(int, row)))
    
    matrix = np.array(matrix)
    
    n = len(matrix)  # Количество узлов (n)
    if n <= 1:
        return 0.0  # Если меньше одного узла, энтропия не считается
    
    entropy = 0.0

    # Двойное суммирование по всем узлам и связям
    for j in range(n):
        for i in range(n):
            l_ij = matrix[i, j]  # Значение экстенсиональной длины для узла i по отношению j
            if l_ij > 0:
                # Рассчитываем вклад по формуле H(m, r)
                probability = l_ij / (n - 1)  # Вероятность
                entropy -= probability * math.log2(probability)

    # Округление до 1 знака после запятой
    return round(entropy, 1)

# Пример использования
if __name__ == "__main__":
    # Пример данных: CSV строки
    strings = [
        "0 1 1 1 1 1\n1 0 0 0 0 0\n1 0 0 0 0 0\n1 0 0 0 0 0\n1 0 0 0 0 0\n1 0 0 0 0 0",
        "0 1 0 0 0 0\n1 0 1 0 0 0\n0 1 0 1 0 0\n0 0 1 0 1 0\n0 0 0 1 0 1\n0 0 0 0 1 0",
        "0 1 0 0 1 0\n1 0 1 1 0 0\n0 1 0 0 0 0\n0 1 0 0 0 0\n1 0 0 0 0 1\n0 0 0 0 1 0",
        "0 1 0 0 0 0\n1 0 1 0 1 0\n0 1 0 1 0 0\n0 0 1 0 0 0\n0 1 0 0 0 1\n0 0 0 0 1 0"
    ]

    # Пример вызова для матриц
    for i, csv_data in enumerate(strings, start=1):
        entropy_value = task(csv_data)
        print(f"Entropy for matrix #{i}: {entropy_value}")
