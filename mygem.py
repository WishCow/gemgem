import pygame, sys
from pygame.locals import *
from controller import *
from event import EventManager, InitEvent

WINDOWWIDTH = 600
WINDOWHEIGHT = 600

BOARD = (8, 8)

def main():
    evtmgr = EventManager()
    cpu = CPUTickController(evtmgr)
    evtmgr.add(cpu)
    evtmgr.add(KeyboardController(evtmgr))
    evtmgr.add(PygameController(evtmgr))
    evtmgr.add(ModelController(evtmgr))
    evtmgr.trigger(InitEvent())
    cpu.run()

if __name__ == '__main__':
    main()
