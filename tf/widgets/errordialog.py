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

class ErrorDialog(gtk.MessageDialog):
    
    def __init__(self, markup_text, secondary_text, parent=None):
        super(ErrorDialog, self).__init__(parent, 0, gtk.MESSAGE_ERROR,
                                               gtk.BUTTONS_NONE, None)

        self.format_secondary_text(secondary_text)
        self.set_markup(markup_text)
        self.add_button(gtk.STOCK_OK, 1)
