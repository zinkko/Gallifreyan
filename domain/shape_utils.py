import library
from .shapes import *
from math import atan2, cos, sin, hypot, sqrt, pi

def line_to_infinity(child, angle):
    x1, y1 = map(sum, zip(child.pos, library.vector(angle, child.radius)))
    x2, y2 = x1 + cos(angle) * 3, y1 + sin(angle) * 3  # with scaling this should leave the window

    return Line(x1, y1, x2, y2)

def line(child1, child2):
    dy = child2.y - child1.y
    dx = child2.x - child1.x
    angle = atan2(dy, dx)

    x1, y1 = map(sum, zip(child1.pos, library.vector(angle, child1.radius)))
    x2, y2 = map(sum, zip(child2.pos, library.vector(angle, -child2.radius)))

    return Line(x1, y1, x2, y2)

def line_to_parent_arc(child, angle):
    x1, y1 = map(sum, zip(child.pos, library.vector(angle, child.radius)))

    # a = 1
    b = 2 * cos(angle) * x1 + 2 * sin(angle) * y1
    c = x1 ** 2 + y1 ** 2 - 1

    D = b**2 - 4*c

    if D < 0:
        return Line(0,0,0,0) # this wont break anything :D

    l1 = (-b + sqrt(D)) / 2
    l2 = (-b - sqrt(D)) / 2

    # choose one

    x2, y2 = library.point_at(x1, y1, l1, angle)

    return Line(x1, y1, x2, y2)
