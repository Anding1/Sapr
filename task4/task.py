import numpy as np
from collections import defaultdict

def calculate_entropy_purchases():
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

    return [round(H_AB, 2), round(H_A, 2), round(H_B, 2), round(H_B_given_A, 2), round(I_A_B, 2)]

def calculate_entropy_dice():
    # Шаг 1: Определение вероятностей
    outcomes = [(i, j) for i in range(1, 7) for j in range(1, 7)]
    total_outcomes = len(outcomes)
    
    # Вычисляем вероятности для A (суммы) и B (произведения)
    sum_counts = defaultdict(int)
    product_counts = defaultdict(int)
    joint_counts = defaultdict(int)
    
    for i, j in outcomes:
        sum_value = i + j
        product_value = i * j
        sum_counts[sum_value] += 1
        product_counts[product_value] += 1
        joint_counts[(sum_value, product_value)] += 1
    
    # Вероятности для A, B и совместные вероятности
    P_A = {k: v / total_outcomes for k, v in sum_counts.items()}
    P_B = {k: v / total_outcomes for k, v in product_counts.items()}
    P_AB = {k: v / total_outcomes for k, v in joint_counts.items()}
    
    # Шаг 2: Вычисление энтропии H(AB)
    H_AB = -sum(p * np.log2(p) for p in P_AB.values() if p > 0)
    
    # Шаг 3: Вычисление энтропии H(A)
    H_A = -sum(p * np.log2(p) for p in P_A.values() if p > 0)
    
    # Шаг 4: Вычисление энтропии H(B)
    H_B = -sum(p * np.log2(p) for p in P_B.values() if p > 0)
    
    # Шаг 5: Вычисление условной энтропии H(B|A) и информации I(A, B)
    H_B_given_A = H_AB - H_A
    I_A_B = H_B - H_B_given_A
    
    return [round(H_AB, 2), round(H_A, 2), round(H_B, 2), round(H_B_given_A, 2), round(I_A_B, 2)]

def main():
    purchases_results = calculate_entropy_purchases()
    dice_results = calculate_entropy_dice()
    
    return {
        "Purchases": purchases_results,
        "Dice": dice_results
    }

if __name__ == "__main__":
    results = main()
    print("Purchases Entropy Results:", results["Purchases"])
    print("Dice Entropy Results:", results["Dice"])
