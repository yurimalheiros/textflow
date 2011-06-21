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
This module implements a class responsible create a alert dialog.
"""

import gtk
from tf.core import constants
from tf.preferences import Preferences

class OtherTabSizeDialog(gtk.MessageDialog):
    
    def __init__(self, parent=None):
        """
        Constructor.
        """
        
        super(OtherTabSizeDialog, self).__init__(parent, 0,
                                                 gtk.MESSAGE_QUESTION,
                                                 gtk.BUTTONS_NONE, None)

        self.set_markup(constants.MESSAGE_0037)
        self.format_secondary_text(constants.MESSAGE_0038)
        
        self.add_button(gtk.STOCK_CANCEL, 2)
        self.add_button(gtk.STOCK_OK, 1)
        
        self.preferences_manager = Preferences()
        current_tab_size = self.preferences_manager.get_value("indentation/tab_width")
        
        adj = gtk.Adjustment(current_tab_size, 1.0, 30.0, 1.0, 5.0, 0.0)
        self.tab_size_spin = gtk.SpinButton(adj)
         
        vbox = self.vbox.get_children()[0].get_children()[1]
        vbox.pack_start(self.tab_size_spin)
        vbox.show_all()

    #################### Public Methods ####################
    
    def get_tab_size(self):
        return self.tab_size_spin.get_value_as_int()
