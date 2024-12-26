import numpy as np

def main():
    purchases = np.array([
        [20, 15, 10, 5],
        [30, 20, 15, 10],
        [25, 25, 20, 15],
        [20, 20, 25, 20],
        [15, 15, 30, 25]
    ])

    total_purchases = purchases.sum()

    # Шаг 1: Вероятности для A (возрастные группы) и B (товары)
    P_A = purchases.sum(axis=1) / total_purchases  # Сумма по строкам для возрастных групп
    P_B = purchases.sum(axis=0) / total_purchases  # Сумма по столбцам для товаров
    P_AB = purchases / total_purchases             # Совместные вероятности для (A, B)

    # Шаг 2: Вычисление энтропии H(AB)
    H_AB = -np.sum(P_AB * np.log2(P_AB, where=(P_AB > 0)))

    # Шаг 3: Вычисление энтропии H(A)
    H_A = -np.sum(P_A * np.log2(P_A, where=(P_A > 0)))

    # Шаг 4: Вычисление энтропии H(B)
    H_B = -np.sum(P_B * np.log2(P_B, where=(P_B > 0)))

    # Шаг 5: Условная энтропия H(B|A) и информация I(A, B)
    H_B_given_A = H_AB - H_A
    I_A_B = H_B - H_B_given_A

    results = [round(H_AB, 2), round(H_A, 2), round(H_B, 2), round(H_B_given_A, 2), round(I_A_B, 2)]

    return results

print(main())
