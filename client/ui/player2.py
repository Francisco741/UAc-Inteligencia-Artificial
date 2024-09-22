import pygame as pg
from ui import UP, DOWN, LEFT, RIGHT, PLAYER_KEYS


class PlayerExtra(pg.sprite.DirtySprite):
    def __init__(
        self,
        nr_player: int,
        name: str,
        pos_x: int,
        pos_y: int,
        size: int,
        points: int = 0,
        *groups,
    ) -> None:
        """Classe que representa um Jogador Extra

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
        self.keys: tuple[int, int, int, int, int] = PLAYER_KEYS
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
        self.pos: tuple = (pos_x, pos_y)

    def get_size(self) -> tuple[int, int]:
        """Função que retorna o tamanho do jogador

        :return: Tamanho do jogador
        :rtype: tuple[int, int]
        """
        return self.new_size

    def set_pos(self, pos: list) -> None:
        """Função para definir a posição do jogdor

        :param pos: Posição do jogdor a ser definida
        :type pos: list
        """
        self.rect.x = pos[0] * self.size
        self.rect.y = pos[1] * self.size

    def set_points(self, points: int) -> None:
        """Função para definir os pontos do jogador

        :param points: Pontos do jogador a serem definidos
        :type points: int
        """
        self.points = points

    def get_id(self) -> int:
        """Função que retorna o ID do jogador

        :return: ID do jogador
        :rtype: int
        """
        return self.my_id

    def update(self) -> None:
        """Função que mantém o sprite do jogador extra visível"""
        # Manter visível o sprite
        self.dirty = 1

    def player_sprite_direction(self, new_pos: tuple[int, int], direction: int) -> None:
        """Função que atualiza o sprite do jogador ao andar ou virar

        :param new_pos: Nova posição do jogador
        :type new_pos: tuple[int, int]
        :param direction: Direção do jogador
        :type direction: int
        """
        self.rect.x = new_pos[0] * self.size
        self.rect.y = new_pos[1] * self.size
        # Se a direção for 'esquerda'
        if direction == LEFT:
            # Atualiza o sprite do jogador
            self.image = pg.image.load(
                f"Sprites/Player{self.my_id}/p{self.my_id}_l.png"
            )
            self.atualizar_sprite_direcao(new_pos)
        # Se a direção for 'direita'
        elif direction == RIGHT:
            # Atualiza o sprite do jogador
            self.image = pg.image.load(
                f"Sprites/Player{self.my_id}/p{self.my_id}_r.png"
            )
            self.atualizar_sprite_direcao(new_pos)
        # Se a direção for 'cima'
        elif direction == UP:
            # Atualiza o sprite do jogador
            self.image = pg.image.load(
                f"Sprites/Player{self.my_id}/p{self.my_id}_b.png"
            )
            self.atualizar_sprite_direcao(new_pos)
        # Se a direção for 'baixo'
        elif direction == DOWN:
            # Atualiza o sprite do jogador
            self.image = pg.image.load(
                f"Sprites/Player{self.my_id}/p{self.my_id}_f.png"
            )
            self.atualizar_sprite_direcao(new_pos)
        # Manter visível o sprite
        self.dirty = 1

    def player_dig_direction(self, new_pos: tuple[int, int], direction: int) -> None:
        # Se a direção for 'esquerda'
        if direction == LEFT:
            # Atualiza o sprite do jogador
            self.image = pg.image.load(
                f"Sprites/Player{self.my_id}/p{self.my_id}_l_pa.png"
            )
            self.atualizar_sprite_escavar()
            self.rect = pg.rect.Rect(
                ((new_pos[0] - 1) * self.size, new_pos[1] * self.size),
                self.image.get_size(),
            )
        # Se a direção for 'direita'
        elif direction == RIGHT:
            # Atualiza o sprite do jogador
            self.image = pg.image.load(
                f"Sprites/Player{self.my_id}/p{self.my_id}_r_pa.png"
            )
            self.atualizar_sprite_escavar()
            self.rect = pg.rect.Rect(
                (new_pos[0] * self.size, new_pos[1] * self.size),
                self.image.get_size(),
            )
        # Se a direção for 'cima'
        elif direction == UP:
            # Atualiza o sprite do jogador
            self.image = pg.image.load(
                f"Sprites/Player{self.my_id}/p{self.my_id}_b_pa.png"
            )
            self.atualizar_sprite_escavar()
            self.rect = pg.rect.Rect(
                (new_pos[0] * self.size, (new_pos[1] - 1) * self.size),
                self.image.get_size(),
            )
        # Se a direção for 'baixo'
        elif direction == DOWN:
            # Atualiza o sprite do jogador
            self.image = pg.image.load(
                f"Sprites/Player{self.my_id}/p{self.my_id}_f_pa.png"
            )
            self.atualizar_sprite_escavar()
            self.rect = pg.rect.Rect(
                (new_pos[0] * self.size, new_pos[1] * self.size),
                self.image.get_size(),
            )
        # Manter visível o sprite
        self.dirty = 1

    def atualizar_sprite_direcao(self, new_pos) -> None:
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
