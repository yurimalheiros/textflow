# -*- coding: utf-8 -*-

#######################################################################
# Copyright © 2007-2008 Yuri Malheiros.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# the Free Software Foundation; version 2 only.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#######################################################################

"""
This module implements a popup window.
"""

import gtk

from tf.widgets.popupwindow import PopupWindow
from tf.core import constants

class FilterWindow(PopupWindow):
    def __init__(self):
        PopupWindow.__init__(self)
        self.connect('focus-out-event', self.on_focus_out)

    def run(self, pos=None):
        self.show_all()
        self.entry.set_position(-1)

        if pos != None:
            self.move(pos[0], pos[1])
                
        self.entry.grab_focus()
                        
        return True

    #################### Public Methods ####################

    def build(self):
        self.set_border_width(6)
        frame = gtk.Frame(constants.MESSAGE_0027)

        frame.set_shadow_type(gtk.SHADOW_NONE)

        self.entry = gtk.Entry()

        frame.add(self.entry)
        self.add(frame)
        
        self.entry.connect('key-press-event', self.on_entry_key_press)

    #################### Signals ####################
    
    def on_entry_key_press(self, entry, event):
        if event.keyval == gtk.gdk.keyval_from_name('Escape'):
            self.destroy()
            return True

        return False
    
    def on_focus_out(self, wnd, event):
        self.destroy()
        return False
