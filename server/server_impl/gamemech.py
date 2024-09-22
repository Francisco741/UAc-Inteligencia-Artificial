from random import shuffle
from server_impl import UP, RIGHT, DOWN, LEFT


class GameMech:
    def __init__(
        self, game_map: list[list[int]], map_nr_items: dict[str, int], map_number: int
    ) -> None:
        """Classe com todas as mecânicas do jogo

        :param game_map: Mapa do jogo
        :type game_map: list[list[int]]
        :param map_nr_items: Número de cada tipo de item presente no map
        :type map_nr_items: dict[str, int]
        :param map_number: Número do mapa
        :type map_number: int
        """
        # ID da música do mapa selecionado
        self.game_music: int = map_number
        # Mapa do jogo selecionado
        self.game_map: list[list[int]] = game_map
        # Dimensões do mapa
        self.nr_max_x: int = len(self.game_map[0])
        self.nr_max_y: int = len(self.game_map)
        # Dicionário com todos os objetos presentes em cada posição da grelha do jogo
        self.world: dict = dict()
        for x in range(self.nr_max_x):
            for y in range(self.nr_max_y):
                self.world[(x, y)] = []
        # Dicionário com todos os pedaços de terra escaváveis
        self.dirt_holes: dict = dict()
        # Lista com todas as posições dos pedaços de terra escaváveis
        self.dirt_holes_positions: list[tuple[int, int]] = []
        # Número de cada tipo de objeto no mundo
        self.nr_dirts: int = 0
        self.nr_walls: int = 0
        self.nr_grasses: int = 0
        self.nr_dirt_holes: int = 0
        self.nr_obstacles: int = 0
        self.nr_tents: int = 0
        self.nr_waters: int = 0
        # Adiciona cada objeto ao mundo consoante a sua posição no mapa
        # Cada número corresponde a um tipo de objeto
        for i in range(len(self.game_map)):
            for j in range(len(self.game_map[i])):
                if self.game_map[i][j] == 0:
                    self.world[(j, i)].append(["soil", "dirt", self.nr_dirts])
                    self.nr_dirts += 1
                if self.game_map[i][j] == 1:
                    self.world[(j, i)].append(["obst", "wall", self.nr_walls])
                    self.nr_walls += 1
                if self.game_map[i][j] == 2:
                    self.world[(j, i)].append(["obst", "grass", self.nr_grasses])
                    self.nr_grasses += 1
                if self.game_map[i][j] == 3:
                    # Adicona um pedaço de terra coberto ao dicionário
                    self.dirt_holes[self.nr_dirt_holes] = [
                        "dirt_hole",
                        (j, i),
                        "covered",
                        "empty",
                    ]
                    # Adiciona a posição do pedaço de terra coberto à lista
                    self.dirt_holes_positions.append((j, i))
                    self.world[(j, i)].append(["obst", "dirt_hole", self.nr_dirt_holes])
                    self.nr_dirt_holes += 1
                if self.game_map[i][j] == 4:
                    self.world[(j, i)].append(["obst", "obstacle", self.nr_obstacles])
                    self.nr_obstacles += 1
                if self.game_map[i][j] == 5:
                    self.world[(j, i)].append(["obst", "tent", self.nr_tents])
                    self.nr_tents += 1
                if self.game_map[i][j] == 6:
                    self.world[(j, i)].append(["obst", "water", self.nr_waters])
                    self.nr_waters += 1
        # Listas com as posições de cada item escavável
        self.bones_positions: list[tuple[int, int]] = []
        self.diamonds_positions: list[tuple[int, int]] = []
        self.skulls_positions: list[tuple[int, int]] = []
        self.potions_positions: list[tuple[int, int]] = []
        self.fishes_positions: list[tuple[int, int]] = []
        self.coins_positions: list[tuple[int, int]] = []
        self.chalices_positions: list[tuple[int, int]] = []
        self.crowns_positions: list[tuple[int, int]] = []
        # Número de cada tipo de item escondido no mapa
        self.nr_bones: int = map_nr_items["bones"]
        self.nr_diamonds: int = map_nr_items["diamonds"]
        self.nr_skulls: int = map_nr_items["skulls"]
        self.nr_potions: int = map_nr_items["potions"]
        self.nr_fishes: int = map_nr_items["fishes"]
        self.nr_coins: int = map_nr_items["coins"]
        self.nr_chalices: int = map_nr_items["chalices"]
        self.nr_crowns: int = map_nr_items["crowns"]
        # Número de pedaços de terra escavados
        self.nr_dug_holes: int = 0
        # Função que distribui aleatóriamente os items pelo mapa
        self.distribute_items()
        # Dicionário com todos os jogadores
        self.players: dict = dict()
        # Número de jogadores no mapa
        self.nr_players: int = 0
        # Posição inicial dos jogadores
        self.pos_players: list[tuple[int, int]] = [
            (1, 1),
            (self.nr_max_x - 2, self.nr_max_y - 2),
        ]

    def get_map(self) -> list[list[int]]:
        """Função que retorna o mapa do jogo

        :return: mapa do jogo
        :rtype: list[list[int]]
        """
        return self.game_map

    def get_music(self) -> int:
        """Função que retorna o ID da música do jogo

        :return: ID da música do jogo
        :rtype: int
        """
        return self.game_music

    def get_dirt_holes(self) -> dict:
        """Função que retorna o diconário com todos os pedaços de terra escaváveis

        :return: diconário com todos os pedaços de terra escaváveis
        :rtype: dict
        """
        return self.dirt_holes

    def get_players(self) -> dict:
        """Função que retorna o dicionário com todos os jogadores presentes no mapa

        :return: Dicionário com todos os jogadores presentes no mapa
        :rtype: dict
        """
        return self.players

    def distribute_items(self) -> None:
        """Função que distribui aleatóriamente os items pelo mapa"""
        # Baralha a lista com as posições dos pedaços de terra escaváveis
        shuffle(self.dirt_holes_positions)
        # Adiciona ossos aos pedaços de terra escaváveis
        for bone in range(self.nr_bones):
            self.bones_positions.append(self.dirt_holes_positions[bone])
            self.dirt_holes[self.world[self.dirt_holes_positions[bone]][0][2]] = [
                "dirt_hole",
                self.dirt_holes_positions[bone],
                "covered",
                "bone",
            ]
        # Verifica quais são os pedaços de terra escaváveis sem items
        empty_dirt_holes: list[tuple[int, int]] = [
            e for e in self.dirt_holes_positions if e not in self.bones_positions
        ]
        # Adiciona diamantes aos pedaços de terra escaváveis
        for diamond in range(self.nr_diamonds):
            self.diamonds_positions.append(empty_dirt_holes[diamond])
            self.dirt_holes[self.world[empty_dirt_holes[diamond]][0][2]] = [
                "dirt_hole",
                empty_dirt_holes[diamond],
                "covered",
                "diamond",
            ]
        # Verifica quais são os pedaços de terra escaváveis sem items
        empty_dirt_holes_2: list[tuple[int, int]] = [
            e2 for e2 in empty_dirt_holes if e2 not in self.diamonds_positions
        ]
        # Adiciona caveiras aos pedaços de terra escaváveis
        for skull in range(self.nr_skulls):
            self.skulls_positions.append(empty_dirt_holes_2[skull])
            self.dirt_holes[self.world[empty_dirt_holes_2[skull]][0][2]] = [
                "dirt_hole",
                empty_dirt_holes_2[skull],
                "covered",
                "skull",
            ]

        # Verifica quais são os pedaços de terra escaváveis sem items
        empty_dirt_holes_3: list[tuple[int, int]] = [
            e3 for e3 in empty_dirt_holes_2 if e3 not in self.skulls_positions
        ]
        # Adiciona poções aos pedaços de terra escaváveis
        for potion in range(self.nr_potions):
            self.potions_positions.append(empty_dirt_holes_3[potion])
            self.dirt_holes[self.world[empty_dirt_holes_3[potion]][0][2]] = [
                "dirt_hole",
                empty_dirt_holes_3[potion],
                "covered",
                "potion",
            ]

        # Verifica quais são os pedaços de terra escaváveis sem items
        empty_dirt_holes_4: list[tuple[int, int]] = [
            e4 for e4 in empty_dirt_holes_3 if e4 not in self.potions_positions
        ]
        # Adiciona espinhas de peixe aos pedaços de terra escaváveis
        for fish in range(self.nr_fishes):
            self.fishes_positions.append(empty_dirt_holes_4[fish])
            self.dirt_holes[self.world[empty_dirt_holes_4[fish]][0][2]] = [
                "dirt_hole",
                empty_dirt_holes_4[fish],
                "covered",
                "fish",
            ]

        # Verifica quais são os pedaços de terra escaváveis sem items
        empty_dirt_holes_5: list[tuple[int, int]] = [
            e5 for e5 in empty_dirt_holes_4 if e5 not in self.fishes_positions
        ]
        # Adiciona moedas aos pedaços de terra escaváveis
        for coin in range(self.nr_coins):
            self.coins_positions.append(empty_dirt_holes_5[coin])
            self.dirt_holes[self.world[empty_dirt_holes_5[coin]][0][2]] = [
                "dirt_hole",
                empty_dirt_holes_5[coin],
                "covered",
                "coin",
            ]

        # Verifica quais são os pedaços de terra escaváveis sem items
        empty_dirt_holes_6: list[tuple[int, int]] = [
            e6 for e6 in empty_dirt_holes_5 if e6 not in self.coins_positions
        ]
        # Adiciona cálices aos pedaços de terra escaváveis
        for chalice in range(self.nr_chalices):
            self.chalices_positions.append(empty_dirt_holes_6[chalice])
            self.dirt_holes[self.world[empty_dirt_holes_6[chalice]][0][2]] = [
                "dirt_hole",
                empty_dirt_holes_6[chalice],
                "covered",
                "chalice",
            ]

        # Verifica quais são os pedaços de terra escaváveis sem items
        empty_dirt_holes_7: list[tuple[int, int]] = [
            e7 for e7 in empty_dirt_holes_6 if e7 not in self.chalices_positions
        ]
        # Adiciona coroas aos pedaços de terra escaváveis
        for crown in range(self.nr_crowns):
            self.crowns_positions.append(empty_dirt_holes_7[crown])
            self.dirt_holes[self.world[empty_dirt_holes_7[crown]][0][2]] = [
                "dirt_hole",
                empty_dirt_holes_7[crown],
                "covered",
                "crown",
            ]

    def add_player(self, name: str) -> tuple[int, (int, int)]:
        """Função que adiciona um jogador ao jogo

        :param name: Nome do jogador
        :type name: str
        :return: ID do jogador e a sua posição
        :rtype: tuple[int, (int, int)]
        """
        # Adiciona um jogador com id, nome, posição no mapa,
        # direção que está virado, número de pontos e ação a executar
        self.players[self.nr_players] = [
            name,
            self.pos_players[self.nr_players],
            DOWN,
            0,
            "walk",
        ]
        # Adiciona o jogador ao mapa
        self.world[self.pos_players[self.nr_players]].append(
            ["player", name, self.nr_players]
        )
        # Aumenta o contador de jogadores
        self.nr_players += 1
        # Retorna o id e a posição do jogador
        return self.nr_players - 1, self.pos_players[self.nr_players - 1]

    def calculate_adjacent_position(
        self, pos: tuple[int, int], direction: int
    ) -> tuple[int, int]:
        """Função que calcula a próxima posição do jogador consoante a sua direção

        :param pos: Posição do jogador
        :type pos: tuple[int, int]
        :param direction: Direção do jogador
        :type direction: int
        :return: Nova posição do jogador
        :rtype: tuple[int, int]
        """
        new_pos: tuple[int, int] = pos
        if direction == UP:
            new_pos = (pos[0], pos[1] - 1)
        elif direction == DOWN:
            new_pos = (pos[0], pos[1] + 1)
        elif direction == LEFT:
            new_pos = (pos[0] - 1, pos[1])
        elif direction == RIGHT:
            new_pos = (pos[0] + 1, pos[1])
        return new_pos

    def obstacle_in_pos(self, pos: tuple[int, int]) -> bool:
        """Função que verifica se existe um obstáculo na direção em que o jogador se quer movimentar

        :param pos: Posição em frente ao jogador
        :type pos: tuple[int, int]
        :return: True se houver um obstáculo e False se não houver
        :rtype: bool
        """
        objects: list = self.world[pos]
        for obj in objects:
            if obj[0] == "obst":
                return True
        return False

    def dig_dirt_hole(self, pos: tuple[int, int]) -> str | None:
        """Função que verifica se o objeto em frente ao jogador é um pedaço de terra escavável

        :param pos: Posição em frente ao jogador
        :type pos: tuple[int, int]
        :return: Se não for um pedaço de terra escavável retorna None
        Se for, retorna o item presente nele
        :rtype: str | None
        """
        objects: list = self.world[pos]
        for obj in objects:
            # Verifica se o objeto é um pedaço de terra ainda não escavado
            if obj[1] == "dirt_hole" and self.dirt_holes[obj[2]][2] == "covered":
                # Marca o pedaço de terra como escavado
                self.dirt_holes[obj[2]][2] = "dug"
                # Aumenta o contador de buracos de terra escavados
                self.nr_dug_holes += 1
                # Verifica qual o item presente no buraco de terra
                if pos in self.bones_positions:
                    return "bone"
                if pos in self.diamonds_positions:
                    return "diamond"
                if pos in self.skulls_positions:
                    return "skull"
                if pos in self.potions_positions:
                    return "potion"
                if pos in self.fishes_positions:
                    return "fish"
                if pos in self.coins_positions:
                    return "coin"
                if pos in self.chalices_positions:
                    return "chalice"
                if pos in self.crowns_positions:
                    return "crown"
                else:
                    return "empty"
        return None

    def execute(self, nr_player: int, direction: int) -> tuple[int, int]:
        """Função que altera a posição do jogador se não houver osbtáculos

        :param nr_player: ID do jogador
        :type nr_player: int
        :param direction: Direção do jogador
        :type direction: int
        :return: Nova posição do jogador
        :rtype: tuple[int, int]
        """
        # Nome do jogador
        name: str = self.players[nr_player][0]
        # Posição do jogador
        pos: tuple[int, int] = self.players[nr_player][1]
        # Pontos do jogador
        points: int = self.players[nr_player][3]
        # Calcula a próxima posição do jogador consoante a sua direção
        new_pos: tuple[int, int] = self.calculate_adjacent_position(pos, direction)
        # Verifica se existe um obstáculo na direção em que o jogador se quer movimentar
        if self.obstacle_in_pos(new_pos):
            new_pos = pos
        # Atualiza os atributos do jogador no dicionário players
        self.players[nr_player] = [name, new_pos, direction, points, "walk"]
        # Atualiza o mundo com a nova posição do jogador
        self.world[pos].remove(["player", name, nr_player])
        self.world[new_pos].append(["player", name, nr_player])
        return new_pos

    def dig(self, nr_player: int) -> str | None:
        """Função que verifica se o objeto em frente ao jogador é um pedaço de terra escavável
        e adiciona pontos ao jogador consoante o tipo de item escavado

        :param nr_player: ID do jogador
        :type nr_player: int
        :return: Se não for um pedaço de terra escavável retorna None
        Se for, retorna o item presente nele
        :rtype: str | None
        """
        # Posição do jogador
        pos: tuple[int, int] = self.players[nr_player][1]
        # Direção do jogador
        direction: int = self.players[nr_player][2]
        # Calcula a posição do objeto que está em frente ao jogador
        hole_pos: tuple[int, int] = self.calculate_adjacent_position(pos, direction)
        # Verifica se o objeto em frente ao jogador é um pedaço de terra escavável
        result: str | None = self.dig_dirt_hole(hole_pos)
        # Verifica qual o item presente no buraco de terra
        if result == "bone":
            # Adiciona 10 pontos ao jogador
            self.players[nr_player][3] += 10
            print(f"{self.players[nr_player][0]}: {self.players[nr_player][3]} pontos")
        elif result == "diamond":
            # Adiciona 50 pontos ao jogador
            self.players[nr_player][3] += 50
            print(f"{self.players[nr_player][0]}: {self.players[nr_player][3]} pontos")
        elif result == "fish":
            # Adiciona 5 pontos ao jogador
            self.players[nr_player][3] += 5
            print(f"{self.players[nr_player][0]}: {self.players[nr_player][3]} pontos")
        elif result == "coin":
            # Adiciona 20 pontos ao jogador
            self.players[nr_player][3] += 20
            print(f"{self.players[nr_player][0]}: {self.players[nr_player][3]} pontos")
        elif result == "chalice":
            # Adiciona 30 pontos ao jogador
            self.players[nr_player][3] += 30
            print(f"{self.players[nr_player][0]}: {self.players[nr_player][3]} pontos")
        elif result == "crown":
            # Adiciona 40 pontos ao jogador
            self.players[nr_player][3] += 40
            print(f"{self.players[nr_player][0]}: {self.players[nr_player][3]} pontos")
        # Se o jogador escavou um buraco
        if result is not None:
            # Altera a ação atual do jogador para "escavar"
            self.players[nr_player][4] = "dig"
        # Retorna o item escavado ou "None" se não encontrou um pedaço de terra escavável
        return result

    def end(self) -> list | None:
        """Função que verifica se o jogo terminou e apura o vencedor
        ou vencedores (em caso de empate)

        :return: None se o jogo ainda não terminou
        e uma lista com o vencedor ou vencedores (em caso de empate) se o jogo terminou
        :rtype: list | None
        """
        # Verifica se todos os pedaços de terra foram escavados
        if self.nr_dug_holes >= self.nr_dirt_holes:
            # Número máximo de pontos conseguidos
            max_points: int = 0
            # Itera sobre os jogadores para encontrar a maior pontuação obtida
            for player_info in self.players.values():
                # Número de pontos de um jogador
                player_points: int = player_info[3]
                # Atualiza o número máximo de pontos conseguidos se for maior ao anterior
                if player_points > max_points:
                    max_points = player_points
            # Lista dos vencedores
            winners: list = []
            # Itera sobre os jogadores para encontrar os vencedores
            for player_info in self.players.values():
                # Se o jogador tiver uma pontuação igual à pontuação máxima obtida
                if player_info[3] == max_points:
                    # Adiciona o nome do jogador à lista de vencedores
                    winners.append(player_info[0])
            print(f"Vencedor: {', '.join(winners)}, com {max_points} pontos.")
            # Retorna a lista com os vencedores do jogo
            return winners
        # Se o jogo ainda não terminou retorna "None"
        return None
