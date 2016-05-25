from gi.repository import Gtk, Gdk
from math import pi
from signal import signal
from signal import SIGINT, SIG_DFL

class UI(Gtk.Window):

    def __init__(self, painter):
        super(UI, self).__init__()
        self.setup()
        self.painter = painter
        #self.painter.scale_view(2)

    def setup(self):
        self.canvas = Gtk.DrawingArea()
        self.canvas.connect("draw", self.on_draw)
        self.canvas.set_events(Gdk.EventMask.BUTTON_PRESS_MASK | Gdk.EventMask.KEY_PRESS_MASK)
        self.canvas.connect("button-press-event", self.on_button_press)
        self.canvas.connect("key-press-event", self.on_key_press)
        self.add(self.canvas)

        self.set_title("Gallifreyan")
        self.resize(600,500)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect('delete-event', Gtk.main_quit)
        self.show_all()

    def on_draw(self, wid, context):

        context.set_source_rgb(0.33, 0.02, 0.26)
        context.set_line_width(1.4)
        w,h = self.get_size()
        context.translate(w/2, h/2)

        context.scale(1,-1)

        self.painter.paint(context, h)

    def on_button_press(self, wid, e):
        self.translate(e.x,e.y)

        if e.type == Gdk.EventType.BUTTON_PRESS \
          and e.button == 1:

            self.zoom(2)
        if e.type == Gdk.EventType.BUTTON_PRESS \
          and e.button == 3:

            self.zoom(0.5)

    def on_key_press(self, widget, event):
        keyname = Gdk.keyval_name(event.keyval)
        print(keyname)

    def start(self):
        signal(SIGINT, SIG_DFL)
        Gtk.main()

    def zoom(self, factor):

        if self.painter.size < 2**-16 and factor > 1:
            print('no more zooming in')
            return

        self.painter.size /= 1.*factor
        self.canvas.queue_draw()

    def translate(self, x, y):
        w,h = self.get_size()
        x,y = (x-w/2)/(h/2), 1-y/(h/2)

        n, (o_x, o_y) = self.painter.size, self.painter.pos
        self.painter.pos = (o_x + n*x, o_y + n*y)
        self.canvas.queue_draw()
