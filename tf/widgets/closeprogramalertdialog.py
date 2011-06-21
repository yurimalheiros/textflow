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
import gobject

from tf.core import constants

class CloseProgramAlertDialog(gtk.MessageDialog):
    
    def __init__(self, files, parent=None):
        """
        Constructor.
        
        @param files: File names with all path.
        @type files: A List.
        """
        
        super(CloseProgramAlertDialog, self).__init__(parent, 0,
                                                      gtk.MESSAGE_QUESTION,
                                                      gtk.BUTTONS_NONE, None)

        self.set_markup(constants.MESSAGE_0007)
        
        self.add_button(constants.MESSAGE_0006, 1)
        self.add_button(gtk.STOCK_CANCEL, 2)
        self.add_button(gtk.STOCK_SAVE, 3)
        
        self.liststore = gtk.ListStore(gobject.TYPE_BOOLEAN, str)
        self.treeview = gtk.TreeView(self.liststore)
        self.treeview.show()
        
        self.tvcolumn = gtk.TreeViewColumn()
        self.tvcolumn.set_clickable(True)

        self.tvcolumn2 = gtk.TreeViewColumn()
        
        self.cell = gtk.CellRendererToggle()
        self.cell.set_property('activatable', True)
        self.cell2 = gtk.CellRendererText()
        
        self.treeview.set_headers_visible(False)
        self.tvcolumn2.pack_start(self.cell, False)
        self.tvcolumn.pack_start(self.cell2, False)
        self.tvcolumn2.add_attribute(self.cell, 'active', 0)
        self.tvcolumn.add_attribute(self.cell2, 'text', 1)
        
        self.cell.connect("toggled", self.toggled_cb, (self.liststore, 0))

        self.treeview.append_column(self.tvcolumn2)
        self.treeview.append_column(self.tvcolumn)
        self.treeview.set_search_column(0)
        
        self.__create_items(files)
        
        self.vbox.pack_start(self.treeview)
        self.vbox.show_all()

    #################### Public Methods ####################
    
    def get_checkboxes(self):
        """
        Get the state of all checkboxes.
        
        @return: A list with True or False according checkbox state.
        @rtype: A List.
        """
        checks = []
        for i in range(len(self.liststore)):
            checks.append(self.liststore[i][0])
            
        return checks
        
    #################### Signals ####################
    
    def toggled_cb(self, cell, path, user_data):
        model, column = user_data
        
        model[path][0] = not model[path][0]
        
        return
        
    #################### Private Methods ####################
    
    def __create_items(self, items):
        """
        Add items to the liststore.
        
        @param items: A list with the text of the items
        @type items: A List.
        """
        if len(items) > 1:
            self.format_secondary_text(constants.MESSAGE_0013)
        else:
            self.format_secondary_text(constants.MESSAGE_0004)
        
        for i in items:
            self.liststore.append((True, i))
