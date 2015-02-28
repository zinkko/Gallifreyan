import cairo
from gi.repository import Gtk
from math import pi

class Painter(Gtk.Window):
    
    def __init__(self, objects):
        #super(Painter,self).__init__()
        #self.setup()
        self.objects = objects
        self.epsilon = 0.01
        self.pos = (0,0) # position of center in logical coordinates
        self.size = 1 # window_height/2 in logical coordinates
        self.scale = lambda x, factor: tuple(map(lambda a:factor*a, x))
        
    
    def paint(self, context, height):

        # window mappings
        initial_factor = (height/2)/self.size
        x,y = self.pos
        context.translate(-x*initial_factor, -y*initial_factor)

        for obj in self.objects:
            self.recursive_draw(obj, context, initial_factor) 
        

    def recursive_draw(self, drawable, context, size_factor):
        new_factor = size_factor * drawable.radius
        if size_factor > self.epsilon:
            self.draw(drawable.get_draw_params(), context, size_factor)
        else:
            return # this will cause issues if tiny objects have large children
            # still, something like this is necessary for infinite nesting
        context.save()
        context.translate(*self.scale(drawable.pos, size_factor))
        for child in drawable.children:
            self.recursive_draw(child, context, new_factor)
        context.restore()

    def draw(self, draw_objs, context, size_factor):
        functions = {'circle':self.draw_circle, 
          'arc':self.draw_arc,
          'polygon':self.draw_polygon}
        for parameters in draw_objs:
            name, params = parameters[0], parameters[1:]
            functions[name](params, context, size_factor)

    def draw_circle(self, params, context, factor):
        params = self.scale(params, factor) + (0,2*pi)
        context.arc(*params)
        context.stroke()

    def draw_arc(self, params, context, factor):
        params = self.scale(params[:3], factor) + params[3:]
        context.arc(*params)
        context.stroke()

    def draw_polygon(self, points, context, factor):
        points = points[0] # unpack totally unnecessary tuple...
        for i in range(len(points)-1):
            context.move_to(*self.scale(points[i], factor))
            context.line_to(*self.scale(points[i+1], factor))
        context.move_to(*self.scale(points[-1], factor))
        context.line_to(*self.scale(points[0], factor))
        context.stroke()


