import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk

class ToolBar(Gtk.VBox):

    def __init__(self, ui):
        super(Gtk.VBox, self).__init__(True, 0)
        self.ui = ui
        btnA = Gtk.Button("button A")
        btnB = Gtk.Button("button B")
        helloBtn = Gtk.Button("hello!")

        btnA.connect("button-press-event", self.btn_a)

        self.pack_start(btnA, expand = False, fill = True, padding = 0)
        self.pack_start(btnB, expand = False, fill = True, padding = 0)
        self.pack_start(helloBtn, expand = False, fill = True, padding = 0)

    def btn_a(self, wid, e):
        print('a')
