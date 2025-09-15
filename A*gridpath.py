import heapq
import time

ROWS, COLS = 6, 6

def print_grid(grid, open_set=set(), closed_set=set(), path=set(), start=None, end=None, step=None):
    print(f"Step {step}" if step is not None else "")
    horizontal_border = '+' + ('---+' * COLS)
    print(horizontal_border)
    for r in range(ROWS):
        row_str = '|'
        for c in range(COLS):
            pos = (r, c)
            if pos == start:
                cell = ' S '
            elif pos == end:
                cell = ' E '
            elif pos in path:
                cell = ' * '
            elif pos in closed_set:
                cell = ' . '
            elif pos in open_set:
                cell = ' o '
            elif grid[r][c] == 1:
                cell = ' # '
            else:
                cell = '   '
            row_str += cell + '|'
        print(row_str)
        print(horizontal_border)
    print()  # empty line

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def neighbors(pos):
    r, c = pos
    for nr, nc in [(r-1,c), (r+1,c), (r,c-1), (r,c+1)]:
        if 0 <= nr < ROWS and 0 <= nc < COLS:
            yield (nr, nc)

def a_star(grid, start, end):
    open_heap = []
    heapq.heappush(open_heap, (0 + heuristic(start, end), 0, start))

    came_from = {}
    g_score = {start: 0}

    open_set = {start}
    closed_set = set()

    step_count = 0
    print_grid(grid, open_set, closed_set, set(), start, end, step=step_count)
    time.sleep(1)

    while open_heap:
        f, g, current = heapq.heappop(open_heap)
        open_set.discard(current)
        closed_set.add(current)

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            print_grid(grid, open_set, closed_set, set(path), start, end, step=step_count)
            return path

        for neighbor in neighbors(current):
            if grid[neighbor[0]][neighbor[1]] == 1 or neighbor in closed_set:
                continue

            tentative_g = g + 1

            if tentative_g < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor, end)
                if neighbor not in open_set:
                    heapq.heappush(open_heap, (f_score, tentative_g, neighbor))
                    open_set.add(neighbor)

        step_count += 1
        print_grid(grid, open_set, closed_set, set(), start, end, step=step_count)
        time.sleep(0.3)

    print("No path found!")
    return []

def create_grid():
    grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    print(f"Enter obstacle positions as 'row col' (0-indexed, max {ROWS-1} {COLS-1}). Enter empty line to finish:")
    while True:
        line = input()
        if not line.strip():
            break
        try:
            r, c = map(int, line.strip().split())
            if 0 <= r < ROWS and 0 <= c < COLS:
                grid[r][c] = 1
            else:
                print("Position out of bounds.")
        except:
            print("Invalid input format.")
    return grid

def main():
    print(f"Grid size is {ROWS} rows x {COLS} cols")
    grid = create_grid()

    while True:
        try:
            start = tuple(map(int, input("Enter start position (row col): ").split()))
            end = tuple(map(int, input("Enter end position (row col): ").split()))
            if not (0 <= start[0] < ROWS and 0 <= start[1] < COLS and
                    0 <= end[0] < ROWS and 0 <= end[1] < COLS):
                print("Positions out of bounds. Try again.")
                continue
            if grid[start[0]][start[1]] == 1 or grid[end[0]][end[1]] == 1:
                print("Start or end is blocked by an obstacle. Try again.")
                continue
            break
        except:
            print("Invalid input format. Try again.")

    path = a_star(grid, start, end)
    if path:
        print("Final path:")
        print(path)
    else:
        print("Could not find a path.")

if __name__ == "__main__":
    main()

