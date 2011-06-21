# -*- coding: utf-8 -*-

#######################################################################
# Copyright © 2007-2008 Waldecir Filho.
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
This module implements a class responsible for creating the SearchBar.
"""

import gtk

from tf.core import constants

class GotoBar(gtk.HBox):

    def __init__(self, document_manager):
        """
        Constructor.
        
        @param document_manager: The Document Manager.
        @type document_manager: A DocumentManger object
        """
        super(GotoBar, self).__init__()
        self.hide()
        self.search_functions = document_manager.search_functions
        self.document_manager = document_manager

        label = gtk.Label(constants.MESSAGE_0028)
        self.entry = gtk.Entry()
        self.search_functions.entry = self.entry
        
        close_button_style = ''' 
            style 'close_button' {
                xthickness = 0
                ythickness = 0
            }
            widget '*.close_button' style 'close_button'
        '''
        gtk.rc_parse_string(close_button_style)

        #create the bar widgets...
        self.close_button = gtk.Button()
        self.close_button.set_name('gotobarbar.close_button')
        self.close_button.set_relief(gtk.RELIEF_NONE)
        self.__add_icon_to_button(self.close_button)

        close_button_vbox = gtk.VBox()
        close_button_vbox.pack_start(self.close_button, True, False, 0)
        
        self.set_spacing(6)
        self.pack_start(close_button_vbox, False, False, 0)
        self.pack_start(label, False, False, 0)
        self.pack_start(self.entry, False, False, 0)

        self.__set_all_signals()

    #################### Public Methods ####################
    
    #def entry_change(self, widget):
    #    gotoline = self.entry.get_text()
    #    gobject.timeout_add(100, self.search_functions.check_last_line , gotoline)
        
    def on_entry_key_press(self, entry, event):
        if event.keyval == gtk.gdk.keyval_from_name('Escape'):
            self.hide()
            self.search_functions.view_focus()
            
            return True
            
        if event.keyval == gtk.gdk.keyval_from_name('Return'):         
            self.hide()
            
            
            try:
                gotoline = int(self.entry.get_text())
            except ValueError:
                self.document_manager.get_active_view().grab_focus()
                return True
            
            self.buffer = None 
            if not self.document_manager.get_active_view() == None:
                self.buffer = self.document_manager.get_active_view().buffer 
            if gotoline > 0 and gotoline <= self.buffer.get_line_count():
                self.search_functions.goto_line(gotoline)
                
            self.document_manager.get_active_view().grab_focus()

            return True

        return False

    def close_gotobar(self, widget):
        self.hide()
        self.search_functions.view_focus()
        
    def show_bar(self):
        self.show_all()
        self.entry.grab_focus()

    #################### Private Methods ####################
    
    def __set_all_signals(self):
        """
        Set all signals.
        """
        #self.entry.connect("changed", self.entry_change)
        self.close_button.connect("clicked", self.close_gotobar)
        self.entry.connect('key-press-event', self.on_entry_key_press)
    
    def __add_icon_to_button(self, button):
        """
        Add the close image to a button.
        
        @param button: Reference to a button.
        @type button: A Button object.
        """
        iconBox = gtk.HBox(False, 0)
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
        gtk.Button.set_relief(button, gtk.RELIEF_NONE)
        settings = gtk.Widget.get_settings(button)
        (w,h) = gtk.icon_size_lookup_for_settings(settings, gtk.ICON_SIZE_MENU)
        gtk.Widget.set_size_request(button, w + 0, h + 2)
        image.show()
        iconBox.pack_start(image, True, False, 0)
        button.add(iconBox)

        iconBox.show()
