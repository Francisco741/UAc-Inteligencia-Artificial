import pygame as pg
from time import sleep
from gamemech import GameMech
from player1 import Player
from wall import Wall
from dirt import Dirt
from grass import Grass
from dirt_hole import DirtHole
from obstacle import Obstacle
from tent import Tent
from water import Water


class Game(object):
    def __init__(self, gm: GameMech, size: int = 50) -> None:
        """Classe com toda a parte visual do jogo

        :param gm: Mecânicas do Jogo
        :type gm: GameMech
        :param size: Tamanho de cada quadrícula, com valor default 50
        :type size: int, optional
        """
        # Mecânicas do Jogo
        self.gm: GameMech = gm
        # Mapa do jogo selecionado
        self.game_map: list[list[int]] = self.gm.get_map()
        # Dimensões do mapa
        self.width: int = len(self.game_map[0]) * size
        self.height: int = len(self.game_map) * size
        # Ecrã do jogo
        self.screen: pg.Surface = pg.display.set_mode((self.width, self.height + 40))
        # ícone do jogo na janela
        pg.display.set_icon(pg.image.load("Other/icon.png"))
        # Título do jogo na janela
        pg.display.set_caption("OssoSaurus: Desenterrando o Passado")
        # Background do jogo
        self.background: pg.Surface = pg.Surface(self.screen.get_size())
        self.background: pg.Surface = self.background.convert()
        self.background.fill((56, 136, 48))
        self.screen.blit(self.background, (0, 0))
        # Fonte usada na mensagem de espera
        self.font: pg.font.Font = pg.font.Font("Other/PressStart2P-Regular.ttf", 28)
        # Mensagem de espera pelo oponente
        waiting_message = self.font.render(
            "Insirem os seus nomes", True, (255, 255, 255)
        )
        self.screen.blit(waiting_message, (80, 300, self.width, self.height + 40))
        # Tamanho da grelha do jogo
        self.grid_size: int = size
        # Desenha a grelha do jogo (desativada por questões de estética)
        # self.draw_grid(self.width, self.height, self.grid_size, (153, 135, 64))
        # Fonte usada no GUI
        self.font: pg.font.Font = pg.font.Font("Other/PressStart2P-Regular.ttf", 13)
        # Música selecionada
        self.music: int = self.gm.get_music()
        # Música do jogo
        pg.mixer_music.load(f"Music/main_song{self.music}.mp3")
        pg.mixer_music.set_volume(0.4)
        pg.mixer_music.play(-1)
        # Relógio do jogo
        self.clock: pg.time.Clock = pg.time.Clock()
        # Número de Jogadores
        self.nr_players: int = 2
        # Grupo com os jogadores no jogo
        self.players = pg.sprite.LayeredDirty()
        # Update ao display
        pg.display.update()

    def draw_gui(self) -> None:
        """Função para desenhar o GUI do jogo"""
        # Cor de fundo e posição do GUI
        self.screen.fill((56, 136, 48), (0, self.height, self.width, 40))
        # Espaço entre os nomes dos jogadoes
        space: int = 100
        # Escreve os nomes dos jogadores no GUI e a sua pontuação
        for player in self.players:
            player_points: pg.Surface = self.font.render(
                f"{player.name}: {player.points}", True, (255, 255, 255)
            )
            self.screen.blit(player_points, (space, self.height + 15))
            space += 400

    def end_screen(self, winners: list[str]) -> None:
        """Função para desenhar o ecrã de fim do jogo

        :param winners: Nome do vencedor ou vencedores (em caso de empate) do jogo
        :type winners: list[str]
        """
        # Cor de fundo e posição do ecrã de fim do jogo
        self.screen.fill(
            (56, 136, 48),
            (10, 10, 880, 70),
        )
        # Escreve o nome do vencedor ou vencedores (em caso de empate) do jogo
        list_winners: pg.Surface = self.font.render(
            f"Vencedor: {' & '.join(winners)}", True, (255, 255, 255)
        )
        self.screen.blit(list_winners, (40, 40, self.width, self.height))
        # Update ao display
        pg.display.update()
        pg.mixer_music.load("Music/win.mp3")
        pg.mixer_music.set_volume(0.7)
        pg.mixer_music.play(1)

    def play_sound(self, sound: pg.mixer.Sound, volume: float) -> None:
        """Função para reproduzir um som

        :param sound: Som a ser reproduzido
        :type sound: pg.mixer.Sound
        :param volume: Volume do som
        :type volume: float
        """
        # Altera o volume do som
        sound.set_volume(volume)
        # Reproduz o som
        sound.play()

    def draw_grid(self, width: int, height: int, size: int, colour: tuple) -> None:
        """Desenha uma grelha no ecrã do jogo

        :param width: Dimensão no eixo dos xx da janela
        :type width: int
        :param height: Dimensão no eixo dos yy da janela
        :type height: int
        :param size: Tamanho da grelha
        :type size: int
        :param colour: Cor da grelha
        :type colour: tuple
        """
        # Desenha as linhas horizontais
        for pos in range(0, height, size):
            pg.draw.line(self.screen, colour, (0, pos), (width, pos))
        # Desenha as linhas verticais
        for pos in range(0, width, size):
            pg.draw.line(self.screen, colour, (pos, 0), (pos, height))

    def create_player(self, size: int) -> None:
        """Função para criar um jogador

        :param size: Tamanho do sprite do jogador
        :type size: int
        """
        # Pede ao utilizador o seu nome de jogador
        name: str = str(input("Insira o seu nome (máximo 20 caracteres): "))
        # Pede o nome novamente se ultrapassar o limite de caracteres
        while len(name) > 20:
            name: str = str(input("Nome demasiado grande. Insira um novo nome: "))
        # Adiciona o jogador ao jogo
        (id, pos) = self.gm.add_player(name)
        print("Player ", name, " created with id: ", id)
        new_player: Player = Player(id, name, pos[0], pos[1], size, 0, self.players)
        self.players.add(new_player)

    def create_map_objects(self, size: int) -> None:
        """Função para criar objetos do mundo

        :param size: Tamanho dos sprites dos objetos do mundo
        :type size: int
        """
        # Grupos com os objetos do mundo
        self.dirts = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.grasses = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()
        self.tents = pg.sprite.Group()
        self.waters = pg.sprite.Group()
        # Itera sobre o mapa para criar os objetos na posição correta
        for i in range(len(self.game_map)):
            for j in range(len(self.game_map[i])):
                if self.game_map[i][j] == 0:
                    dirt: Dirt = Dirt(
                        size * j,
                        size * i,
                        size,
                        self.dirts,
                    )
                    self.dirts.add(dirt)
                if self.game_map[i][j] == 1:
                    wall: Wall = Wall(
                        size * j,
                        size * i,
                        size,
                        self.walls,
                    )
                    self.walls.add(wall)
                if self.game_map[i][j] == 2:
                    grass: Grass = Grass(
                        size * j,
                        size * i,
                        size,
                        self.grasses,
                    )
                    self.grasses.add(grass)
                if self.game_map[i][j] == 4:
                    obstacle: Obstacle = Obstacle(
                        size * j,
                        size * i,
                        size,
                        self.obstacles,
                    )
                    self.obstacles.add(obstacle)
                if self.game_map[i][j] == 5:
                    tent: Tent = Tent(
                        size * j,
                        size * i,
                        size,
                        self.tents,
                    )
                    self.tents.add(tent)

                if self.game_map[i][j] == 6:
                    water: Water = Water(
                        size * j,
                        size * i,
                        size,
                        self.waters,
                    )
                    self.waters.add(water)

    def get_dirt_holes(self, dirt_hole_size: int) -> None:
        """Função para criar pedaços de terra escaváveis no mundo

        :param dirt_hole_size: Tamanho dos sprites dos pedaços de terra escaváveis
        :type dirt_hole_size: int
        """
        # Dicionário com os pedaços de terra escaváveis
        holes: dict = self.gm.get_dirt_holes()
        # Grupo com os pedaços de terra escaváveis
        self.dirt_holes = pg.sprite.Group()
        # Itera sobre o dicionário para adicionar os pedaços de terra ao mundo
        for id, atributes in holes.items():
            dirt_hole: DirtHole = DirtHole(
                id,
                dirt_hole_size * atributes[1][0],
                dirt_hole_size * atributes[1][1],
                dirt_hole_size,
                self.dirt_holes,
            )
            self.dirt_holes.add(dirt_hole)

    def update_world(self) -> None:
        """Função para atualizar o estado do mundo"""
        # Dicionário com os pedaços de terra escaváveis
        holes: dict = self.gm.get_dirt_holes()
        # Itera sobre o grupo para verificar se algum buraco foi escavado
        for dh in self.dirt_holes:
            # Se um buraco foi escavado
            if holes[dh.hole_id][2] == "dug" and dh.state == "covered":
                # Altera o seu estado para "escavado"
                dh.state = "dug"
                # Reproduz um som
                self.play_sound(pg.mixer.Sound("Music/dig.mp3"), 1)
                # Verifica qual item foi encontrado no buraco e altera o seu sprite e
                # reproduz um som consoante o tipo de item
                if holes[dh.hole_id][3] == "empty":
                    dh.dug()
                elif holes[dh.hole_id][3] == "bone":
                    dh.bone_dug()
                    self.play_sound(pg.mixer.Sound("Music/bone.mp3"), 0.5)
                elif holes[dh.hole_id][3] == "diamond":
                    dh.diamond_dug()
                    self.play_sound(pg.mixer.Sound("Music/diamond.mp3"), 1)
                elif holes[dh.hole_id][3] == "skull":
                    dh.skull_dug()
                    self.play_sound(pg.mixer.Sound("Music/skull.mp3"), 0.5)
                elif holes[dh.hole_id][3] == "potion":
                    dh.potion_dug()
                    self.play_sound(pg.mixer.Sound("Music/potion.mp3"), 0.4)
                elif holes[dh.hole_id][3] == "fish":
                    dh.fish_dug()
                    self.play_sound(pg.mixer.Sound("Music/bonefish.mp3"), 0.5)
                elif holes[dh.hole_id][3] == "coin":
                    dh.coin_dug()
                    self.play_sound(pg.mixer.Sound("Music/gold.mp3"), 0.5)
                elif holes[dh.hole_id][3] == "chalice":
                    dh.chalice_dug()
                    self.play_sound(pg.mixer.Sound("Music/gold.mp3"), 0.5)
                elif holes[dh.hole_id][3] == "crown":
                    dh.crown_dug()
                    self.play_sound(pg.mixer.Sound("Music/gold.mp3"), 0.5)

    def run(self) -> None:
        """Inicia o jogo e vai atualizando o ecrã até o jogo terminar"""
        # Cria os objetos do mapa
        self.create_map_objects(self.grid_size)
        # Desenha os sprites dos objetos do mapa
        self.dirts.draw(self.screen)
        self.walls.draw(self.screen)
        self.grasses.draw(self.screen)
        self.obstacles.draw(self.screen)
        self.tents.draw(self.screen)
        self.waters.draw(self.screen)
        # Cria os pedaços de terra escaváveis
        self.get_dirt_holes(self.grid_size)
        # Desenha os sprites dos pedaços de terra escaváveis
        self.dirt_holes.draw(self.screen)
        # Cria os jogadores
        for _ in range(self.nr_players):
            self.create_player(self.grid_size)
        # Variável que sinaliza se o jogo terminou ou não
        end: bool = False
        # Loop do jogo que corre enquanto não terminar
        while not end:
            # Relógio do jogo
            self.clock.tick(10)
            # Tecla para fechar o jogo
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    end = True
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    end = True
            # Faz update da posição dos jogadores e se estes escavaram um buraco retorna o item escavado
            for player in self.players:
                item: str | None = player.update(self.gm)
                # Atualiza a pontuação do jogador conforme o item escavado
                if item == "bone":
                    player.points += 10
                elif item == "diamond":
                    player.points += 50
                elif item == "fish":
                    player.points += 5
                elif item == "coin":
                    player.points += 20
                elif item == "chalice":
                    player.points += 30
                elif item == "crown":
                    player.points += 40
            # Faz update do mundo
            self.update_world()
            # Desenha os sprites dos pedaços de terra escaváveis novamente
            self.dirt_holes.draw(self.screen)
            # Desenha os sprites dos blocos de terra novamente
            self.dirts.draw(self.screen)
            # Desenha os sprites dos jogadores novamente
            self.players.draw(self.screen)
            # Desenha a grelha novamente
            # self.draw_grid(self.width, self.height, self.grid_size, (153, 135, 64))
            # Desenha e atualiza o GUI
            self.draw_gui()
            # Update ao display
            pg.display.update()
            # Verifica se o jogo terminou
            winners: list = self.gm.end()
            # Se o jogo terminou
            if winners is not None:
                # Desenha o ecrã de fim do jogo onde mostra o vencedor
                self.end_screen(winners)
                sleep(6)
                # Termina o jogo
                end = True
        return None
