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
This module implements a popup window.
"""

import gtk

from tf.widgets.popupwindow import PopupWindow

class SnippetPopupWindow(PopupWindow):
    def __init__(self):
        PopupWindow.__init__(self, gtk.WINDOW_POPUP)

    #################### Public Methods ####################    
    
    def run(self, words, pos=None):
        if pos != None:
            self.move(pos[0], pos[1])
        
        self.show_all()
        
        self.__add_words(words)

    def build(self):
        self.set_border_width(6)

        vbox = gtk.VBox()
        vbox.set_spacing(6)
        
        self.add(vbox)
        
        # List
        self.liststore = gtk.ListStore(str)
        self.treeview = gtk.TreeView(self.liststore)
        self.treeview.show()
        self.scrolled_window = gtk.ScrolledWindow()
        self.scrolled_window.set_shadow_type(gtk.SHADOW_IN)
        
        self.scrolled_window.add(self.treeview)
        
        tvcolumn = gtk.TreeViewColumn()
        cell = gtk.CellRendererText()
        self.treeview.set_headers_visible(False)
        tvcolumn.pack_start(cell, False)
        tvcolumn.add_attribute(cell, 'text', 0)
        
        self.treeview.append_column(tvcolumn)
        self.treeview.set_search_column(0)
        
        vbox.pack_start(self.scrolled_window)
    
    def get_selected(self):
        tree_selection = self.treeview.get_selection()
        model, tree_iter = tree_selection.get_selected()
        path = self.liststore.get_path(tree_iter)
        return path[0]
        
    def item_down(self):
        tree_selection = self.treeview.get_selection()
        model, tree_iter = tree_selection.get_selected()

        path = self.liststore.get_path(tree_iter)
        position = path[0]

        if position == (len(self.liststore) - 1):
            position = 0
        else:
            position += 1

        tree_selection = self.treeview.get_selection()
        tree_selection.select_path((position,))
        self.treeview.scroll_to_cell((position,))
        
    def item_up(self):
        tree_selection = self.treeview.get_selection()
        model, tree_iter = tree_selection.get_selected()

        path = self.liststore.get_path(tree_iter)
        position = path[0]

        if position == 0:
            position = len(self.liststore) - 1
        else:
            position -= 1

        tree_selection = self.treeview.get_selection()
        tree_selection.select_path((position,))
        self.treeview.scroll_to_cell((position,))
    
    #################### Private Methods ####################
        
    def __add_words(self, words):
        if len(words) > 7:
            self.scrolled_window.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
            self.resize(190, 190)
        else:
            self.scrolled_window.set_policy(gtk.POLICY_NEVER, gtk.POLICY_NEVER)
            self.resize(190, 1)
        for word in words:
            self.liststore.append((word.name,))
        
        tree_iter = self.liststore.get_iter_first()
        tree_selection = self.treeview.get_selection()
        tree_selection.select_iter(tree_iter)
