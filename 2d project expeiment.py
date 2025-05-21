import pygame
import sys
import random
import os

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.init()

# --- SCREEN SETUP ---
SCREEN_WIDTH, SCREEN_HEIGHT = 480, 640
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Block Climber")
clock = pygame.time.Clock()

# --- COLORS ---
GREEN = (34, 139, 34)
BROWN = (139, 69, 19)
RED = (200, 0, 0)
BLUE = (0, 102, 204)
YELLOW = (255, 215, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY = (135, 206, 235)

# --- SOUND LOADING ---
def load_sound(filename):
    if os.path.exists(filename):
        try:
            return pygame.mixer.Sound(filename)
        except pygame.error as e:
            print(f"Error loading {filename}: {e}")
    else:
        print(f"Sound file {filename} not found!")
    return None

jump_sound = load_sound('jump.wav')
coin_sound = load_sound('coin.wav')

# --- CHARACTER IMAGE LOADING ---
def load_character_image():
    if os.path.exists('character.png'):
        img = pygame.image.load('character.png').convert_alpha()
        return pygame.transform.scale(img, (40, 40))
    else:
        print("character.png not found! Using a blue box instead.")
        surf = pygame.Surface((40, 40), pygame.SRCALPHA)
        surf.fill(BLUE)
        return surf

character_img = load_character_image()

# --- PLAYER CLASS ---
class Player:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH//2-20, SCREEN_HEIGHT-100, 40, 40)
        self.image = character_img
        self.velocity_y = 0
        self.on_ground = False
        self.score = 0

    def update(self, blocks):
        keys = pygame.key.get_pressed()
        dx = 0
        if keys[pygame.K_LEFT]:
            dx = -5
        if keys[pygame.K_RIGHT]:
            dx = 5
        self.rect.x += dx
        self.velocity_y += 1  # gravity
        if self.velocity_y > 10:
            self.velocity_y = 10
        self.rect.y += self.velocity_y

        # Collision with blocks
        self.on_ground = False
        for block in blocks:
            if self.rect.colliderect(block.rect) and self.velocity_y > 0:
                self.rect.bottom = block.rect.top
                self.velocity_y = 0
                self.on_ground = True
                self.score += 1

        # Stay in bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def jump(self):
        if self.on_ground:
            self.velocity_y = -15
            if jump_sound:
                jump_sound.play()

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

# --- BLOCK CLASS ---
class Block:
    def __init__(self, x, y, w=80, h=20):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = random.choice([GREEN, RED, BLUE, YELLOW])
        self.speed = 2

    def update(self):
        self.rect.y -= self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

# --- TREE EFFECT ---
def draw_tree(x, y):
    pygame.draw.rect(screen, BROWN, (x+15, y+30, 10, 30))
    pygame.draw.circle(screen, GREEN, (x+20, y+25), 20)

# --- COIN CLASS ---
class Coin:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.collected = False

    def update(self):
        self.rect.y -= 2

    def draw(self, surface):
        if not self.collected:
            pygame.draw.circle(surface, YELLOW, self.rect.center, 10)
            pygame.draw.circle(surface, WHITE, (self.rect.centerx-3, self.rect.centery-3), 3)

# --- GAME SETUP ---
player = Player()
blocks = [Block(SCREEN_WIDTH//2-40, SCREEN_HEIGHT-60)]
coins = []
tree_positions = [(30, SCREEN_HEIGHT-100), (400, SCREEN_HEIGHT-150), (200, SCREEN_HEIGHT-220)]

font = pygame.font.SysFont("Comic Sans MS", 30, bold=True)
game_over = False

# --- MAIN LOOP ---
while True:
    clock.tick(60)
    jump_pressed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if not game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jump_pressed = True
        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                player = Player()
                blocks = [Block(SCREEN_WIDTH//2-40, SCREEN_HEIGHT-60)]
                coins = []
                game_over = False

    if not game_over:
        # Add new block
        if len(blocks) < 8 or blocks[-1].rect.y < SCREEN_HEIGHT - 120:
            new_x = random.randint(0, SCREEN_WIDTH-80)
            blocks.append(Block(new_x, SCREEN_HEIGHT+20))
            # Sometimes add a coin
            if random.random() < 0.5:
                coins.append(Coin(new_x+30, SCREEN_HEIGHT))

        # Update blocks and remove if off screen
        for block in blocks:
            block.update()
        blocks = [b for b in blocks if b.rect.bottom > 0]

        # Update coins
        for coin in coins:
            coin.update()
            if player.rect.colliderect(coin.rect) and not coin.collected:
                coin.collected = True
                player.score += 5
                if coin_sound:
                    coin_sound.play()
        coins = [c for c in coins if c.rect.bottom > 0 and not c.collected]

        # Player jump (sound only on jump, not every frame)
        if jump_pressed:
            player.jump()

        # Update player
        player.update(blocks)

        # Game over if player falls off the bottom or top
        if player.rect.top > SCREEN_HEIGHT or player.rect.bottom < 0:
            game_over = True

    # Draw everything
    screen.fill(SKY)
    for tx, ty in tree_positions:
        draw_tree(tx, ty)
    for block in blocks:
        block.draw(screen)
    for coin in coins:
        coin.draw(screen)
    player.draw(screen)

    # Score
    score_surf = font.render(f"Score: {player.score}", True, BLACK)
    screen.blit(score_surf, (10, 10))

    # Game over
    if game_over:
        go_surf = font.render("GAME OVER! Press R to restart", True, RED)
        screen.blit(go_surf, (40, SCREEN_HEIGHT//2-40))

    pygame.display.flip()
