import pygame
import pygame_menu
from game import Game
from gamemech import GameMech
from constants import (
    SQUARE_SIZE,
    MAP_1,
    MAP_1_ITEMS,
    MAP_2,
    MAP_2_ITEMS,
    MAP_3,
    MAP_3_ITEMS,
)
from random import randint


COLOR_BACKGROUND = (31, 31, 31)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
FPS = 60.0
MENU_BACKGROUND_COLOR = (56, 136, 48)
MENU_TITLE_COLOR = (255, 255, 255)
WINDOW_SCALE = 0.9

pygame.display.init()
INFO = pygame.display.Info()
TILE_SIZE = int(INFO.current_h * 0.07)
WINDOW_SIZE = (15 * TILE_SIZE, 11 * TILE_SIZE)

# Tipo do jogador 1
p1_type = "Jogador"
# Tipo do jogador 2
p2_type = "Jogador"
# Dificuldade da AI
ai_difficulty = 5
# Número do Mapa
map_number = 0
surface = pygame.display.set_mode(WINDOW_SIZE)


def change_player1(value, c):
    global p1_type
    p1_type = c


def change_player2(value, c):
    global p2_type
    p2_type = c


def change_ai_speed(value, c):
    global ai_difficulty
    ai_difficulty = c


def change_map(value, c):
    global map_number
    map_number = c


def run_game():
    """Função que executa o jogo"""
    # Mapa do jogo
    game_map: list[list[int]] = []
    # Itens existentes no mapa do jogo
    game_map_items: dict[str, int] = {}

    global map_number

    # Entre os 3 mapas existentes, um será aleatóriamente escolhido
    if map_number == 0:
        mapa: int = randint(1, 3)
        if mapa == 1:
            game_map = MAP_1
            game_map_items = MAP_1_ITEMS
        elif mapa == 2:
            game_map = MAP_2
            game_map_items = MAP_2_ITEMS
        elif mapa == 3:
            game_map = MAP_3
            game_map_items = MAP_3_ITEMS
    elif map_number == 1:
        game_map = MAP_1
        game_map_items = MAP_1_ITEMS
        mapa = 1
    elif map_number == 2:
        game_map = MAP_2
        game_map_items = MAP_2_ITEMS
        mapa = 2
    elif map_number == 3:
        game_map = MAP_3
        game_map_items = MAP_3_ITEMS
        mapa = 3
    # Classe com todas as mecânicas do jogo
    gm = GameMech(game_map, game_map_items, mapa)
    # Classe com o jogo
    game = Game(gm, SQUARE_SIZE, p1_type, p2_type, ai_difficulty)
    # Executa o jogo
    game.run()


def main_background():
    global surface
    surface.fill(COLOR_BACKGROUND)


def main():
    pygame.init()
    pygame.display.set_caption("OssoSaurus: Desenterrando o Passado")
    clock = pygame.time.Clock()
    pygame.mixer_music.load("Music/main_song1.mp3")
    pygame.mixer_music.set_volume(0.4)
    pygame.mixer_music.play(-1)

    menu_theme = pygame_menu.Theme(
        selection_color=COLOR_WHITE,
        widget_font=pygame_menu.font.FONT_BEBAS,
        title_font_size=TILE_SIZE,
        title_font_color=COLOR_BLACK,
        title_font=pygame_menu.font.FONT_BEBAS,
        widget_font_color=COLOR_BLACK,
        widget_font_size=int(TILE_SIZE * 0.7),
        background_color=MENU_BACKGROUND_COLOR,
        title_background_color=MENU_TITLE_COLOR,
    )

    play_menu = pygame_menu.Menu(
        theme=menu_theme,
        height=int(WINDOW_SIZE[1] * WINDOW_SCALE),
        width=int(WINDOW_SIZE[0] * WINDOW_SCALE),
        title="Jogar",
    )

    play_options = pygame_menu.Menu(
        theme=menu_theme,
        height=int(WINDOW_SIZE[1] * WINDOW_SCALE),
        width=int(WINDOW_SIZE[0] * WINDOW_SCALE),
        title="Opcoes",
    )
    play_options.add.selector(
        "Jogador  1",
        [
            ("Jogador", "Jogador"),
            ("A*  Tipo 1", "A*  Tipo 1"),
            ("A*  Tipo 2", "A*  Tipo 2"),
        ],
        onchange=change_player1,
    )
    play_options.add.selector(
        "Jogador  2",
        [
            ("Jogador", "Jogador"),
            ("A*  Tipo 1", "A*  Tipo 1"),
            ("A*  Tipo 2", "A*  Tipo 2"),
        ],
        onchange=change_player2,
    )
    play_options.add.selector(
        "Dificuldade  AI",
        [
            ("Facil", 5),
            ("Medio", 3),
            ("Dificil", 2),
            ("Impossivel", 1),
        ],
        onchange=change_ai_speed,
    )
    play_options.add.selector(
        "Mapa",
        [
            ("Aleatorio", 0),
            ("Mapa  1", 1),
            ("Mapa  2", 2),
            ("Mapa  3", 3),
        ],
        onchange=change_map,
    )
    play_options.add.button("Voltar", pygame_menu.events.BACK)

    play_menu.add.button("Jogar", run_game)
    play_menu.add.button("Opcoes", play_options)
    play_menu.add.button("Voltar", pygame_menu.events.BACK)

    about_menu_theme = pygame_menu.themes.Theme(
        selection_color=COLOR_WHITE,
        widget_font=pygame_menu.font.FONT_BEBAS,
        title_font_size=TILE_SIZE,
        title_font_color=COLOR_BLACK,
        title_font=pygame_menu.font.FONT_BEBAS,
        widget_font_color=COLOR_BLACK,
        widget_font_size=int(TILE_SIZE * 0.5),
        background_color=MENU_BACKGROUND_COLOR,
        title_background_color=MENU_TITLE_COLOR,
    )
    about_menu = pygame_menu.Menu(
        theme=about_menu_theme,
        height=int(WINDOW_SIZE[1] * WINDOW_SCALE),
        width=int(WINDOW_SIZE[0] * WINDOW_SCALE),
        overflow=False,
        title="Controlos",
    )
    about_menu.add.label("Jogador  1  :")
    about_menu.add.label("Movimentar :  WASD")
    about_menu.add.label("Escavar :  Barra  de  Espaco")
    about_menu.add.vertical_margin(10)
    about_menu.add.label("Jogador  2  :")
    about_menu.add.label("Movimentar :  Setas")
    about_menu.add.label("Escavar :  Enter  Numpad")
    about_menu.add.vertical_margin(25)
    about_menu.add.button("Voltar", pygame_menu.events.BACK)

    about_menu_team = pygame_menu.Menu(
        theme=about_menu_theme,
        height=int(WINDOW_SIZE[1] * WINDOW_SCALE),
        width=int(WINDOW_SIZE[0] * WINDOW_SCALE),
        overflow=False,
        title="Sobre",
    )
    about_menu_team.add.label("Criadores :")
    about_menu_team.add.vertical_margin(5)
    about_menu_team.add.label("Francisco  Arruda")
    about_menu_team.add.label("Joao  Machado")
    about_menu_team.add.label("Miguel  Pacheco")
    about_menu_team.add.vertical_margin(25)
    about_menu_team.add.button("Voltar", pygame_menu.events.BACK)

    main_menu = pygame_menu.Menu(
        theme=menu_theme,
        height=int(WINDOW_SIZE[1] * WINDOW_SCALE),
        width=int(WINDOW_SIZE[0] * WINDOW_SCALE),
        onclose=pygame_menu.events.EXIT,
        title="MENU PRINCIPAL",
    )
    main_menu.add.button("Jogar", play_menu)
    main_menu.add.button("Controlos", about_menu)
    main_menu.add.button("Sobre", about_menu_team)
    main_menu.add.button("Sair", pygame_menu.events.EXIT)

    running = True
    while running:
        clock.tick(FPS)
        main_background()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        if main_menu.is_enabled():
            main_menu.mainloop(surface, main_background)
        pygame.display.flip()
    exit()


if __name__ == "__main__":
    main()
