import random

WIDTH = 15
HEIGHT = 10

WALL = "█"
PATH = " "
VISITED = "·"

def create_grid(width, height):
    return [[WALL for _ in range(width)] for _ in range(height)]

def carve_passages(x, y, grid):
    directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
    random.shuffle(directions)

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 < nx < WIDTH-1 and 0 < ny < HEIGHT-1:
            if grid[ny][nx] == WALL:
                grid[ny - dy//2][nx - dx//2] = PATH
                grid[ny][nx] = PATH
                carve_passages(nx, ny, grid)

def solve(x, y, grid, visited):
    if (x, y) == (WIDTH-2, HEIGHT-2):
        return True

    visited.add((x, y))

    for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
            if grid[ny][nx] == PATH and (nx, ny) not in visited:
                if solve(nx, ny, grid, visited):
                    grid[ny][nx] = VISITED
                    return True
    return False

def display(grid):
    for row in grid:
        print("".join(row))

def main():
    grid = create_grid(WIDTH, HEIGHT)
    grid[1][1] = PATH
    carve_passages(1, 1, grid)

    print("Labyrinthe généré :\n")
    display(grid)

    solve(1, 1, grid, set())
    grid[1][1] = "S"
    grid[HEIGHT-2][WIDTH-2] = "E"

    print("\nSolution trouvée :\n")
    display(grid)

if __name__ == "__main__":
    main()
