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
This module implements a class responsible for creating the SearchBar.
"""

import gtk
import gobject

from tf.core import constants
from tf.widgets.closebutton import CloseButton

class SearchBar(gtk.HBox):

    def __init__(self, document_manager):
        """
        Constructor.
        
        @param document_manager: The Document Manager.
        @type document_manager: A DocumentManger object
        """
        super(SearchBar, self).__init__()
        self.hide()
        self.search_functions = document_manager.search_functions

        label = gtk.Label(constants.MESSAGE_0009)
        self.entry = gtk.Entry()
        self.search_functions.entry = self.entry
        
        next_image = gtk.Image()
        next_image.set_from_stock(gtk.STOCK_GO_FORWARD, gtk.ICON_SIZE_MENU)
        previous_image = gtk.Image()
        previous_image.set_from_stock(gtk.STOCK_GO_BACK, gtk.ICON_SIZE_MENU)
       

        #create the bar widgets...
        self.close_button = CloseButton()

        close_button_vbox = gtk.VBox()
        close_button_vbox.pack_start(self.close_button, True, False, 0)

        self.next_button = gtk.Button()
        self.next_button.set_image(next_image)
        self.next_button.set_relief(gtk.RELIEF_NONE)
        self.next_button.set_focus_on_click(False)
        
        self.previous_button = gtk.Button()
        self.previous_button.set_image(previous_image)
        self.previous_button.set_relief(gtk.RELIEF_NONE)
        self.previous_button.set_focus_on_click(False)
        
        self.check_regexp = gtk.CheckButton("Regexp")
        self.check_regexp.set_focus_on_click(False)
        
        self.set_spacing(6)
        self.pack_start(close_button_vbox, False, False, 0)
        self.pack_start(label, False, False, 0)
        self.pack_start(self.entry, False, False, 0)
        self.pack_start(self.previous_button, False, False, 0)
        self.pack_start(self.next_button, False, False, 0)
        self.pack_start(self.check_regexp, False, False, 0)
        
        self.__set_all_tooltips()
        self.__set_all_signals()

    #################### Public Methods ####################
    
    def entry_change(self, widget):
        text = self.entry.get_text()
        gobject.timeout_add(100, self.incremental, text)
        
    def on_entry_key_press(self, entry, event):
        if event.keyval == gtk.gdk.keyval_from_name('Escape'):
            self.entry.set_text("")
            self.hide()
            self.search_functions.view_focus()
            return True

        return False
        
    def incremental(self, text):
        current_text = self.entry.get_text()
        if (text == current_text):
            self.search_functions.incremental()

    def next_search(self, widget):
        self.search_functions.next()

    def previous_search(self, widget):
        self.search_functions.previous()
    
    def close_searchbar(self, widget):
        self.hide()
        self.entry.set_text("")
        self.search_functions.view_focus()
        
    def view_focus(self, widget):
        self.search_functions.view_focus()
        self.hide()
        
    def show_bar(self):
        self.show_all()
        self.search_functions.entry = self.entry
        self.search_functions.entry_replace = None
        self.entry.grab_focus()
        
    def regexp_toggled(self, widget):
        self.search_functions.regexp = widget.get_active()
        self.search_functions.incremental()

    #################### Private Methods ####################
    
    def __set_all_signals(self):
        """
        Set all signals.
        """
        self.close_button.connect("clicked", self.close_searchbar)
        self.next_button.connect("clicked", self.next_search)
        self.previous_button.connect("clicked", self.previous_search)
        self.entry.connect("changed", self.entry_change)
        self.entry.connect("activate", self.view_focus)
        self.entry.connect('key-press-event', self.on_entry_key_press)
        self.check_regexp.connect("toggled", self.regexp_toggled)
    
    def __set_all_tooltips(self):
        """
        Set all tooltips.
        """
        self.next_button.set_tooltip_text("Find next")
        self.previous_button.set_tooltip_text("Find previous")
