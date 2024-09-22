import pygame as pg
from random import randint


class Obstacle(pg.sprite.Sprite):
    def __init__(self, pos_x: int, pos_y: int, size: int, *groups) -> None:
        """Classe que representa um obstáculo

        :param pos_x: posição x do obstáculo
        :type pos_x: int
        :param pos_y: posição y do obstáculo
        :type pos_y: int
        :param size: tamanho do obstáculo
        :type size: int
        """
        super().__init__(*groups)
        # Seleciona aleatóriamente o sprite do obstáculo
        self.image = self.random_sprite()
        initial_size: tuple[int, int] = self.image.get_size()
        size_rate: float = size / initial_size[0]
        self.new_size: tuple[int, int] = (
            int(self.image.get_size()[0] * size_rate),
            int(self.image.get_size()[1] * size_rate),
        )
        self.image = pg.transform.scale(self.image, self.new_size)
        self.rect = pg.rect.Rect((pos_x, pos_y), self.image.get_size())

    def random_sprite(self) -> pg.Surface:
        """Função que seleciona aleatóriamente o sprite do obstáculo

        :return: Sprite do obstáculo
        :rtype: pg.Surface
        """
        sprite: int = randint(0, 1)
        if sprite == 0:
            return pg.image.load("Sprites/World/pedra.png")
        elif sprite == 1:
            return pg.image.load("Sprites/World/cacto.png")

    def get_size(self) -> tuple[int, int]:
        """Função que retorna o tamanho do obstáculo

        :return: Tamanho do obstáculo
        :rtype: tuple[int, int]
        """
        return self.new_size
