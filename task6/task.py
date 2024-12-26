import json
import numpy as np

def calculate_membership(value, points):
    """Вычисляет степень принадлежности value для трапециевидной функции."""
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        if x1 <= value <= x2:
            if x1 == x2:
                return max(y1, y2)  # На случай плоской области
            return y1 + (y2 - y1) * (value - x1) / (x2 - x1)
    return 0

def fuzzify(value, fuzzy_sets):
    """Фаззификация значения для всех термов."""
    memberships = {}
    for term in fuzzy_sets:
        term_id = term["id"]
        term_points = term["points"]
        memberships[term_id] = calculate_membership(value, term_points)
    return memberships

def apply_rules(temp_memberships, rules, heating_sets):
    """Применяет правила логического вывода."""
    outputs = []
    for temp_term, heating_term in rules:
        activation = temp_memberships.get(temp_term, 0)  # Получаем активацию для терма температуры
        if activation > 0:  # Если активен терм
            # Найдем соответствующий терм уровня нагрева
            for heating_set in heating_sets:
                if heating_set["id"] == heating_term:
                    # Масштабируем значения нагрева по активации
                    scaled_points = [
                        [x, min(y, activation)] for x, y in heating_set["points"]
                    ]
                    outputs.append(scaled_points)
                    break
    return outputs

def aggregate(outputs):
    """Агрегирует нечеткие множества (по максимуму)."""
    combined = {}
    for output in outputs:
        for x, y in output:
            if x in combined:
                combined[x] = max(combined[x], y)  # Мы объединяем по максимуму
            else:
                combined[x] = y
    return sorted(combined.items())

def defuzzify(aggregated):
    """Дефаззификация методом центра тяжести."""
    numerator = sum(x * y for x, y in aggregated)
    denominator = sum(y for _, y in aggregated)
    return numerator / denominator if denominator != 0 else 0

def task(temp_json, heating_json, rules_json, current_temp):
    """Основная функция для выполнения задания."""
    # Загрузка данных из JSON
    temp_sets = json.loads(temp_json)["температура"]
    heating_sets = json.loads(heating_json)["уровень нагрева"]
    rules = json.loads(rules_json)
    
    # Фаззификация
    temp_memberships = fuzzify(current_temp, temp_sets)
    
    # Применение правил
    outputs = apply_rules(temp_memberships, rules, heating_sets)
    
    # Агрегация
    aggregated = aggregate(outputs)
    
    # Дефаззификация
    optimal_control = defuzzify(aggregated)
    return optimal_control

if __name__ == "__main__":
    # Пример данных
    temp_json = """
    {
        "температура": [
            {
            "id": "холодно",
            "points": [
                [0,1],
                [18,1],
                [22,0],
                [50,0]
            ]
            },
            {
            "id": "комфортно",
            "points": [
                [18,0],
                [22,1],
                [24,1],
                [26,0]
            ]
            },
            {
            "id": "жарко",
            "points": [
                [0,0],
                [24,0],
                [26,1],
                [50,1]
            ]
            }
        ]
    }
    """
    heating_json = """
    {
        "уровень нагрева": [
            {
                "id": "слабый",
                "points": [
                    [0,0],
                    [0,1],
                    [5,1],
                    [8,0]
                ]
            },
            {
                "id": "умеренный",
                "points": [
                    [5,0],
                    [8,1],
                    [13,1],
                    [16,0]
                ]
            },
            {
                "id": "интенсивный",
                "points": [
                    [13,0],
                    [18,1],
                    [23,1],
                    [26,0]
                ]
            }
        ]
    }
    """
    rules_json = """
    [
        ["холодно", "интенсивный"],
        ["комфортно", "умеренный"],
        ["жарко", "слабый"]
    ]
    """
    current_temp = 20  # Текущая температура в градусах Цельсия
    result = task(temp_json, heating_json, rules_json, current_temp)
    print(f"Оптимальное управление: {result:.2f}")
