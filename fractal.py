from ui import UI
from cairo_painter import Painter
from shapes import Polygon
from math import sqrt, pi


# Poly(x,y,n,size,orientation = pi/2)

main = Polygon(0, 0, 6, 0.5)

l = 0.75
h = sqrt(3)*l

one = Polygon(-2*l, 0, 6, 0.3)
two = Polygon( 2*l, 0, 6, 0.3)
three = Polygon(l, h, 6, 0.3)
four = Polygon(l, -h, 6, 0.3)
five = Polygon(-l, h, 6, 0.3)
six =  Polygon(-l, -h, 6, 0.3)

even = [two, five, six]

odd = [one, three, four]

main.children.extend(odd + [main])

for _hex in odd:
    _hex.children.extend(odd)

for _hex in even:
    _hex.children.extend(odd)

painter = Painter([main])

ui = UI(painter)

ui.start()
