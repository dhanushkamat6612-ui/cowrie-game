import pygame
import random
import os
import asyncio  # This is the magic for the web!

# --- Constants ---
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 5
CELL_SIZE = 100
BOARD_ORIGIN = (50, 50)
WHITE, BLACK, GRAY, GOLD, RED = (255,255,255), (0,0,0), (200,200,200), (255,215,0), (220,20,60)

# --- The Main Game Function must be ASYNC ---
async def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Kamat Studio v2 - Web Edition")
    font = pygame.font.SysFont("Arial", 22)
    
    # --- Asset Loading ---
    def load_img(name, sz):
        if not os.path.exists(name): return None
        return pygame.transform.scale(pygame.image.load(name), sz)

    # Note: Using exact names from your GitHub screenshot
    img_hollow = load_img("Hollow.png", (60, 100))
    img_curved = load_img("Curved.png", (60, 100))
    img_logo = load_img("1000116381.png", (90, 90))

    results, score = [0, 0, 0, 0], 0
    running = True

    # --- THE GAME LOOP ---
    while running:
        screen.fill(WHITE)
        
        # 1. Draw Board
        for r in range(5):
            for c in range(5):
                rect = pygame.Rect(BOARD_ORIGIN[0]+c*100, BOARD_ORIGIN[1]+r*100, 100, 100)
                pygame.draw.rect(screen, BLACK, rect, 2)
                if r == 2 and c == 2 and img_logo:
                    screen.blit(img_logo, (rect.x + 5, rect.y + 5))

        # 2. Draw Roll Button
        btn_roll = pygame.Rect(600, 500, 150, 50)
        pygame.draw.rect(screen, GOLD, btn_roll)
        screen.blit(font.render("THROW KAUDE", True, BLACK), (615, 515))

        # 3. Draw Cowrie Results
        for i, res in enumerate(results):
            img = img_hollow if res == 1 else img_curved
            if img: screen.blit(img, (585 + (i % 2) * 85, 120 + (i // 2) * 110))

        # 4. Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_roll.collidepoint(event.pos):
                    results = [random.randint(0, 1) for _ in range(4)]
                    h = sum(results)
                    score = 8 if h == 0 else (4 if h == 4 else h)

        # 5. Update Display
        pygame.display.flip()

        # --- CRITICAL WEB LOGIC ---
        # This tells the browser: "I'm done with this frame, you can catch up now."
        await asyncio.sleep(0) 

    pygame.quit()

# This starts the async function
asyncio.run(main())
