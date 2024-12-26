import numpy as np
from collections import deque
import pandas as pd  

class TreeLayers:
    def __init__(self, adjacency_matrix):
        self.adjacency_matrix = adjacency_matrix
        self.n = len(adjacency_matrix)  # Количество узлов в дереве
        self.nodes = [chr(i + 65) for i in range(self.n)]  # Узлы: A, B, C...
        self.layers = []  # Слои наследства
        self.parents = [-1] * self.n  # Родители каждого узла (-1 если корень)

    def find_root(self):
        """Найти корень дерева (узел без родителей)"""
        for j in range(self.n):
            if all(self.adjacency_matrix[i][j] == 0 for i in range(self.n)):
                return j  # Возвращаем индекс корня
        return None

    def bfs_layers(self, root):
        """Разделение дерева на слои наследства с помощью обхода в ширину (BFS)"""
        visited = [False] * self.n  # Список посещенных узлов
        queue = deque([(root, 0)])  # Очередь для BFS, содержит кортежи (узел, уровень)
        visited[root] = True

        # Словарь для хранения узлов на каждом уровне
        layer_dict = {}

        while queue:
            node, level = queue.popleft()
            
            # Добавляем узел на соответствующий уровень
            if level not in layer_dict:
                layer_dict[level] = []
            layer_dict[level].append(node)

            # Добавляем всех детей текущего узла в очередь
            for child in range(self.n):
                if self.adjacency_matrix[node, child] == 1 and not visited[child]:
                    queue.append((child, level + 1))
                    visited[child] = True
                    self.parents[child] = node  # Устанавливаем родителя

        # Конвертируем слои в список для удобного отображения
        self.layers = [layer_dict[level] for level in sorted(layer_dict)]

    def get_node_info(self, node):
        """Получение информации о вершине"""
        idx = self.nodes.index(node)  # Индекс узла

        # 1. Предшественник
        parent = self.parents[idx]
        parent_node = self.nodes[parent] if parent != -1 else None

        # 2. Наследники
        children = [self.nodes[child] for child in range(self.n) if self.adjacency_matrix[idx, child] == 1]

        # 3. Наследники наследников (внуки)
        grandchildren = []
        for child in children:
            child_idx = self.nodes.index(child)
            grandchildren += [self.nodes[gc] for gc in range(self.n) if self.adjacency_matrix[child_idx, gc] == 1]

        # 4. Предшественник предшественника (дедушка)
        grandparent = self.parents[parent] if parent != -1 else -1
        grandparent_node = self.nodes[grandparent] if grandparent != -1 else None

        # 5. Вершины на одном уровне
        node_level = -1
        for level, layer in enumerate(self.layers):
            if idx in layer:
                node_level = level
                break

        same_level_nodes = [self.nodes[n] for n in self.layers[node_level] if n != idx] if node_level != -1 else []

        return {
            "parent": parent_node,
            "children": children,
            "grandchildren": grandchildren,
            "grandparent": grandparent_node,
            "same_level": same_level_nodes
        }

    def create_relation_table(self):
        """Создание таблицы с количеством связей по каждому параметру"""
        data = []
        columns = ["Вершина", "Родитель", "Дети", "Внуки", "Дедушка", "Соседи"]
        
        for node in self.nodes:
            info = self.get_node_info(node)
            row = [
                node,                          # Вершина
                1 if info["parent"] else 0,    # Родитель (1 или 0)
                len(info["children"]),         # Дети (количество)
                len(info["grandchildren"]),    # Внуки (количество)
                1 if info["grandparent"] else 0,  # Дедушка (1 или 0)
                len(info["same_level"])        # Соседи (количество)
            ]
            data.append(row)

        # Используем pandas для красивой таблицы
        df = pd.DataFrame(data, columns=columns)
        return df

# Пример матрицы смежности
adjacency_matrix = np.array([
    [0, 1, 0, 0, 0, 0],
    [0, 0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0]
])

# Создаем объект класса TreeLayers
tree_layers = TreeLayers(adjacency_matrix)

# Находим корень дерева
root = tree_layers.find_root()
if root is not None:
    print(f"Корень дерева: {tree_layers.nodes[root]}")

    # Разделяем дерево на слои наследства
    tree_layers.bfs_layers(root)

    # Создаем и выводим таблицу с информацией о вершинах
    relation_table = tree_layers.create_relation_table()
    print(relation_table)
else:
    print("Корень дерева не найден!")
