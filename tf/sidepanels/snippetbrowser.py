# -*- coding: utf-8 -*-

#######################################################################
# Copyright © 2007-2009 Waldecir Santos.
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
This module implements a class responsible for the snippets browser side panel.
"""

import gtk
import glob
import os
import tf.app
import gnomevfs
import tf.com.files as Files
from tf.core import constants
from tf.ui.snippetbrowserdialog import SnippetBrowseDialog
from xml.dom.minidom import parse, parseString

#import gnomevfs
#import os
import gettext
#import re

_ = gettext.gettext

#The name of this side panel
name = _("Snippet Browser")


class SnippetBrowser(gtk.VBox):
    """
    This class is responsible for the snippet browser side panel.
    """
    def __init__(self, sidepanel):
        """
        Constructor.
        
        @param sidepanel: Reference to the sidepanels container.
        @type sidepanel: A VBox object.
        """        
        super(SnippetBrowser, self).__init__()

        self.document_manager = tf.app.document_manager     

        self.actualLanguage = None

        self.snippet_browse_dialog = SnippetBrowseDialog(self)

        self.liststore = gtk.ListStore(str)
        
        self.treeview = gtk.TreeView(self.liststore)
        self.treeview.set_headers_visible(False)
        
        self.scrolled_window = gtk.ScrolledWindow()
        self.scrolled_window.set_policy(gtk.POLICY_AUTOMATIC,
                                        gtk.POLICY_ALWAYS)
                                        
        self.tvcolumn = gtk.TreeViewColumn()

        self.cell = gtk.CellRendererText()


        self.tvcolumn.pack_start(self.cell, True)

        self.tvcolumn.add_attribute(self.cell, 'text', 0)                                        

        self.treeview.append_column(self.tvcolumn)
        
        self.scrolled_window.add(self.treeview)    
        
        self.__set_bottom_bar()                                    

        self.pack_start(self.scrolled_window)
        self.pack_start(self.bottom_bar, False, False)        
              
        self.document_manager.connect("switch-page", self.change_tab)
        self.document_manager.connect("save-file", self.save_file)
        
        #self.treeview.connect('row-activated', self.double_click)        
    def __set_bottom_bar(self):
        """
        Create the bottom bar.
        """
        self.bottom_bar = gtk.HBox()
        
        image_new = gtk.Image()
        image_new.set_from_stock(gtk.STOCK_NEW, gtk.ICON_SIZE_MENU)
        
        image_open = gtk.Image()
        image_open.set_from_stock(gtk.STOCK_DELETE, gtk.ICON_SIZE_MENU)
              
        self.button_new = gtk.Button()
        self.button_new.set_image(image_new)
        self.button_new.set_property('relief', gtk.RELIEF_NONE)
        self.button_new.set_tooltip_text(_("New Snippet"))
        
        self.button_delete = gtk.Button()
        self.button_delete.set_image(image_open)
        self.button_delete.set_property('relief', gtk.RELIEF_NONE)
        self.button_delete.set_tooltip_text(_("Delete Snippet"))
        
        self.bottom_bar.pack_start(self.button_new, False, False)
        self.bottom_bar.pack_start(self.button_delete, False, False)

        self.button_new.connect('clicked', self.button_new_clicked)
        
    def button_new_clicked(self, widget):
        self.snippet_browse_dialog.run()
                
        
        
    def __put_snippets(self):

        self.liststore.clear()
        
        if self.actualLanguage != None:
            dom_snippet = parse(constants.LANGUAGES_DIR + os.sep + self.actualLanguage +"/snippets.xml")

            for node in dom_snippet.getElementsByTagName('snippet'):  
                for snippet_node in node.getElementsByTagName('name'):
                    key = snippet_node.childNodes[0].data
                    self.liststore.append([key])
                       
    #def double_click(self, widget, path, view_column):
    #    pass

    def change_tab(self, widget, page, page_num):

        self.actualBuffer = self.document_manager.get_nth_page(page_num).view.buffer

        if self.actualBuffer.get_language() != None:
            self.actualLanguage = self.actualBuffer.get_language().get_name().lower()
        else:
            self.actualLanguage = None

        self.__put_snippets()

        
    def save_file(self, document_manager, document):

        self.actualLanguage = Files.get_language_from_mime(gnomevfs.get_mime_type(document.file_uri))

        #
        #   Why this codes three lines dont work, why they always return None ???
        #
        #print document.view.buffer.get_language()
        #print document_manager.get_active_document().view.buffer.get_language()
        #print self.document_manager.get_nth_page(self.document_manager.get_current_page()).view.buffer.get_language()
        #self.actualBuffer = document_manager.get_active_document().view.buffer

        # self.actualBuffer = self.document_manager.get_nth_page(self.document_manager.get_current_page()).view.buffer
        #if self.actualBuffer.get_language() != None:
        #    self.actualLanguage = self.actualBuffer.get_language().get_name().lower()
        #else:
        #    self.actualLanguage = None

        self.__put_snippets()
         
        
        
    def unload(self):
        pass


















