import pygame as pg
from heapq import heappush, heappop
from gamemech import GameMech
from constants import UP, DOWN, LEFT, RIGHT
from random import randint


class PlayerAI(pg.sprite.DirtySprite):
    def __init__(
        self,
        nr_player: int,
        name: str,
        pos_x: int,
        pos_y: int,
        size: int,
        points: int = 0,
        algorithm: int = 1,
        *groups,
    ) -> None:
        """Classe que representa um Jogador

        :param nr_player: ID do jogador
        :type nr_player: int
        :param name: Nome do jogador
        :type name: str
        :param pos_x: posição x do jogador
        :type pos_x: int
        :param pos_y: posição y do jogador
        :type pos_y: int
        :param size: tamanho do jogador
        :type size: int
        :param points: pontos do jogador, tem como default 0
        :type points: int, optional
        """
        super().__init__(*groups)
        # ID do jogador
        self.my_id: int = nr_player
        # Nome do jogador
        self.name: str = name
        # Pontuação do jogador
        self.points: int = points
        # Controlos do jogador
        self.keys: tuple[int, int, int, int, int] = (0, 1, 2, 3, 4)
        # Direção do jogador
        self.direction = DOWN
        # Tamanho do jogador
        self.size: int = size
        # Sprite do jogador
        self.image = pg.image.load(f"Sprites/Player{self.my_id}/p{self.my_id}_f.png")
        initial_size: tuple[int, int] = self.image.get_size()
        self.size_rate: float = size / initial_size[0]
        self.new_size: tuple[int, int] = (
            int(self.image.get_size()[0] * self.size_rate),
            int(self.image.get_size()[1] * self.size_rate),
        )
        self.image = pg.transform.scale(self.image, self.new_size)
        self.rect = pg.rect.Rect((pos_x * size, pos_y * size), self.image.get_size())
        # Posição do jogador
        self.pos: tuple[int, int] = (pos_x, pos_y)
        # Algoritmo da AI
        self.algorithm = algorithm

    def get_size(self) -> tuple[int, int]:
        """Função que retorna o tamanho do jogador

        :return: Tamanho do jogador
        :rtype: tuple[int, int]
        """
        return self.new_size

    def get_id(self) -> int:
        """Função que retorna o ID do jogador

        :return: ID do jogador
        :rtype: int
        """
        return self.my_id

    # AI com movimento aleatório
    def random_movement(self) -> int:
        return randint(0, 4)

    # AI que vai atrás do jogador
    def astar_perseguir_jogador(self, world: dict) -> str:
        opponent_id = 0 if self.my_id == 1 else 1
        ai_pos = None
        human_pos = None

        # Localizar posições dos jogadores
        for coord, items in world.items():
            for item in items:
                if item[0] == "player" and item[2] == self.my_id:
                    ai_pos = coord
                elif item[0] == "player" and item[2] == opponent_id:
                    human_pos = coord

        # Se os Jogadores não forem encontrados
        if ai_pos is None or human_pos is None:
            return None

        ai_y, ai_x = ai_pos
        human_y, human_x = human_pos

        # Direções possíveis
        directions = {
            "UP": (0, -1),
            "DOWN": (0, 1),
            "LEFT": (-1, 0),
            "RIGHT": (1, 0),
        }

        # Função para verificar se uma célula é válida
        def is_valid(cell):
            y, x = cell
            # Verificar se a célula está dentro do mundo
            if (y, x) not in world:
                return False
            # Verificar se há um obstáculo
            for item in world[(y, x)]:
                if item[0] == "obst":
                    return False
            return True

        # Função heurística (distância Manhattan)
        def heuristic(y1, x1, y2, x2):
            return abs(y1 - y2) + abs(x1 - x2)

        # Fila de prioridade para o algoritmo A*
        open_set = []
        heappush(
            open_set, (0, ai_y, ai_x, None)
        )  # (custo_total, y, x, movimento_inicial)

        # Custos conhecidos para cada célula
        g_costs = {ai_pos: 0}

        # Conjunto de células visitadas
        visited = set()

        while open_set:
            _, current_y, current_x, first_move = heappop(open_set)

            # Se chegarmos à posição do adversário, retornar o primeiro movimento
            if (current_y, current_x) == (human_y, human_x):
                print(
                    f"Chegou ao humano em ({current_y}, {current_x}) com movimento {first_move}"
                )
                return first_move

            # Marcar a célula atual como visitada
            visited.add((current_y, current_x))

            # Explorar os vizinhos
            for direction, (dy, dx) in directions.items():
                neighbor_y, neighbor_x = current_y + dy, current_x + dx
                neighbor_pos = (neighbor_y, neighbor_x)

                # Validar a célula vizinha
                if neighbor_pos in visited or not is_valid(neighbor_pos):
                    continue

                # Calcular o custo do caminho até a célula vizinha
                tentative_g_cost = g_costs[(current_y, current_x)] + 1

                if (
                    neighbor_pos not in g_costs
                    or tentative_g_cost < g_costs[neighbor_pos]
                ):
                    g_costs[neighbor_pos] = tentative_g_cost
                    f_cost = tentative_g_cost + heuristic(
                        neighbor_y, neighbor_x, human_y, human_x
                    )
                    heappush(
                        open_set,
                        (f_cost, neighbor_y, neighbor_x, first_move or direction),
                    )
                    print(
                        f"Explorando ({neighbor_y}, {neighbor_x}) com custo {f_cost} e direção {first_move or direction}"
                    )

        # Se não houver caminho, retornar None
        return None

    # AI que procura os blocos mais próximos
    def astar1(self, world: dict, dirt_holes: dict) -> str:
        opponent_id = 0 if self.my_id == 1 else 1
        ai_pos = None
        human_pos = None
        dirt_hole_position = None
        target_pos = None

        # Localizar posições dos jogadores
        for coord, items in world.items():
            for item in items:
                if item[0] == "player" and item[2] == self.my_id:
                    ai_pos = coord
                elif item[0] == "player" and item[2] == opponent_id:
                    human_pos = coord

        # Procurar blocos não escavados
        for hole_id, hole in dirt_holes.items():
            if hole[2] == "covered":
                if not dirt_hole_position:
                    dirt_hole_position = []
                dirt_hole_position.append(hole[1])

        # Procurar a target
        if dirt_hole_position:
            # Encontrar bloco mais próximo
            target_pos = min(
                dirt_hole_position,
                key=lambda pos: abs(pos[0] - ai_pos[0]) + abs(pos[1] - ai_pos[1]),
            )
        elif human_pos:
            target_pos = human_pos
        else:
            return None

        ai_y, ai_x = ai_pos
        human_y, human_x = target_pos

        # Direções possíveis
        directions = {
            "UP": (0, -1),
            "DOWN": (0, 1),
            "LEFT": (-1, 0),
            "RIGHT": (1, 0),
        }

        # Função para verificar se uma célula é válida
        def is_valid(cell):
            y, x = cell
            # Verificar se a célula está dentro do mundo
            if (y, x) not in world:
                return False
            # Verificar se há um obstáculo
            for item in world[(y, x)]:
                if item[0] == "obst" and item[1] != "dirt_hole":
                    return False
            for hole_id, hole in dirt_holes.items():
                if hole[1] == (y, x):
                    if hole[2] == "dug":
                        return False
            return True

        # Função heurística (distância Manhattan)
        def heuristic(y1, x1, y2, x2):
            return abs(y1 - y2) + abs(x1 - x2)

        # Fila de prioridade para o algoritmo A*
        open_set = []
        heappush(
            open_set, (0, ai_y, ai_x, None)
        )  # (custo_total, y, x, movimento_inicial)

        # Custos conhecidos para cada célula
        g_costs = {ai_pos: 0}

        # Conjunto de células visitadas
        visited = set()

        close_to_hole = False
        while open_set:
            _, current_y, current_x, first_move = heappop(open_set)

            # Se chegarmos à posição do adversário, retornar o primeiro movimento
            if (current_y, current_x) == (human_y, human_x):
                print(
                    f"Chegou ao buraco em ({current_y}, {current_x}) com movimento {first_move}"
                )
                if close_to_hole == True:
                    if self.direction == UP:
                        direction_value = "UP"
                    elif self.direction == DOWN:
                        direction_value = "DOWN"
                    elif self.direction == LEFT:
                        direction_value = "LEFT"
                    elif self.direction == RIGHT:
                        direction_value = "RIGHT"
                    else:
                        direction = None
                    if (
                        ai_pos[0] + directions[direction_value][0] == target_pos[0]
                    ) and (ai_pos[1] + directions[direction_value][1] == target_pos[1]):
                        return "DIG"
                return first_move

            # Marcar a célula atual como visitada
            visited.add((current_y, current_x))

            # Explorar os vizinhos
            for direction, (dy, dx) in directions.items():
                neighbor_y, neighbor_x = current_y + dy, current_x + dx
                neighbor_pos = (neighbor_y, neighbor_x)

                # Validar a célula vizinha
                if neighbor_pos in visited or not is_valid(neighbor_pos):
                    continue

                # Calcular o custo do caminho até a célula vizinha
                tentative_g_cost = g_costs[(current_y, current_x)] + 1

                if (
                    neighbor_pos not in g_costs
                    or tentative_g_cost < g_costs[neighbor_pos]
                ):
                    g_costs[neighbor_pos] = tentative_g_cost
                    f_cost = tentative_g_cost + heuristic(
                        neighbor_y, neighbor_x, human_y, human_x
                    )
                    heappush(
                        open_set,
                        (f_cost, neighbor_y, neighbor_x, first_move or direction),
                    )
                    if f_cost == 1:
                        close_to_hole = True
                    print(
                        f"Explorando ({neighbor_y}, {neighbor_x}) com custo {f_cost} e direção {first_move or direction}"
                    )

        # Se não houver caminho, retornar None
        return None

    # AI que procura os blocos num raio do adversário
    def astar2(self, world: dict, dirt_holes: dict) -> str:
        opponent_id = 0 if self.my_id == 1 else 1
        ai_pos = None
        human_pos = None
        dirt_hole_position = None
        target_pos = None

        # Localizar posições dos jogadores
        for coord, items in world.items():
            for item in items:
                if item[0] == "player" and item[2] == self.my_id:
                    ai_pos = coord
                elif item[0] == "player" and item[2] == opponent_id:
                    human_pos = coord

        # Procurar blocos não escavados
        for hole_id, hole in dirt_holes.items():
            if hole[2] == "covered":
                if not dirt_hole_position:
                    dirt_hole_position = []
                dirt_hole_position.append(hole[1])

        # Distância de Manhattan
        def manhattan_distance(pos1, pos2):
            return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

        # Procurar a target
        if dirt_hole_position and human_pos:
            # Encontrar blocos escaváveis num raio de 2 unidades de distância do adversário
            nearby_dirt_holes = [
                pos
                for pos in dirt_hole_position
                if manhattan_distance(pos, human_pos) <= 2
            ]
            # Destes encontra o mais próximo de si
            if nearby_dirt_holes:
                target_pos = min(
                    nearby_dirt_holes, key=lambda pos: manhattan_distance(pos, ai_pos)
                )
            else:
                # Se não encontrar, persegue o adversário
                return self.astar_perseguir_jogador(world)
        else:
            return None

        ai_y, ai_x = ai_pos
        human_y, human_x = target_pos

        # Direções possíveis
        directions = {
            "UP": (0, -1),
            "DOWN": (0, 1),
            "LEFT": (-1, 0),
            "RIGHT": (1, 0),
        }

        # Função para verificar se uma célula é válida
        def is_valid(cell):
            y, x = cell
            # Verificar se a célula está dentro do mundo
            if (y, x) not in world:
                return False
            # Verificar se há um obstáculo
            for item in world[(y, x)]:
                if item[0] == "obst" and item[1] != "dirt_hole":
                    return False
            for hole_id, hole in dirt_holes.items():
                if hole[1] == (y, x):
                    if hole[2] == "dug":
                        return False
            return True

        # Função heurística (distância Manhattan)
        def heuristic(y1, x1, y2, x2):
            return abs(y1 - y2) + abs(x1 - x2)

        # Fila de prioridade para o algoritmo A*
        open_set = []
        heappush(
            open_set, (0, ai_y, ai_x, None)
        )  # (custo_total, y, x, movimento_inicial)

        # Custos conhecidos para cada célula
        g_costs = {ai_pos: 0}

        # Conjunto de células visitadas
        visited = set()

        close_to_hole = False
        while open_set:
            _, current_y, current_x, first_move = heappop(open_set)

            # Se chegarmos à posição do adversário, retornar o primeiro movimento
            if (current_y, current_x) == (human_y, human_x):
                print(
                    f"Chegou ao buraco em ({current_y}, {current_x}) com movimento {first_move}"
                )
                if close_to_hole == True:
                    if self.direction == UP:
                        direction_value = "UP"
                    elif self.direction == DOWN:
                        direction_value = "DOWN"
                    elif self.direction == LEFT:
                        direction_value = "LEFT"
                    elif self.direction == RIGHT:
                        direction_value = "RIGHT"
                    else:
                        direction = None
                    if (
                        ai_pos[0] + directions[direction_value][0] == target_pos[0]
                    ) and (ai_pos[1] + directions[direction_value][1] == target_pos[1]):
                        return "DIG"
                return first_move

            # Marcar a célula atual como visitada
            visited.add((current_y, current_x))

            # Explorar os vizinhos
            for direction, (dy, dx) in directions.items():
                neighbor_y, neighbor_x = current_y + dy, current_x + dx
                neighbor_pos = (neighbor_y, neighbor_x)

                # Validar a célula vizinha
                if neighbor_pos in visited or not is_valid(neighbor_pos):
                    continue

                # Calcular o custo do caminho até a célula vizinha
                tentative_g_cost = g_costs[(current_y, current_x)] + 1

                if (
                    neighbor_pos not in g_costs
                    or tentative_g_cost < g_costs[neighbor_pos]
                ):
                    g_costs[neighbor_pos] = tentative_g_cost
                    f_cost = tentative_g_cost + heuristic(
                        neighbor_y, neighbor_x, human_y, human_x
                    )
                    heappush(
                        open_set,
                        (f_cost, neighbor_y, neighbor_x, first_move or direction),
                    )
                    if f_cost == 1:
                        close_to_hole = True
                    print(
                        f"Explorando ({neighbor_y}, {neighbor_x}) com custo {f_cost} e direção {first_move or direction}"
                    )

        # Se não houver caminho, retornar None
        return None

    def update(self, gm: GameMech, stop: bool) -> str | None:
        """Função que processa uma ação do jogador

        :param gm: Mecânicas do Jogo
        :type gm: GameMech
        :param stop: Se deve ficar parado ou não
        :type stop: bool
        :return: None ou o nome do item encontrado num buraco de terra
        :rtype: str | None
        """
        if stop == True:
            self.dirty = 1
            return None

        world: dict = gm.get_world()
        dirt_holes: dict = gm.get_dirt_holes()

        # Escolhe o algoritmo a utilizar
        if self.algorithm == 1:
            result = self.astar1(world, dirt_holes)
        else:
            result = self.astar2(world, dirt_holes)

        if result == "UP":
            key = UP
        elif result == "DOWN":
            key = DOWN
        elif result == "LEFT":
            key = LEFT
        elif result == "RIGHT":
            key = RIGHT
        elif result == "DIG":
            key = 4
        else:
            key = None

        # Nova posição do jogador
        new_pos: tuple[int, int] = self.pos
        # Andar para a esquerda
        if key == LEFT:
            # Nova posição do jogador
            new_pos = gm.execute(self.my_id, LEFT)
            # Nova direção do jogador
            self.direction = LEFT
            # Novo sprite do jogador
            self.image = pg.image.load(
                f"Sprites/Player{self.my_id}/p{self.my_id}_l.png"
            )
            self.atualizar_sprite_direcao(new_pos)
        # Andar para a direita
        elif key == RIGHT:
            # Nova posição do jogador
            new_pos = gm.execute(self.my_id, RIGHT)
            # Nova direção do jogador
            self.direction = RIGHT
            # Novo sprite do jogador
            self.image = pg.image.load(
                f"Sprites/Player{self.my_id}/p{self.my_id}_r.png"
            )
            self.atualizar_sprite_direcao(new_pos)
        # Andar para cima
        elif key == UP:
            # Nova posição do jogador
            new_pos = gm.execute(self.my_id, UP)
            # Nova direção do jogador
            self.direction = UP
            # Novo sprite do jogador
            self.image = pg.image.load(
                f"Sprites/Player{self.my_id}/p{self.my_id}_b.png"
            )
            self.atualizar_sprite_direcao(new_pos)
        # Andar para baixo
        elif key == DOWN:
            # Nova posição do jogador
            new_pos = gm.execute(self.my_id, DOWN)
            # Nova direção do jogador
            self.direction = DOWN
            # Novo sprite do jogador
            self.image = pg.image.load(
                f"Sprites/Player{self.my_id}/p{self.my_id}_f.png"
            )
            self.atualizar_sprite_direcao(new_pos)
        # Escavar um buraco
        elif key == self.keys[4]:
            # Verifica se encontrou algo
            item_found: str | None = gm.dig(self.my_id)
            # Se encontrou um item
            if item_found is not None:
                # Se estiver virado para a esquerda
                if self.direction == LEFT:
                    # Atualiza o sprite do jogador
                    self.image = pg.image.load(
                        f"Sprites/Player{self.my_id}/p{self.my_id}_l_pa.png"
                    )
                    self.atualizar_sprite_escavar()
                    self.rect = pg.rect.Rect(
                        ((self.pos[0] - 1) * self.size, self.pos[1] * self.size),
                        self.image.get_size(),
                    )
                    self.dirty = 1
                    # Retorna o item encontrado
                    return item_found
                # Se estiver virado para a direita
                elif self.direction == RIGHT:
                    # Atualiza o sprite do jogador
                    self.image = pg.image.load(
                        f"Sprites/Player{self.my_id}/p{self.my_id}_r_pa.png"
                    )
                    self.atualizar_sprite_escavar()
                    self.rect = pg.rect.Rect(
                        (self.pos[0] * self.size, self.pos[1] * self.size),
                        self.image.get_size(),
                    )
                    self.dirty = 1
                    # Retorna o item encontrado
                    return item_found
                # Se estiver virado para cima
                elif self.direction == UP:
                    # Atualiza o sprite do jogador
                    self.image = pg.image.load(
                        f"Sprites/Player{self.my_id}/p{self.my_id}_b_pa.png"
                    )
                    self.atualizar_sprite_escavar()
                    self.rect = pg.rect.Rect(
                        (self.pos[0] * self.size, (self.pos[1] - 1) * self.size),
                        self.image.get_size(),
                    )
                    self.dirty = 1
                    # Retorna o item encontrado
                    return item_found
                # Se estiver virado para baixo
                elif self.direction == DOWN:
                    # Atualiza o sprite do jogador
                    self.image = pg.image.load(
                        f"Sprites/Player{self.my_id}/p{self.my_id}_f_pa.png"
                    )
                    self.atualizar_sprite_escavar()
                    self.rect = pg.rect.Rect(
                        (self.pos[0] * self.size, self.pos[1] * self.size),
                        self.image.get_size(),
                    )
                    self.dirty = 1
                    # Retorna o item encontrado
                    return item_found
        # Posição do jogador é atualizada
        self.pos = new_pos
        # Manter visível o sprite
        self.dirty = 1

    def atualizar_sprite_direcao(self, new_pos: tuple[int, int]) -> None:
        """Função que atualiza o sprite do jogador ao andar ou virar

        :param new_pos: Nova posição do jogador
        :type new_pos: tuple[int, int]
        """
        self.image = pg.transform.scale(self.image, self.new_size)
        self.rect = pg.rect.Rect(
            (new_pos[0] * self.size, new_pos[1] * self.size), self.image.get_size()
        )

    def atualizar_sprite_escavar(self) -> None:
        """Função que atualiza o sprite do jogador ao escavar um buraco"""
        image_size: tuple[int, int] = (
            int(self.image.get_size()[0] * self.size_rate),
            int(self.image.get_size()[1] * self.size_rate),
        )
        self.image = pg.transform.scale(self.image, image_size)
