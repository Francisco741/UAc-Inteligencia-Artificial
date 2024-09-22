import pygame
from stub.client_stub import ClientStub
from ui.game import Game
from stub import SQUARE_SIZE, PORT, SERVER_ADDRESS


def main() -> None:
    """Função que executa o jogo"""
    pygame.init()
    cs = ClientStub(SERVER_ADDRESS, PORT)
    game = Game(cs, SQUARE_SIZE)
    game.run()


if __name__ == "__main__":
    main()
