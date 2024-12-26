import numpy as np
from collections import defaultdict

def main():
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
    
    results = [round(H_AB, 2), round(H_A, 2), round(H_B, 2), round(H_B_given_A, 2), round(I_A_B, 2)]
    
    return results

print(main())
