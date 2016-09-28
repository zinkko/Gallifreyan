import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk

class ToolBar(Gtk.VBox):

    def __init__(self, ui, logic):
        super(Gtk.VBox, self).__init__(True, 0)
        self.ui = ui
        self.logic = logic

        self.create_radio_buttons()

        saveBtn = Gtk.Button("Save")
        loadBtn = Gtk.Button("Load from file")
        clearBtn = Gtk.Button("clear shapes")

        clearBtn.connect("button-press-event", self.clear_all)

        for button in [saveBtn, loadBtn, clearBtn]:
            self.pack_start(button, expand = False, fill = True, padding = 0)

    def create_radio_buttons(self):
        button = None

        for shape in ["circle", "polygon"]:
            button = Gtk.RadioButton(group=button, label=shape)
            button.connect("toggled", self.change_shape, shape)
            self.pack_start(button, False, True, 0)

    def change_shape(self, widget, data):
        self.logic.set_draw_shape(data)

    def clear_all(self, widget, event):
        self.logic.clear_all()
        self.ui.queue_draw()
