from ui import UI
from cairo_painter import Painter
from shapes import *

# ui = UserInterface(some_nice_painter)

test_shape1 = CirclePlusPlus(0.12,-0.32,0.40)
test_shape2 = CirclePlusPlus(-0.20,0.52,0.40)
test_shape3 = Polygon(0.8,0.8,7,0.12)

step = pi/6

test_shape1.add_inset(0, step)
test_shape1.add_inset(4*step,5*step)
test_shape1.children.append(Circle(-0.8, 0, 0.2))
test_shape1.add_overlapping_circle(0.2, 5*pi/4, 1.1)



ins = Inset(step, 2*step)
ins.children.append(Polygon(0,0, 6, 0.5, 3*step/2))
ins.children.append(Circle(-0.7,-0.5, 0.1))
test_shape2.children.append(ins)
test_shape2.children.append(Circle(-1,0,0.2))
scnd = Inset(9.8*step, 10.8*step)
scnd.children.append(test_shape2)
test_shape2.children.append(scnd)

shapes = [test_shape1, test_shape2, test_shape3]

painter = Painter(shapes)

ui = UI(painter)

ui.start()
