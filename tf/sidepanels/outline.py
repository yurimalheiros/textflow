# -*- coding: utf-8 -*-

#######################################################################
# Copyright © 2008 Waldecir Santos.
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
This module implements a class responsible for the outline side panel.
"""

import gtk
import gettext
import re

import tf.app

_ = gettext.gettext
name = _("OutLine")

class OutLine(gtk.VBox):
    """
    This class is responsible for the outline side panel.
    """
    def __init__(self, sidepanel):
        """
        Constructor.
        
        @param sidepanel: Reference to the sidepanels container.
        @type sidepanel: A VBox object.
        """
        super(OutLine, self).__init__()

        self.preferences_manager = tf.app.preferences_manager
        self.document_manager = tf.app.document_manager
        self.search_functions = tf.app.document_manager.search_functions

        self.icons = {}
        self.icons['moduleicon'] = gtk.Window().render_icon(gtk.STOCK_COPY, gtk.ICON_SIZE_MENU)
        self.icons['importicon'] = gtk.Window().render_icon(gtk.STOCK_JUMP_TO, gtk.ICON_SIZE_MENU)
        self.icons['classicon'] = gtk.Window().render_icon(gtk.STOCK_FILE, gtk.ICON_SIZE_MENU)
        self.icons['functionicon'] = gtk.Window().render_icon(gtk.STOCK_EXECUTE, gtk.ICON_SIZE_MENU)

        self.lineend = {'LF': '\n', 'CR LF':'\r\n'}


        self.treestore = gtk.TreeStore(gtk.gdk.Pixbuf, str, int)
        
        self.treeview = gtk.TreeView(self.treestore)
        self.treeview.set_headers_visible(False)
        
        self.scrolled_window = gtk.ScrolledWindow()
        self.scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        self.scrolled_window.set_shadow_type(gtk.SHADOW_IN)
        self.scrolled_window.add(self.treeview)

        self.pack_start(self.scrolled_window)

        self.tvcolumn = gtk.TreeViewColumn()
        self.cell = gtk.CellRendererPixbuf()
        self.cell2 = gtk.CellRendererText()

        self.tvcolumn.pack_start(self.cell, False)
        self.tvcolumn.pack_start(self.cell2, True)
        self.tvcolumn.add_attribute(self.cell, 'pixbuf', 0)
        self.tvcolumn.add_attribute(self.cell2, 'text', 1)
        
        self.treeview.append_column(self.tvcolumn)
        self.treeview.set_search_column(1)

        self.document_manager.connect("open-file", self.updateOutLineTree_open)
        self.document_manager.connect("switch-page", self.updateOutLineTree_switch)
        self.treeview.connect('cursor-changed', self.on_cursor_changed)

    def on_cursor_changed(self, widget):
        model,iter = self.treeview.get_selection().get_selected()
        self.search_functions.goto_line(model.get_value(iter,2))


    def updateOutLineTree(self, text):
        self.treestore.clear()
        tablevel = 0
        parent = None
        importsparent = None
        regexClass = re.compile(r'class (.*)\(.*\):')
        regexImport = re.compile(r'import (.*)')
        regexFunc = re.compile(r'def (.*)\(.*\):')

        for index, line in enumerate(text.split(self.lineend[self.preferences_manager.get_value('open_save/line_ending')])): 
            classFind = regexClass.findall(line)
            importFind = regexImport.findall(line)
            funcFind = regexFunc.findall(line)            
            if classFind:
                self.treeview.set_model(self.treestore)
                self.treeview.columns_autosize()
                parent = self.treestore.append(None, [self.icons['classicon'], classFind[0],index+1])
               
            if importFind:
                self.treeview.set_model(self.treestore)
                self.treeview.columns_autosize()
                if importsparent == None:
                    importsparent = self.treestore.append(parent, [self.icons['importicon'], 'imports',index+1]) 
                self.treestore.append(importsparent, [self.icons['importicon'], importFind[0],index+1])   

            if funcFind:
                self.treeview.set_model(self.treestore)
                self.treeview.columns_autosize()
                self.treestore.append(parent, [self.icons['functionicon'], funcFind[0],index+1])               
    

    def updateOutLineTree_open(self, document_manager, document):
        self.updateOutLineTree(document.get_text())

    def updateOutLineTree_switch(self, document_manager, page, page_num):
        self.updateOutLineTree(document_manager.get_nth_page(page_num).get_text())

    def unload(self):
        pass

