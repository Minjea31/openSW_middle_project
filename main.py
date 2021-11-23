import pygame
import random
import sys
from pygame.locals import *

pygame.init()
fps_time = pygame.time.Clock()

# pygame.mixer.music.load('data/music/background_music.mp3')
# pygame.mixer.music.play(-1)


pygame.display.set_caption('🚢BattleShip')
pixel_x = 800
pixel_y = 800
screen = pygame.display.set_mode((pixel_x, pixel_y))

ocean = pygame.image.load("data/background/ocean.png")
ocean = pygame.transform.scale(ocean, (pixel_x, pixel_y))
cloud = pygame.image.load("data/background/cloud.png")
cloud = pygame.transform.scale(cloud, (pixel_x, pixel_y))
grid = pygame.image.load("data/grid/grid.png")
grid = pygame.transform.scale(grid, (600, 600))


class make_cell:
    def __init__(self):
        self.burning = False
        self.ship = False
        self.boundary = False
        self.dot = False
        self.empty = pygame.image.load("data/Empty.png")
        self.empty = pygame.transform.scale(self.empty, (600 / 8, 600 / 8))
        self.empty_rect = pygame.Rect(self.empty.get_rect())
        self.aim = pygame.image.load("data/aim/aim.png")
        self.aim = pygame.transform.scale(self.aim, (600 / 8, 600 / 8))
        self.aim_rect = pygame.Rect(self.aim.get_rect())
        self.aim_unclicked = pygame.image.load("data/aim/aim_unclicked.png")
        self.aim_unclicked = pygame.transform.scale(self.aim_unclicked, (600 / 8, 600 / 8))
        self.aim_unclicked_rect = pygame.Rect(self.aim_unclicked.get_rect())
        self.clicked = False

    def blit(self, position):
        global boom_position_step_clicked
        self.empty_rect.left = position[0]
        self.empty_rect.top = position[1]
        screen.blit(self.empty, self.empty_rect)
        if self.clicked:
            self.aim_rect.left = position[0]
            self.aim_rect.top = position[1]
            screen.blit(self.aim, self.aim_rect)

        if not boom_position_step_clicked:
            return self.check_click(position)
        else:
            return True

    def check_click(self, position):
        mouse_pos = pygame.mouse.get_pos()
        if self.empty_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True

            else:
                if not self.clicked:
                    self.aim_unclicked_rect.left = position[0]
                    self.aim_unclicked_rect.top = position[1]
                    screen.blit(self.aim_unclicked, self.aim_unclicked_rect)
        return self.clicked


cell = [[make_cell() for col in range(8)] for row in range(8)]


class make_ship:
    def __init__(self, type_size):
        way = ['width', 'depth']
        self.size = type_size
        self.way = random.choice(way)
        self.ship_position = []
        self.boundary_position = []
        self.ship_showing = False

        self.image = pygame.image.load("data/ship/ship.png")
        self.image = pygame.transform.scale(self.image, (600 / 8, 600 / 8 * self.size))

        if self.way is 'width':
            self.image = pygame.transform.rotate(self.image, 90)
            self.image = pygame.transform.scale(self.image, (600 / 8 * self.size, 600 / 8))

    def put(self, position):
        self.x = x = position[0]
        self.y = y = position[1]

        if self.way is 'width':
            if not x + self.size <= 8:
                return False

            for l in range(x, x + self.size):
                if cell[l][y].boundary or cell[l][y].ship:
                    return False

            for i in range(self.size):
                cell[x + i][y].ship = True
                self.ship_position.append((x + i, y))
            for k in range(x - 1 if x - 1 >= 0 else 0, x + self.size + 1 if x + self.size <= 7 else 7 + 1):
                for j in range(y - 1 if y - 1 >= 0 else 0, y + 1 + 1 if y + 1 <= 7 else 7 + 1):
                    if not cell[k][j].ship:
                        cell[k][j].boundary = True
                        self.boundary_position.append((k, j))

        else:
            if not y + self.size <= 8:
                return False

            for l in range(y, y + self.size):
                if cell[x][l].boundary or cell[x][l].ship:
                    return False

            for i in range(self.size):
                cell[x][y + i].ship = True
                self.ship_position.append((x, y + i))
            for k in range(x - 1 if x - 1 >= 0 else 0, x + 1 + 1 if x + 1 <= 7 else 7 + 1):
                for j in range(y - 1 if y - 1 >= 0 else 0, y + self.size + 1 if y + self.size <= 7 else 7 + 1):
                    if not cell[k][j].ship:
                        cell[k][j].boundary = True
                        self.boundary_position.append((k, j))

        return True

    def blit(self):
        screen.blit(self.image, (100 + self.x * 600 / 8, 50 + self.y * 600 / 8))


ship_showing_cnt = 0


class make_button:
    def __init__(self, text, background_size, font_size):
        self.background = pygame.image.load("data/button/button.png")
        self.background = pygame.transform.scale(self.background, background_size)
        self.background_rect = pygame.Rect(self.background.get_rect())
        self.font = pygame.font.Font("data/font/Outfit-Bold.ttf", font_size)
        self.text = self.font.render(text, True, "#37364e")
        self.text_rect = pygame.Rect(self.text.get_rect())

    def blit(self, position):
        self.background_rect.center = position
        self.text_rect.center = position
        screen.blit(self.background, self.background_rect)
        screen.blit(self.text, self.text_rect)
        return self.check_click()

    def get_width(self):
        return self.background.get_width()

    def check_click(self):
        mouse_position = pygame.mouse.get_pos()
        if self.background_rect.collidepoint(mouse_position):
            if pygame.mouse.get_pressed()[0]:
                return False
        return True


ship = [make_ship(1), make_ship(2), make_ship(2), make_ship(3), make_ship(3), make_ship(1)]

cnt = 0
while cnt <= len(ship) - 1:
    if ship[cnt].put((random.randint(0, 7), random.randint(0, 7))):
        cnt += 1

for y in range(8):
    for x in range(8):
        if cell[x][y].burning:
            print('bu', end=' ')
        elif cell[x][y].ship:
            print('sh', end=' ')
        elif cell[x][y].boundary:
            print('  ', end=' ')
        elif cell[x][y].dot:
            print('do', end=' ')
        else:
            print('  ', end=' ')
    print()

tittle_step = True
tittle_font = pygame.font.Font("data/font/Outfit-Bold.ttf", 100)
tittle_font_text = tittle_font.render("Battle Ship", True, "#000000")
tittle_x = pixel_x // 2 - tittle_font_text.get_width() // 2

button_start = make_button("start", (150, 75), 50)
button_start_x = pixel_x // 2

boom_position_step = False
boom_position_step_clicked = False
boom_position_x = None
boom_position_y = None
button_launch = make_button("launch", (150, 75), 40)
button_launch_x = pixel_x // 2

boom_down_step = False

bomb = pygame.image.load("data/bomb/bomb.png")
bomb = pygame.transform.scale(bomb, (600 / 8, 600 / 8))
bomb_rect = pygame.Rect(bomb.get_rect())

smoke = pygame.image.load("data/smoke/smoke.png")
smoke = pygame.transform.scale(smoke, (600 / 8, 600 / 8))
dot = pygame.image.load("data/dot/dot.png")
dot = pygame.transform.scale(dot, (10, 10))
dot_rect = pygame.Rect(dot.get_rect())

completed_font = pygame.font.Font("data/font/Outfit-Bold.ttf", 100)
completed_font_text = completed_font.render("COMPLETED!", True, "#000000")
completed_font_text_rect = pygame.Rect(completed_font_text.get_rect())

programing = True
while programing:
    for event in pygame.event.get():
        # print(event)

        if event.type == pygame.QUIT:
            programing = False
            pygame.quit()
            sys.exit()

    screen.blit(ocean, (0, 0))
    screen.blit(cloud, (0, 0))

    # print(ship_showing_cnt, len(ship))
    if ship_showing_cnt == len(ship):
        completed_font_text_rect.center = (pixel_x // 2, pixel_y // 2)
        screen.blit(completed_font_text, completed_font_text_rect)
        pygame.display.update()
        continue

    if boom_position_step or boom_down_step:
        screen.blit(grid, (100, 50))

    if tittle_step:
        screen.blit(tittle_font_text, (tittle_x, 300))
        tittle_step = button_start.blit((button_start_x, 475))
        if not tittle_step:
            boom_position_step = True
            boom_position_step_start_time = pygame.time.get_ticks()

    if boom_down_step:
        if pygame.time.get_ticks() - boom_position_step_end_time <= 1500:
            screen.blit(bomb, (100 + boom_position_x * 600 / 8, 50 + boom_position_y * 600 / 8))
        else:
            if cell[boom_position_x][boom_position_y].ship:
                for i in ship:
                    for j in i.ship_position:
                        if j == (boom_position_x, boom_position_y):
                            i.ship_position.remove(j)
                            if not i.ship_position:
                                cell[boom_position_x][boom_position_y].burning = True
                                for k in i.boundary_position:
                                    cell[k[0]][k[1]].dot = True
                                i.ship_showing = True
                                ship_showing_cnt += 1
                            else:
                                cell[boom_position_x][boom_position_y].burning = True
                            boom_down_step = False
            else:
                cell[boom_position_x][boom_position_y].dot = True
                boom_down_step = False

        if not boom_down_step:
            boom_position_step = True
            boom_position_step_clicked = False
            cell[boom_position_x][boom_position_y].clicked = False
            boom_position_x = None
            boom_position_y = None
            boom_position_step_start_time = pygame.time.get_ticks()

    for i in ship:
        if i.ship_showing:
            i.blit()

    for row in range(8):
        for col in range(8):
            if cell[col][row].burning:
                screen.blit(smoke, (100 + col * 600 / 8, 50 + row * 600 / 8))
            elif cell[col][row].dot:
                dot_rect.center = (100 + 600 / 8 / 2 + col * 600 / 8, 50 + 600 / 8 / 2 + row * 600 / 8)
                screen.blit(dot, dot_rect)

    if boom_position_step:
        if pygame.time.get_ticks() - boom_position_step_start_time >= 500:
            for row in range(8):
                for col in range(8):
                    boom_position_step_clicked = cell[col][row].blit((100 + col * 600 / 8, 50 + row * 600 / 8))
                    if boom_position_step_clicked and boom_position_x is None:
                        boom_position_x = col
                        boom_position_y = row

            if boom_position_step_clicked:
                boom_position_step = button_launch.blit((button_launch_x, 730))
                if not boom_position_step:
                    boom_down_step = True
                    boom_position_step_end_time = pygame.time.get_ticks()

    pygame.display.update()
    fps_time.tick(60)
