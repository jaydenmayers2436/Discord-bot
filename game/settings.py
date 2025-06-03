"""
Game Settings and Constants
"""

# Display settings
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# Game settings
PLAYER_SPEED = 5.0
PLAYER_ROTATION_SPEED = 2.0
MOUSE_SENSITIVITY = 0.002

# Rendering settings
FOV = 60  # Field of view in degrees
RENDER_DISTANCE = 20
RAY_COUNT = SCREEN_WIDTH // 2  # Number of rays for raycasting

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)

# HUD Colors
HUD_TEXT_COLOR = WHITE
HUD_BG_COLOR = (0, 0, 0, 128)  # Semi-transparent black

# Map settings
TILE_SIZE = 64
MAP_WIDTH = 20
MAP_HEIGHT = 15

# Player settings
PLAYER_SIZE = 16
PLAYER_START_X = 3 * TILE_SIZE
PLAYER_START_Y = 3 * TILE_SIZE
PLAYER_START_HEALTH = 100
PLAYER_MAX_HEALTH = 100

# Weapon settings
BULLET_SPEED = 800
BULLET_DAMAGE = 50

# Zombie settings
ZOMBIE_SPEED = 1.5
ZOMBIE_HEALTH = 100
ZOMBIE_DAMAGE = 25

# Points system
POINTS_PER_KILL = 50
POINTS_PER_HEADSHOT = 100
POINTS_PER_REPAIR = 10

# Game states
GAME_STATE_MENU = "menu"
GAME_STATE_PLAYING = "playing"
GAME_STATE_PAUSED = "paused"
GAME_STATE_GAME_OVER = "game_over"
