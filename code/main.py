import pygame
import random
import heapq

# Константы
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
CELL_SIZE = WIDTH // GRID_SIZE

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Pathfinding")
clock = pygame.time.Clock()

# Функция для генерации лабиринта
def generate_maze(grid_size):
    maze = [[1 if random.random() < 0.3 else 0 for _ in range(grid_size)] for _ in range(grid_size)]
    maze[0][0] = maze[grid_size - 1][grid_size - 1] = 0  # Гарантируем начало и конец
    return maze

# Визуализация лабиринта
def draw_maze(maze, start=None, goal=None, path=None, open_set=None, closed_set=None):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            # Цвет клетки
            color = WHITE if maze[row][col] == 0 else BLACK
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, GRAY, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

    # Отрисовка начальной и конечной точки
    if start:
        pygame.draw.rect(screen, GREEN, (start[1] * CELL_SIZE, start[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))  # start[0] - row, start[1] - col
    if goal:
        pygame.draw.rect(screen, RED, (goal[1] * CELL_SIZE, goal[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))  # goal[0] - row, goal[1] - col

    # Отрисовка открытых и закрытых узлов
    if open_set:
        for row, col in open_set:
            pygame.draw.rect(screen, GREEN, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    if closed_set:
        for row, col in closed_set:
            pygame.draw.rect(screen, RED, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Отрисовка пути
    if path:
        for row, col in path:
            pygame.draw.rect(screen, YELLOW, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    pygame.display.flip()

# Алгоритм A*
def a_star(maze, start, goal):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Манхэттенская эвристика

    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    open_set_hash = {start}
    closed_set = set()

    while open_set:
        current = heapq.heappop(open_set)[1]
        open_set_hash.remove(current)

        if current == goal:
            path = []
            node_info = []  # Список для хранения значений h(n), g(n), f(n) для узлов на пути
            while current in came_from:
                path.append(current)
                node_info.append((current, heuristic(current, goal), g_score[current], f_score[current]))
                current = came_from[current]
            path.append(start)
            node_info.append((start, heuristic(start, goal), g_score[start], f_score[start]))
            path.reverse()
            node_info.reverse()

            # Вывод значений h(n), g(n), f(n) для узлов на пути
            print("\nИнформация о пройденных узлах на пути:")
            for idx, (node, h, g, f) in enumerate(node_info):
                print(f"Узел {node}: h(n) = {h}, g(n) = {g}, f(n) = {f}")
                # Выводим узлы каждые 5 шагов или начальный и конечный узлы
                #if idx % 5 == 0 or idx == len(node_info) - 1:
                #    print(f"*** Узел {node}: h(n) = {h}, g(n) = {g}, f(n) = {f} ***")

            print(f"\nДлина кратчайшего пути: {len(path)}")
            return path, closed_set

        closed_set.add(current)

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE and maze[neighbor[0]][neighbor[1]] == 0:
                if neighbor in closed_set:
                    continue

                tentative_g_score = g_score[current] + 1

                if neighbor not in open_set_hash or tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    if neighbor not in open_set_hash:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
                        open_set_hash.add(neighbor)

        draw_maze(maze, None, None, None, open_set_hash, closed_set)
        clock.tick(10)

    return None, closed_set

# Главная программа
def main():
    maze = generate_maze(GRID_SIZE)
    start = (0, 0)
    goal = (GRID_SIZE - 1, GRID_SIZE - 1)
    path = None  # Путь, который будет отображаться

    running = True
    while running:
        screen.fill(WHITE)
        draw_maze(maze, start, goal, path)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Ввод начальной и конечной точки
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col, row = x // CELL_SIZE, y // CELL_SIZE  # Вычисляем индексы клетки

                print(f"Mouse position: ({x}, {y}), Cell: ({col}, {row})")  # Отладочный вывод

                if event.button == 1:  # Левая кнопка для установки начальной точки
                    start = (row, col)  # Начальная точка
                elif event.button == 3:  # Правая кнопка для установки конечной точки
                    goal = (row, col)  # Конечная точка
                elif event.button == 2:  # Средняя кнопка для переключения стен
                    maze[row][col] = 1 - maze[row][col]  # Переключаем стену
                    print(
                        f"Cell ({row}, {col}) changed to {'wall' if maze[row][col] == 1 else 'empty'}")  # Проверка обновления

            # Запуск A* при нажатии Enter
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                path, closed_set = a_star(maze, start, goal)
                draw_maze(maze, start, goal, path, None, closed_set)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
