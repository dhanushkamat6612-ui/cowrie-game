import pygame
import random
import time

# --- Configuration & Colors ---
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 5
CELL_SIZE = 100
BOARD_ORIGIN = (50, 50)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GOLD = (255, 215, 0)
RED = (220, 20, 60)

# --- Initialize Pygame ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kamat Studio: Chowka Bara v2.0")
font = pygame.font.SysFont("Arial", 24)
large_font = pygame.font.SysFont("Arial", 32, bold=True)

# --- Load Assets ---
try:
    img_hollow = pygame.transform.scale(pygame.image.load("Hollow.png"), (60, 100))
    img_curved = pygame.transform.scale(pygame.image.load("Curved.png"), (60, 100))
    img_logo = pygame.transform.scale(pygame.image.load("1000116381.png"), (CELL_SIZE-10, CELL_SIZE-10))
except:
    print("Error: Ensure Hollow.png, Curved.png, and 1000116381.png are in the folder.")
    pygame.quit()
    exit()

class GameState:
    def __init__(self):
        self.turn_history = []
        self.player_has_killed = False
        self.pawns_home = 0
        self.current_turn_score = 0
        self.popup_msg = None
        self.is_joda = False # Simplified for logic demonstration
        
    def throw_cowries(self):
        # 1 = Hollow (Mouth Up), 0 = Curved (Mouth Down)
        results = [random.randint(0, 1) for _ in range(4)]
        hollow_count = sum(results)
        
        # Mapping rules
        if hollow_count == 0: score = 8  # Baara
        elif hollow_count == 4: score = 4 # Chowka
        else: score = hollow_count
        
        return results, score

    def check_triplet(self, score):
        self.turn_history.append(score)
        if len(self.turn_history) >= 3:
            last_three = self.turn_history[-3:]
            if all(x == 4 for x in last_three) or all(x == 8 for x in last_three):
                self.popup_msg = "Triplet of 4s or 8s is invalid — your third throw is void."
                self.turn_history = []
                return True
        return False

def draw_board():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            rect = pygame.Rect(BOARD_ORIGIN[0] + col * CELL_SIZE, 
                               BOARD_ORIGIN[1] + row * CELL_SIZE, 
                               CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 2)
            
            # Draw Safe Zones (Crosses)
            if (row, col) in [(0, 2), (2, 0), (2, 4), (4, 2)]:
                pygame.draw.line(screen, GRAY, rect.topleft, rect.bottomright, 3)
                pygame.draw.line(screen, GRAY, rect.topright, rect.bottomleft, 3)
            
            # Draw Center Goal
            if row == 2 and col == 2:
                screen.blit(img_logo, (rect.x + 5, rect.y + 5))

def show_popup(text):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))
    
    # Modal Box
    modal_rect = pygame.Rect(WIDTH//4, HEIGHT//3, WIDTH//2, 150)
    pygame.draw.rect(screen, WHITE, modal_rect)
    pygame.draw.rect(screen, RED, modal_rect, 4)
    
    lines = text.split('\n')
    for i, line in enumerate(lines):
        txt_surf = font.render(line, True, BLACK)
        screen.blit(txt_surf, (modal_rect.centerx - txt_surf.get_width()//2, modal_rect.y + 30 + (i*30)))
    
    btn_rect = pygame.Rect(modal_rect.centerx - 40, modal_rect.bottom - 45, 80, 35)
    pygame.draw.rect(screen, GRAY, btn_rect)
    screen.blit(font.render("OK", True, BLACK), (btn_rect.x + 25, btn_rect.y + 5))
    return btn_rect

def main():
    state = GameState()
    running = True
    cowrie_results = [0, 0, 0, 0]
    current_score = 0
    show_modal = False
    
    while running:
        screen.fill(WHITE)
        draw_board()
        
        # --- UI Sidebar ---
        pygame.draw.rect(screen, GRAY, (570, 0, 230, HEIGHT))
        screen.blit(large_font, (585, 50), )
        title = font.render("KAMAT STUDIO v2", True, BLACK)
        screen.blit(title, (585, 20))
        
        # Render Cowries
        for i, res in enumerate(cowrie_results):
            img = img_hollow if res == 1 else img_curved
            screen.blit(img, (580 + (i % 2) * 80, 150 + (i // 2) * 110))
            
        score_text = large_font.render(f"SCORE: {current_score}", True, RED if current_score in [4, 8] else BLACK)
        screen.blit(score_text, (610, 400))
        
        roll_btn = pygame.Rect(600, 500, 150, 50)
        pygame.draw.rect(screen, GOLD, roll_btn)
        screen.blit(font.render("THROW KAUDE", True, BLACK), (605, 510))

        if show_modal:
            ok_btn = show_popup(state.popup_msg)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if show_modal:
                    if ok_btn.collidepoint(event.pos):
                        show_modal = False
                        state.popup_msg = None
                elif roll_btn.collidepoint(event.pos):
                    # Simulate Roll
                    cowrie_results, current_score = state.throw_cowries()
                    
                    # 1. Check Triplet Rule
                    if state.check_triplet(current_score):
                        show_modal = True
                        current_score = 0
                    
                    # 2. Example: Inner Ring Restriction (Demo trigger)
                    elif not state.player_has_killed and random.random() < 0.1: # 10% chance to trigger for demo
                        state.popup_msg = "You must capture an opponent pawn\nbefore entering the inner ring."
                        show_modal = True
                        
                    # 3. Example: Joda Rule (Demo trigger)
                    elif current_score % 2 != 0 and random.random() < 0.1:
                        state.popup_msg = "Joda can move only on even rolls."
                        show_modal = True

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
