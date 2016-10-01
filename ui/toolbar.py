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
        entry = Gtk.Entry()

        clearBtn.connect("button-press-event", self.clear_all)

        entry.connect("key-press-event", self.enter_text)
        self.entry = entry # replace with better event

        for button in [entry, saveBtn, loadBtn, clearBtn]:
            self.pack_start(button, expand = False, fill = True, padding = 0)

    def create_radio_buttons(self):
        button = None

        for shape in ["select", "circle", "polygon"]:
            button = Gtk.RadioButton(group=button, label=shape)
            button.connect("toggled", self.change_shape, shape)
            self.pack_start(button, False, True, 0)

    def change_shape(self, widget, data):
        self.ui.set_input_mode(data)

    def enter_text(self, widget, event):
        if event.keyval == 65293: #purkkaa!
            txt = self.entry.get_text()
            self.logic.display_text(txt)
            self.ui.queue_draw()

    def clear_all(self, widget, event):
        self.logic.clear_all()
        self.ui.queue_draw()
