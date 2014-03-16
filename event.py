from weakref import WeakKeyDictionary

class Event:
    def __init__(self, name):
        self.name = name

class TickEvent(Event):
    def __init__(self):
        Event.__init__(self, "Tick")

class QuitEvent(Event):
    def __init__(self):
        Event.__init__(self, "Quit")

class InitEvent(Event):
    def __init__(self):
        Event.__init__(self, "Init")

class DrawEvent(Event):
    def __init__(self, surface):
        Event.__init__(self, "Init")
        self.surface = surface

class KeyboardEvent(Event):
    def __init__(self, key):
        Event.__init__(self, "Keypress")
        self.key = key

class EventManager:
    def __init__(self):
        self.listeners = {}

    def add(self, listener):
        self.listeners[listener] = 1

    def remove(self, listener):
        if listener in self.listeners.keys():
            del self.listeners[listener]

    def trigger(self, event):
        for l in self.listeners.keys():
            l.notify(event)
