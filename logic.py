from shapes import *

from math import hypot

class Logic(object):

    def __init__(self, objects = None):
        self.objects = objects or []
        self.new_object = None

    def clear_all(self):
        self.objects = []

    def start_draw(self, x, y):
        self.new_object = Circle(x, y, 0)
        print("create circle", x, y)
        self.objects.append(self.new_object)

    def notify_motion(self, x, y):
        if self.new_object is None:
            return
        ox, oy, _ = self.new_object.params
        self.new_object.r = hypot(abs(ox-x), abs(oy-y))
        self.new_object.params = (ox, oy, self.new_object.r)
