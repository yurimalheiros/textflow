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

class OtherEncodingDialog(gtk.MessageDialog):
    
    def __init__(self, parent=None):
        """
        Constructor.
        """
        
        super(OtherEncodingDialog, self).__init__(parent, 0,
                                                  gtk.MESSAGE_QUESTION,
                                                  gtk.BUTTONS_NONE, None)

        self.set_markup(constants.MESSAGE_0024)
        self.format_secondary_text(constants.MESSAGE_0022)
        
        self.add_button(gtk.STOCK_CANCEL, 2)
        self.add_button(gtk.STOCK_OK, 1)
        
        self.liststore = gtk.ListStore(str)
        self.treeview = gtk.TreeView(self.liststore)
        self.treeview.show()
        
        self.tvcolumn = gtk.TreeViewColumn()
        self.tvcolumn.set_clickable(True)

        self.tvcolumn2 = gtk.TreeViewColumn()
        
        self.cell = gtk.CellRendererToggle()
        self.cell.set_property('activatable', True)
        self.cell2 = gtk.CellRendererText()
        
        self.treeview.set_headers_visible(False)
        self.tvcolumn.pack_start(self.cell2, False)
        self.tvcolumn.add_attribute(self.cell2, 'text', 0)
        
        self.treeview.append_column(self.tvcolumn)
        self.treeview.set_search_column(0)
        
        self.treeview.connect("row-activated", self.row_activated)
        
        self.__create_items()
        
        scroll_win = gtk.ScrolledWindow()
        scroll_win.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        scroll_win.set_shadow_type(gtk.SHADOW_IN)
        scroll_win.add(self.treeview)
        scroll_win.set_size_request(-1, 100)
        
        vbox = self.vbox.get_children()[0].get_children()[1]
        vbox.pack_start(scroll_win)
        vbox.show_all()

    #################### Public Methods ####################
    
    def get_encoding(self):
        model, selected_iter = self.treeview.get_selection().get_selected()
        #print model.get_value(selected_iter, 0)
        return model.get_value(selected_iter, 0)
        
    #################### Signals ####################
    
    def row_activated(self, widget, path, view_column):
        self.response(3)
        
    #################### Private Methods ####################
    
    def __create_items(self):
        
        items =  ["ascii", 
    "utf-7",  "utf-8-sig", "iso8859-2", "iso8859-3", "iso8859-4", "iso8859-5",
    "iso8859-6", "iso8859-7", "iso8859-8", "iso8859-9", "iso8859-10", "iso8859-13",
    "iso8859-14", "iso8859-15", "iso2022-jp", "iso2022-jp-1", "iso2022-jp-2",
    "iso2022-jp-2004", "iso2022-jp-3", "iso2022-jp-ext", "iso2022-kr", "latin-1",
    "big5", "big5hkscs", "cp037", "cp424", "cp437", "cp500", "cp737", "cp775",
    "cp850", "cp852", "cp855", "cp856", "cp857", "cp860", "cp861", "cp862", "cp863",
    "cp864", "cp865", "cp866", "cp869", "cp874", "cp875", "cp932", "cp949", "cp950",
    "cp1006", "cp1026", "cp1140", "cp1250", "cp1251", "cp1252", "cp1253", "cp1254",
    "cp1255", "cp1256", "cp1257", "cp1258", "euc-jp", "euc-jis-2004", "euc-jisx0213",
    "euc-kr", "gb2312", "gbk", "gb18030", "hz",  "johab", "koi8-r", "koi8-u",
    "mac-cyrillic", "mac-greek", "mac-iceland", "mac-latin2", "mac-roman",
    "mac-turkish", "ptcp154", "shift-jis", "shift-jis-2004", "shift-jisx0213"]
        
        for i in items:
            self.liststore.append((i,))
