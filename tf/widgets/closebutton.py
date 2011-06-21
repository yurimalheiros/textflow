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
This module implements a close button widget.

@author Yuri Malheiros
@copyright: Copyright © 2007-2008 Yuri Malheiros
"""

import gtk

class CloseButton(gtk.Button):
    def __init__(self):
        """
        Constructor.
        """
        
        super(CloseButton, self).__init__()
        
        # Close button style (little button)
        close_button_style = ''' 
            style 'close_button' {
                xthickness = 0
                ythickness = 0
            }
            widget '*.close_button' style 'close_button'
        '''
        gtk.rc_parse_string(close_button_style)
        
        self.set_name('widget.close_button')
        self.__add_icon_to_button()
        
    def __add_icon_to_button(self):
        """
        Add the close image to this button.
        """
        
        self.set_relief(gtk.RELIEF_NONE)
        
        icon_box = gtk.HBox(False, 0)
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
        
        settings = gtk.Widget.get_settings(self)
        width, height = gtk.icon_size_lookup_for_settings(settings, gtk.ICON_SIZE_MENU)
        gtk.Widget.set_size_request(self, width + 0, height + 2)
        
        icon_box.pack_start(image, True, False, 0)
        self.add(icon_box)
        
        image.show()
        icon_box.show()
