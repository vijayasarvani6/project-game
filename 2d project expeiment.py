import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
TILE_SIZE = 32
MAP_ROWS = SCREEN_HEIGHT // TILE_SIZE
MAP_COLS = SCREEN_WIDTH // TILE_SIZE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cute Fantasy")

clock = pygame.time.Clock()
FPS = 60

# Colors - Pastel palette for Cute Fantasy
COLOR_SKY = (180, 215, 255)
COLOR_GRASS = (156, 234, 177)
COLOR_WATER = (135, 206, 235)
COLOR_TREE = (79, 121, 66)
COLOR_FLOWER = (255, 182, 193)
COLOR_STONE = (195, 195, 195)
COLOR_PLAYER = (255, 105, 180)  # Hot pink cute character color
COLOR_PATH = (255, 235, 205)

# Tile types
TILE_GRASS = 0
TILE_WATER = 1
TILE_TREE = 2
TILE_FLOWER = 3
TILE_STONE = 4
TILE_PATH = 5

# A cute player character class
class Player:
    def __init__(self, x, y):
        self.x = x  # in tiles
        self.y = y
        self.speed = 4  # pixels per frame
        self.pixel_x = x * TILE_SIZE
        self.pixel_y = y * TILE_SIZE

    def move(self, dx, dy, game_map):
        # Calculate new tile position
        new_x = self.pixel_x + dx * self.speed
        new_y = self.pixel_y + dy * self.speed

        # Boundaries in pixels
        max_x = SCREEN_WIDTH - TILE_SIZE
        max_y = SCREEN_HEIGHT - TILE_SIZE
        new_x = max(0, min(new_x, max_x))
        new_y = max(0, min(new_y, max_y))

        # Calculate which tile the player would be on center-bottom for collision
        center_x = new_x + TILE_SIZE//2
        center_y = new_y + TILE_SIZE - 5  # slightly above bottom of tile for feet

        tile_x = center_x // TILE_SIZE
        tile_y = center_y // TILE_SIZE

        # Check collision - can move if tile is not water or tree or stone
        if 0 <= tile_x < MAP_COLS and 0 <= tile_y < MAP_ROWS:
            tile = game_map[tile_y][tile_x]
            if tile not in (TILE_WATER, TILE_TREE, TILE_STONE):
                self.pixel_x = new_x
                self.pixel_y = new_y

    def draw(self, surface):
        # Draw a cute round player with eyes and smiling face
        center = (self.pixel_x + TILE_SIZE // 2, self.pixel_y + TILE_SIZE // 2)
        radius = TILE_SIZE // 2 - 2
        # Body
        pygame.draw.circle(surface, COLOR_PLAYER, center, radius)
        # Eyes
        eye_y_offset = -6
        eye_x_offset = 6
        eye_radius = 3
        pygame.draw.circle(surface, (255, 255, 255), (center[0] - eye_x_offset, center[1] + eye_y_offset), eye_radius)
        pygame.draw.circle(surface, (255, 255, 255), (center[0] + eye_x_offset, center[1] + eye_y_offset), eye_radius)
        pygame.draw.circle(surface, (0, 0, 0), (center[0] - eye_x_offset, center[1] + eye_y_offset), 1)
        pygame.draw.circle(surface, (0, 0, 0), (center[0] + eye_x_offset, center[1] + eye_y_offset), 1)
        # Smile
        smile_rect = pygame.Rect(0,0,10,6)
        smile_rect.center = (center[0], center[1]+5)
        pygame.draw.arc(surface, (0,0,0), smile_rect, 3.14, 0, 2)

def draw_tile(surface, tile, x, y):
    rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

    if tile == TILE_GRASS:
        pygame.draw.rect(surface, COLOR_GRASS, rect)
        # Some grass details - little lighter lines
        pygame.draw.line(surface, (170, 250, 190), (rect.left+5, rect.bottom-5), (rect.left+5, rect.top+5), 1)
        pygame.draw.line(surface, (170, 250, 190), (rect.left+10, rect.bottom-10), (rect.left+10, rect.top+10), 1)
    elif tile == TILE_WATER:
        pygame.draw.rect(surface, COLOR_WATER, rect)
        # Waves - white squiggles
        for i in range(rect.left, rect.right, 8):
            pygame.draw.arc(surface, (224, 239, 255), (i, rect.top+8, 8, 8), 3.14, 0, 1)
    elif tile == TILE_TREE:
        # brown trunk
        trunk_rect = pygame.Rect(rect.centerx - 4, rect.bottom - 12, 8, 12)
        pygame.draw.rect(surface, (120, 75, 35), trunk_rect)
        # green leaves circle on top
        pygame.draw.circle(surface, COLOR_TREE, (rect.centerx, rect.top + 12), 14)
        # Some lighter green circles for leaf details
        pygame.draw.circle(surface, (120, 160, 120), (rect.centerx - 7, rect.top + 8), 6)
        pygame.draw.circle(surface, (120, 160, 120), (rect.centerx + 7, rect.top + 8), 6)
    elif tile == TILE_FLOWER:
        pygame.draw.rect(surface, COLOR_GRASS, rect)
        # Draw cute flower: circle + petals
        center = rect.center
        pygame.draw.circle(surface, (255, 192, 203), center, 8)
        # Petals
        petal_offsets = [(-6, 0), (6, 0), (0, -6), (0, 6)]
        for ox, oy in petal_offsets:
            pygame.draw.circle(surface, (255, 105, 180), (center[0]+ox, center[1]+oy), 5)
        # Flower center
        pygame.draw.circle(surface, (255, 255, 255), center, 4)
    elif tile == TILE_STONE:
        pygame.draw.rect(surface, COLOR_STONE, rect)
        # Stones darker spots
        pygame.draw.circle(surface, (140, 140, 140), (rect.left+8, rect.top+8), 4)
        pygame.draw.circle(surface, (140, 140, 140), (rect.right-8, rect.bottom-8), 3)
    elif tile == TILE_PATH:
        pygame.draw.rect(surface, COLOR_PATH, rect)
    else:
        pygame.draw.rect(surface, COLOR_GRASS, rect)


# Define multiple maps as 2D lists of tile types
maps = []

# Map 1: Forest clearing with water pond, flowers, and trees
map1 = [
    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,3,3,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,1,1,1,1,0,3,3,0,0,0,0,2],
    [2,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,2],
    [2,0,0,0,0,3,0,0,0,0,0,0,0,0,3,0,0,0,0,2],
    [2,0,0,0,0,3,0,0,0,0,0,0,0,0,3,0,0,0,0,2],
    [2,0,3,3,0,0,0,0,0,0,0,0,0,0,0,0,3,3,0,2],
    [2,0,3,3,0,0,0,2,2,0,0,2,2,0,0,0,3,3,0,2],
    [2,0,0,0,0,0,0,2,2,0,0,2,2,0,0,0,0,0,0,2],
    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
    ]

maps.append(map1)

# Map 2: Stone path in meadow with flowers and trees
map2 = [
    [0,0,0,0,0,0,0,0,3,3,3,0,0,0,0,0,0,0,0,0],
    [0,3,3,0,0,0,2,2,2,2,2,2,0,0,0,3,3,0,0,0],
    [0,3,3,0,0,0,2,3,0,0,0,2,0,0,0,3,3,0,0,0],
    [0,0,0,0,0,0,2,3,0,0,0,2,0,0,0,0,0,0,0,0],
    [0,0,1,1,1,1,2,3,0,2,2,2,0,0,1,1,1,1,0,0],
    [0,0,1,5,5,1,2,2,0,2,3,2,0,0,1,5,5,1,0,0],
    [0,0,1,5,5,1,0,0,0,2,3,2,0,0,1,5,5,1,0,0],
    [0,0,1,1,1,1,0,0,0,2,2,2,0,0,1,1,1,1,0,0],
    [0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    ]
maps.append(map2)

# Map 3: Water lake with islands and flowers around
map3 = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,3,0,0,0,0,0,0,3,1,1,1,1,1,1],
    [1,1,1,3,3,0,0,0,2,2,2,2,2,0,0,3,3,1,1,1],
    [1,1,0,0,0,0,0,2,2,0,0,0,2,2,0,0,0,0,1,1],
    [1,1,0,0,3,0,0,2,2,0,0,0,2,2,0,3,0,0,1,1],
    [1,1,0,0,3,0,0,0,0,0,3,3,0,0,0,3,0,0,1,1],
    [1,1,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,1,0,0,3,3,0,3,0,0,3,3,0,0,0,1,1,1,1],
    [1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1],
    [1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    ]
maps.append(map3)

# Current map index
current_map = 0

# Starting player position in tiles for each map
player_start_positions = [
    (1, 8),
    (0, 9),
    (5, 5),
]

player = Player(*player_start_positions[current_map])

# Font for UI
font = pygame.font.SysFont('Comic Sans MS', 20)

def draw_map(surface, game_map):
    for y in range(len(game_map)):
        for x in range(len(game_map[0])):
            draw_tile(surface, game_map[y][x], x, y)

def draw_ui(surface):
    text = font.render(f'Cute Fantasy - Map {current_map+1} (Press 1,2,3 to switch maps)', True, (80, 80, 80))
    surface.blit(text, (10, 10))

def main():
    global current_map, player
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Switch maps with keys 1,2,3
                if event.key == pygame.K_1:
                    current_map = 0
                    player = Player(*player_start_positions[current_map])
                elif event.key == pygame.K_2:
                    current_map = 1
                    player = Player(*player_start_positions[current_map])
                elif event.key == pygame.K_3:
                    current_map = 2
                    player = Player(*player_start_positions[current_map])

        keys = pygame.key.get_pressed()
        dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]

        # Normalizing movement so diagonal speed is same
        if dx != 0 and dy != 0:
            dx *= 0.7
            dy *= 0.7

        player.move(dx, dy, maps[current_map])

        # Draw everything
        screen.fill(COLOR_SKY)
        draw_map(screen, maps[current_map])
        player.draw(screen)
        draw_ui(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

