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

class CloseAlertDialog(gtk.MessageDialog):
    
    def __init__(self, parent=None):
        super(CloseAlertDialog, self).__init__(parent, 0, gtk.MESSAGE_QUESTION,
                                               gtk.BUTTONS_NONE, None)

        self.format_secondary_text(constants.MESSAGE_0004)
        self.set_markup(constants.MESSAGE_0005)
        self.add_button(constants.MESSAGE_0006, 1)
        self.add_button(gtk.STOCK_CANCEL, 2)
        self.add_button(gtk.STOCK_SAVE, 3)
