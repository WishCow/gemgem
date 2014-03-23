from event import *
from pygame.locals import *
from model import *
import pygame
from pprint import pprint

class CPUTickController:
    def __init__(self, evtmgr):
        self.evtmgr = evtmgr
        self.keep_going = True
        self.clock = pygame.time.Clock()

    def notify(self, event):
        if isinstance(event, QuitEvent):
            self.keep_going = False

    def run(self):
        while self.keep_going:
            self.clock.tick(20)
            self.evtmgr.trigger(TickEvent())

class KeyboardController:
    def __init__(self, evtmgr):
        self.evtmgr = evtmgr
        self.suspend = False

    def notify(self, event):
        if isinstance(event, TickEvent):
            for event in pygame.event.get():
                ev = None
                if event.type == QUIT:
                    ev = QuitEvent()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        ev = QuitEvent()
                    else:
                        ev = KeyboardEvent(event.key)
                if ev:
                    self.evtmgr.trigger(ev)
        elif isinstance(event, MatchEvent):
            self.suspend = True
        elif isinstance(event, MatchResolvedEvent):
            self.suspend = False

class PygameController:
    def __init__(self, evtmgr):
        self.evtmgr = evtmgr

    def notify(self, event):
        if isinstance(event, InitEvent):
            pygame.display.init()
            pygame.font.init()
            self.window = pygame.display.set_mode((600, 600))
            pygame.display.set_caption('Gemgem')
            pygame.font.Font('freesansbold.ttf', 36)

        if isinstance(event, TickEvent):
            self.window.fill((0, 0, 0))
            self.evtmgr.trigger(DrawEvent(self.window))
            pygame.display.flip()

class ModelController:
    def __init__(self, evtmgr, board):
        self.evtmgr = evtmgr
        self.board = board

    def notify(self, e):
        if isinstance(e, MatchResolvedEvent):
            for p in e.matches:
                self.board.remove(p)

        if isinstance(e, KeyboardEvent):
            if e.key in [ K_UP, K_DOWN, K_LEFT, K_RIGHT ]:
                self.board.move(e.key)
            if e.key == K_RETURN:
                if (self.board.is_holding()):
                    if (self.board.is_valid_swap()):
                        self.board.swap()
                        if self.board.has_match():
                            self.evtmgr.trigger(MatchEvent(self.board.find_matches()))
                    else:
                        self.board.release()
                else:
                    self.board.hold()

GEMSIZE = 64
class AnimationController:
    def __init__(self, evtmgr, board):
        self.evtmgr = evtmgr
        self.matches = []
        self.board = board
        self.tick = 0

    def notify(self, e):
        if isinstance(e, MatchEvent):
            self.matches = e.matches
        if isinstance(e, DrawEvent):
            for x, row in enumerate(self.board.gems):
                for y, gem in enumerate(row):
                    pos = (x * GEMSIZE, y * GEMSIZE)
                    color = (30, 30, 30)
                    if self.board.held == (x, y):
                        color = (255, 0, 0)
                    elif self.board.selected == (x, y):
                        color = (255, 255, 0)
                    pygame.draw.rect(e.surface, color, pygame.Rect(pos, (GEMSIZE, GEMSIZE)), 1)
                    if gem:
                        if (x, y) in self.matches:
                            self.evtmgr.trigger(MatchResolvedEvent(self.matches))
                        else:
                            e.surface.blit(gem.surface, pos)
        if isinstance(e, MatchResolvedEvent):
            self.reset()

    def reset(self):
        self.tick = 0
        self.matches = []
