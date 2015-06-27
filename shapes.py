from math import pi
from library import *


class CirclePlusPlus(object):
    
    def __init__(self,x,y,r):
        self.pos = (x,y)
        self.params = (self.x, self.y, self.radius) = (x,y,r)
        self.children = []
        self.arcs = [(0, 2*pi)]

    def get_draw_params(self):
        return map(lambda x: ('arc',) + self.params + x, self.arcs)

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
            self.remove_segment(begin, 2*pi)
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

    #def add_overlapping_circle(self, radius, pos_angle, distance):
    #    x, y = point_at(0,0, distance, pos_angle) # relative coords
    #    circle = Circle(x,y,radius, True)
    #    angle = alpha(radius, 1, distance) # self.radius is 1 in the relative coords
    #    circle.start_angle = pos_angle - angle
    #    circle.end_angle = pos_angle + angle
    #    self.children.append(circle)
    #    return circle # should the caller want to use this circle

class Inset(object):
    
    def __init__(self, start, end, inset = pi/3):
        x,y, self.radius = inset_params(start, end, inset)
        self.pos = (x,y)
        self.crop_angles = start, end
        a_s, a_e = end - inset + pi, start + inset - pi
        self.params = (x, y, self.radius, a_s, a_e)
        self.start_angle, self.end_angle = start, end
        self.inset = inset
        if end > start:
            self.opening = end - start
        else:
            self.opening = 2*pi - start + end
        self.overlap = True
        self.children = []

    def get_draw_params(self):
        return [('arc',) + self.params]


class Circle(object):
    
    def __init__(self, x, y, r, overlap = False):
        self.params = (x,y,r)
        self.pos = (x,y)
        self.overlap = overlap 
        self.radius = r
        self.children = []
        self.crop_angles = circle_crop_angles(self.params)
    
    def get_draw_params(self):
        return [('circle',) + self.params]

class Polygon(object):
    
    def __init__(self, x, y, n, size, alpha=pi/2):
        if n<3:
            raise ValueError('n must be at least 3')
        self.x = x
        self.y = y
        self.pos = (x,y)
        self.n = n # number of sides
        self.radius = self.size = size
        self.alpha = alpha # orientation of the polygon
        self.points = self.init_points()
        self.children = []
        
    def init_points(self):
        points = []
        angle = self.alpha
        increment = 2*pi/self.n
        x,y = 0,0
        for i in range(self.n):
            point = point_at(self.x, self.y, self.size, angle)
            points.append(point)
            angle += increment
        return points

    def set_points(list_of_points):
        # arbitrary polygon
        # this should be an overriding constructor...
        self.points = list_of_points

    def get_draw_params(self):
        return [('polygon', self.points)]
