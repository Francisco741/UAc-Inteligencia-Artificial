import socket
import json


class Socket:
    def __init__(self, connection, port: int) -> None:
        """Classe que representa um socket para estabelecer ligações entre clientes e servidor

        :param connection: Conexão atual
        :param port: Porta usada na conexão
        :type port: int
        """
        self._current_connection = connection
        self._port: int = port

    @property
    def port(self) -> int:
        """Função que retorna a porta usada na conexão

        :return: Porta usada na conexão
        :rtype: int
        """
        return self._port

    def get_address(self):
        """Função que obtém o endereço da ligação estabelecida

        :return: endereço da ligação estabelecida
        """
        return self._current_connection.getpeername()

    @property
    def current_connection(self):
        """Função que retorna a conexão atual

        :return: Conexão atual
        """
        return self._current_connection

    def receive_int(self, n_bytes: int) -> int:
        """Função de comunicação que recebe um inteiro

        :param n_bytes: Número de bytes a ler na conexão atual
        :type n_bytes: int
        :return: Inteiro lido na conexão atual
        :rtype: int
        """
        data = self._current_connection.recv(n_bytes)
        return int.from_bytes(data, byteorder="big", signed=True)

    def send_int(self, value: int, n_bytes: int) -> None:
        """Função de comunicação que envia um inteiro

        :param value: Valor do inteiro a ser enviado na conexão atual
        :type value: int
        :param n_bytes: Número de bytes a mandar na conexão atual
        :type n_bytes: int
        """
        self._current_connection.send(
            value.to_bytes(n_bytes, byteorder="big", signed=True)
        )

    def receive_str(self, n_bytes: int) -> str:
        """Função de comunicação que recebe uma string

        :param n_bytes: Número de bytes a ler na conexão atual
        :type n_bytes: int
        :return: String lida na conexão atual
        :rtype: str
        """
        data = self._current_connection.recv(n_bytes)
        return data.decode()

    def send_str(self, value: str) -> None:
        """Função de comunicação que envia uma string

        :param value: String a ser enviada na conexão atual
        :type value: str
        """
        self._current_connection.send(value.encode())

    def send_obj(self, value: object, n_bytes: int) -> None:
        """Função de comunicação que envia um objeto

        :param value: Objeto a ser enviado na conexão atual
        :type value: object
        :param n_bytes: Número de bytes a mandar na conexão atual
        :type n_bytes: int
        """
        msg = json.dumps(value)
        # print("SEND_OBJ:",msg)
        size = len(msg)
        self.send_int(size, n_bytes)
        self.send_str(msg)

    def receive_obj(self, n_bytes: int) -> object:
        """Função de comunicação que recebe um objeto

        :param n_bytes: Número de bytes a ler na conexão atual
        :type n_bytes: int
        :return: Objeto lido na conexão atual
        :rtype: object
        """
        size = self.receive_int(n_bytes)
        obj = self.receive_str(size)
        return json.loads(obj)

    def close(self) -> None:
        """Função que fecha a conexão"""
        self._current_connection.close()
        self._current_connection = None

    def server_connect(self) -> tuple:
        """Função de conexão ao servidor

        :return: Conexão, porta e endereço usados na conexão
        :rtype: tuple
        """
        connection, address = self._current_connection.accept()
        return Socket(connection, self._port), address

    @staticmethod
    def create_server_connection(host: str, port: int):
        """Função que cria uma ligação ao servidor

        :param host: endereço do host
        :type host: str
        :param port: porta usada
        :type port: int
        :return: Socket
        """
        connection = socket.socket()
        connection.bind((host, port))
        connection.listen(1)
        return Socket(connection, port)

    @staticmethod
    def create_client_connection(host: str, port: int):
        """Função que cria uma ligação ao cliente

        :param host: endereço do host
        :type host: str
        :param port: porta usada
        :type port: int
        :return: Socket
        """
        connection = socket.socket()
        connection.connect((host, port))
        return Socket(connection, port)
