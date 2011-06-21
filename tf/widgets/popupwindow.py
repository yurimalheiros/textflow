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

class PopupWindow(gtk.Window):
    def __init__(self, wtype=gtk.WINDOW_TOPLEVEL):
        gtk.Window.__init__(self, wtype)
        self.set_keep_above(True)
        self.set_decorated(False)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)

        self.build()
        self.connect('delete-event', lambda x, y: x.destroy())

    #################### Public Methods ####################
    
    def run(self, pos=None):
        self.show_all()
        
        if pos != None:
            self.move(pos[0], pos[1])
            
        return True

    def build(self):
        self.set_size_request(202, 55)
        self.set_border_width(6)

