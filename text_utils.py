import library
from domain.shapes import *
from domain.shape_utils import *
from random import random, shuffle

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

def length(word):
    length = sum([1 if c in consonants else 0 for c in word])
    # double length consonants will waste space
    for i in range(len(word)-1):
        if word[i] in vowels and word[i+1] in vowels:
            length += 1
    if word[0] in vowels:
        length += 1
    return length

def parse_objects(word):

    angle = 0
    tokens = []
    skip = False
    word_len = length(word)
    angle_increment = 1.9 * pi / word_len

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
                angle -= angle_increment
        else:
            creator, emb, amount = consonants[letter]

        tokens.append((creator(angle), emb, amount, angle))

        angle += angle_increment

    return tokens

def random_point(earlier_points, r, center, radius):
    overlap = True
    while overlap:
        overlap = False
        #x = (random() * 2 -1) * radius + center[0]
        #y = (random() * 2 -1) * radius + center[1]
        x, y = library.vector(random() * library.FULL, random()*radius)
        x, y = library.vector_add((x, y), center)
        for x0, y0 in earlier_points:
            if abs(x-x0) + abs(y-y0) < 2*r:
                overlap = True
                break
    return x, y

def equalize(groupA, groupB, sizeA, sizeB):
    if abs(sizeA - sizeB) < 2:
        return

    if sizeA < sizeB:
        smaller, bigger = groupA, groupB
    else:
        smaller, bigger = groupB, groupA

    planB = None
    swap = None
    for amount, obj in bigger:
        if amount == 1:
            swap = obj
            break
        elif planB is None and amount == 3:
            planB = obj

    if swap is not None:
        bigger.remove((1, swap))
        smaller.append((1, swap))
        return

    swap = None
    if planB is not None:
        for amount, obj in smaller:
            if amount == 2:
                swap = obj
                break
    if swap is not None:
        bigger.remove((3, planB))
        smaller.append((3, planB))
        smaller.remove((2, swap))
        bigger.append((2, swap))

def connect(parent, one, other, angles):
    if parent.connected is None:
        parent.connected = [(one, other), (other, one)]
        parent.children.append(line(one, other))
    elif (one, other) not in parent.connected:
        parent.connected.append((one, other))
        parent.connected.append((other, one))
        parent.children.append(line(one, other))
    else:
        #TODO: get a sane angle
        parent.children.append(line_to_parent_arc(one, angles[one]))
        parent.children.append(line_to_parent_arc(other, angles[other]))
        angles[one] += 0.3
        angles[other] += 0.3

def create_word(word, x, y, size):
    dot_size = Dot(0,0).radius

    base = CirclePlusPlus(x, y, size)

    children = parse_objects(word)

    groupA = []
    groupB = []

    sizeA = 0
    sizeB = 0

    angles = {}

    for child, emb, amount, angle in children:
        base.add_child(child)
        angles[child] = angle - pi
        if emb == '-':
            if amount == -1: # 'u'
                base.children.append(line_to_infinity(child, angle))
            else:
                if sizeA < sizeB:
                    groupA.append((amount, child))
                    sizeA += amount
                else:
                    groupB.append((amount, child))
                    sizeB += amount
        elif emb == '.':
            if type(child) is Inset:
                center = library.vector(angle - pi, 0.7)
                radius = 0.4
            else:
                center = (0,0)
                radius = 0.7
            earlier_points = [] # ensure point don't overlap
            for i in range(amount):
                point = random_point(earlier_points, dot_size, center, radius)
                child.children.append(Dot(*point))
                earlier_points.append(point)

    equalize(groupA, groupB, sizeA, sizeB)

    groupB = groupB[::-1]

    while groupA:
        amount, a = groupA.pop()
        xyz = []
        print(amount, a)
        i = 0
        while i < amount:
            if groupB:
                other_amount, b = groupB.pop()
                if abs(angles[b] - angles[a]) < 0.001:
                    xyz.append((other_amount, b))
                    continue
                connect(base, a, b, angles)
                if other_amount > 1:
                    groupB.insert(0, (other_amount-1, b))
            else:
                angle = angles[a]
                if type(a) is Circle and a.radius == 0.05:
                    angle += 0.2
                base.children.append(line_to_parent_arc(a, angle))
            i += 1
        groupB.extend(xyz)

    while groupB:
        amount, b = groupB.pop()
        for i in range(amount):
            print('line', b)
            angle = angles[b]
            if type(b) is Circle and b.radius == 0.05:
                angle += 0.2
            base.children.append(line_to_parent_arc(b, angle))

    return base
