import pygame, sys
from pygame.locals import *
from controller import *
from event import EventManager, InitEvent

def main():
    board = Board(6, 5)
    board.init()
    board.fill_random()

    evtmgr = EventManager()
    cpu = CPUTickController(evtmgr)
    evtmgr.add(cpu)
    evtmgr.add(KeyboardController(evtmgr))
    evtmgr.add(PygameController(evtmgr))
    evtmgr.add(ModelController(evtmgr, board))
    evtmgr.add(AnimationController(evtmgr, board))
    evtmgr.trigger(InitEvent())
    cpu.run()

if __name__ == '__main__':
    main()
