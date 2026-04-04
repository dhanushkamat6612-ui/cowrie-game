import pygame
import random
import os

# --- 1. Basic Configuration ---
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 5
CELL_SIZE = 100
BOARD_ORIGIN = (50, 50)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GOLD = (255, 215, 0)
RED = (220, 20, 60)
GREEN = (34, 139, 34)

# --- 2. Initialize & Load Assets ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kamat Studio: Chowka Bara v2.0")
font = pygame.font.SysFont("Arial", 22)
large_font = pygame.font.SysFont("Arial", 32, bold=True)

def safe_load(filename, size):
    """Checks if file exists before loading to prevent 404/Crash."""
    if not os.path.exists(filename):
        print(f"!!! ERROR: Could not find {filename} !!!")
        return None
    img = pygame.image.load(filename)
    return pygame.transform.scale(img, size)

# Load your specific GitHub files (Case-Sensitive!)
img_hollow = safe_load("Hollow.png", (60, 100))
img_curved = safe_load("Curved.png", (60, 100))
img_logo = safe_load("1000116381.png", (CELL_SIZE-10, CELL_SIZE-10))

# --- 3. Game Logic Engine ---
class ChowkaBaraLogic:
    def __init__(self):
        self.history = []
        self.player_killed = False
        self.popup_msg = None

    def throw_kaude(self):
        # 1 = Hollow, 0 = Curved
        results = [random.randint(0, 1) for _ in range(4)]
        hollows = sum(results)
        
        # Scoring: 0 hollows = 8 (Baara), 4 hollows = 4 (Chowka)
        score = 8 if hollows == 0 else (4 if hollows == 4 else hollows)
        
        # Check Triplet Rule (4-4-4 or 8-8-8)
        self.history.append(score)
        if len(self.history) >= 3:
            if all(x == 4 for x in self.history[-3:]) or all(x == 8 for x in self.history[-3:]):
                self.popup_msg = "Triplet of 4s or 8s is invalid!\nThird throw void, turn ends."
                self.history = []
                return results, 0
        
        return results, score

# --- 4. Drawing Functions ---
def draw_ui(state, results, score):
    # Sidebar
    pygame.draw.rect(screen, GRAY, (570, 0, 230, HEIGHT))
    screen.blit(font.render("KAMAT STUDIO", True, BLACK), (590, 20))
    
    # Draw the Kaude results
    for i, res in enumerate(results):
        img = img_hollow if res == 1 else img_curved
        if img: screen.blit(img, (585 + (i % 2) * 85, 100 + (i // 2) * 110))

    # Score Display
    txt = "EXTRA THROW!" if score in [4, 8] else "Score"
    color = GREEN if score in [4, 8] else BLACK
    screen.blit(font.render(txt, True, color), (610, 360))
    screen.blit(large_font.render(str(score), True, color), (650, 390))

def draw_board():
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            rect = pygame.Rect(BOARD_ORIGIN[0]+c*CELL_SIZE, BOARD_ORIGIN[1]+r*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 2)
            # Safe Zones
            if (r, c) in [(0, 2), (2, 0), (2, 4), (4, 2)]:
                pygame.draw.line(screen, GRAY, rect.topleft, rect.bottomright, 2)
                pygame.draw.line(screen, GRAY, rect.topright, rect.bottomleft, 2)
            # Center Goal
            if r == 2 and c == 2 and img_logo:
                screen.blit(img_logo, (rect.x+5, rect.y+5))

def show_modal(msg):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    modal = pygame.Rect(150, 200, 500, 200)
    pygame.draw.rect(screen, WHITE, modal)
    pygame.draw.rect(screen, RED, modal, 5)
    
    lines = msg.split('\n')
    for i, line in enumerate(lines):
        t = font.render(line, True, BLACK)
        screen.blit(t, (modal.centerx - t.get_width()//2, modal.y + 50 + (i*30)))
    
    btn = pygame.Rect(modal.centerx-50, modal.bottom-60, 100, 40)
    pygame.draw.rect(screen, GRAY, btn)
    screen.blit(font.render("OK", True, BLACK), (btn.x+35, btn.y+10))
    return btn

# --- 5. Main Loop ---
def main():
    game = ChowkaBaraLogic()
    results, score = [0,0,0,0], 0
    running = True
    active_popup = False

    while running:
        screen.fill(WHITE)
        draw_board()
        draw_ui(game, results, score)
        
        # Roll Button
        btn_roll = pygame.Rect(600, 500, 150, 50)
        pygame.draw.rect(screen, GOLD, btn_roll)
        screen.blit(font.render("THROW KAUDE", True, BLACK), (615, 515))

        if active_popup:
            btn_ok = show_modal(game.popup_msg)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if active_popup:
                    if btn_ok.collidepoint(event.pos):
                        active_popup = False
                        game.popup_msg = None
                elif btn_roll.collidepoint(event.pos):
                    results, score = game.throw_kaude()
                    if game.popup_msg: active_popup = True

        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()
