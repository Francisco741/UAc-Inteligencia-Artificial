from server_impl.gamemech import GameMech
from skeleton.server_skeleton import GameServerSkeleton
from server_impl import MAP_1, MAP_1_ITEMS, MAP_2, MAP_2_ITEMS, MAP_3, MAP_3_ITEMS
from server_shared_state import ServerSharedState
from random import randint


def main() -> None:
    """Função que executa o servidor"""
    # Mapa do jogo
    game_map: list[list[int]] = []
    # Itens existentes no mapa do jogo
    game_map_items: dict[str, int] = {}
    # Entre os 3 mapas existentes, um será aleatóriamente escolhido
    map_number: int = randint(1, 3)
    if map_number == 1:
        game_map = MAP_1
        game_map_items = MAP_1_ITEMS
    elif map_number == 2:
        game_map = MAP_2
        game_map_items = MAP_2_ITEMS
    elif map_number == 3:
        game_map = MAP_3
        game_map_items = MAP_3_ITEMS
    # Classe com todas as mecânicas do jogo
    gamemech = GameMech(game_map, game_map_items, map_number)
    # Estado partilhado entre os clientes
    shared_state = ServerSharedState(gamemech)
    # Esqueleto do servidor
    skeleton = GameServerSkeleton(shared_state)
    # Executa o servidor
    skeleton.run()


if __name__ == "__main__":
    main()
