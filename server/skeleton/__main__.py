from server_impl.gamemech import GameMech
from skeleton.server_skeleton import GameServerSkeleton
from server_impl import MAP_1, MAP_1_ITEMS
from server_shared_state import ServerSharedState


def main() -> None:
    """Função que executa o servidor"""

    # Classe com todas as mecânicas do jogo
    gamemech = GameMech(MAP_1, MAP_1_ITEMS, 1)
    # Estado partilhado entre os clientes
    shared_state = ServerSharedState(gamemech)
    # Esqueleto do servidor
    skeleton = GameServerSkeleton(shared_state)
    # Executa o servidor
    skeleton.run()


if __name__ == "__main__":
    main()
