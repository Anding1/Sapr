import numpy as np
import json

def build_relation_matrix(ranking, n):
    Y = np.zeros((n, n), dtype=int)
    np.fill_diagonal(Y, 1)

    for idx, cluster in enumerate(ranking):
        if isinstance(cluster, int):
            cluster = [cluster]
        else:
            cluster = [item for sublist in cluster for item in (sublist if isinstance(sublist, list) else [sublist])]

        for i in cluster:
            for j in cluster:
                Y[i - 1][j - 1] = 1

        for i in cluster:
            for prev_cluster in ranking[:idx]:
                if isinstance(prev_cluster, int):
                    prev_cluster = [prev_cluster]
                else:
                    prev_cluster = [item for sublist in prev_cluster for item in (sublist if isinstance(sublist, list) else [sublist])]

                for j in prev_cluster:
                    Y[j - 1][i - 1] = 1

    return Y

def find_discrepancies(YA, YB):
    n = YA.shape[0]
    discrepancies = []
    for i in range(n):
        for j in range(n):
            if YA[i, j] == 1 and YB[i, j] == 0 and YA[j, i] == 0 and YB[j, i] == 1:
                discrepancies.append((i + 1, j + 1))
            elif YA[i, j] == 0 and YB[i, j] == 1 and YA[j, i] == 1 and YB[j, i] == 0:
                discrepancies.append((j + 1, i + 1))
    return discrepancies

def find_core_AB(discrepancies):
    core_AB = []
    added = set()

    for x, y in discrepancies:
        if any(x in group or y in group for group in core_AB):
            for group in core_AB:
                if x in group or y in group:
                    if x not in group:
                        group.append(x)
                    if y not in group:
                        group.append(y)
                    break
        else:
            core_AB.append([x, y])

        added.update([x, y])

    return core_AB

def main(file_A, file_B):
    # Чтение данных из файлов
    with open(file_A, 'r') as f:
        ranking_A = json.load(f)
    
    with open(file_B, 'r') as f:
        ranking_B = json.load(f)

    n_A = sum(len(item) if isinstance(item, list) else 1 for item in ranking_A)
    n_B = sum(len(item) if isinstance(item, list) else 1 for item in ranking_B)
    n = max(n_A, n_B)

    YA = build_relation_matrix(ranking_A, n)
    YB = build_relation_matrix(ranking_B, n)

    discrepancies = find_discrepancies(YA, YB)
    core_AB = find_core_AB(discrepancies)

    # Возвращаем результат в формате JSON-строки
    return json.dumps({"core_AB": core_AB}, indent=4)

# Пример использования
if __name__ == "__main__":
    file_A = 'C:/Users/Наталья/Desktop/task5/A.json'  # Укажите путь к вашему файлу A
    file_B = 'C:/Users/Наталья/Desktop/task5/B.json'  # Укажите путь к вашему файлу B
    result = main(file_A, file_B)
    print(result)
