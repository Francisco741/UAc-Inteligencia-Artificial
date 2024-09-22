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
