import pygame
import random

colors = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 125, 0),
    (255, 0, 125),
    (0, 125, 255),
    (125, 0, 255),
    (0, 255, 125),
    (125, 255, 0)
]


class Figure:
    x = 0
    y = 0

    # main list is list of figures
    # inner lists store rotation
    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[0, 1, 5, 6], [1, 4, 5, 8]],
        [[0, 4, 5, 9], [1, 2, 4, 5]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],]

    # in the constructor we select the TYPE and COLOUR of figure randomly
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0

    # returns the figure image chosen randomly
    def image(self):
        return self.figures[self.type][self.rotation]

    # rotates the figure image (circular method)
    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])


class Tetris:
    level = 2
    score = 0
    state = "start"  # if game is still being played or not
    field = []  # game field filled with 0s and colours of fallen blocks
    height = 0
    width = 0
    x = 150
    y = 120
    zoom = 20
    figure = None

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "start"
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def new_figure(self):
        self.figure = Figure(3, 0)

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if (i + self.figure.y > self.height - 1) or (j + self.figure.x > self.width - 1) or (j + self.figure.x < 0) or (self.field[i + self.figure.y][j + self.figure.x] > 0):
                        intersection = True
        return intersection

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines * 10

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation


# initialize game engine
pygame.init()
#initialize mixer engine
pygame.mixer.init()


# define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

size = (500, 600)
screen = pygame.display.set_mode(size)
#bg = pygame.image.load('purple1.jpg').convert()


pygame.display.set_caption("Tetris")

# loop until user clicks the close button.
done = False
clock = pygame.time.Clock()
fps = 60
game = Tetris(20, 10)
counter = 0

pressing_down = False

while not done:
    if game.figure is None:
        game.new_figure()
    counter += 1
    if counter > 100000:
        counter = 0

    # load sound
    #pygame.mixer.music.load('tetris_theme.mp3')
    #pygame.mixer.music.set_volume(0.8)
    #pygame.mixer.music.play()

    if counter % (fps // game.level // 2) == 0 or pressing_down:
        if game.state == "start":
            game.go_down()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                game.go_side(-1)
            if event.key == pygame.K_RIGHT:
                game.go_side(1)
            if event.key == pygame.K_SPACE:
                game.go_space()
            if event.key == pygame.K_ESCAPE:
                game.__init__(20, 10)

    if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False

    screen.fill(BLACK)

    # draw grid and figures
    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, colors[game.field[i][j]],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    pygame.draw.rect(screen, colors[game.figure.color],
                                     [game.x + game.zoom * (j + game.figure.x) + 1,
                                      game.y + game.zoom * (i + game.figure.y) + 1,
                                      game.zoom - 2, game.zoom - 2])

    font = pygame.font.Font('tetris_font.ttf', 45)
    font1 = pygame.font.Font('tetris_font.ttf', 30)
    font2 = pygame.font.Font('font2.otf', 25)
    font3 = pygame.font.Font('font2.otf', 60)
    
    text_tetris = font.render("TETRIS", True, (150, 0, 255))
    text_score = font1.render("Score: " + str(game.score), True, WHITE)
    #text_names = font2.render("By Aarti", True, (200, 0, 255))

    text_game_over = font3.render("Game Over", True, (0, 200, 200), BLACK)
    text_game_over1 = font3.render("Press ESC", True, (255, 0, 100), BLACK)

    screen.blit(text_tetris, [165, 20])
    #screen.blit(text_names, [150, 70])
    screen.blit(text_score, [180, 530])
    if game.state == "gameover":
        screen.blit(text_game_over, [120, 250])
        screen.blit(text_game_over1, [120, 310])

    pygame.display.flip()
    clock.tick(40)

pygame.quit()
