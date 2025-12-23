# Импорт библиотек
import os

# Директория изображений
IMAGE_DIR = './images'

# Путь для дефолтной карты которая будет у всех чтобы скрывать карту
DEFAULT_CARD_PATH = os.path.join(IMAGE_DIR, "card_default.png")

# Все файлы карт
CARD_FILES = [f for f in os.listdir(IMAGE_DIR) if f.endswith('.webp')]

# Все названия карт
CARDS = [f.replace('.webp', '') for f in CARD_FILES]

# Активные комнаты
ACTIVE_ROOMS = {}

# Отношение пользователь-комната
USER_ROOMS = {}

# Игроки
PLAYERS = {}

# Режимы игры
GAME_MODES = {
    "spy_one": "Один шпион",
    "spy_one1": "Один шпион",
    "spy_one2": "Один шпион",
    "spy_one3": "Один шпион",
    "spy_one4": "Один шпион",
    "spy_one5": "Один шпион",
    "all_spies": "Все — шпионы",
    "one_innocent": "Один невиновный",
    "all_unique": "У всех разные карты",
    "no_spies": "Никто не шпион"
}

# Максимально колво игроков
MAX_PLAYERS = 8

# Минимальное колво игроков
MIN_PLAYERS = 3

