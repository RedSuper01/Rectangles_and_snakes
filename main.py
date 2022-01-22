import pygame
import sys
import os
import random

FPS = 100
pygame.init()
size = width, height = 900, 700
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

levels_dict_coord = {'1': '', '2': '', '3': '', '4': '', '5': '',
                     '6': '', '7': '', '8': '', '9': '', '10': '',
                     '11': '', '12': '', '13': '', '14': '', '15': '',
                     '16': '', '17': '', '18': '', '19': '', '20': ''}
main_fon_dict_coord = {'1': ['fon1.png'], '2': ['fon2.png'], '3': ['fon3.png'], '4': ['fon4.png'], '5': ['fon5.png'],
                       '6': ['fon6.png'], '7': ['fon7.png'], '8': ['fon8.png'], '9': ['fon9.png'], '10': ['fon10.png'],
                       '11': ['fon11.png'], '12': ['victory_fon.png'], '13': ['fon13.png'], '14': ['fon14.png'], '15': ['fon15.png'],
                       'main': 'main'
                       }
level_fon_dict_coord = {'1': ['fon1.png'], '2': ['fon2.png'], '3': ['fon3.png'], '4': ['fon4.png'], '5': ['fon5.png'],
                       '6': ['fon6.png'], '7': ['fon7.png'], '8': ['fon8.png'], '9': ['fon9.png'], '10': ['fon10.png'],
                       '11': ['fon11.png'], '12': ['fon12.png'], '13': ['fon13.png'], '14': ['fon14.png'], '15': ['fon15.png'],
                        'level': 'level'
                       }
victory_fon_dict_coord = {'1': ['victory_fon.png'], '2': ['victory_fon2.png'], '3': ['victory_fon3.png'],
                        '4': ['victory_fon4.png'], '5': ['victory_fon5.png'], '6': ['victory_fon6.png'],
                         '7': ['victory_fon7.png'],
                          'victory': 'victory'}
losing_fon_dict_coord = {'1': ['losing_fon1.png'], '2': ['losing_fon2.png'], 'losing': 'losing'}

dc_of_all_dict = {'main': main_fon_dict_coord, 'level': level_fon_dict_coord, 'victory': victory_fon_dict_coord, 'losing': losing_fon_dict_coord}

all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
vertical_lines = pygame.sprite.Group()
horizontal_lines = pygame.sprite.Group()
all_snakes = pygame.sprite.Group()
dc_snakes = {}

count_of_done_cuts = 0
coord_of_rectangle = (x1, y1, x2, y2) = (150, 150, 750, 550)

file_of_fon = open('fon.txt', 'r', encoding='utf-8')

main_fon, level_fon, victory_fon, losing_fon = [i.rstrip('\n') for i in file_of_fon.readlines()]
file_of_fon.close()


def load_image(name, color_key=None):
    fullname = 'data\\' + name
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def check_click(mouse_x, mouse_y, tuple_of_coord, dc):
    text_x, text_y, text_w, text_h = tuple_of_coord
    start_x, end_x, start_y, end_y = text_x, text_x + text_w, text_y, text_y + text_h
    if start_x <= mouse_x <= end_x and start_y <= mouse_y <= end_y:
        for i in list(dc.keys()):
            if dc[i] == tuple_of_coord:
                number = int(i)
                return number
    else:
        return ''


class Snake(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.radius = radius
        self.image = pygame.Surface((225, 225), pygame.SRCALPHA, 32)
        fon = pygame.transform.scale(load_image('snake1.png', -1), (50, 50))
        self.image.blit(fon, (0, 0))
        self.rect = pygame.Rect(x, y, 50, 45)
        self.vx = random.randint(-5, 5)
        self.vy = random.randint(-5, 5)

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2
        if self.x1 == self.x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([5, self.y2 - self.y1])
            self.rect = pygame.Rect(self.x1, self.y1, 5, self.y2 - self.y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([self.x2 - self.x1, 5])
            self.rect = pygame.Rect(self.x1, self.y1, self.x2 - self.x1, 5)


class Lines(pygame.sprite.Sprite):
    def __init__(self, x, y, type_of_line):
        super().__init__(all_sprites)
        self.ax, self.ay, self.type_of_line = x, y, type_of_line
        self.losing = False

        if self.type_of_line == 'vertical':
            self.add(vertical_lines)
            self.image = pygame.Surface([5, 430])
            self.rect = pygame.Rect(x, y, 5, 430)
            pygame.draw.line(screen, (0, 0, 0), (self.ax + 1, 135), (self.ax + 1, 570), 5)

        elif self.type_of_line == 'horizontal':
            self.add(horizontal_lines)
            self.image = pygame.Surface([630, 5])
            self.rect = pygame.Rect(x, y, 630, 5)
            pygame.draw.line(screen, (0, 0, 0), (135, self.ay + 1), (765, self.ay + 1), 5)

    def update(self):
        if pygame.sprite.spritecollide(self, all_snakes, False):
            if self.type_of_line == 'vertical':
                pygame.draw.line(screen, (255, 0, 0), (self.ax + 1, 135), (self.ax + 1, 570), 7)
                self.losing = True
            elif self.type_of_line == 'horizontal':
                pygame.draw.line(screen, (255, 0, 0), (135, self.ay + 1), (765, self.ay + 1), 7)
                self.losing = True

    def check_game(self):
        return self.losing


def change_diff(number_of_level):
    if number_of_level <= 2:
        return 10, 5
    elif number_of_level <= 4:
        return 12, 5
    elif number_of_level <= 10:
        return 16, 6
    elif number_of_level <= 14:
        return 18, 6
    elif number_of_level <= 19:
        return 20, 7
    else:
        return 30, 7


def victory_screen(number_of_level):
    global coord_of_rectangle
    global count_of_done_cuts
    x1, y1, x2, y2 = coord_of_rectangle
    victory_sprite_group = pygame.sprite.Group()

    try_again_sprite = pygame.sprite.Sprite()
    try_again_sprite.image = pygame.transform.scale(load_image('try_again_2.png', -1), (100, 100))
    try_again_sprite.rect = try_again_sprite.image.get_rect()
    try_again_sprite.rect.x, try_again_sprite.rect.y = 350, 562
    victory_sprite_group.add(try_again_sprite)

    exit_button_sprite = pygame.sprite.Sprite()
    exit_button_sprite.image = pygame.transform.scale(load_image('exit_button_5.png', -1), (100, 100))
    exit_button_sprite.rect = exit_button_sprite.image.get_rect()
    exit_button_sprite.rect.x, exit_button_sprite.rect.y = 500, 562
    victory_sprite_group.add(exit_button_sprite)

    fon = pygame.transform.scale(load_image(victory_fon), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 70)
    text = font.render('Поздравляю!!!', True, (0, 0, 0))
    screen.blit(text, (275, 50))
    text_1 = font.render('Вы прошли ' + str(number_of_level) + '-ый уровень', True, (0, 0, 0))
    screen.blit(text_1, (160, 100))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(*event.pos)
                x, y = event.pos
                if 350 <= x <= 450 and 562 <= y <= 662:
                    count_of_done_cuts = 0
                    launch_level(number_of_level, x1, y1, x2, y2)
                    break
                elif 500 <= x <= 600 and 562 <= y <= 662:
                    count_of_done_cuts = 0
                    splash_screen()
                    break
        victory_sprite_group.draw(screen)
        pygame.display.flip()
        clock.tick(70)


def launch_level(number_of_level, x1, y1, x2, y2):
    global all_sprites
    global all_snakes
    global vertical_borders
    global horizontal_borders
    global vertical_lines
    global horizontal_lines
    global screen
    global count_of_done_cuts
    global coord_of_rectangle

    all_sprites = pygame.sprite.Group()
    horizontal_borders = pygame.sprite.Group()
    vertical_borders = pygame.sprite.Group()
    vertical_lines = pygame.sprite.Group()
    horizontal_lines = pygame.sprite.Group()
    all_snakes = pygame.sprite.Group()
    fon = pygame.transform.scale(load_image(level_fon), (width, height))
    screen.blit(fon, (0, 0))

    Border(x1, y1, x2, y1)
    Border(x1, y2, x2, y2)
    Border(x1, y1, x1, y2)
    Border(x2, y1, x2, y2)

    cursor = pygame.sprite.Sprite()
    cursor.image = pygame.transform.scale(load_image('cursor.png'), (30, 30))
    cursor.rect = cursor.image.get_rect()
    cursor.rect.x, cursor.rect.y = x1 - 15, y1 - 15
    all_sprites.add(cursor)

    try_again_sprite = pygame.sprite.Sprite()
    try_again_sprite.image = load_image('try_again.png', -1)
    try_again_sprite.rect = try_again_sprite.image.get_rect()
    all_sprites.add(try_again_sprite)
    try_again_sprite.rect.x, try_again_sprite.rect.y = 1000, 1000

    exit_sprite = pygame.sprite.Sprite()
    exit_sprite.image = load_image('exit_button_4.png', -1)
    exit_sprite.rect = exit_sprite.image.get_rect()
    all_sprites.add(exit_sprite)
    exit_sprite.rect.x, exit_sprite.rect.y = 1000, 1000

    pause = False

    n, count_cuts = change_diff(int(number_of_level))
    for i in range(n):
        bg = Snake(20, x1 + 50, y1 + 50)
        all_snakes.add(bg)
        dc_snakes[i] = bg
    losing = False
    victory = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if not losing:
                    if event.key == pygame.K_w:
                        if cursor.rect.x == x1 - 15 or cursor.rect.x == x2 - 15:
                            cursor.rect.y -= 25
                            if cursor.rect.y < y1 - 15:
                                cursor.rect.y = y1 - 15
                    elif event.key == pygame.K_s:
                        if cursor.rect.x == x1 - 15 or cursor.rect.x == x2 - 15:
                            cursor.rect.y += 25
                            if cursor.rect.y > y2 - 15:
                                cursor.rect.y = y2 - 15
                    elif event.key == pygame.K_a:
                        if cursor.rect.y == y1 - 15 or cursor.rect.y == y2 - 15:
                            cursor.rect.x -= 25
                            if cursor.rect.x < x1 - 15:
                                cursor.rect.x = x1 - 15
                    elif event.key == pygame.K_d:
                        if cursor.rect.y == y1 - 15 or cursor.rect.y == y2 - 15:
                            cursor.rect.x += 25
                            if cursor.rect.x > x2 - 15:
                                cursor.rect.x = x2 - 15
                    elif event.key == pygame.K_SPACE:

                        if (cursor.rect.x == x1 - 15 and cursor.rect.y == y1 - 15) or (
                                cursor.rect.x == x1 - 15 and cursor.rect.y == y2 - 15):
                            pass
                        elif (cursor.rect.x == x2 - 15 and cursor.rect.y == y1 - 15) or (
                                cursor.rect.x == x2 - 15 and cursor.rect.y == y2 - 15):
                            pass
                        elif cursor.rect.x == x1 - 15 or cursor.rect.x == x2 - 15:
                            lines_type = Lines(cursor.rect.x, cursor.rect.y, 'horizontal')
                            pause = True

                        elif cursor.rect.y == y1 - 15 or cursor.rect.y == y2 - 15:
                            lines_type = Lines(cursor.rect.x, cursor.rect.y, 'vertical')
                            pause = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if losing:
                    x, y = event.pos
                    if 200 <= x <= 425 and 500 <= y <= 725:
                        x1, y1, x2, y2 = coord_of_rectangle
                        launch_level(number_of_level, x1, y1, x2, y2)
                        break
                    elif 400 <= x <= 710 and 530 <= y <= 693:
                        splash_screen()
                        break

        if not victory:
            if pause:
                vertical_lines.update()  # Это чтобы понять проиграли ли мы или нет
                horizontal_lines.update()  # Проверка на столкновение со змейкой
                if lines_type.check_game():
                    fon = pygame.transform.scale(load_image(losing_fon), (width, height))
                    screen.blit(fon, (0, 0))
                    all_sprites.draw(screen)
                    losing = True
                    vertical_lines.update()
                    horizontal_lines.update()
                    try_again_sprite.rect.x, try_again_sprite.rect.y = 200, 500
                    exit_sprite.rect.x, exit_sprite.rect.y = 400, 530

                    count_of_done_cuts = 0
                else:
                    count_of_done_cuts += 1
                    print(count_of_done_cuts, count_cuts)
                    if count_of_done_cuts < count_cuts:
                        if cursor.rect.x == x1 - 15 or cursor.rect.x == x2 - 15:
                            if cursor.rect.y - 150 <= (y2 - y1) // 2:
                                y1 = cursor.rect.y
                                if abs(x2 - x1) < 200 or abs(y2 - y1) < 200:
                                    count_of_done_cuts = count_cuts
                                    break
                                launch_level(number_of_level, x1, y1, x2, y2)
                            else:
                                y2 = cursor.rect.y
                                if abs(x2 - x1) < 200 or abs(y2 - y1) < 200:
                                    count_of_done_cuts = count_cuts
                                    break

                                launch_level(number_of_level, x1, y1, x2, y2)
                        elif cursor.rect.y == y1 - 15 or cursor.rect.y == y2 - 15:
                            if cursor.rect.x - 150 <= (x2 - x1) // 2:
                                x1 = cursor.rect.x
                                if abs(x2 - x1) < 200 or abs(y2 - y1) < 200:
                                    count_of_done_cuts = count_cuts
                                    break

                                launch_level(number_of_level, x1, y1, x2, y2)
                            else:
                                x2 = cursor.rect.x
                                if x2 - x1 < 200 or y2 - y1 < 200:
                                    count_of_done_cuts = count_cuts
                                    break
                                launch_level(number_of_level, x1, y1, x2, y2)
                    else:
                        victory = True
                        pause = True
                        victory_screen(number_of_level)
                        count_of_done_cuts = 0

            else:
                vertical_lines.update()
                horizontal_lines.update()
                fon = pygame.transform.scale(load_image(level_fon), (width, height))
                screen.blit(fon, (0, 0))
                all_sprites.draw(screen)
                all_sprites.update()

        pygame.display.flip()
        clock.tick(70)


def terminate():
    pygame.quit()
    sys.exit()


def look_levels():
    global coord_of_rectangle
    x1, y1, x2, y2 = coord_of_rectangle
    all_sprites = pygame.sprite.Group()
    fon = pygame.transform.scale(load_image(main_fon), size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 150)
    intro_text = list()
    intro_text.append(list(map(str, range(1, 6))))
    intro_text.append(list(map(str, range(6, 11))))
    intro_text.append(list(map(str, range(11, 16))))
    intro_text.append(list(map(str, range(16, 21))))
    for i in intro_text:
        for j in i:
            text = font.render(j, True, (255, 255, 255))
            if int(j) % 5 != 0:
                text_x = (int(j) % 5) * 150 - 50
            else:
                text_x = 5 * 150 - 50
            text_y = 50 + 150 * intro_text.index(i)
            text_w = text.get_width()
            text_h = text.get_height()
            screen.blit(text, (text_x, text_y))

            levels_dict_coord[str(j)] = (text_x, text_y, text_w, text_h)

    back_arrow_sprite = pygame.sprite.Sprite()

    back_arrow_sprite.image = load_image('back_arrow.png', color_key=-1)
    back_arrow_sprite.image = pygame.transform.scale(back_arrow_sprite.image, (100, 100))

    back_arrow_sprite.rect = back_arrow_sprite.image.get_rect()
    back_arrow_sprite.rect.x = 0
    back_arrow_sprite.rect.y = 0

    all_sprites.add(back_arrow_sprite)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:

                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if x <= 100 and y <= 100:
                    splash_screen()
                for i in list(levels_dict_coord.values()):
                    something = check_click(x, y, i, levels_dict_coord)
                    if something != '':
                        all_sprites.remove(back_arrow_sprite)
                        launch_level(int(something), x1, y1, x2, y2)

        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

def check_click_for_fon(mouse_x, mouse_y, tuple_of_coord, dc):
    text_x, text_y, text_w, text_h = tuple_of_coord
    start_x, end_x, start_y, end_y = text_x, text_x + text_w, text_y, text_y + text_h
    if start_x <= mouse_x <= end_x and start_y <= mouse_y <= end_y:
        for i in list(dc.keys()):
            if dc[i][1] == tuple_of_coord:
                print(dc[i][1], 'skfjdk')
                print(tuple_of_coord, 'fsd')
                number = int(i)
                return number
    else:
        return ''


def getting_num_from_dict(x, y, dc):
    for i in list(dc.values())[:len(list(dc.values())) - 1]:
        something = check_click_for_fon(x, y, i[1], dc)
        if something != '':
            print(something)
            return (something, list(dc.values())[-1])
    return ('', '')


def putting_image(name):
    print(name)
    image = pygame.transform.scale(load_image(name), (370, 400))
    screen.blit(image, (500, 277))


def changing_design():
    global main_fon
    global level_fon
    global victory_fon
    global losing_fon
    fon = pygame.transform.scale(load_image(main_fon), size)
    screen.blit(fon, (0, 0))

    sprites_for_design_window = pygame.sprite.Group()
    back_arrow_sprite = pygame.sprite.Sprite()
    back_arrow_sprite.image = pygame.transform.scale(load_image('back_arrow2.png', -1), (150, 150))
    back_arrow_sprite.rect = back_arrow_sprite.image.get_rect()
    back_arrow_sprite.rect.x, back_arrow_sprite.rect.y = 20, 530
    sprites_for_design_window.add(back_arrow_sprite)

    accept_button_sprite = pygame.sprite.Sprite()
    accept_button_sprite.image = pygame.transform.scale(load_image('accept_button3.png', -1), (300, 300))
    accept_button_sprite.rect = accept_button_sprite.image.get_rect()
    accept_button_sprite.rect.x, accept_button_sprite.rect.y = 170, 460
    sprites_for_design_window.add(accept_button_sprite)

    font = pygame.font.Font(None, 60)
    text = font.render('Главный фон', True, (255, 255, 255))
    screen.blit(text, (50, 30))

    intro_text_main = [list(map(str, range(1, 6))), list(map(str, range(6, 11))), list(map(str, range(11, 16)))]
    for i in intro_text_main:
        for j in i:
            if int(j) % 5 != 0:
                text_x = (int(j) % 5) * 60
            else:
                text_x = 300
            text_y = 80 + intro_text_main.index(i) * 60
            text_w, text_h = text.get_width(), text.get_height()
            print(j, text_x, text_y, text_w, text_h)
            print(j, text_w)
            if j == '1':
                text_x, text_y, text_w, text_h = 60, 80, 23, 42
            text = font.render(str(j), True, (255, 255, 255))
            screen.blit(text, (text_x, text_y))
            main_fon_dict_coord[j].append((text_x, text_y, text_w, text_h))
            print(main_fon_dict_coord)

    text_level = font.render('Фон уровня', True, (255, 255, 255))
    screen.blit(text_level, (550, 30))
    intro_text_level = [list(map(str, range(1, 6))), list(map(str, range(6, 11))), list(map(str, range(11, 16)))]
    for i in intro_text_level:
        for j in i:
            if int(j) % 5 != 0:
                text_x = 500 + (int(j) % 5) * 60
            else:
                text_x = 800
            text_y = 80 + intro_text_level.index(i) * 60
            text_w, text_h = text.get_width(), text.get_height()

            text = font.render(str(j), True, (255, 255, 255))
            screen.blit(text, (text_x, text_y))
            level_fon_dict_coord[j].append((text_x, text_y, text_w, text_h))

    text_victory = font.render('Выигрышный экран', True, (255, 255, 255))
    screen.blit(text_victory, (20, 270))
    intro_text_victory = [list(map(str, range(1, 8)))]
    for i in intro_text_victory:
        for j in i:
            text_x = int(j) * 60  - 20
            text_y = 320
            text_w, text_h = text.get_width(), text.get_height()
            text = font.render(str(j), True, (255, 255, 255))
            screen.blit(text, (text_x, text_y))
            victory_fon_dict_coord[j].append((text_x, text_y, text_w, text_h))
    text_losing = font.render('Проигрышный экран', True, (255, 255, 255))
    screen.blit(text_losing, (20, 400))
    intro_text_losing = [list(map(str, range(1, 3)))]
    for i in intro_text_losing:
        for j in i:
            text_x = int(j) * 60 - 20
            text_y = 450
            text = font.render(j, True, (255, 255, 255))
            text_w, text_h = text.get_width(), text.get_height()
            screen.blit(text, (text_x, text_y))
            losing_fon_dict_coord[j].append((text_x, text_y, text_w, text_h))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect((500, 277), (370, 400)), 1)

    num, type_of_fon = '', ''

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                print(x, y)
                if 20 <= x <= 170 and 530 <= y <= 680:
                    splash_screen()
                    break
                elif 170 <= x <= 470 and 460 <= y <= 760:
                    if type_of_fon != '':
                        if type_of_fon == 'main':
                            main_fon = dc_of_all_dict[type_of_fon][num][0]
                        elif type_of_fon == 'level':
                            level_fon = dc_of_all_dict[type_of_fon][num][0]
                        elif type_of_fon == 'victory':
                            victory_fon = dc_of_all_dict[type_of_fon][num][0]
                        elif type_of_fon == 'losing':
                            losing_fon = dc_of_all_dict[type_of_fon][num][0]
                        file_of_fon = open('fon.txt', 'w', encoding='utf-8')
                        file_of_fon.write(main_fon + '\n')
                        file_of_fon.write(level_fon + '\n')
                        file_of_fon.write(victory_fon + '\n')
                        file_of_fon.write(losing_fon + '\n')
                        file_of_fon.close()
                        changing_design()
                        break
                else:
                    num_main, type_of_fon_main = getting_num_from_dict(x, y, main_fon_dict_coord)
                    num_level, type_of_fon_level = getting_num_from_dict(x, y, level_fon_dict_coord)
                    num_victory, type_of_fon_victory = getting_num_from_dict(x, y, victory_fon_dict_coord)
                    num_losing, type_of_fon_losing = getting_num_from_dict(x, y, losing_fon_dict_coord)
                    if num_main != '':
                        num, type_of_fon = str(num_main), type_of_fon_main
                        putting_image(dc_of_all_dict[type_of_fon][num][0])
                    elif num_level != '':
                        num, type_of_fon = str(num_level), type_of_fon_level
                        putting_image(dc_of_all_dict[type_of_fon][num][0])
                    elif num_victory != '':
                        num, type_of_fon = str(num_victory), type_of_fon_victory
                        putting_image(dc_of_all_dict[type_of_fon][num][0])
                    elif num_losing != '':
                        num, type_of_fon = str(num_losing), type_of_fon_losing
                        putting_image(dc_of_all_dict[type_of_fon][num][0])


        sprites_for_design_window.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def splash_screen():
    intro_text = ['Прямоугольники и змейки', '', 'Правила игры',
                  'Начать игру',
                  'Изменение дизайна',
                  'Настройки']
    fon = pygame.transform.scale(load_image(main_fon), size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 70)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 50
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if (10 <= x <= 350) and (298 <= y <= 350):
                    print('Правила игры')
                elif (10 <= x <= 300) and (397 <= y <= 450):
                    look_levels()

                elif (10 <= x <= 490) and (497 <= y <= 545):
                    changing_design()
                elif (10 <= x <= 265) and (595 <= y <= 644):
                    print('Настройки')
        pygame.display.flip()
        clock.tick(FPS)


splash_screen()
pygame.quit()
