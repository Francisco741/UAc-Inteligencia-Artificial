from socket_impl.sockets import Socket
import stub as client


class ClientStub:
    def __init__(self, host: str, port: int) -> None:
        """Stub do cliente

        :param host: Endereço do servidor
        :type host: str
        :param port: Porta do servidor
        :type port: int
        """
        self._host: str = host
        self._port: int = port
        self.socket = Socket.create_client_connection(self._host, self._port)

    def get_map(self) -> list:
        """Comunica com o servidor para receber o mapa do jogo

        :return: Mapa do jogo
        :rtype: list
        """
        self.socket.send_str(client.MAP_OP)
        return self.socket.receive_obj(client.INT_SIZE)

    def get_music(self) -> int:
        """Comunica com o servidor para receber o ID da música a tocar no jogo

        :return: ID da música a tocar no jogo
        :rtype: int
        """
        self.socket.send_str(client.MUSIC_OP)
        return self.socket.receive_int(client.INT_SIZE)

    def set_player(self, name: str) -> tuple:
        """Comunica com o servidor para adicionar um jogador ao jogo

        :param name: nome do jogador
        :type name: str
        :return: ID e posição inicial do jogador
        :rtype: tuple
        """
        self.socket.send_str(client.PLAYER_OP)
        self.socket.send_str(name)
        return self.socket.receive_obj(client.INT_SIZE)

    def execute_start_game(self) -> int:
        """Comunica com o servidor para iniciar o jogo

        :return: Verificação se o jogo pode começar
        :rtype: int
        """
        self.socket.send_str(client.START_GAME)
        return self.socket.receive_int(client.INT_SIZE)

    def get_objects(self) -> dict:
        """Comunica com o servidor para obter os objetos presentes no mundo

        :return: Objetos presentes no mundo
        :rtype: dict
        """
        self.socket.send_str(client.GET_OBJTS)
        return self.socket.receive_obj(client.INT_SIZE)

    def step(self, id: int, dir: int) -> tuple:
        """Comunica com o servidor para obter a nova posição de um determinado jogador

        :param id: ID do jogador
        :type id: int
        :param dir: Direção do jogador
        :type dir: int
        :return: nova posição do jogador
        :rtype: tuple
        """
        self.socket.send_str(client.STEP_OP)
        self.socket.send_int(id, client.INT_SIZE)
        self.socket.send_int(dir, client.INT_SIZE)
        return self.socket.receive_obj(client.INT_SIZE)

    def update_world(self) -> dict:
        """Comunica com o servidor para obter o novo estado do mundo

        :return: Novo estado do mundo
        :rtype: dict
        """
        self.socket.send_str(client.UPDATE_WORLD)
        return self.socket.receive_obj(client.INT_SIZE)

    def dig_hole(self, id: int) -> str | None:
        """Comunica com o servidor para obter o resultado da escavação de um jogador

        :param id: ID do jogador
        :type id: int
        :return: Resultado da escavação de um jogador
        :rtype: str | None
        """
        self.socket.send_str(client.DIG_OP)
        self.socket.send_int(id, client.INT_SIZE)
        return self.socket.receive_obj(client.INT_SIZE)

    def end_game(self) -> list:
        """Comunica com o servidor para terminar o jogo e obter o vencedor

        :return: Vencedor ou vencedores (em caso de empate)
        :rtype: list
        """
        self.socket.send_str(client.END_GAME)
        return self.socket.receive_obj(client.INT_SIZE)

    def exec_stop_client(self) -> None:
        """Comunica com o servidor para terminar a ligação com o cliente"""
        self.socket.send_str(client.BYE_OP)
        self.socket.close()

    def exec_stop_server(self) -> None:
        """Comunica com o servidor para encerrar o servidor"""
        self.socket.send_str(client.STOP_SERVER_OP)
        self.socket.close()
