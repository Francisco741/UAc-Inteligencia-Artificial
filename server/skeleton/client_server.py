from threading import Thread
from server_impl.gamemech import GameMech
import logging
import server_impl as server
from server_shared_state import ServerSharedState


class ClientThread(Thread):
    def __init__(
        self, shared_state: ServerSharedState, current_connection, address
    ) -> None:
        """Classe que processa os pedidos dos clientes

        :param shared_state: Classe que representa o estado partilhado entre os clientes
        :type shared_state: ServerSharedState
        :param current_connection: ligação estabelecida com o cliente
        :param address: Endereço do cliente
        """
        self.current_connection = current_connection
        self.shared_state: ServerSharedState = shared_state
        self.gamemech: GameMech = self.shared_state.gamemech()
        self.address = address
        Thread.__init__(self)

    def process_objects(self) -> None:
        """Processa um pedido para obter os objetos presentes no mundo"""
        res: dict = self.shared_state.get_objects()
        self.current_connection.send_obj(res, server.INT_SIZE)

    def process_step(self) -> None:
        """Processa um pedido para obter a nova posição de um determinado jogador"""
        # ID do jogador
        id: int = self.current_connection.receive_int(server.INT_SIZE)
        # Direção do jogador
        dir: int = self.current_connection.receive_int(server.INT_SIZE)
        res: tuple = self.shared_state.get_step(id, dir)
        self.current_connection.send_obj(res, server.INT_SIZE)

    def process_update_world(self) -> None:
        """Processa um pedido para obter o novo estado do mundo"""
        world: dict = self.shared_state.get_world()
        self.current_connection.send_obj(world, server.INT_SIZE)

    def process_dig(self) -> None:
        """Processa um pedido para obter o resultado da escavação de um jogador"""
        # ID do jogador
        id: int = self.current_connection.receive_int(server.INT_SIZE)
        res: str | None = self.shared_state.get_dig_result(id)
        self.current_connection.send_obj(res, server.INT_SIZE)

    def process_add_player(self) -> None:
        """Processa um pedido para adicionar um jogador com um determinado nome"""
        # Nome do jogador
        name: str = self.current_connection.receive_str(server.MAX_STR_SIZE)
        res: tuple = self.gamemech.add_player(name)
        self.current_connection.send_obj(res, server.INT_SIZE)
        self.shared_state.add_client()

    def process_get_map(self) -> None:
        """Processa um pedido para obter o mapa do jogo"""
        game_map: list = self.shared_state.get_map()
        self.current_connection.send_obj(game_map, server.INT_SIZE)

    def process_get_music(self) -> None:
        """Processa um pedido para obter o ID da música a tocar no jogo"""
        game_music: int = self.shared_state.get_music()
        self.current_connection.send_int(game_music, server.INT_SIZE)

    def process_start_game(self) -> None:
        """Processa um pedido de um cliente para iniciar o jogo"""
        self.shared_state.start_game_sem().acquire()
        val: bool = True
        self.current_connection.send_int(int(val), server.INT_SIZE)

    def process_end_game(self) -> None:
        """Processa um pedido para terminar o jogo e obter os vencedores"""
        winners: list = self.shared_state.get_winners()
        self.current_connection.send_obj(winners, server.INT_SIZE)

    def dispatch_request(self) -> tuple[bool, bool]:
        """Chama funções de processamento baseado no tipo de pedido

        :return: valores de 'keep_running' e 'last_request'
        :rtype: tuple[bool, bool]
        """
        # Obtém a string do pedido
        request_type: str = self.current_connection.receive_str(server.COMMAND_SIZE)
        # Não imprime estes pedidos, pois são executados constantemente
        if (
            request_type != "get objts"
            and request_type != "upd world"
            and request_type != "end game "
        ):
            print(request_type)
        keep_running = True
        last_request = False
        # Se o pedido for STEP_OP
        if request_type == server.STEP_OP:
            logging.info("Step operation requested " + str(self.address))
            self.process_step()
        # Se o pedido for GET_OBJTS
        elif request_type == server.GET_OBJTS:
            logging.info("Get objects operation requested " + str(self.address))
            self.process_objects()
        # Se o pedido for UPDATE_WORLD
        elif request_type == server.UPDATE_WORLD:
            logging.info("Update world operation requested " + str(self.address))
            self.process_update_world()
        # Se o pedido for DIG_OP
        elif request_type == server.DIG_OP:
            logging.info("Dig operaton requested " + str(self.address))
            self.process_dig()
        # Se o pedido for MAP_OP
        elif request_type == server.MAP_OP:
            logging.info("Ask for map info operation requested " + str(self.address))
            self.process_get_map()
        # Se o pedido for MUSIC_OP
        elif request_type == server.MUSIC_OP:
            logging.info("Ask for music info operation requested " + str(self.address))
            self.process_get_music()
        # Se o pedido for PLAYER_OP
        elif request_type == server.PLAYER_OP:
            logging.info("Adding player " + str(self.address))
            self.process_add_player()
        # Se o pedido for START_GAME
        elif request_type == server.START_GAME:
            logging.info("Asking for starting game:" + str(self.address))
            self.process_start_game()
        # Se o pedido for END_GAME
        elif request_type == server.END_GAME:
            logging.info("Asking for ending game:" + str(self.address))
            self.process_end_game()
        # Se o pedido for BYE_OP
        elif request_type == server.BYE_OP:
            last_request = True
        # Se o pedido for STOP_SERVER_OP
        elif request_type == server.STOP_SERVER_OP:
            last_request = True
            keep_running = False
        return keep_running, last_request

    def run(self) -> None:
        """Enquanto o cliente está conectado, esperar pelos seus pedidos para executar uma ação"""
        last_request = False
        # Se não for o último pedido recebe o pedido
        while not last_request:
            keep_running, last_request = self.dispatch_request()
        # Se for o último pedido o cliente está a se desconectar do servidor
        logging.debug(
            "Client " + str(self.current_connection.get_address()) + " disconnected"
        )
