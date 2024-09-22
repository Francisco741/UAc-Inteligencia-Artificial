import threading
from server_impl.gamemech import GameMech
from server_impl import NR_CLIENTS


class ServerSharedState:
    def __init__(self, gamemech: GameMech) -> None:
        """Classe que representa o estado partilhado entre os clientes

        :param gamemech: Classe com todas as mecânicas do jogo
        :type gamemech: GameMech
        """
        # Número de clientes conectados ao servidor
        self._nr_connections: int = 0
        # Lock usado nas operações entre cliente e servidor
        self._connections_lock: threading.Lock = threading.Lock()
        # Variável que sinaliza se o jogo começou ou não
        self._start_game: bool = False
        # Semáforo que verifica se o número suficiente de clientes foi atingido para começar o jogo
        self._start_game_sem: threading.Semaphore = threading.Semaphore(0)
        # Classe com todas as mecânicas do jogo
        self._gamemech: GameMech = gamemech

    def add_client(self) -> None:
        """Adiciona um cliente ao estado partilhado entre os clientes"""
        with self._connections_lock:
            self._nr_connections += 1
        # Testar se já existe o número suficiente de jogadores
        if self._nr_connections == NR_CLIENTS:
            with self._connections_lock:
                self._start_game = True
                for i in range(self._nr_connections):
                    self._start_game_sem.release()

    def get_objects(self) -> dict:
        """Obtém os objetos presentes no mundo

        :return: Objetos presentes no mundo (jogadores)
        :rtype: dict
        """
        with self._connections_lock:
            res: dict = self._gamemech.get_players()
        return res

    def get_step(self, id: int, dir: int) -> tuple:
        """Obtém a nova posição de um determinado jogador

        :param id: ID do jogador
        :type id: int
        :param dir: Direção do jogador
        :type dir: int
        :return: Nova posição de um determinado jogador
        :rtype: tuple
        """
        with self._connections_lock:
            res: tuple[int, int] = self._gamemech.execute(id, dir)
        return res

    def get_world(self) -> dict:
        """Obtém o novo estado do mundo

        :return: novo estado do mundo (estado dos buracos de terra)
        :rtype: dict
        """
        with self._connections_lock:
            res: dict = self._gamemech.get_dirt_holes()
        return res

    def get_music(self) -> int:
        """Obtém o ID da música a tocar no jogo consoante o mapa

        :return: ID da música a tocar no jogo
        :rtype: int
        """
        with self._connections_lock:
            res: int = self._gamemech.get_music()
        return res

    def get_dig_result(self, id: int) -> str | None:
        """Obtém o resultado da escavação de um jogador

        :param id: ID do jogador
        :type id: int
        :return: resultado da escavação de um jogador
        :rtype: str | None
        """
        with self._connections_lock:
            res: str | None = self._gamemech.dig(id)
        return res

    def get_map(self) -> list:
        """Obtém o mapa do jogo

        :return: mapa do jogo
        :rtype: list
        """
        with self._connections_lock:
            res: list[list[int]] = self._gamemech.get_map()
        return res

    def get_winners(self) -> list:
        """Obtém a lista de vencedores do jogo

        :return: lista de vencedores do jogo
        :rtype: list
        """
        with self._connections_lock:
            res: list | None = self._gamemech.end()
        return res

    def start_game_sem(self) -> threading.Semaphore:
        """Obtém o semáforo para iniciar o jogo

        :return: Semáforo para iniciar o jogo
        :rtype: threading.Semaphore
        """
        return self._start_game_sem

    def gamemech(self) -> GameMech:
        """Obtém a classe com todas as mecânicas do jogo

        :return: classe com todas as mecânicas do jogo
        :rtype: GameMech
        """
        return self._gamemech

    def start_game(self) -> bool:
        """Obtém o estado da variável que sinaliza se o jogo começou ou não

        :return: variável que sinaliza se o jogo começou ou não
        :rtype: bool
        """
        return self._start_game
