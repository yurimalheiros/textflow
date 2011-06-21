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
This module implements a class responsible for creating a button widget that
simulates the behavior of nautilus side panel combobox.
"""

import gtk

class ComboButton(gtk.ToggleButton):
    """
    This class implements ComboButton widget.
    """
    
    def __init__(self, label, use_arrow=False):
        """
        Constructor.
        
        @param label: the initial text of ComboButton.
        @type label: a String.
        """
        super(ComboButton, self).__init__()
        
        self.hbox = gtk.HBox(False, 6)
        
        self.label = gtk.Label(label)
        self.hbox.pack_start(self.label)
        
        if use_arrow == True:        
            self.arrow = gtk.Arrow(gtk.ARROW_DOWN, gtk.SHADOW_NONE)
            self.hbox.pack_start(self.arrow, False)
        
        self.add(self.hbox)
        
        self.props.relief = gtk.RELIEF_NONE
        self.set_focus_on_click(False)
        self.set_property("can-focus", False)
        
        self.menu = gtk.Menu()
        
        self.connect('button-press-event', self.toogled)
        self.menu.connect('deactivate', self.menu_close)
        
    #################### Public Methods ####################
    
    def set_label(self, text):
        """
        Set the displayed text of combobutton.
        
        @param text: The new text of combobutton.
        @type: A String.
        """
        self.label.set_label(text)
    
    def toogled(self, widget, event):
        """
        Show ComboButton's menu when it clicked.
        
        @param widget: The clicked button.
        @type widget: A Button object.
        
        @param event: The type of the event.
        @type event: A integer.
        """
        if event.button == 1:
            self.set_active(True)
            #self.menu.popup(None, None, None, event.button,
            #                event.time)
            self.menu.popup(None, None, self.__menu_position, event.button,
                            event.time)
            
    def menu_close(self, widget):
        """
        Set the state of ComboButton's Button desactived
        when the menu is closed.
        
        @param menu: The menu.
        @type menu: A Menu object.
        
        @return: The menu position.
        @rtype: A tuple.
        """
        self.set_active(False)
    
    def append(self, menu_item):
        """
        Append a new item in the menu.
        
        @param menu_item: The new menu item.
        @type menu_item: A MenuItem object.
        """
        self.menu.append(menu_item)
    
    def set_active_item(self, menu_item):
        """
        Set the active menu item.
        
        @param menu_item: The menu item that will be actived.
        @type menu_item: A MenuItem object.
        """
        self.menu.activate_item(menu_item, False)
    
    def set_text_center(self, status):
        if status:
            self.label.set_alignment(0.5, 0.5)
        else:
            self.label.set_alignment(0, 0.5)
    
    #################### Private Methods ####################
    
    def __menu_position(self, menu):
        """
        Return the position of the ComboButton's menu.
        
        @param menu: The menu.
        @type menu: A Menu object.
        
        @return: The menu position.
        @rtype: A tuple.
        """
        button_position = self.get_allocation()
        #menu_position = self.menu.get_allocation()
        menu_position_x, menu_position_y = self.menu.size_request()
        
        #items = len(self.menu.get_children())
        
        window_position_x, window_position_y = self.window.get_origin()
        window_width, window_height = self.window.get_size()
        
        position_x = button_position.x + window_position_x
        position_y = button_position.y + button_position.height + window_position_y
        
        if (position_y + menu_position_y) > (window_position_y + window_height):
            position_y = position_y - menu_position_y - button_position.height
        
        #return (button_position.x + window_position_x,
        #        button_position.y + button_position.height + window_position_y,
        #        False)
        
        return (position_x, position_y, False)
