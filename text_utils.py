import library
from domain.shapes import *

from math import pi

def circle_maker(radius, distance_from_arc):
    def f(angle):
        dist_from_origin = distance_from_arc - 0
        x, y = library.point_at(0, 0, 1 + distance_from_arc, angle)
        return Circle(x, y, radius)
    return f

def inset_maker(depth, breadth):
    def f(angle):
        return Inset(angle - breadth/2, angle + breadth/2, depth)
    return f

vowels = {
    'a': circle_maker(0.05, 0.15),
    'e': circle_maker(0.05, 0),
    'i': circle_maker(0.05, 0),
    'o': circle_maker(0.05, -0.15),
    'u': circle_maker(0.05, 0),
}

c1 = inset_maker(2.6*pi/3, pi/14)
c2 = circle_maker(0.25, -0.25)
c3 = inset_maker(pi/3, pi/6)
c4 = circle_maker(0.25, 0)

consonants = {
    'b': c1, 'ch': c1, 'd': c1, 'f': c1,  'g': c1, 'h': c1,
    'j': c2, 'k' : c2, 'l': c2, 'm': c2,  'n': c2, 'p': c2,
    't': c3, 'sh': c3, 'r': c3, 's': c3,  'v': c3, 'w': c3,
    'th':c4, 'y' : c4, 'ng': c4, 'qu':c4, 'x': c4, 'z': c4,
}


def create_word(word):
    base = CirclePlusPlus(0, 0, 0.8)
    for i, thing in enumerate([c1, c2, c3, c4]):
        base.add_child(thing(i*0.4*pi + 0.1))
        base.add_child(vowels['a'](i*0.4*pi + 0.1))
    return base
