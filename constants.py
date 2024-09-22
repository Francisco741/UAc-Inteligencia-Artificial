from pygame import K_LEFT, K_RIGHT, K_UP, K_DOWN, K_SPACE, K_a, K_d, K_w, K_s, K_TAB

# Constantes
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
SQUARE_SIZE = 50

# Constantes não utilizadas
MAX_STR_SIZE = 20  # Número máximo de caracteres do nome do jogador
NR_CLIENTS = 2  # Número de jogadores

# Controlos do Jogador
PLAYER_KEYS: dict[int, tuple[int, int, int, int, int]] = {
    0: (K_LEFT, K_RIGHT, K_UP, K_DOWN, K_SPACE),
    1: (K_a, K_d, K_w, K_s, K_TAB),
    # 2: (pg.K_j, pg.K_l, pg.K_i, pg.K_k, pg.K_SPACE),
    # 3: (pg.K_KP4, pg.K_KP6, pg.K_KP8, pg.K_KP5, pg.K_KP_ENTER),
}

# Controlos do Jogador revertidos
PLAYER_REVERSE_KEYS: dict[int, tuple[int, int, int, int, int]] = {
    0: (K_RIGHT, K_LEFT, K_DOWN, K_UP, K_SPACE),
    1: (K_d, K_a, K_s, K_w, K_TAB),
    # 2: (pg.K_l, pg.K_j, pg.K_k, pg.K_i, pg.K_SPACE),
    # 3: (pg.K_KP6, pg.K_KP4, pg.K_KP5, pg.K_KP8, pg.K_KP_ENTER),
}

# Mapas do Jogo
"""
Mapa é uma matriz 18x12
24 pedaços de terra escaváveis no total

ID de cada Objeto presente no mapa:
0: Dirt
1: Wall
2: Grass
3: DirtHole
4: Obstacle
5: Tent
6: Water
"""

MAP_1: list[list[int]] = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [2, 0, 0, 0, 3, 0, 3, 3, 0, 0, 3, 3, 0, 0, 0, 3, 4, 2],
    [2, 0, 0, 0, 0, 0, 0, 4, 0, 0, 4, 0, 0, 2, 0, 0, 3, 2],
    [2, 0, 4, 5, 1, 0, 0, 0, 0, 0, 0, 0, 3, 2, 2, 0, 0, 2],
    [2, 0, 0, 1, 1, 0, 0, 4, 0, 3, 4, 0, 0, 4, 2, 2, 0, 2],
    [2, 3, 0, 0, 0, 0, 0, 3, 6, 6, 0, 0, 0, 0, 3, 0, 0, 2],
    [2, 0, 0, 3, 0, 0, 0, 0, 6, 6, 3, 0, 0, 0, 0, 0, 3, 2],
    [2, 0, 2, 2, 4, 0, 0, 4, 3, 0, 4, 0, 0, 5, 1, 0, 0, 2],
    [2, 0, 0, 2, 2, 3, 0, 0, 0, 0, 0, 0, 0, 1, 1, 4, 0, 2],
    [2, 3, 0, 0, 2, 0, 0, 4, 0, 0, 4, 0, 0, 0, 0, 0, 0, 2],
    [2, 4, 3, 0, 0, 0, 3, 3, 0, 0, 3, 3, 0, 3, 0, 0, 0, 2],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

MAP_1_ITEMS: dict[str, int] = {
    "bones": 10,
    "diamonds": 1,
    "skulls": 1,
    "potions": 1,
    "fishes": 1,
    "coins": 1,
    "chalices": 1,
    "crowns": 1,
}

MAP_2: list[list[int]] = [
    [1, 1, 1, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 1, 1, 1],
    [2, 0, 0, 3, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 3, 0, 4, 2],
    [2, 0, 4, 0, 3, 6, 6, 6, 6, 6, 6, 6, 6, 3, 0, 0, 3, 2],
    [2, 0, 0, 0, 0, 3, 6, 6, 6, 6, 6, 6, 3, 0, 0, 0, 0, 2],
    [2, 3, 0, 0, 0, 0, 4, 6, 6, 6, 6, 4, 0, 0, 3, 0, 3, 2],
    [2, 0, 5, 1, 4, 0, 0, 3, 0, 0, 0, 0, 0, 3, 5, 1, 4, 2],
    [2, 4, 1, 1, 3, 0, 0, 0, 0, 0, 3, 0, 0, 4, 1, 1, 0, 2],
    [2, 3, 0, 3, 0, 0, 4, 6, 6, 6, 6, 4, 0, 0, 0, 0, 3, 2],
    [2, 0, 0, 0, 0, 3, 6, 6, 6, 6, 6, 6, 3, 0, 0, 0, 0, 2],
    [2, 3, 0, 0, 3, 6, 6, 6, 6, 6, 6, 6, 6, 3, 0, 4, 0, 2],
    [2, 4, 0, 3, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 3, 0, 0, 2],
    [1, 1, 1, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 1, 1, 1],
]

MAP_2_ITEMS: dict[str, int] = {
    "bones": 8,
    "diamonds": 1,
    "skulls": 1,
    "potions": 1,
    "fishes": 4,
    "coins": 1,
    "chalices": 1,
    "crowns": 1,
}

MAP_3: list[list[int]] = [
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 0, 0, 0, 0, 4, 3, 0, 0, 0, 0, 4, 3, 6, 6, 6, 6, 2],
    [2, 0, 5, 1, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 6, 6, 6, 2],
    [2, 0, 1, 1, 0, 3, 2, 0, 0, 0, 0, 2, 3, 0, 0, 6, 6, 2],
    [2, 0, 0, 0, 3, 2, 0, 0, 6, 6, 0, 0, 2, 3, 0, 3, 6, 2],
    [2, 0, 3, 0, 4, 3, 0, 6, 6, 6, 6, 0, 0, 0, 0, 4, 3, 2],
    [2, 3, 4, 0, 0, 0, 0, 6, 6, 6, 6, 0, 3, 4, 0, 3, 0, 2],
    [2, 6, 3, 0, 3, 2, 0, 0, 6, 6, 0, 0, 2, 3, 0, 0, 0, 2],
    [2, 6, 6, 0, 0, 3, 2, 0, 0, 0, 0, 2, 3, 0, 5, 1, 0, 2],
    [2, 6, 6, 6, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 1, 1, 0, 2],
    [2, 6, 6, 6, 6, 3, 4, 0, 0, 0, 0, 3, 4, 0, 0, 0, 0, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
]

MAP_3_ITEMS: dict[str, int] = {
    "bones": 10,
    "diamonds": 1,
    "skulls": 1,
    "potions": 1,
    "fishes": 1,
    "coins": 2,
    "chalices": 2,
    "crowns": 2,
}
