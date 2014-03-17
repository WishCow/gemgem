from event import *
from pygame.locals import *
from model import *
import pygame

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
    def __init__(self, evtmgr):
        self.evtmgr = evtmgr
        self.board = None

    def notify(self, e):
        if isinstance(e, InitEvent):
            self.board = Board(6, 5)
            self.board.init()
            self.board.fill_random()
            self.board.select((2, 2))
        if isinstance(e, DrawEvent):
            self.board.draw(e.surface)
        if isinstance(e, KeyboardEvent):
            if e.key in [ K_UP, K_DOWN, K_LEFT, K_RIGHT ]:
                self.board.move(e.key)
            if e.key == K_RETURN:
                if (self.board.is_holding()):
                    self.board.swap()
                else:
                    self.board.hold()
