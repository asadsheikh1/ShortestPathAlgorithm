from queue import PriorityQueue
from Spot import *


class ShortestPathAlgorithm:
    def __init__(self):
        self.width = 800
        self.window = pygame.display.set_mode((self.width, self.width))
        pygame.display.set_caption('Shortest Path Algorithm')

    @staticmethod
    def h(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return abs(x1 - x2) + abs(y1 - y2)

    @staticmethod
    def reconstruct_path(came_from, current, draw):
        while current in came_from:
            current = came_from[current]
            current.make_path()
            draw()

    @staticmethod
    def algorithm(draw, grid, start, end):
        count = 0
        open_set = PriorityQueue()
        open_set.put((0, count, start))
        came_from = {}
        g_score = {spot: float('inf') for row in grid for spot in row}
        g_score[start] = 0
        f_score = {spot: float('inf') for row in grid for spot in row}
        f_score[start] = ShortestPathAlgorithm.h(start.get_pos(), end.get_pos())

        open_set_hash = {start}

        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            current = open_set.get()[2]
            open_set_hash.remove(current)

            if current == end:
                ShortestPathAlgorithm.reconstruct_path(came_from, end, draw)
                end.make_end()
                return True

            for neighbor in current.neighbors:
                temp_g_score = g_score[current] + 1

                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + ShortestPathAlgorithm.h(neighbor.get_pos(), end.get_pos())
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        neighbor.make_open()
            draw()
            if current != start:
                current.make_closed()

        return False

    @staticmethod
    def make_grid(rows, width):
        grid = []
        gap = width // rows
        for i in range(rows):
            grid.append([])
            for j in range(rows):
                spot = Spot(i, j, gap, rows)
                grid[i].append(spot)
        return grid

    @staticmethod
    def grid_lines(win, rows, width):
        gap = width // rows
        for i in range(rows):
            pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
            for j in range(rows):
                pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

    @staticmethod
    def draw(win, grid, rows, width):

        for row in grid:
            for spot in row:
                spot.draw(win)

        ShortestPathAlgorithm.grid_lines(win, rows, width)
        pygame.display.update()

    @staticmethod
    def get_clicked_pos(pos, rows, width):
        gap = width // rows
        y, x = pos

        row = y // gap
        col = x // gap

        return row, col


shortest_path_algorithm = ShortestPathAlgorithm()
inside_gap = 30
grid = ShortestPathAlgorithm.make_grid(inside_gap, shortest_path_algorithm.width)

start = None
end = None

run = True
while run:
    shortest_path_algorithm.draw(shortest_path_algorithm.window, grid, inside_gap, shortest_path_algorithm.width)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if pygame.mouse.get_pressed()[0]:  # LEFT
            pos = pygame.mouse.get_pos()
            row, col = shortest_path_algorithm.get_clicked_pos(pos, inside_gap, shortest_path_algorithm.width)
            spot = grid[row][col]
            if not start and spot != end:
                start = spot
                start.make_start()

            elif not end and spot != start:
                end = spot
                end.make_end()

            elif spot != end and spot != start:
                spot.make_barrier()

        elif pygame.mouse.get_pressed()[2]:  # RIGHT
            pos = pygame.mouse.get_pos()
            row, col = shortest_path_algorithm.get_clicked_pos(pos, inside_gap, shortest_path_algorithm.width)
            spot = grid[row][col]
            spot.reset()
            if spot == start:
                start = None
            elif spot == end:
                end = None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and start and end:
                for row in grid:
                    for spot in row:
                        spot.update_neighbors(grid)

                shortest_path_algorithm.algorithm(
                    lambda: shortest_path_algorithm.draw(
                        shortest_path_algorithm.window,
                        grid,
                        inside_gap,
                        shortest_path_algorithm.width
                    ), grid, start, end)

            if event.key == pygame.K_c:
                start = None
                end = None
                grid = shortest_path_algorithm.make_grid(inside_gap, shortest_path_algorithm.width)

pygame.quit()