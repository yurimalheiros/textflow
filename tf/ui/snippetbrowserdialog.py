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
This module implements a class responsible for creating the preferences window.

@author Yuri Malheiros
@copyright: Copyright © 2007 Yuri Malheiros
"""

import gtk
import gtksourceview2
import pango
import shutil
import tf.core.constants as constants
import tf.app
from tf.widgets.filedialog import ChooseFileDialog
from xml.dom.minidom import parse, parseString
import os


class SnippetBrowseDialog(object):
    """
    This class creates the preferences window.
    """
    
    def __init__(self, main_window):
        """
        Constructor.
        
        @param main_window: The main window.
        @type main_window: A Window object.
        """
        self.main_window = main_window
        self.document_manager = tf.app.document_manager
        self.preferences_manager = tf.app.preferences_manager
        self.styles = {}
        
        self.buffer = gtksourceview2.Buffer()
        
        self.buffer.create_tag("searchmatch", background="lightblue")
        self.buffer.create_tag("sticky", background="#ff6100")
        self.buffer.set_highlight_syntax(True)        
        
        self.view = gtksourceview2.View(self.buffer)
        self.view.buffer = self.buffer # The set_style try to access buffer in view object
        
        self.gladefile = constants.SNIPPET_WINDOW
        self.widgets_tree = gtk.glade.XML(self.gladefile)
     
      
        self.__set_all_widgets()
        self.__set_style()
              
    #################### Public Methods ####################
        
    def run(self):
        """
        Open the dialog.
        """      

        dialog_run = self.snippet_browse_dialog.run()
        
        if dialog_run == gtk.RESPONSE_DELETE_EVENT:
            self.snippet_browse_dialog.hide()
        elif dialog_run == 0:
            self.snippet_browse_dialog.hide()
    
    
    #################### Private Methods ####################
          
    def __set_all_widgets(self):
        """
        Initialize all widgets used by the preferences window.
        """
        wt = self.widgets_tree
        
        self.snippet_browse_dialog = wt.get_widget("snippet_browse_dialog")
        
        self.vbox1 = wt.get_widget("vbox1")
              
        self.iptKey = wt.get_widget("iptKey")
        self.iptName = wt.get_widget("iptName")
              
              
        self.btnSave = wt.get_widget("btnSave")
        self.btnSave.connect("clicked", self.__save)
              
        #self.vbox1.scrolled_window = gtk.ScrolledWindow()
        #self.vbox1.scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        #self.vbox1.scrolled_window.add(self.view)        
        #self.vbox1.scrolled_window.show_all()
        
        self.scrolled_window = gtk.ScrolledWindow()
        self.scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        self.scrolled_window.add(self.view)        
        
        #self.vbox1.pack_start(gtk.Label('label 1'))
        
        
        
        self.vbox1.pack_start(self.scrolled_window)

        self.vbox1.reorder_child(self.scrolled_window, 1)

        self.vbox1.show_all()
        
    def __set_style(self):
        self.document_manager.set_style(self.view, self.preferences_manager.get_value("color_style"))

    def __save(self, widget):
        snippet = self.buffer.get_text(self.buffer.get_start_iter(), self.buffer.get_end_iter(), True)
        name = self.iptName.get_text()
        key = self.iptKey.get_text()
        xmlstring = '''
       	<snippet>
        	<key>%s</key>
        	<body>%s</body>
          	<name>%s</name>
	    </snippet>
	    ''' % (key, snippet, name)
	    
        actualBuffer = self.document_manager.get_active_view().buffer
        actualLanguage = actualBuffer.get_language().get_name().lower()

        dom_snippet = parse(constants.LANGUAGES_DIR + os.sep + actualLanguage +"/snippets.xml")
        print type(dom_snippet)
        print dir(dom_snippet) 
        dom_snippets = dom_snippet.getElementsByTagName('snippets')
        dom_new_snippet = parseString(xmlstring)
        dom_snippets.appendChild(dom_new_snippet)
        
        print dom_snippets.toxml()

