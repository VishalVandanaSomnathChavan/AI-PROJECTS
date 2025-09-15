import time
from collections import deque

# Maze representation
# 0 - free path
# 1 - wall/block

maze = [
    [0, 1, 0, 0, 0, 0],
    [0, 1, 0, 1, 1, 0],
    [0, 0, 0, 1, 0, 0],
    [1, 1, 1, 1, 0, 1],
    [0, 0, 0, 0, 0, 0]
]

ROWS, COLS = len(maze), len(maze[0])
start = (0, 0)
end = (4, 5)

def print_maze(path=set(), visited=set()):
    for r in range(ROWS):
        for c in range(COLS):
            if (r, c) == start:
                print('S', end=' ')
            elif (r, c) == end:
                print('E', end=' ')
            elif (r, c) in path:
                print('*', end=' ')  # path found
            elif (r, c) in visited:
                print('.', end=' ')  # visited cell
            elif maze[r][c] == 1:
                print('#', end=' ')  # wall
            else:
                print(' ', end=' ')  # free space
        print()
    print()

def neighbors(r, c):
    for nr, nc in [(r-1,c), (r+1,c), (r,c-1), (r,c+1)]:
        if 0 <= nr < ROWS and 0 <= nc < COLS and maze[nr][nc] == 0:
            yield (nr, nc)

def dfs(current, visited, path):
    if current == end:
        path.append(current)
        return True
    r, c = current
    visited.add(current)
    print_maze(path=set(path), visited=visited)
    time.sleep(0.3)

    for nxt in neighbors(r, c):
        if nxt not in visited:
            if dfs(nxt, visited, path):
                path.append(current)
                return True
    return False

def bfs():
    queue = deque([start])
    visited = set([start])
    parent = {start: None}

    while queue:
        current = queue.popleft()
        print_maze(visited=visited)
        time.sleep(0.3)

        if current == end:
            # reconstruct path
            path = []
            while current:
                path.append(current)
                current = parent[current]
            path.reverse()
            return path

        for nxt in neighbors(*current):
            if nxt not in visited:
                visited.add(nxt)
                parent[nxt] = current
                queue.append(nxt)
    return []

def menu():
    print("Maze Solver using DFS and BFS")
    print("1. Solve maze with DFS")
    print("2. Solve maze with BFS")
    print("3. Exit")

def main():
    while True:
        menu()
        choice = input("Enter choice: ")
        if choice == '1':
            visited = set()
            path = []
            print("Solving with DFS...")
            found = dfs(start, visited, path)
            if found:
                print_maze(path=set(path))
                print("Path found by DFS:")
                print(path[::-1])
            else:
                print("No path found!")
        elif choice == '2':
            print("Solving with BFS...")
            path = bfs()
            if path:
                print_maze(path=set(path))
                print("Path found by BFS:")
                print(path)
            else:
                print("No path found!")
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()


