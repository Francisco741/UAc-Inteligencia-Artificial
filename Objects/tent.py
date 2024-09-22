import pygame as pg


class Tent(pg.sprite.Sprite):
    def __init__(self, pos_x: int, pos_y: int, size: int, *groups) -> None:
        """Classe que representa uma tenda

        :param pos_x: posição x da tenda
        :type pos_x: int
        :param pos_y: posição y da tenda
        :type pos_y: int
        :param size: tamanho da tenda
        :type size: int
        """
        super().__init__(*groups)
        # Sprite da tenda
        self.image = pg.image.load("Sprites/World/tenda.png")
        initial_size: tuple[int, int] = self.image.get_size()
        size_rate: float = size / initial_size[0]
        self.new_size: tuple[int, int] = (
            int(self.image.get_size()[0] * size_rate * 2),
            int(self.image.get_size()[1] * size_rate * 2),
        )
        self.image = pg.transform.scale(self.image, self.new_size)
        self.rect = pg.rect.Rect((pos_x, pos_y), self.image.get_size())

    def get_size(self) -> tuple[int, int]:
        """Função que retorna o tamanho da tenda

        :return: Tamanho da tenda
        :rtype: tuple[int, int]
        """
        return self.new_size
