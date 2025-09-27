import pygame, sys, random

# --- CONSTANTS ---
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 3, 3
SQSIZE = WIDTH // COLS

LINE_COLOR = (0, 0, 0)
BG_COLOR = (200, 200, 200)
CROSS_COLOR = (66, 66, 66)
CIRC_COLOR = (239, 231, 200)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe AI")
screen.fill(BG_COLOR)

# --- BOARD ---
board = [[0]*COLS for _ in range(ROWS)]

def draw_grid():
    for i in range(1, COLS):
        pygame.draw.line(screen, LINE_COLOR, (i*SQSIZE, 0), (i*SQSIZE, HEIGHT), 3)
        pygame.draw.line(screen, LINE_COLOR, (0, i*SQSIZE), (WIDTH, i*SQSIZE), 3)

def draw_figures():
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == 1:  # X
                pygame.draw.line(screen, CROSS_COLOR, (c*SQSIZE+20, r*SQSIZE+20), 
                                 (c*SQSIZE+SQSIZE-20, r*SQSIZE+SQSIZE-20), 4)
                pygame.draw.line(screen, CROSS_COLOR, (c*SQSIZE+20, r*SQSIZE+SQSIZE-20), 
                                 (c*SQSIZE+SQSIZE-20, r*SQSIZE+20), 4)
            elif board[r][c] == 2:  # O
                pygame.draw.circle(screen, CIRC_COLOR, 
                                   (c*SQSIZE+SQSIZE//2, r*SQSIZE+SQSIZE//2), SQSIZE//3, 4)

def empty_sqrs():
    return [(r,c) for r in range(ROWS) for c in range(COLS) if board[r][c] == 0]

def check_win(player):
    # Rows and Cols
    for i in range(ROWS):
        if all(board[i][j] == player for j in range(COLS)): return True
        if all(board[j][i] == player for j in range(ROWS)): return True
    # Diagonals
    if all(board[i][i] == player for i in range(ROWS)): return True
    if all(board[i][ROWS-1-i] == player for i in range(ROWS)): return True
    return False

# --- AI ---
def ai_move(level=1):
    if level == 0: return random.choice(empty_sqrs())
    best_score, best_move = -1000, None
    for (r,c) in empty_sqrs():
        board[r][c] = 2
        score = minimax(False)
        board[r][c] = 0
        if score > best_score:
            best_score, best_move = score, (r,c)
    return best_move

def minimax(maximizing):
    if check_win(2): return 1
    if check_win(1): return -1
    if not empty_sqrs(): return 0

    if maximizing:
        best = -1000
        for (r,c) in empty_sqrs():
            board[r][c] = 2
            best = max(best, minimax(False))
            board[r][c] = 0
        return best
    else:
        best = 1000
        for (r,c) in empty_sqrs():
            board[r][c] = 1
            best = min(best, minimax(True))
            board[r][c] = 0
        return best

# --- MAIN LOOP ---
player = 1
game_over = False
draw_grid()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()

        if not game_over and player == 1 and event.type == pygame.MOUSEBUTTONDOWN:
            x,y = event.pos
            row, col = y//SQSIZE, x//SQSIZE
            if board[row][col] == 0:
                board[row][col] = player
                if check_win(player): game_over = True
                player = 2

    if not game_over and player == 2:
        row, col = ai_move(level=1)  # 0=random, 1=smart
        board[row][col] = player
        if check_win(player): game_over = True
        player = 1

    screen.fill(BG_COLOR)
    draw_grid()
    draw_figures()
    pygame.display.update()
