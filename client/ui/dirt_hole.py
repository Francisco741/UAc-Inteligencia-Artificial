import pygame as pg


class DirtHole(pg.sprite.Sprite):
    def __init__(
        self, hole_id: int, pos_x: int, pos_y: int, size: int, *groups
    ) -> None:
        """Classe que representa um pedaço de terra escavável

        :param hole_id: ID do pedaço de terra escavável
        :type hole_id: int
        :param pos_x: posição x do pedaço de terra escavável
        :type pos_x: int
        :param pos_y: posição y do pedaço de terra escavável
        :type pos_y: int
        :param size: tamanho do pedaço de terra escavável
        :type size: int
        """
        super().__init__(*groups)
        self.hole_id: int = hole_id
        # Estado do pedaço de terra escavável
        self.state = "covered"
        # Sprite do pedaço de terra por escavar
        self.image = pg.image.load("Sprites/World/terra_escavavel.png")
        initial_size: tuple[int, int] = self.image.get_size()
        size_rate: float = size / initial_size[0]
        self.new_size: tuple[int, int] = (
            int(self.image.get_size()[0] * size_rate),
            int(self.image.get_size()[1] * size_rate),
        )
        self.image = pg.transform.scale(self.image, self.new_size)
        self.rect = pg.rect.Rect((pos_x, pos_y), self.image.get_size())
        self.pos_x_grid = int(pos_x / size)
        self.pos_y_grid = int(pos_y / size)

    def get_pos_x(self) -> int:
        """Função que retorna a posição x do pedaço de terra escavável

        :return: Posição x do pedaço de terra escavável
        :rtype: int
        """
        return self.pos_x_grid

    def get_pos_y(self) -> int:
        """Função que retorna a posição y do pedaço de terra escavável

        :return: Posição y do pedaço de terra escavável
        :rtype: int
        """
        return self.pos_y_grid

    def get_pos(self) -> list:
        """Função que retorna a posição do pedaço de terra escavável

        :return: Posição do pedaço de terra escavável
        :rtype: list
        """
        return [self.pos_x_grid, self.pos_y_grid]

    def dug(self) -> None:
        """Altera o sprite para um buraco de terra vazio"""
        self.image = pg.image.load("Sprites/World/terra_escavada.png")
        self.image = pg.transform.scale(self.image, self.new_size)

    def bone_dug(self) -> None:
        """Altera o sprite para um buraco de terra com um osso"""
        self.image = pg.image.load("Sprites/World/terra_escavada_osso.png")
        self.image = pg.transform.scale(self.image, self.new_size)

    def diamond_dug(self) -> None:
        """Altera o sprite para um buraco de terra com um diamante"""
        self.image = pg.image.load("Sprites/World/terra_escavada_diamante.png")
        self.image = pg.transform.scale(self.image, self.new_size)

    def skull_dug(self) -> None:
        """Altera o sprite para um buraco de terra com uma caveira"""
        self.image = pg.image.load("Sprites/World/terra_escavada_caveira.png")
        self.image = pg.transform.scale(self.image, self.new_size)

    def potion_dug(self) -> None:
        """Altera o sprite para um buraco de terra com uma poção"""
        self.image = pg.image.load("Sprites/World/terra_escavavel_potion.png")
        self.image = pg.transform.scale(self.image, self.new_size)

    def fish_dug(self) -> None:
        """Altera o sprite para um buraco de terra com uma espinha de peixe"""
        self.image = pg.image.load("Sprites/World/terra_escavada_fishbone.png")
        self.image = pg.transform.scale(self.image, self.new_size)

    def coin_dug(self) -> None:
        """Altera o sprite para um buraco de terra com moedas"""
        self.image = pg.image.load("Sprites/World/terra_escavada_moedas.png")
        self.image = pg.transform.scale(self.image, self.new_size)

    def chalice_dug(self) -> None:
        """Altera o sprite para um buraco de terra com um cálice"""
        self.image = pg.image.load("Sprites/World/terra_escavada_taca.png")
        self.image = pg.transform.scale(self.image, self.new_size)

    def crown_dug(self) -> None:
        """Altera o sprite para um buraco de terra com uma coroa"""
        self.image = pg.image.load("Sprites/World/terra_escavada_coroa.png")
        self.image = pg.transform.scale(self.image, self.new_size)
