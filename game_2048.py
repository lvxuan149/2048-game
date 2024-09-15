import pygame
import random

# 初始化Pygame
pygame.init()

# 设置颜色
BACKGROUND_COLOR = (250, 248, 239)
GRID_COLOR = (187, 173, 160)
EMPTY_CELL_COLOR = (205, 193, 180)
TILE_COLORS = {
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}
TEXT_COLOR = (119, 110, 101)

# 设置游戏参数
GRID_SIZE = 4
CELL_SIZE = 100
GRID_PADDING = 10
WINDOW_SIZE = (GRID_SIZE * (CELL_SIZE + GRID_PADDING) + GRID_PADDING, 
               GRID_SIZE * (CELL_SIZE + GRID_PADDING) + GRID_PADDING + 100)

# 创建游戏窗口
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("2048")

# 初始化字体
font = pygame.font.Font(None, 36)

class Game2048:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4

    def move(self, direction):
        moved = False
        if direction == "up":
            for j in range(GRID_SIZE):
                column = [self.grid[i][j] for i in range(GRID_SIZE) if self.grid[i][j] != 0]
                column = self.merge(column)
                for i in range(GRID_SIZE):
                    new_value = column[i] if i < len(column) else 0
                    if self.grid[i][j] != new_value:
                        moved = True
                    self.grid[i][j] = new_value
        elif direction == "down":
            for j in range(GRID_SIZE):
                column = [self.grid[i][j] for i in range(GRID_SIZE-1, -1, -1) if self.grid[i][j] != 0]
                column = self.merge(column)
                for i in range(GRID_SIZE-1, -1, -1):
                    new_value = column[GRID_SIZE-1-i] if GRID_SIZE-1-i < len(column) else 0
                    if self.grid[i][j] != new_value:
                        moved = True
                    self.grid[i][j] = new_value
        elif direction == "left":
            for i in range(GRID_SIZE):
                row = [self.grid[i][j] for j in range(GRID_SIZE) if self.grid[i][j] != 0]
                row = self.merge(row)
                for j in range(GRID_SIZE):
                    new_value = row[j] if j < len(row) else 0
                    if self.grid[i][j] != new_value:
                        moved = True
                    self.grid[i][j] = new_value
        elif direction == "right":
            for i in range(GRID_SIZE):
                row = [self.grid[i][j] for j in range(GRID_SIZE-1, -1, -1) if self.grid[i][j] != 0]
                row = self.merge(row)
                for j in range(GRID_SIZE-1, -1, -1):
                    new_value = row[GRID_SIZE-1-j] if GRID_SIZE-1-j < len(row) else 0
                    if self.grid[i][j] != new_value:
                        moved = True
                    self.grid[i][j] = new_value
        if moved:
            self.add_new_tile()
        return moved

    def merge(self, line):
        for i in range(len(line) - 1):
            if line[i] == line[i + 1]:
                line[i] *= 2
                self.score += line[i]
                line.pop(i + 1)
                line.append(0)
        return [x for x in line if x != 0]

    def game_over(self):
        if any(0 in row for row in self.grid):
            return False
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if j < GRID_SIZE - 1 and self.grid[i][j] == self.grid[i][j + 1]:
                    return False
                if i < GRID_SIZE - 1 and self.grid[i][j] == self.grid[i + 1][j]:
                    return False
        return True

    def draw(self):
        screen.fill(BACKGROUND_COLOR)
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                x = j * (CELL_SIZE + GRID_PADDING) + GRID_PADDING
                y = i * (CELL_SIZE + GRID_PADDING) + GRID_PADDING
                pygame.draw.rect(screen, GRID_COLOR, (x, y, CELL_SIZE, CELL_SIZE))
                if self.grid[i][j] != 0:
                    pygame.draw.rect(screen, TILE_COLORS.get(self.grid[i][j], (237, 194, 46)), 
                                     (x, y, CELL_SIZE, CELL_SIZE))
                    text = font.render(str(self.grid[i][j]), True, TEXT_COLOR)
                    text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                    screen.blit(text, text_rect)

        score_text = font.render(f"Score: {self.score}", True, TEXT_COLOR)
        screen.blit(score_text, (10, WINDOW_SIZE[1] - 50))

        pygame.display.flip()

game = Game2048()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.move("up")
            elif event.key == pygame.K_DOWN:
                game.move("down")
            elif event.key == pygame.K_LEFT:
                game.move("left")
            elif event.key == pygame.K_RIGHT:
                game.move("right")

    game.draw()

    if game.game_over():
        game_over_text = font.render("Game Over!", True, TEXT_COLOR)
        screen.blit(game_over_text, (WINDOW_SIZE[0] // 2 - 70, WINDOW_SIZE[1] // 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

pygame.quit()