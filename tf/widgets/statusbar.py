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
This module implements a class responsible for creating the TextFlow status bar.
"""

import gtk
from tf.core import constants
from tf.widgets.combobutton import ComboButton
from tf.widgets.otherencodingdialog import OtherEncodingDialog
from tf.widgets.othertabsizedialog import OtherTabSizeDialog

class StatusBar(gtk.HBox):
    def __init__(self, document_manager):
        """
        Constructor.
        """
        super(StatusBar, self).__init__()
        
        self.document_manager = document_manager
        self.statusbar_line = gtk.Statusbar()
        self.statusbar_line.set_has_resize_grip(False)
        self.statusbar_column = gtk.Statusbar()
        self.statusbar_column.set_has_resize_grip(False)
        self.statusbar_end = gtk.Statusbar()
        self.statusbar_end.set_size_request(15,0)
        
        # Close button style (little button)
        close_button_style = ''' 
            style 'close_button' {
                xthickness = 0
                ythickness = 0
            }
            widget '*.statusbar' style 'close_button'
        '''
        gtk.rc_parse_string(close_button_style)
        
        self.statusbar = gtk.Statusbar()
        
        status_hbox = gtk.HBox()
        status_hbox.set_spacing(12)
        self.line_label = gtk.Label("")
        self.line_label.set_alignment(0.1, 0.5)
        self.line_label.set_width_chars(len(constants.MESSAGE_0016) + 3)
        #self.line_label.set_size_request(80, 0)
        self.col_label = gtk.Label("")
        self.col_label.set_alignment(0, 0.5)
        self.col_label.set_width_chars(len(constants.MESSAGE_0017) + 3)
        #self.col_label.set_size_request(100, 0)
        
        self.encoding_label = gtk.Label("")
        self.encoding_label.set_alignment(0, 0.5)
        #self.encoding_label.set_size_request(65, 0)
        
        self.permission_label = gtk.Label("")
        #self.permission_label.set_size_request(75, 0)
        self.permission_label.set_alignment(0, 0.5)
        
        # Encoding combobutton
        self.combobutton_encoding = ComboButton("")
        self.combobutton_encoding.set_name("combobutton_encoding.statusbar")
        #self.combobutton_encoding.set_size_request(80, -1)
        self.__create_encoding_menu()
        
        # Tab size combobutton
        self.combobutton_tab_size = ComboButton("")
        self.combobutton_tab_size.set_name("combobutton_tab_size.statusbar")
        #self.combobutton_tab_size.set_size_request(78, -1)
        self.__create_tab_size_menu()
        
        self.statusbar.get_children()[0].remove(self.statusbar.get_children()[0].get_children()[0])
        self.statusbar.get_children()[0].add(status_hbox)
        self.pack_start(self.statusbar, True, True, 0)
        
        status_hbox.pack_start(self.line_label, False, False, 0)
        status_hbox.pack_start(gtk.VSeparator(), False, False, 0)
        status_hbox.pack_start(self.col_label, False, False, 0)
        status_hbox.pack_start(gtk.VSeparator(), False, False, 0)
        status_hbox.pack_start(self.combobutton_tab_size, False, False, 0)
        status_hbox.pack_start(gtk.VSeparator(), False, False, 0)
        status_hbox.pack_start(self.combobutton_encoding, False, False, 0)
        status_hbox.pack_start(gtk.VSeparator(), False, False, 0)
        status_hbox.pack_start(self.permission_label, False, False, 0)
        
        self.set_size_request(-1, 27)
        self.queue_resize()
        
    #################### Public Methods ####################
    
    def set_line_column(self, line_num, col_num):
        self.line_label.set_text(constants.MESSAGE_0016 + str(line_num))
        self.col_label.set_text(constants.MESSAGE_0017 + str(col_num))
        
    def clear(self):
        self.line_label.set_text("")
        self.col_label.set_text("")
        
    def hide_info(self):
        """
        Hide all widgets inside the statusbar.
        """
        self.statusbar.get_children()[0].get_children()[0].hide_all()
    
    def show_info(self):
        """
        Show all widgets inside the statusbar.
        """
        self.statusbar.get_children()[0].get_children()[0].show_all()
        
    #################### Signals ####################
    
    def tab_size_changed(self, widget, num):
        self.__set_tab_size(num)
        
    def other_tab_size(self, widget):
        dialog = OtherTabSizeDialog()
        response = dialog.run()
        
        if response == gtk.RESPONSE_DELETE_EVENT:
            dialog.destroy()
            return
        elif response == 1:
            tab_size = dialog.get_tab_size()
            self.__set_tab_size(tab_size)
            dialog.destroy()
            return
        elif response == 2:
            dialog.destroy()
            return

    def encoding_changed(self, widget, encode):
        document = self.document_manager.get_active_document()
        self.document_manager.change_encode(document, encode)
        self.combobutton_encoding.set_label(encode)
        
    def other_encoding(self, widget):
        dialog = OtherEncodingDialog()
        response = dialog.run()
        
        if response == gtk.RESPONSE_DELETE_EVENT:
            dialog.destroy()
            return
        elif response == 1 or response == 3:
            encode = dialog.get_encoding()
            document = self.document_manager.get_active_document()
            self.document_manager.change_encode(document, encode)
            dialog.destroy()
            return
        elif response == 2:
            dialog.destroy()
            return

    #################### Private Methods ####################
    
    def __create_tab_size_menu(self):

        tab_menu_item_start = gtk.MenuItem("2")
        tab_menu_item_start.show()
        self.combobutton_tab_size.append(tab_menu_item_start)
        tab_menu_item_start.connect('activate', self.tab_size_changed, 2)
        
        tab_menu_item = gtk.MenuItem("3")
        tab_menu_item.show()
        self.combobutton_tab_size.append(tab_menu_item)
        tab_menu_item.connect('activate', self.tab_size_changed, 3)
        
        tab_menu_item = gtk.MenuItem("4")
        tab_menu_item.show()
        self.combobutton_tab_size.append(tab_menu_item)
        tab_menu_item.connect('activate', self.tab_size_changed, 4)
        
        tab_menu_item = gtk.MenuItem("6")
        tab_menu_item.show()
        self.combobutton_tab_size.append(tab_menu_item)
        tab_menu_item.connect('activate', self.tab_size_changed, 6)
        
        tab_menu_item = gtk.MenuItem("8")
        tab_menu_item.show()
        self.combobutton_tab_size.append(tab_menu_item)
        tab_menu_item.connect('activate', self.tab_size_changed, 8)
        
        tab_menu_item = gtk.SeparatorMenuItem()
        tab_menu_item.show()
        self.combobutton_tab_size.append(tab_menu_item)
            
        tab_menu_item = gtk.MenuItem("Other size")
        tab_menu_item.show()
        self.combobutton_tab_size.append(tab_menu_item)
        tab_menu_item.connect('activate', self.other_tab_size)
        
    def __create_encoding_menu(self):
        
        tab_menu_item = gtk.MenuItem("utf-7")
        tab_menu_item.show()
        self.combobutton_encoding.append(tab_menu_item)
        tab_menu_item.connect('activate', self.encoding_changed, "utf-7")
        
        tab_menu_item = gtk.MenuItem("utf-8")
        tab_menu_item.show()
        self.combobutton_encoding.append(tab_menu_item)
        tab_menu_item.connect('activate', self.encoding_changed, "utf-8")
        
        tab_menu_item = gtk.MenuItem("iso8859-1")
        tab_menu_item.show()
        self.combobutton_encoding.append(tab_menu_item)
        tab_menu_item.connect('activate', self.encoding_changed, "iso8859-1")

        tab_menu_item = gtk.MenuItem("iso8859-2")
        tab_menu_item.show()
        self.combobutton_encoding.append(tab_menu_item)
        tab_menu_item.connect('activate', self.encoding_changed, "iso8859-2")
        
        tab_menu_item = gtk.MenuItem("iso8859-4")
        tab_menu_item.show()
        self.combobutton_encoding.append(tab_menu_item)
        tab_menu_item.connect('activate', self.encoding_changed, "iso8859-4")
        
        tab_menu_item = gtk.MenuItem("iso8859-5")
        tab_menu_item.show()
        self.combobutton_encoding.append(tab_menu_item)
        tab_menu_item.connect('activate', self.encoding_changed, "iso8859-5")
        
        tab_menu_item = gtk.MenuItem("iso8859-6")
        tab_menu_item.show()
        self.combobutton_encoding.append(tab_menu_item)
        tab_menu_item.connect('activate', self.encoding_changed, "iso8859-6")
        
        tab_menu_item = gtk.MenuItem("iso8859-7")
        tab_menu_item.show()
        self.combobutton_encoding.append(tab_menu_item)
        tab_menu_item.connect('activate', self.encoding_changed, "iso8859-7")
        
        tab_menu_item = gtk.MenuItem("iso8859-9")
        tab_menu_item.show()
        self.combobutton_encoding.append(tab_menu_item)
        tab_menu_item.connect('activate', self.encoding_changed, "iso8859-9")
        
        tab_menu_item = gtk.MenuItem("iso8859-15")
        tab_menu_item.show()
        self.combobutton_encoding.append(tab_menu_item)
        tab_menu_item.connect('activate', self.encoding_changed, "iso8859-15")
        
        tab_menu_item = gtk.MenuItem("gb2312")
        tab_menu_item.show()
        self.combobutton_encoding.append(tab_menu_item)
        tab_menu_item.connect('activate', self.encoding_changed, "gb2312")
        
        tab_menu_item = gtk.SeparatorMenuItem()
        tab_menu_item.show()
        self.combobutton_encoding.append(tab_menu_item)
        
        tab_menu_item = gtk.MenuItem(constants.MESSAGE_0023)
        tab_menu_item.show()
        self.combobutton_encoding.append(tab_menu_item)
        tab_menu_item.connect('activate', self.other_encoding)
        
        #self.combobutton_encoding.set_active_item(tab_menu_item)
        
    def __set_tab_size(self, num):
        view = self.document_manager.get_active_view()
        view.set_tab_width(num)
        self.document_manager.preferences_manager.set_value("indentation/tab_width", num)
        self.combobutton_tab_size.set_label(constants.MESSAGE_0026 + " " + str(num))
