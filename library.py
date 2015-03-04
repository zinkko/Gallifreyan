from math import hypot, acos, cos, sin, tan, pi
RIGHT = pi/2.
STRAIGHT = pi
FULL = 2*pi

# parameter 'circle' will expect a tuple (x,y,r)

def vector(angle, length):
    ''' vector (x,y)'''
    return (cos(angle)*length, sin(angle)*length)

def point_at(x, y, radius, angle):
    ''' coordinates of point on circumference of circle (x,y,r) at specified angle'''
    dx, dy = vector(angle, radius)
    return (x+dx, y+dy)

def apollonian_circle(c1,c2,c3, solution_type = 0):
    x1, y1, r1 = c1.params
    x2, y2, r2 = c2.params
    x3, y3, r3 = c3.params
    x,y,r = 0,0,0
    return (x,y,r)

def inset_crop_angles():
    pass

def inset_radius(start_angle, end_angle, inset_angle):
    span = abs(end_angle - start_angle)
    num = sin(span/2)
    den = sin(inset_angle-span/2)
    return num/den

def inset_params(start_angle, end_angle, inset_angle):
    r = inset_radius(start_angle, end_angle, inset_angle)
    x1, y1 = vector(start_angle, 1)
    x2, y2 = vector(start_angle + inset_angle, r)
    x = x1 + x2; y = y1 + y2
    return (x,y,r)

def alpha(a,b,c):
    '''find angle opposite to side "a" in a triangle with sides a,b,c'''
    a2,b2,c2 = map(lambda x:x*x, (a,b,c))
    cos_alpha = (a2-b2-c2)/(2*b*c)
    return acos(cos_alpha)

    
