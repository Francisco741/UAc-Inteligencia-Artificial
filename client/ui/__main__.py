import pygame
from ui.game import Game
from stub import SQUARE_SIZE
from gamemech import GameMech
from server.server_impl import (
    MAP_1,
    MAP_1_ITEMS,
)


def main() -> None:
    """Função que executa o jogo"""
    pygame.init()

    # Classe com todas as mecânicas do jogo
    gm = GameMech(MAP_1, MAP_1_ITEMS, 1)

    game = Game(gm, SQUARE_SIZE)
    game.run()


if __name__ == "__main__":
    main()
