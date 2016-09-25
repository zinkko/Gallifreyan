import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk

def btn_a(widget, event):
    print('a')

class ToolBar(Gtk.VBox):

    def __init__(self, ui, logic):
        super(Gtk.VBox, self).__init__(True, 0)
        self.ui = ui
        self.logic = logic
        btnA = Gtk.Button("button A")
        btnB = Gtk.Button("button B")
        helloBtn = Gtk.Button("hello!")
        clearBtn = Gtk.Button("clear shapes")

        btnA.connect("button-press-event", btn_a)
        clearBtn.connect("button-press-event", self.clear_all)

        for button in [btnA, btnB, helloBtn, clearBtn]:
            self.pack_start(button, expand = False, fill = True, padding = 0)

    def clear_all(self, widget, event):
        self.logic.clear_all()
        self.ui.queue_draw()
