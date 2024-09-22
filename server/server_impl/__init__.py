# Informação da conexão
PORT = 35000
SERVER_ADDRESS = "localhost"

# Operações de comunicação
COMMAND_SIZE = 9
INT_SIZE = 8
MAX_STR_SIZE = 20  # Número máximo de caracteres do nome do jogador
NR_CLIENTS = 2  # Número de jogadores
MAP_OP = "get map  "
MUSIC_OP = "get music"
PLAYER_OP = "player   "
START_GAME = "game     "
UPDATE_WORLD = "upd world"
GET_OBJTS = "get objts"
STEP_OP = "step     "
DIG_OP = "dig      "
END_GAME = "end game "
BYE_OP = "bye      "
STOP_SERVER_OP = "stop    "

# Registo do servidor
LOG_FILENAME = "server.log"
LOG_LEVEL = 1

# Constantes
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

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
