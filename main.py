from ui.ui import UI
from cairo_painter import Painter
from shapes import *
from logic import Logic

# ui = UserInterface(some_nice_painter)

def inset_around(pos, inclination, step=9):
    center = pos * (2 * pi/step)
    half = pi/step
    return Inset(center - half, center + half, inclination)


test_shape1 = CirclePlusPlus(0.12,-0.32,0.40)
test_shape2 = CirclePlusPlus(-0.20,0.52,0.40)
test_shape3 = Polygon(0.8,0.8,7,0.12)

step = pi/6

test_shape1.make_inset(0, step)
test_shape1.make_inset(4*step,5*step)
test_shape1.add_child(Circle(0, 0.8, 0.2), True)
test_shape1.add_child(Circle(-0.8, -0.7, 0.2),False)

circle_test = CirclePlusPlus(-0.55, 0, 0.20)

circle_test.add_child(Circle(0.6, 0.8, 0.2))
circle_test.add_child(Circle(-0.6, 0.8, 0.2))
circle_test.add_child(Circle(0.8, -0.6, 0.2))
circle_test.add_child(Circle(-0.8, -0.6, 0.2))
circle_test.add_child(Circle(0, 1, 0.2))
circle_test.add_child(Circle(1, 0, 0.2))
circle_test.add_child(Circle(-1, 0, 0.2))

inset_test = CirclePlusPlus(0.57, 0.31, 0.20)


big = inset_around(1, pi/1.1)

inset_test.add_child(big)
inset_test.add_child(inset_around(3, pi/3))
inset_test.add_child(inset_around(5, pi/2))
inset_test.add_child(inset_around(7, pi/3))
#inset_test.add_child(inset_around(0, 9, pi/3))

big.children.extend([
    Polygon(0,0, 6, 0.2, pi/9),
    Polygon(0.5, 0.5, 6, 0.15, pi/9),
    Polygon(1,1, 6, 0.1, pi/9)
])


ins = Inset(step, 2*step)
ins.children.append(Polygon(0,0, 6, 0.5, 3*step/2))
ins.children.append(Circle(-0.7,-0.5, 0.1))
test_shape2.add_child(ins)
test_shape2.add_child(Circle(-1,0,0.2), True)
scnd = Inset(9.8*step, 10.8*step)
scnd.children.append(test_shape2)
test_shape2.add_child(scnd)

ring = Ring(0,0,0.92, [(0,1), (3,4), (11/6*pi, 2*pi - 0.1)])
a = 2.95
b = 5.4
l = 1.05
ring.children.append(Circle(cos(a), sin(a), 0.05))
ring.children.append(Circle(cos(b)*l, sin(b)*l, 0.05))

# circle_test
shapes = [test_shape1, test_shape2, inset_test, ring]

painter = Painter()

ui = UI(painter, Logic(shapes))

ui.start()
