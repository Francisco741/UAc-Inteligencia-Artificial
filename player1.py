import pygame as pg
from gamemech import GameMech
from constants import UP, DOWN, LEFT, RIGHT, PLAYER_KEYS, PLAYER_REVERSE_KEYS


class Player(pg.sprite.DirtySprite):
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
        self.keys: tuple[int, int, int, int, int] = PLAYER_KEYS[self.my_id]
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

    def update(self, gm: GameMech) -> str | None:
        """Função que processa uma ação do jogador

        :param gm: Mecânicas do Jogo
        :type gm: GameMech
        :return: None ou o nome do item encontrado num buraco de terra
        :rtype: str | None
        """
        # Tecla pressionada
        key = pg.key.get_pressed()
        # Nova posição do jogador
        new_pos: tuple[int, int] = self.pos
        # Andar para a esquerda
        if key[self.keys[0]]:
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
        elif key[self.keys[1]]:
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
        elif key[self.keys[2]]:
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
        elif key[self.keys[3]]:
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
        elif key[self.keys[4]]:
            # Verifica se encontrou algo
            item_found: str | None = gm.dig(self.my_id)
            # Se encontrou um item
            if item_found is not None:
                # Se encontrou uma caveira reverte os controlos
                if item_found == "skull":
                    self.reverse_keys()
                # Se encontrou uma poçao os controlos voltam à normalidade
                elif item_found == "potion":
                    self.fix_keys()
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

    def reverse_keys(self) -> None:
        """Função que reverte os controlos do jogador"""
        self.keys = PLAYER_REVERSE_KEYS[self.my_id]

    def fix_keys(self) -> None:
        """Função que traz os controlos do jogador de volta à normalidade"""
        self.keys = PLAYER_KEYS[self.my_id]
