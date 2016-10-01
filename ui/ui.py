import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk
from math import pi
from signal import signal
from signal import SIGINT, SIG_DFL

from .toolbar import ToolBar

class UI(Gtk.Window):

    def __init__(self, painter, logic):
        self.logic = logic
        super(UI, self).__init__()
        self.setup()
        self.painter = painter
        self.input_mode = 'select'

    def setup(self):

        self.box = Gtk.HBox(False, 0)

        self.canvas = Gtk.DrawingArea()
        self.canvas.connect("draw", self.on_draw)
        self.canvas.set_events(Gdk.EventMask.BUTTON_PRESS_MASK
                                | Gdk.EventMask.BUTTON_RELEASE_MASK
                                | Gdk.EventMask.BUTTON1_MOTION_MASK)
        self.canvas.connect("motion-notify-event", self.on_drag)
        self.canvas.connect("button-press-event", self.on_button_press)
        self.canvas.connect("button-press-event", self.on_button_release)
        self.box.pack_start(self.canvas, expand=True, fill=True, padding=0)

        self.set_events(Gdk.EventMask.KEY_PRESS_MASK)
        self.connect("key-press-event", self.on_key_press)

        toolbar = ToolBar(self, self.logic)
        self.box.pack_start(toolbar, expand = False, fill = True, padding = 0)

        self.add(self.box)

        self.set_title("Gallifreyan")
        self.resize(1000,500)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect('delete-event', Gtk.main_quit)
        self.show_all()

    def map_coordinates(self, x, y):
        win_x, win_y, width, height = self.canvas.get_window().get_geometry()
        scale = min(width, height) / 2
        x = (x - win_x - width/2) / scale
        y = -1 * (y - win_y - height/2) / scale
        return (x,y)

    def on_draw(self, wid, context):

        #context.set_source_rgb(0.33, 0.02, 0.26)
        #context.set_line_width(1.4)

        _,_,w,h = self.canvas.get_window().get_geometry()
        context.translate(w/2, h/2)

        context.scale(1,-1)

        self.painter.paint(context, h, self.logic.objects)

    def set_input_mode(self, mode):
        self.input_mode = mode
        if mode != 'select':
            self.logic.set_draw_shape(mode)

    def on_button_press(self, widget, event):

        if event.button == 3: # right mouse btn
            self.painter.hilight(self.logic.selected_object, None)
            self.logic.deselect()
            self.queue_draw()
            return

        _, x, y, _ = event.window.get_pointer()
        x,y = self.map_coordinates(x,y)
        
        if self.input_mode == 'select':
            self.painter.hilight(self.logic.selected_object, None)
            self.logic.select_shape_at(x, y)
            self.painter.hilight(self.logic.selected_object, (0,1,0))
            self.queue_draw()
        else:
            self.logic.start_draw(x,y)

    def on_button_release(self, wid, event):
        pass

    def on_key_press(self, widget, event):
        keyname = Gdk.keyval_name(event.keyval)
        try:
            self.logic.set_n(int(keyname))
        except ValueError:
            pass

    def on_drag(self, widget, event):
        if self.input_mode == 'select':
            return
        _, x, y, _ = event.window.get_pointer()
        x,y = self.map_coordinates(x,y)
        self.logic.notify_motion(x,y)
        self.queue_draw()

    def start(self):
        signal(SIGINT, SIG_DFL)
        Gtk.main()
