# ===============================
# GAME CONFIGURATION
# ===============================

# Camera
CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FPS = 60

# Hand Tracking
MAX_HANDS = 1
DRAW_HAND_LANDMARKS = True

# ===============================
# FRUIT SETTINGS
# ===============================

FRUIT_SPEED_MIN = 6
FRUIT_SPEED_MAX = 10
FRUIT_SPAWN_Y = 0

# Fruit types. The extra fruit sprites are drawn by the game, so they do not
# need separate image files in the assets folder.
FRUIT_TYPES = [
    "cherry", "peach", "banana", "apple", "orange", "strawberry",
    "lemon", "grape", "watermelon", "kiwi", "mango", "pineapple",
    "bomb", "gift_small", "gift_large",
]

# Image size (used instead of FRUIT_RADIUS)
FRUIT_SIZE = 80          # Width & height of PNG
FRUIT_RADIUS = FRUIT_SIZE // 2  # Collision radius

# Fruit Images (PNG with transparency)
FRUIT_IMAGES = {
    "cherry": "assets/fruits/cherry.png",
    "peach": "assets/fruits/peach.png",
    "banana": "assets/fruits/banana.png",
    "bomb": "assets/fruits/bomb.png"
}

# Bomb behavior
BOMB_PENALTY = True

# ===============================
# UI COLORS (BGR)
# ===============================

COLOR_SWORD = (0, 0, 255)
COLOR_TEXT = (255, 255, 255)

# ===============================
# SCORE DISPLAY
# ===============================

FONT_SCALE = 1
FONT_THICKNESS = 2
SCORE_POSITION = (20, 40)

# ===============================
# GAME
# ===============================

ESC_KEY = 27
