import pygame
from pprint import pprint
import random
from pygame.locals import *
from exception import NoGemAtPosition

GEMSIZE = 64
DIRECTIONS = { K_UP: (0, -1), K_DOWN: (0, 1), K_RIGHT: (1, 0), K_LEFT: (-1, 0) }
MATCH = 3

class Board:
    def __init__(self, columns, rows):
        self.rows = rows
        self.columns = columns
        self.gems = []
        self.selected = ()
        self.held = ()

    def init(self):
        for x in range(self.columns):
            self.gems.append([])
            for y in range(self.rows):
                self.gems[x].append(None)

    def fill_random(self):
        colors = [ "gem{}".format(i) for i in range(1, 7) ];
        for col in range(self.columns):
            for row in range(self.rows):
                pos = (col, row)
                possibilities = colors
                random.shuffle(possibilities)
                for possibility in possibilities:
                    print "{} @ {}".format(possibility, pos)
                    self.put(Gem(possibility, "{}.png".format(possibility)), pos)
                    if self.has_match():
                        print "Backtrack"
                        self.remove(pos)
                    else:
                        break

    def at(self, pos):
        x, y = pos
        if 0 <= x < len(self.gems):
            row = self.gems[x]
            if 0 <= y < len(row):
                gem = row[y]
                if isinstance(gem, Gem):
                    return gem
        raise NoGemAtPosition(pos)

    def has(self, pos):
        try:
            gem = self.at(pos)
            return True if isinstance(gem, Gem) else False
        except NoGemAtPosition:
            return False

    def flood_horizontal(self, starting):
        matches = [ starting ]
        gem = self.at(starting)
        i = 1
        while True:
            look_at = tuple(map(sum, zip(starting, (0, i))))
            if self.has(look_at) and self.at(look_at).id == gem.id:
                matches.append(look_at)
                i += 1
            else:
                break
        i = -1
        while True:
            look_at = tuple(map(sum, zip(starting, (0, i))))
            if self.has(look_at) and self.at(look_at).id == gem.id:
                matches.append(look_at)
                i -= 1
            else:
                break
        return matches

    def flood_vertical(self, starting):
        matches = [ starting ]
        gem = self.at(starting)
        i = 1
        while True:
            look_at = tuple(map(sum, zip(starting, (i, 0))))
            if self.has(look_at) and self.at(look_at).id == gem.id:
                matches.append(look_at)
                i += 1
            else:
                break
        i = -1
        while True:
            look_at = tuple(map(sum, zip(starting, (i, 0))))
            if self.has(look_at) and self.at(look_at).id == gem.id:
                matches.append(look_at)
                i -= 1
            else:
                break
        return matches

    def find_matches(self):
        matches = []
        for x in range(self.columns):
            for y in range(self.rows):
                pos = (x, y)
                if not self.has(pos):
                    continue
                horizontal = self.flood_horizontal(pos)
                vertical = self.flood_vertical(pos)
                if len(vertical) >= MATCH:
                    print "Vertical: {}".format(vertical)
                    matches += vertical
                if len(horizontal) >= MATCH:
                    print "Horizontal: {}".format(horizontal)
                    matches += horizontal
        return matches

    def has_match(self):
        return len(self.find_matches()) > 0

    def remove(self, pos):
        x, y = pos
        self.gems[x][y] = None

    def hold(self):
        self.held = self.selected

    def release(self):
        self.held = ()

    def select(self, pos):
        self.selected = pos

    def remove_matches(self):
        for m in self.find_matches():
            self.remove(m)

    def remove(self, pos):
        x, y = pos
        self.gems[x][y] = None

    def move(self, direction):
        change = DIRECTIONS.get(direction)
        x, y = map(sum, zip(self.selected, change))
        if x < 0:
            x = self.columns - 1
        elif x > self.columns - 1:
            x = 0
        elif y < 0:
            y = self.rows - 1
        elif y > self.rows - 1:
            y = 0
        self.select((x, y))

    def swap(self):
        if self.held != self.selected:
            s, h = self.selected, self.held
            self.gems[s[0]][s[1]], self.gems[h[0]][h[1]] = self.gems[h[0]][h[1]], self.gems[s[0]][s[1]]
        self.held = ()

    def is_valid_swap(self):
        return True

    def is_holding(self):
        return self.held != ()

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
