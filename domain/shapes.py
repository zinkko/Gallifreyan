from math import pi
from library import *

class Shape(object):

    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.pos = x,y
        self.radius = r
        self.children = []
        self.params = (x,y,r)

    def get_draw_params(self):
        return []

class CirclePlusPlus(Shape):

    def __init__(self,x,y,r):
        super(CirclePlusPlus, self).__init__(x,y,r)
        self.arcs = [(0, 2*pi)]
        self.connected = None

    def get_draw_params(self):
        return [('arc',) + self.params + x for x in self.arcs]

    def main_arc(self, a1, a2, context):
        context.arc(self.x, self.y,  self.r, a1, a2)
        context.stroke()


    def make_inset(self, begin, end, angle = pi/3):
        inset = Inset(begin, end, angle)
        self.add_child(inset)


    def add_child(self, child, allow_overlap=False):
        self.children.append(child)
        if (not allow_overlap):
            self.remove_segment(*child.crop_angles)

    def remove_segment(self, begin, end):
        epsilon = 0.001
        begin %= 2*pi + epsilon
        end %= 2*pi + epsilon
        if (begin > end):
            if begin < 2*pi:
                self.remove_segment(begin, 2*pi)
            if end > 0:
                self.remove_segment(0, end)
            return
        new_arcs = []
        for arc in self.arcs:
            if not self.collide((begin, end), arc):
                new_arcs.append(arc)
                continue
            arc_a, arc_b = arc
            left = (arc_a, begin)
            right = (end, arc_b)
            if (left[0] < left[1]):
                new_arcs.append(left)
            if (right[0] < right[1]):
                new_arcs.append(right)
        self.arcs = new_arcs

    def collide(self, t1, t2):
        if t1 < t2:
            smaller, larger = t1, t2
        else:
            smaller, larger = t2, t1
        return smaller[1] > larger[0]

class Inset(Shape):

    def __init__(self, start, end, inset = pi/3):
        super(Inset, self).__init__(*inset_params(start, end, inset))
        self.crop_angles = start, end
        a_s, a_e = end - inset + pi, start + inset - pi
        self.angles = (a_s, a_e)
        self.start_angle, self.end_angle = start, end
        self.inset = inset
        if end > start:
            self.opening = end - start
        else:
            self.opening = 2*pi - start + end
        self.overlap = True

    def get_draw_params(self):
        return [('arc',) + self.params + self.angles]

class Circle(Shape):

    def __init__(self, x, y, r, overlap = False):
        super(Circle, self).__init__(x,y,r)
        self.overlap = overlap
        self.crop_angles = circle_crop_angles(self.params)

    def get_draw_params(self):
        return [('circle',) + self.params]

class Ring(Shape):

    def __init__(self, x, y, r, arcs = [(0, 2*pi)]):
        super(Ring, self).__init__(x,y,r)
        self.arcs = arcs

    def get_draw_params(self):
        return [('arc',) + self.params + arc for arc in self.arcs]

class Line(Shape):

    def __init__(self, x1, y1, x2, y2):
        super(Line, self).__init__(0,0,1)
        self.start = (x1, y1)
        self.end = (x2, y2)

    def get_draw_params(self):
        return [('line',) + self.start + self.end]

class Dot(Shape):

    def __init__(self, x, y):
        super(Dot, self).__init__(x, y, .1)

    def get_draw_params(self):
        return [('dot',) + self.params]

class Polygon(Shape):

    def __init__(self, x, y, n, r, alpha=pi/2, overlap=False):
        if n<3:
            raise ValueError('n must be at least 3')
        super(Polygon, self).__init__(x,y,r)
        self.n = n # number of sides
        self.alpha = alpha # orientation of the polygon
        self.overlap = overlap
        self.children = []
        self.crop_angles = polygon_crop_angles(self)

    def get_points(self):
        points = []
        angle = self.alpha
        increment = 2*pi/self.n
        x,y = 0,0
        for i in range(self.n):
            point = point_at(*self.params, angle)
            points.append(point)
            angle += increment
        return points

    def set_points(list_of_points):
        # arbitrary polygon
        # this should be an overriding constructor...
        self.points = list_of_points

    def get_draw_params(self):
        return [('polygon', self.get_points())]
