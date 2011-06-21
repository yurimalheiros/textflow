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

class ChangeEncodingDialog(gtk.MessageDialog):
    
    def __init__(self, parent=None):
        """
        Constructor.
        """
        super(ChangeEncodingDialog, self).__init__(parent, 0,
                                                   gtk.MESSAGE_ERROR,
                                                   gtk.BUTTONS_NONE, None)

        self.set_markup(constants.MESSAGE_0020)
        self.format_secondary_text(constants.MESSAGE_0021)
        
        self.add_button(gtk.STOCK_CANCEL, 2)
        self.add_button(gtk.STOCK_OK, 1)
        
        hbox = gtk.HBox()
        hbox.set_spacing(6)
        label_encoding = gtk.Label(constants.MESSAGE_0022)
        
        self.combobox_encoding = gtk.combo_box_new_text()
        self.combobox_encoding.append_text("utf-8")
        self.combobox_encoding.append_text("utf-7")
        self.combobox_encoding.append_text("iso8859-1")
        self.combobox_encoding.append_text("iso8859-2")
        self.combobox_encoding.append_text("iso8859-4")
        self.combobox_encoding.append_text("iso8859-5")
        self.combobox_encoding.append_text("iso8859-6")
        self.combobox_encoding.append_text("iso8859-7")
        self.combobox_encoding.append_text("iso8859-9")
        self.combobox_encoding.append_text("iso8859-15")
        self.combobox_encoding.append_text("gb2312")
        self.combobox_encoding.set_active(0)
        
        hbox.pack_start(label_encoding, False)
        hbox.pack_start(self.combobox_encoding, True)
        
        vbox = self.vbox.get_children()[0].get_children()[1]
        
        vbox.pack_start(hbox)
        vbox.show_all()

    #################### Public Methods ####################
        
    def get_encoding(self):
        """
        Return the combobox_encoding text
        """
        return self.combobox_encoding.get_active_text()
