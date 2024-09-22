from pygame import K_LEFT, K_RIGHT, K_UP, K_DOWN, K_SPACE

# Constantes
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

# Controlos do Jogador
PLAYER_KEYS: tuple[int, int, int, int, int] = (K_LEFT, K_RIGHT, K_UP, K_DOWN, K_SPACE)

# Controlos do Jogador revertidos
PLAYER_REVERSE_KEYS: tuple[int, int, int, int, int] = (
    K_RIGHT,
    K_LEFT,
    K_DOWN,
    K_UP,
    K_SPACE,
)
