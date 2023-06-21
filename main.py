import pygame
import random

# Game constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
BLOCK_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE
FONT_SIZE = 36
FONT_COLOR = (255, 255, 255)
FPS = 60
TITLE_FONT_SIZE = 48
TEXT_FONT_SIZE = 24

# Colors 
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

TETROMINOS = [
    [[1, 1, 1],
     [0, 1, 0]],
    [[0, 2, 2],
     [2, 2, 0]],
    [[3, 3, 0],
     [0, 3, 3]],
    [[4, 0, 0],
     [4, 4, 4]],
    [[0, 0, 5],
     [5, 5, 5]],
    [[6, 6],
     [6, 6]],
    [[7, 7, 7, 7]]
]
TETROMINO_COLORS = [
    (200, 200, 200),  # Light gray
    (150, 150, 150),  # Gray
    (100, 100, 100),  # Dark gray
    (200, 150, 150),  # Pinkish gray
    (150, 200, 150),  # Greenish gray
    (150, 150, 200),  # Bluish gray
    (200, 200, 150)   # Yellowish gray
]

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, FONT_SIZE)

# Initialize game variables
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
score = 0
game_over = False

# Helper functions
def draw_block(x, y, color):
    pygame.draw.rect(screen, color, [x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE], 0)
    pygame.draw.rect(screen, (255, 255, 255), [x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE], 1)

def draw_grid():
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, (128, 128, 128), rect, 1)

def draw_text(text, x, y):
    surface = font.render(text, True, FONT_COLOR)
    rect = surface.get_rect()
    rect.center = (x, y)
    screen.blit(surface, rect)

def get_random_tetromino():
    tetromino = random.choice(TETROMINOS)
    color = random.choice(TETROMINO_COLORS)
    return tetromino, color

def draw_tetromino(x, y, tetromino, color):
    for row in range(len(tetromino)):
        for col in range(len(tetromino[row])):
            if tetromino[row][col]:
                draw_block(x + col, y + row, color)

def rotate_tetromino(tetromino):
    return [[tetromino[row][col] for row in range(len(tetromino) - 1, -1, -1)] for col in range(len(tetromino[0]))]

def check_collision(x, y, tetromino):
    for row in range(len(tetromino)):
        for col in range(len(tetromino[row])):
            if tetromino[row][col] and (x + col < 0 or x + col >= GRID_WIDTH or y + row >= GRID_HEIGHT or grid[y + row][x + col]):
                return True
    return False

def merge_tetromino(x, y, tetromino, color):
    for row in range(len(tetromino)):
        for col in range(len(tetromino[row])):
            if tetromino[row][col]:
                grid[y + row][x + col] = TETROMINO_COLORS.index(color) + 1

def rotate_block(block):
    rotated_block = []
    for c in range(len(block[0])):
        rotated_row = []
        for r in range(len(block) - 1, -1, -1):
            rotated_row.append(block[r][c])
        rotated_block.append(rotated_row)
    return rotated_block

def remove_complete_rows():
    global score
    row_index = GRID_HEIGHT - 1
    num_complete_rows = 0
    while row_index >= 0:
        if all(grid[row_index]):
            grid.pop(row_index)
            grid.insert(0, [0 for _ in range(GRID_WIDTH)])
            num_complete_rows += 1
            score += 100 * num_complete_rows
        else:
            row_index -= 1

def draw_title_screen():
    title_font = pygame.font.Font(None, TITLE_FONT_SIZE)
    text_font = pygame.font.Font(None, TEXT_FONT_SIZE)
    title_text = title_font.render("Pygame Tetris", True, WHITE)
    start_text = text_font.render("Press SPACE to start", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH/2 - title_text.get_width()/2, SCREEN_HEIGHT/4))
    screen.blit(start_text, (SCREEN_WIDTH/2 - start_text.get_width()/2, SCREEN_HEIGHT/2))

# Main game loop
tetromino, color = get_random_tetromino()
tetromino_x = GRID_WIDTH // 2 - len(tetromino[0]) // 2
tetromino_y = 0
move_delay = 0


draw_title_screen()
pygame.display.update()
start = False

# Wait for user to start game
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            start = True
            break
    if start:
            break

while not game_over:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if not check_collision(tetromino_x - 1, tetromino_y, tetromino):
                    tetromino_x -= 1
            elif event.key == pygame.K_RIGHT:
                if not check_collision(tetromino_x+ 1, tetromino_y, tetromino):
                    tetromino_x += 1
            elif event.key == pygame.K_UP:
                rotated_tetromino = rotate_tetromino(tetromino)
                if not check_collision(tetromino_x, tetromino_y, rotated_tetromino):
                    tetromino = rotated_tetromino
            elif event.key == pygame.K_DOWN:
                move_delay = 0

    # Move tetromino down
    move_delay += 1
    if move_delay >= FPS // 2:
        move_delay = 0
        if not check_collision(tetromino_x, tetromino_y + 1, tetromino):
            tetromino_y += 1
        else:
            merge_tetromino(tetromino_x, tetromino_y, tetromino, color)
            remove_complete_rows()
            tetromino, color = get_random_tetromino()
            tetromino_x = GRID_WIDTH // 2 - len(tetromino[0]) // 2
            tetromino_y = 0
            if check_collision(tetromino_x, tetromino_y, tetromino):
                game_over = True
    
    # Draw game elements
    screen.fill((0, 0, 0))
    draw_grid()
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            if grid[row][col]:
                draw_block(col, row, TETROMINO_COLORS[grid[row][col] - 1])
    draw_tetromino(tetromino_x, tetromino_y, tetromino, color)
    draw_text("Score: {}".format(score), SCREEN_WIDTH // 2, FONT_SIZE // 2)
    pygame.display.update()

    # Limit FPS
    clock.tick(FPS)

# Game over screen
screen.fill((0, 0, 0))
draw_text("GAME OVER!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - FONT_SIZE)
draw_text("Final score: {}".format(score), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + FONT_SIZE)
pygame.display.update()

# Wait for player to close window
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()