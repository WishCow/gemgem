import pygame
from pprint import pprint
import random
from pygame.locals import *
from pprint import pprint

GEMSIZE = 64

class Board:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.gems = []
        self.selected = ()
        self.held = ()

    def init(self):
        for x in range(self.rows):
            self.gems.append([])
            for y in range(self.columns):
                self.gems[x].append(None)

    def fill_random(self):
        colors = [ "gem{}".format(x) for x in range(1, 7) ];
        for row in range(self.rows):
            for col in range(self.columns):
                color = random.choice(colors)
                self.put(Gem(color, "{}.png".format(color)), (row, col))

    def hold(self):
        self.held = self.selected

    def select(self, pos):
        self.selected = pos

    def move(self, direction):
        changes = { K_UP: (0, -1), K_DOWN: (0, 1), K_RIGHT: (1, 0), K_LEFT: (-1, 0) }
        change = changes.get(direction)
        new_pos = map(sum, zip(self.selected, change))
        if new_pos[1] < 0:
            new_pos[1] = self.columns - 1
        elif new_pos[1] > self.columns - 1:
            new_pos[1] = 0
        elif new_pos[0] < 0:
            new_pos[0] = self.rows - 1
        elif new_pos[0] > self.rows - 1:
            new_pos[0] = 0
        self.select(tuple(new_pos))

    def swap(self):
        if self.held != self.selected:
            s, h = self.selected, self.held
            self.gems[s[0]][s[1]], self.gems[h[0]][h[1]] = self.gems[h[0]][h[1]], self.gems[s[0]][s[1]]
        self.held = ()

    def is_valid_swap():
        return True

    def is_holding(self):
        return self.held != ()

    def move_down(self):
        self.select((self.selected[0], self.selected[1] + 1))

    def move_left(self):
        self.select((self.selected[0] - 1, self.selected[1]))

    def move_right(self):
        self.select((self.selected[0] + 1, self.selected[1]))

    def draw(self, surface):
        for x, row in enumerate(self.gems):
            for y, gem in enumerate(row):
                pos = (x * GEMSIZE, y * GEMSIZE)
                color = (30, 30, 30)
                if self.held == (x, y):
                    color = (255, 0, 0)
                elif self.selected == (x, y):
                    color = (255, 255, 0)
                pygame.draw.rect(surface, color, pygame.Rect(pos, (GEMSIZE, GEMSIZE)), 1)
                if (gem):
                    surface.blit(gem.surface, pos)


    def put(self, gem, at):
        x, y = at
        self.gems[x][y] = gem

    def get(pos):
        return self.gems[pos[0]][pos[1]]

class Gem:
    def __init__(self, id, picture):
        self.picture = picture
        self._surface = None
        self.id = id

    @property
    def surface(self):
        if (self._surface is None):
            self._surface = pygame.image.load(self.picture)
        return self._surface
