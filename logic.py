from shapes import *

from math import hypot

class Logic(object):

    def __init__(self, objects = None):
        self.objects = objects or []
        self.new_object = None
        self.next_shape = 'circle'
        self.n = 6

    def clear_all(self):
        self.objects = []

    def create_object(self, x, y):
        xyz = {
                'circle' : lambda x, y : Circle(x,y,0),
                'polygon' : lambda x, y : Polygon(x, y, self.n, 0),
              }
        return xyz[self.next_shape](x,y)

    def set_n(self, n):
        if n > 2: self.n = n

    def start_draw(self, x, y):
        self.new_object = self.create_object(x, y)
        self.objects.append(self.new_object)

    def notify_motion(self, x, y):
        if self.new_object is None:
            return
        ox, oy, _ = self.new_object.params
        self.new_object.r = hypot(abs(ox-x), abs(oy-y))
        self.new_object.params = (ox, oy, self.new_object.r)

    def set_draw_shape(self, data):
        self.next_shape = data
