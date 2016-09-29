from shapes import *
from library import distance_from_shape
from math import hypot

class Logic(object):

    def __init__(self, objects = None):
        self.objects = objects or []
        self.new_object = None
        self.selected_object = None
        self.next_shape = 'circle'
        self.n = 6

    def clear_all(self):
        self.objects = []

    def map_coordinates(self, x, y, parent):
        px, py, r = parent.params
        x = (x - px) / r
        y = (y - py) / r
        return x, y

    def select_shape_at(self, x, y):
        if not self.objects:
            return None

        closest, dist  = self.closest(self.objects, x, y)

        if self.selected_object is not None:
            x, y = self.map_coordinates(x, y, self.selected_object)
            closest_in_children, dist2 = self.closest(self.selected_object.children, x, y)
            #favor children
            if closest_in_children is not None and dist2 * 0.8 < dist:
                self.selected_object = closest_in_children
            else:
                self.selected_object = closest
        else:
            self.selected_object = closest

    def closest(self, objects, x, y):
        if not self.objects:
            return None, None
        closest = self.objects[0]
        distance = distance_from_shape(closest, x, y)

        for obj in objects:
            new_distance = distance_from_shape(obj, x, y)
            if new_distance < distance:
                closest = obj
                distance = new_distance
        return (closest, distance)

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
