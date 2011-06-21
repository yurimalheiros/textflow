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
import gobject
import pango
from coloredhbox import ColoredHBox

class Notifier(ColoredHBox):
    
    __gsignals__ = { "close-clicked" : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ()) }
    
    
    def __init__(self):
        """
        Constructor.
        """
        super(Notifier, self).__init__((100/255.0, 100/255.0, 100/255.0),
                                       (245/255.0, 225/255.0, 140/255.0),
                                       (255/255, 240/255.0, 194/255.0),
                                       20.0, 5)
                                       
        # button style (tiny button)
        button_style = ''' 
            style 'custom_button' {
                xthickness = 0
                ythickness = 0
            }
            widget '*.button' style 'custom_button'
        '''
        gtk.rc_parse_string(button_style)
        
        self.set_border_width(3)
        self.set_spacing(12)
        
        self.__image = gtk.Image()
        self.__image.set_from_stock(gtk.STOCK_DIALOG_WARNING, gtk.ICON_SIZE_MENU)
        
        self.__label = gtk.Label()
        self.__label.set_alignment(0, 0.5)
        self.__label.set_ellipsize(pango.ELLIPSIZE_END)
        
        self.buttons_hbox = gtk.HBox()
        self.close_button = gtk.Button()
        close_image = gtk.Image()
        close_image.set_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
        self.close_button.add(close_image)
        
        self.close_button.set_relief(gtk.RELIEF_NONE)
        self.close_button.set_property("can-focus", False)
        self.close_button.set_name("close.button")
        
        self.__custom_widget = None
        
        self.pack_start(self.__image, False, False, 3)
        self.pack_start(self.__label, True, True)
        self.buttons_hbox.pack_end(self.close_button, False, False)
        self.pack_end(self.buttons_hbox, False, False)
        
        self.close_button.connect("clicked", self.close_clicked)
        
    
    #################### Properties ####################
            
    @property
    def label(self):
        return self.__label.get_text()
    
    @label.setter
    def label(self, value):
        self.__label.set_text(value)
        self.__label.set_use_markup(True)
        
    
    @property
    def custom_widget(self):
        return self.__custom_widget
    
    @custom_widget.setter
    def custom_widget(self, value):
        if self.__custom_widget is not None:
            self.remove(self.__custom_widget)

        self.__custom_widget = value
        self.__custom_widget.set_name("custom.button")
        self.__custom_widget.set_relief(gtk.RELIEF_NONE)
        self.__custom_widget.set_property("can-focus", False)
        self.buttons_hbox.pack_end(value, False, False)


    #################### Callbacks ####################
    
    def close_clicked(self, widget):
        self.emit("close-clicked")
