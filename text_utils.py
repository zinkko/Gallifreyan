import library
from domain.shapes import *
from domain.shape_utils import *
from random import random

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
    'a': (circle_maker(0.05, 0.15), '.', 0),
    'e': (circle_maker(0.05, 0), '.', 0),
    'i': (circle_maker(0.05, 0), '-', 1),
    'o': (circle_maker(0.05, -0.15), '.', 0),
    'u': (circle_maker(0.05, 0), '-', -1),
}

c1 = inset_maker(2.6*pi/3, pi/14)
c2 = circle_maker(0.25, -0.25)
c3 = inset_maker(pi/3, pi/6)
c4 = circle_maker(0.25, 0)

consonants = {
    'b': (c1, '.', 0), 'ch': (c1, '.', 2), 'd': (c1, '.', 3), 'f': (c1, '-', 3),  'g': (c1, '-', 1), 'h': (c1, '-', 2),
    'j': (c2, '.', 0), 'k' : (c2, '.', 2), 'l': (c2, '.', 3), 'm': (c2, '-', 3),  'n': (c2, '-', 1), 'p': (c2, '-', 2),
    't': (c3, '.', 0), 'sh': (c3, '.', 2), 'r': (c3, '.', 3), 's': (c3, '-', 3),  'v': (c3, '-', 1), 'w': (c3, '-', 2),
    'th':(c4, '.', 0), 'y' : (c4, '.', 2), 'z': (c4, '.', 3), 'ng':(c4, '-', 3), 'qu': (c4, '-', 1), 'x': (c4, '-', 2),
    'q': (c2, '.', 2), 'c': (c2, '.', 2), # same as 'k'
}

def parse_objects(word):

    angle = 0
    tokens = []
    skip = False

    for i, letter in enumerate(word):

        if skip:
            skip = False
            continue

        double = word[i:i+2]
        if double in consonants:
            creator, emb, amount = consonants[double]
            skip = True
        elif letter in vowels:
            creator, emb, amount = vowels[letter]
            if i > 0 and (word[i-1] not in vowels or word[i-2:i] == 'qu'):
                angle -= 2 * pi / len(word)
        else:
            creator, emb, amount = consonants[letter]

        tokens.append((creator(angle), emb, amount, angle))

        angle += 2 * pi / len(word)

    return tokens

def random_point(earlier_points, r):
    overlap = True
    while overlap:
        overlap = False
        x = random() * 0.8
        y = random() * 0.8
        for x0, y0 in earlier_points:
            if abs(x-x0) + abs(y-y0) < 2*r:
                overlap = True
                break
    return x, y

def create_word(word, x, y, size):
    dot_size = Dot(0,0).radius

    children = parse_objects(word)

    base = CirclePlusPlus(x, y, size)

    for child, emb, amount, angle in children:
        base.add_child(child)
        if emb == '-': # more difficult later
            if amount == -1: # 'u'
                base.children.append(line_to_infinity(child, angle))
                continue
            for i in range(amount):
                base.children.append(line_to_parent_arc(child, angle - pi + (i-1) * pi/6))
        elif emb == '.':
            earlier_points = [] # ensure point don't overlap
            for i in range(amount):
                point = random_point(earlier_points, dot_size)
                child.children.append(Dot(*point))
                earlier_points.append(point)

    return base
