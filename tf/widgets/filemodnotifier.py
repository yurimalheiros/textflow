# -*- coding: utf-8 -*-

#######################################################################
# Copyright © 2009 TextFlow Team
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

import gtk
from notifier import Notifier

class FileModNotifier(Notifier):
    """
    A notify widget to show a message about external file modification and
    show the buttons to cancel ou revert the file.
    """
    
    def __init__(self):
        """
        Constructor.
        """
        super(FileModNotifier, self).__init__()
        
        self.revert_button = gtk.Button()
        
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_REVERT_TO_SAVED, gtk.ICON_SIZE_MENU)
        self.revert_button.add(image)
        
        self.revert_button.set_relief(gtk.RELIEF_NONE)
        self.revert_button.set_property("can-focus", False)
        
        self.custom_widget = self.revert_button
        
        self.connect("close-clicked", self.hide_notifier)
        
        
    #################### Public Methods ####################
    
    def notify(self, text):
        """
        Show the notifier with a message.
        
        @param text: the notifier text.
        @type text: a String.
        """
        self.label = text
        self.show_all()
        
        
    #################### Callbacks ####################
    
    def hide_notifier(self, widget):
        self.hide()
