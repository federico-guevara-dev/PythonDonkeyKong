# DONKEY KONG REBUILD IN PYTHON WITH THE PYGAME MODULE! (HD Edition)
import os
import sys
import random
import pygame

def resource_path(relative_path):
    """Obtiene la ruta absoluta al recurso, compatible con desarrollo y PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def load_smooth(rel_path, width, height):
    """Carga una imagen con canal alfa y aplica smoothscale bilineal para maxima calidad HD"""
    full_path = resource_path(rel_path)
    img = pygame.image.load(full_path).convert_alpha()
    w = max(1, int(round(width)))
    h = max(1, int(round(height)))
    return pygame.transform.smoothscale(img, (w, h))

def get_font(size):
    try:
        return pygame.font.Font('freesansbold.ttf', size)
    except Exception:
        return pygame.font.SysFont('Arial', size, bold=True)

# Variables de ventana y juego
screen = None
window_width = 720
window_height = 660
section_width = 0
section_height = 0
slope = 0
timer = None
fps = 60
font = None
font2 = None

# Sprites
barrel_img = None
flames_img = None
barrel_side = None
dk1 = None
dk2 = None
dk3 = None
peach1 = None
peach2 = None
fireball = None
fireball2 = None
hammer = None
standing = None
jumping = None
running = None
climbing1 = None
climbing2 = None
hammer_stand = None
hammer_jump = None
hammer_overhead = None

# Posiciones y estado
start_y = 0
row2_y = 0
row3_y = 0
row4_y = 0
row5_y = 0
row6_y = 0
row6_top = 0
row5_top = 0
row4_top = 0
row3_top = 0
row2_top = 0
row1_top = 0
fireball_trigger = False
active_level = 0
counter = 0
score = 0
high_score = 0
lives = 5
bonus = 6000
first_fireball_trigger = False
victory = False
reset_game = False
levels = []
player = None
barrels = None
flames = None
hammers = None
hammers_list = []
plats = []
lads = []
oil_drum = None

def init_game():
    global screen, window_width, window_height, section_width, section_height, slope, timer, fps, font, font2
    global barrel_spawn_time, barrel_count, barrel_time
    global barrel_img, flames_img, barrel_side, dk1, dk2, dk3, peach1, peach2, fireball, fireball2, hammer
    global standing, jumping, running, climbing1, climbing2, hammer_stand, hammer_jump, hammer_overhead
    global start_y, row2_y, row3_y, row4_y, row5_y, row6_y, row6_top, row5_top, row4_top, row3_top, row2_top, row1_top
    global fireball_trigger, active_level, counter, score, lives, bonus, first_fireball_trigger, victory, reset_game, levels
    global barrels, flames, hammers, hammers_list, player

    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h

    # Tamaño adaptable a netbooks escolares y monitores de escritorio
    window_width = min(720, max(540, screen_width - 80))
    window_height = min(660, max(520, screen_height - 90))

    timer = pygame.time.Clock()
    fps = 60

    pygame.display.set_caption('Classic Donkey Kong Rebuild! (HD Edition)')
    font = get_font(max(24, int(window_height * 0.065)))
    font2 = get_font(max(18, int(window_height * 0.04)))

    screen = pygame.display.set_mode([window_width, window_height])
    section_width = window_width // 32
    section_height = window_height // 32
    slope = max(1, section_height // 8)

    barrel_spawn_time = 360
    barrel_count = barrel_spawn_time / 2
    barrel_time = 360

    # Carga de Sprites en ALTA CALIDAD con smoothscale y canal alfa
    barrel_img = load_smooth('assets/images/barrels/barrel.png', section_width * 1.5, section_height * 2)
    flames_img = load_smooth('assets/images/fire.png', section_width * 2, section_height)
    barrel_side = load_smooth('assets/images/barrels/barrel2.png', section_width * 2, section_height * 2.5)
    dk1 = load_smooth('assets/images/dk/dk1.png', section_width * 5, section_height * 5)
    dk2 = load_smooth('assets/images/dk/dk2.png', section_width * 5, section_height * 5)
    dk3 = load_smooth('assets/images/dk/dk3.png', section_width * 5, section_height * 5)
    peach1 = load_smooth('assets/images/peach/peach1.png', 2 * section_width, 3 * section_height)
    peach2 = load_smooth('assets/images/peach/peach2.png', 2 * section_width, 3 * section_height)
    fireball = load_smooth('assets/images/fireball.png', 1.5 * section_width, 2 * section_height)
    fireball2 = load_smooth('assets/images/fireball2.png', 1.5 * section_width, 2 * section_height)
    hammer = load_smooth('assets/images/hammer.png', 2 * section_width, 2 * section_height)
    standing = load_smooth('assets/images/mario/standing.png', 2 * section_width, 2.5 * section_height)
    jumping = load_smooth('assets/images/mario/jumping.png', 2 * section_width, 2.5 * section_height)
    running = load_smooth('assets/images/mario/running.png', 2 * section_width, 2.5 * section_height)
    climbing1 = load_smooth('assets/images/mario/climbing1.png', 2 * section_width, 2.5 * section_height)
    climbing2 = load_smooth('assets/images/mario/climbing2.png', 2 * section_width, 2.5 * section_height)
    hammer_stand = load_smooth('assets/images/mario/hammer_stand.png', 2.5 * section_width, 2.5 * section_height)
    hammer_jump = load_smooth('assets/images/mario/hammer_jump.png', 2.5 * section_width, 2.5 * section_height)
    hammer_overhead = load_smooth('assets/images/mario/hammer_overhead.png', 2.5 * section_width, 3.5 * section_height)

    try:
        pygame.display.set_icon(dk1)
    except Exception:
        pass

    start_y = window_height - 2 * section_height
    row2_y = start_y - 4 * section_height
    row3_y = row2_y - 7 * slope - 3 * section_height
    row4_y = row3_y - 4 * section_height
    row5_y = row4_y - 7 * slope - 3 * section_height
    row6_y = row5_y - 4 * section_height
    row6_top = row6_y - 4 * slope
    row5_top = row5_y - 8 * slope
    row4_top = row4_y - 8 * slope
    row3_top = row3_y - 8 * slope
    row2_top = row2_y - 8 * slope
    row1_top = start_y - 5 * slope
    fireball_trigger = False
    active_level = 0
    counter = 0
    score = 0
    lives = 5
    bonus = 6000
    first_fireball_trigger = False
    victory = False
    reset_game = False

    levels = [{'bridges': [(1, start_y, 15), (16, start_y - slope, 3),
                           (19, start_y - 2 * slope, 3), (22, start_y - 3 * slope, 3),
                           (25, start_y - 4 * slope, 3), (28, start_y - 5 * slope, 3),
                           (25, row2_y, 3), (22, row2_y - slope, 3),
                           (19, row2_y - 2 * slope, 3), (16, row2_y - 3 * slope, 3),
                           (13, row2_y - 4 * slope, 3), (10, row2_y - 5 * slope, 3),
                           (7, row2_y - 6 * slope, 3), (4, row2_y - 7 * slope, 3),
                           (2, row2_y - 8 * slope, 2), (4, row3_y, 3),
                           (7, row3_y - slope, 3), (10, row3_y - 2 * slope, 3),
                           (13, row3_y - 3 * slope, 3), (16, row3_y - 4 * slope, 3),
                           (19, row3_y - 5 * slope, 3), (22, row3_y - 6 * slope, 3),
                           (25, row3_y - 7 * slope, 3), (28, row3_y - 8 * slope, 2),
                           (25, row4_y, 3), (22, row4_y - slope, 3),
                           (19, row4_y - 2 * slope, 3), (16, row4_y - 3 * slope, 3),
                           (13, row4_y - 4 * slope, 3), (10, row4_y - 5 * slope, 3),
                           (7, row4_y - 6 * slope, 3), (4, row4_y - 7 * slope, 3),
                           (2, row4_y - 8 * slope, 2), (4, row5_y, 3),
                           (7, row5_y - slope, 3), (10, row5_y - 2 * slope, 3),
                           (13, row5_y - 3 * slope, 3), (16, row5_y - 4 * slope, 3),
                           (19, row5_y - 5 * slope, 3), (22, row5_y - 6 * slope, 3),
                           (25, row5_y - 7 * slope, 3), (28, row5_y - 8 * slope, 2),
                           (25, row6_y, 3), (22, row6_y - slope, 3),
                           (19, row6_y - 2 * slope, 3), (16, row6_y - 3 * slope, 3),
                           (2, row6_y - 4 * slope, 14), (13, row6_y - 4 * section_height, 6),
                           (10, row6_y - 3 * section_height, 3)],
               'ladders': [(12, row2_y + 6 * slope, 2), (12, row2_y + 26 * slope, 2),
                           (25, row2_y + 11 * slope, 4), (6, row3_y + 11 * slope, 3),
                           (14, row3_y + 8 * slope, 4), (10, row4_y + 6 * slope, 1),
                           (10, row4_y + 24 * slope, 2), (16, row4_y + 6 * slope, 5),
                           (25, row4_y + 9 * slope, 4), (6, row5_y + 11 * slope, 3),
                           (11, row5_y + 8 * slope, 4), (23, row5_y + 4 * slope, 1),
                           (23, row5_y + 24 * slope, 2), (25, row6_y + 9 * slope, 4),
                           (13, row6_y + 5 * slope, 2), (13, row6_y + 25 * slope, 2),
                           (18, row6_y - 27 * slope, 4), (12, row6_y - 17 * slope, 2),
                           (10, row6_y - 17 * slope, 2), (12, -5, 13), (10, -5, 13)],
              'hammers': [(4, row6_top + section_height), (4, row4_top+section_height)],
               'target': (13, row6_y - 4 * section_height, 3)}]

    barrels = pygame.sprite.Group()
    flames = pygame.sprite.Group()
    hammers = pygame.sprite.Group()
    hammers_list = levels[active_level]['hammers']
    for ham in hammers_list:
        hammers.add(Hammer(*ham))
    player = Player(250, window_height - 130)


class Player(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.y_change = 0
        self.x_speed = 3
        self.x_change = 0
        self.landed = False
        self.pos = 0
        self.dir = 1
        self.count = 0
        self.climbing = False
        self.image = standing
        self.hammer = False
        self.max_hammer = 450
        self.hammer_len = self.max_hammer
        self.hammer_pos = 1
        self.rect = self.image.get_rect()
        self.hitbox = self.rect
        self.hammer_box = self.rect
        self.rect.center = (x_pos, y_pos)
        self.over_barrel = False
        self.jump_origin_y = y_pos
        self.max_jump_height = int(2.5 * section_height)
        self.bottom = pygame.rect.Rect(self.rect.left, self.rect.bottom - 20, self.rect.width, 20)

    def update(self):
        self.landed = False
        for i in range(len(plats)):
            if self.bottom.colliderect(plats[i]):
                self.landed = True
                if not self.climbing:
                    self.rect.centery = plats[i].top - self.rect.height / 2 + 1
        if self.landed:
            self.jump_origin_y = self.rect.centery
        if not self.landed and not self.climbing:
            self.y_change += 0.25
            # Cap jump height to prevent reaching the platform above
            if self.y_change < 0 and self.jump_origin_y - self.rect.centery >= self.max_jump_height:
                self.y_change = 0.25
        self.rect.move_ip(self.x_change * self.x_speed, self.y_change)
        self.bottom = pygame.rect.Rect(self.rect.left, self.rect.bottom - 20, self.rect.width, 20)
        if self.x_change != 0 or (self.climbing and self.y_change != 0):
            if self.count < 3:
                self.count += 1
            else:
                self.count = 0
                if self.pos == 0:
                    self.pos += 1
                else:
                    self.pos = 0
        else:
            self.pos = 0
        if self.hammer:
            self.hammer_pos = (self.hammer_len // 30) % 2
            self.hammer_len -= 1
            if self.hammer_len == 0:
                self.hammer = False
                self.hammer_len = self.max_hammer

    def draw(self):
        if not self.hammer:
            if not self.climbing and self.landed:
                if self.pos == 0:
                    self.image = standing
                else:
                    self.image = running
            if not self.landed and not self.climbing:
                self.image = jumping
            if self.climbing:
                if self.pos == 0:
                    self.image = climbing1
                else:
                    self.image = climbing2
        else:
            if self.hammer_pos == 0:
                self.image = hammer_jump
            else:
                self.image = hammer_overhead
        if self.dir == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.image = self.image
        self.calc_hitbox()
        if self.hammer_pos == 1 and self.hammer:
            screen.blit(self.image, (self.rect.left, self.rect.top - section_height))
        else:
            screen.blit(self.image, self.rect.topleft)

    def calc_hitbox(self):
        if not self.hammer:
            self.hitbox = pygame.rect.Rect((self.rect[0] + 15, self.rect[1] + 5),
                                           (self.rect[2] - 30, self.rect[3] - 10))
        elif self.hammer_pos == 0:
            if self.dir == 1:
                self.hitbox = pygame.rect.Rect((self.rect[0], self.rect[1] + 5),
                                               (self.rect[2] - 30, self.rect[3] - 10))
                self.hammer_box = pygame.rect.Rect((self.hitbox[0] + self.hitbox[2], self.rect[1] + 5),
                                                   (self.hitbox[2], self.rect[3] - 10))
            else:
                self.hitbox = pygame.rect.Rect((self.rect[0] + 40, self.rect[1] + 5),
                                               (self.rect[2] - 30, self.rect[3] - 10))
                self.hammer_box = pygame.rect.Rect((self.hitbox[0] - self.hitbox[2], self.rect[1] + 5),
                                                   (self.hitbox[2], self.rect[3] - 10))
        else:
            self.hitbox = pygame.rect.Rect((self.rect[0] + 15, self.rect[1] + 5),
                                           (self.rect[2] - 30, self.rect[3] - 10))
            self.hammer_box = pygame.rect.Rect((self.hitbox[0], self.hitbox[1] - section_height),
                                               (self.hitbox[2], section_height))


class Hammer(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = hammer
        self.rect = self.image.get_rect()
        self.rect.top = y_pos
        self.rect.left = x_pos * section_width
        self.used = False

    def draw(self):
        if not self.used:
            screen.blit(self.image, (self.rect[0], self.rect[1]))
            if self.rect.colliderect(player.hitbox):
                self.kill()
                player.hammer = True
                player.hammer_len = player.max_hammer
                self.used = True


class Barrel(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((int(section_width * 1.5), int(section_height * 2)), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = (x_pos, y_pos)
        self.y_change = 0
        self.x_change = 1
        self.pos = 0
        self.count = 0
        self.oil_collision = False
        self.falling = False
        self.check_lad = False
        self.bottom = self.rect

    def update(self, fire_trig):
        if self.y_change < 8 and not self.falling:
            self.y_change += 2
        for i in range(len(plats)):
            if self.bottom.colliderect(plats[i]):
                self.y_change = 0
                self.falling = False
        if self.rect.colliderect(oil_drum):
            if not self.oil_collision:
                self.oil_collision = True
                if random.randint(0, 4) == 4:
                    fire_trig = True
        if not self.falling:
            if row5_top >= self.rect.bottom or row3_top >= self.rect.bottom >= row4_top or row1_top > self.rect.bottom >= row2_top:
                self.x_change = 3
            else:
                self.x_change = -3
        else:
            self.x_change = 0
        self.rect.move_ip(self.x_change, self.y_change)
        if self.rect.top > window_height:
            self.kill()
        if self.count < 15:
            self.count += 1
        else:
            self.count = 0
            if self.x_change > 0:
                if self.pos < 3:
                    self.pos += 1
                else:
                    self.pos = 0
            else:
                if self.pos > 0:
                    self.pos -= 1
                else:
                    self.pos = 3
        self.bottom = pygame.rect.Rect((self.rect[0], self.rect.bottom), (self.rect[2], 3))
        return fire_trig

    def check_fall(self):
        already_collided = False
        below = pygame.rect.Rect((self.rect[0], self.rect[1] + section_height), (self.rect[2], section_height))
        for lad in lads:
            if below.colliderect(lad) and not self.falling and not self.check_lad:
                self.check_lad = True
                already_collided = True
                if random.randint(0, 5) == 0:
                    self.falling = True
                    self.y_change = 4
        if not already_collided:
            self.check_lad = False

    def draw(self):
        screen.blit(pygame.transform.rotate(barrel_img, 90 * self.pos), self.rect.topleft)


class Flame(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = fireball
        self.rect = self.image.get_rect()
        self.rect.center = (x_pos, y_pos)
        self.pos = 1
        self.count = 0
        self.x_count = 0
        self.x_change = 2
        self.x_max = 4
        self.y_change = 0
        self.row = 1
        self.check_lad = False
        self.climbing = False

    def update(self):
        if self.y_change < 3 and not self.climbing:
            self.y_change += 0.25
        for i in range(len(plats)):
            if self.rect.colliderect(plats[i]):
                self.climbing = False
                self.y_change = -4
        if self.count < 15:
            self.count += 1
        else:
            self.count = 0
            self.pos *= -1
            if self.x_count < self.x_max:
                self.x_count += 1
            else:
                self.x_count = 0
                if self.x_change > 0:
                    if self.row in [1, 3, 5]:
                        self.x_max = random.randint(3, 6)
                    else:
                        self.x_max = random.randint(6, 10)
                else:
                    if self.row in [1, 3, 5]:
                        self.x_max = random.randint(6, 10)
                    else:
                        self.x_max = random.randint(3, 6)
                self.x_change *= -1
        if self.pos == 1:
            if self.x_change > 0:
                self.image = fireball
            else:
                self.image = pygame.transform.flip(fireball, True, False)
        else:
            if self.x_change > 0:
                self.image = fireball2
            else:
                self.image = pygame.transform.flip(fireball2, True, False)
        self.rect.move_ip(self.x_change, self.y_change)
        if self.rect.top > window_height or self.rect.top < 0:
            self.kill()

    def check_climb(self):
        already_collided = False
        for lad in lads:
            if self.rect.colliderect(lad) and not self.climbing and not self.check_lad:
                self.check_lad = True
                already_collided = True
                # Higher chance to climb when below the player
                climb_chance = 6 if self.rect.centery > player.rect.centery else 10
                if random.randint(0, climb_chance) == 0:
                    self.climbing = True
                    self.y_change = -4
        if not already_collided:
            self.check_lad = False
        if self.rect.bottom < row6_y:
            self.row = 6
        elif self.rect.bottom < row5_y:
            self.row = 5
        elif self.rect.bottom < row4_y:
            self.row = 4
        elif self.rect.bottom < row3_y:
            self.row = 3
        elif self.rect.bottom < row2_y:
            self.row = 2
        else:
            self.row = 1

    def pursue_player(self):
        """Make the flame tend to move towards the player's X position"""
        if random.randint(0, 9) < 7:  # 70% chance to pursue
            if player.rect.centerx > self.rect.centerx:
                self.x_change = abs(self.x_change)
            elif player.rect.centerx < self.rect.centerx:
                self.x_change = -abs(self.x_change)


class Bridge:
    def __init__(self, x_pos, y_pos, length):
        self.x_pos = x_pos * section_width
        self.y_pos = y_pos
        self.length = length
        self.top = self.draw()

    def draw(self):
        line_width = max(3, section_height // 3)
        platform_color = (225, 51, 129)
        for i in range(self.length):
            bot_coord = self.y_pos + section_height
            left_coord = self.x_pos + (section_width * i)
            mid_coord = left_coord + (section_width * 0.5)
            right_coord = left_coord + section_width
            top_coord = self.y_pos
            pygame.draw.line(screen, platform_color, (left_coord, top_coord),
                             (right_coord, top_coord), line_width)
            pygame.draw.line(screen, platform_color, (left_coord, bot_coord),
                             (right_coord, bot_coord), line_width)
            pygame.draw.line(screen, platform_color, (left_coord, bot_coord),
                             (mid_coord, top_coord), line_width)
            pygame.draw.line(screen, platform_color, (mid_coord, top_coord),
                             (right_coord, bot_coord), line_width)
        top_line = pygame.rect.Rect((self.x_pos, self.y_pos), (self.length * section_width, 2))
        return top_line


class Ladder:
    def __init__(self, x_pos, y_pos, length):
        self.x_pos = x_pos * section_width
        self.y_pos = y_pos
        self.length = length
        self.body = self.draw()

    def draw(self):
        line_width = 3
        lad_color = 'light blue'
        lad_height = 0.6
        for i in range(self.length):
            top_coord = self.y_pos + lad_height * section_height * i
            bot_coord = top_coord + lad_height * section_height
            mid_coord = (lad_height / 2) * section_height + top_coord
            left_coord = self.x_pos
            right_coord = left_coord + section_width
            pygame.draw.line(screen, lad_color, (left_coord, top_coord), (left_coord, bot_coord), line_width)
            pygame.draw.line(screen, lad_color, (right_coord, top_coord), (right_coord, bot_coord), line_width)
            pygame.draw.line(screen, lad_color, (left_coord, mid_coord), (right_coord, mid_coord), line_width)
        body = pygame.rect.Rect((self.x_pos, self.y_pos - section_height),
                                (section_width, int(lad_height * self.length * section_height + section_height)))
        return body


def draw_screen():
    platforms = []
    climbers = []
    ladder_objs = []
    bridge_objs = []

    ladders_data = levels[active_level]['ladders']
    bridges_data = levels[active_level]['bridges']

    for ladder in ladders_data:
        ladder_objs.append(Ladder(*ladder))
        if ladder[2] >= 3:
            climbers.append(ladder_objs[-1].body)
    for bridge in bridges_data:
        bridge_objs.append(Bridge(*bridge))
        platforms.append(bridge_objs[-1].top)

    return platforms, climbers


def draw_extras():
    screen.blit(font.render(f'I*{score}', True, 'white'), (int(3*section_width), int(1.8*section_height)))
    screen.blit(font.render(f'TOP*{high_score}', True, 'white'), (int(13 * section_width), int(1.8 * section_height)))
    screen.blit(font2.render(f'  M    BONUS     L ', True, 'yellow'), (int(19 * section_width + 5), int(3.8 * section_height)))
    screen.blit(font2.render(f'  {lives}       {bonus}        {active_level + 1}  ', True, 'white'),
                (int(19 * section_width + 5), int(4.8 * section_height)))
    if barrel_count < barrel_spawn_time / 2:
        screen.blit(peach1, (10 * section_width, row6_y - 6 * section_height))
    else:
        screen.blit(peach2, (10 * section_width, row6_y - 6 * section_height))
    oil = draw_oil()
    draw_barrels()
    draw_kong()
    return oil


def draw_oil():
    x_coord, y_coord = 4 * section_width, window_height - 4.5 * section_height
    oil = pygame.draw.rect(screen, 'blue', [x_coord, y_coord, 2 * section_width, 2.5 * section_height])
    pygame.draw.rect(screen, 'blue', [x_coord - 0.1 * section_width, y_coord, 2.2 * section_width, .2 * section_height])
    pygame.draw.rect(screen, 'blue',
                     [x_coord - 0.1 * section_width, y_coord + 2.3 * section_height, 2.2 * section_width,
                      .2 * section_height])
    pygame.draw.rect(screen, 'light blue',
                     [x_coord + 0.1 * section_width, y_coord + .2 * section_height, .2 * section_width,
                      2 * section_height])
    pygame.draw.rect(screen, 'light blue',
                     [x_coord, y_coord + 0.5 * section_height, 2 * section_width, .2 * section_height])

    pygame.draw.rect(screen, 'light blue',
                     [x_coord, y_coord + 1.7 * section_height, 2 * section_width, .2 * section_height])
    screen.blit(font2.render('OIL', True, 'light blue'), (x_coord + .4 * section_width, y_coord + 0.7 * section_height))
    for i in range(4):
        pygame.draw.circle(screen, 'red',
                           (int(x_coord + 0.5 * section_width + i * 0.4 * section_width), int(y_coord + 2.1 * section_height)), 3)
    if counter < 15 or 30 < counter < 45:
        screen.blit(flames_img, (x_coord, y_coord - section_height))
    else:
        screen.blit(pygame.transform.flip(flames_img, True, False), (x_coord, y_coord - section_height))
    return oil


def draw_barrels():
    screen.blit(pygame.transform.rotate(barrel_side, 90), (int(section_width * 1.2), int(5.4 * section_height)))
    screen.blit(pygame.transform.rotate(barrel_side, 90), (int(section_width * 2.5), int(5.4 * section_height)))
    screen.blit(pygame.transform.rotate(barrel_side, 90), (int(section_width * 2.5), int(7.7 * section_height)))
    screen.blit(pygame.transform.rotate(barrel_side, 90), (int(section_width * 1.2), int(7.7 * section_height)))


def draw_kong():
    phase_time = barrel_time // 4
    if barrel_spawn_time - barrel_count > 3 * phase_time:
        dk_img = dk2
    elif barrel_spawn_time - barrel_count > 2 * phase_time:
        dk_img = dk1
    elif barrel_spawn_time - barrel_count > phase_time:
        dk_img = dk3
    else:
        dk_img = pygame.transform.flip(dk1, True, False)
        screen.blit(barrel_img, (int(3.5 * section_width + 10), int(row6_y - 3.5 * section_height)))
    screen.blit(dk_img, (int(3.5 * section_width), int(row6_y - 5.5 * section_height)))


def check_climb():
    can_climb = False
    climb_down = False
    under = pygame.rect.Rect((player.rect[0], player.rect[1] + 2 * section_height), (player.rect[2], player.rect[3]))
    for lad in lads:
        if player.hitbox.colliderect(lad) and not can_climb:
            can_climb = True
        if under.colliderect(lad):
            climb_down = True
    if (not can_climb and (not climb_down or player.y_change < 0)) or             (player.landed and can_climb and player.y_change > 0 and not climb_down):
        player.climbing = False
    return can_climb, climb_down


def barrel_collide(reset):
    global score
    under = pygame.rect.Rect((player.rect[0], player.rect[1] + 2 * section_height), (player.rect[2], player.rect[3]))
    for brl in barrels:
        if brl.rect.colliderect(player.hitbox):
            reset = True
        elif not player.landed and not player.over_barrel and under.colliderect(brl):
            player.over_barrel = True
            score += 100
    if player.landed:
        player.over_barrel = False
    return reset


def reset():
    global player, barrels, flames, hammers, first_fireball_trigger, victory, lives, bonus
    global barrel_spawn_time, barrel_count
    pygame.time.delay(600)
    for bar in barrels:
        bar.kill()
    for flam in flames:
        flam.kill()
    for hams in hammers:
        hams.kill()
    for hams in hammers_list:
        hammers.add(Hammer(*hams))
    lives -= 1
    bonus = 6000
    player.kill()
    player = Player(250, window_height - 130)
    first_fireball_trigger = False
    barrel_spawn_time = 360
    barrel_count = barrel_spawn_time / 2
    victory = False


def check_victory():
    target = levels[active_level]['target']
    target_rect = pygame.rect.Rect((target[0]*section_width, target[1]), (section_width*target[2], 1))
    return player.bottom.colliderect(target_rect)


def run_game(existing_high_score=0):
    global score, high_score, bonus, counter, barrel_count, barrel_time, barrel_spawn_time
    global fireball_trigger, first_fireball_trigger, victory, reset_game, lives
    global plats, lads, oil_drum

    init_game()
    if existing_high_score > high_score:
        high_score = existing_high_score

    run = True
    while run:
        screen.fill('black')
        timer.tick(fps)
        if counter < 60:
            counter += 1
        else:
            counter = 0
            if bonus > 0:
                bonus -= 100

        plats, lads = draw_screen()
        oil_drum = draw_extras()
        climb, down = check_climb()
        victory = check_victory()

        if barrel_count < barrel_spawn_time:
            barrel_count += 1
        else:
            barrel_count = random.randint(0, 120)
            barrel_time = barrel_spawn_time - barrel_count
            barrel = Barrel(int(4.5 * section_width), int(row6_y - 4 * section_height))
            barrels.add(barrel)
            if not first_fireball_trigger:
                flame = Flame(5*section_width, window_height - 4*section_height)
                flames.add(flame)
                first_fireball_trigger = True

        for b in list(barrels):
            b.draw()
            b.check_fall()
            fireball_trigger = b.update(fireball_trigger)
            if b.rect.colliderect(player.hammer_box) and player.hammer:
                b.kill()
                score += 500

        if fireball_trigger:
            flame = Flame(5 * section_width, window_height - 4 * section_height)
            flames.add(flame)
            fireball_trigger = False

        for f in list(flames):
            f.check_climb()
            f.pursue_player()
            if f.rect.colliderect(player.hitbox):
                reset_game = True
        flames.draw(screen)
        flames.update()
        player.update()
        player.draw()
        for ham in hammers:
            ham.draw()

        reset_game = barrel_collide(reset_game)
        if reset_game:
            if lives > 0:
                reset()
                reset_game = False
            else:
                run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_RIGHT and not player.climbing:
                    player.x_change = 1
                    player.dir = 1
                if event.key == pygame.K_LEFT and not player.climbing:
                    player.x_change = -1
                    player.dir = -1
                if event.key == pygame.K_SPACE and player.landed:
                    player.landed = False
                    player.y_change = -4.5
                if event.key == pygame.K_UP:
                    if climb:
                        player.y_change = -2
                        player.x_change = 0
                        player.climbing = True
                if event.key == pygame.K_DOWN:
                    if down:
                        player.y_change = 2
                        player.x_change = 0
                        player.climbing = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    player.x_change = 0
                if event.key == pygame.K_LEFT:
                    player.x_change = 0
                if event.key == pygame.K_UP:
                    if climb:
                        player.y_change = 0
                    if player.climbing and player.landed:
                        player.climbing = False
                if event.key == pygame.K_DOWN:
                    if climb:
                        player.y_change = 0
                    if player.climbing and player.landed:
                        player.climbing = False

        if victory:
            vic_surf = font.render('VICTORY!', True, 'gold')
            screen.blit(vic_surf, (window_width // 2 - vic_surf.get_width() // 2, window_height // 2))
            pygame.display.flip()
            pygame.time.delay(1200)
            reset_game = True
            lives += 1
            score += bonus
            if score > high_score:
                high_score = score
            player.climbing = False

        pygame.display.flip()

    if score > high_score:
        high_score = score

    if lives <= 0:
        go_surf = font.render('GAME OVER', True, 'red')
        sc_surf = font2.render(f'Puntaje Final: {score}', True, 'white')
        screen.blit(go_surf, (window_width // 2 - go_surf.get_width() // 2, window_height // 2 - 40))
        screen.blit(sc_surf, (window_width // 2 - sc_surf.get_width() // 2, window_height // 2 + 20))
        pygame.display.flip()
        pygame.time.delay(1800)

    final_score = score
    final_hs = high_score
    try:
        pygame.display.quit()
        pygame.quit()
    except Exception:
        pass

    return final_score, final_hs


if __name__ == '__main__':
    if '--game-only' in sys.argv:
        final_s, final_hs = run_game()
        print(f'Juego finalizado. Puntaje: {final_s}, High Score: {final_hs}')
    else:
        try:
            import gui_launcher
            gui_launcher.main()
        except ImportError:
            run_game()
