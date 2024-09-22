import logging
from socket_impl.sockets import Socket
from server_impl import LOG_FILENAME, LOG_LEVEL, SERVER_ADDRESS, PORT
from server_shared_state import ServerSharedState
import client_server


class GameServerSkeleton:
    def __init__(self, shared_state: ServerSharedState) -> None:
        """Classe que representa o esqueleto do servidor

        :param shared_state: Estado partilhado entre os clientes
        :type shared_state: ServerSharedState
        """
        # Contém informação acerca da execução do programa
        logging.basicConfig(
            filename=LOG_FILENAME,
            level=LOG_LEVEL,
            format="%(asctime)s (%(levelname)s): %(message)s",
        )
        # Estado partilhado entre os clientes
        self.shared_state: ServerSharedState = shared_state

    def run(self) -> None:
        """Executa o servidor até o cliente mandar uma ação de 'terminar'"""
        socket = Socket.create_server_connection(SERVER_ADDRESS, PORT)
        logging.info("Waiting for clients to connect on port " + str(socket.port))
        keep_running = True
        # Enquanto está a correr, obter as conecções e depois interagir com o cliente conectado
        while keep_running:
            current_connection, address = socket.server_connect()
            logging.debug("Client " + str(address) + " just connected")
            client_server.ClientThread(
                self.shared_state, current_connection, address
            ).start()
        # Se não estiver a correr, então o 'socket' tem de ser fechado
        socket.close()
        logging.info("Server stopped")
