# -*- coding: utf-8 -*-

#######################################################################
# Copyright © 2007-2009 Yuri Malheiros.
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
This module implements a class responsible
for manager all side panels available.
"""

import os
import imp
import gtk

import tf.app
from tf.core.constants import SIDEPANELS_DIR

class SidePanelManager(object):
    """
    This class is responsible for loading of all side panels available.
    """
    
    def __init__(self, sidepanel, combobutton):
        """
        Constructor.
        
        @param sidepanel: Reference to the sidepanels container.
        @type sidepanel: A VBox object.
        
        @param combobutton: Reference to a ComboButton widget.
        @type combobutton: A ComboButton object.
        """
        self.document_manager = tf.app.document_manager
        self.sidepanel = sidepanel
        self.combobutton = combobutton
        self.panels = []
        self.panels_class = []
        
        self.__get_panels()
        self.__load_panels()

    #################### Public Methods ####################
            
    def sidepanel_load(self, widget, sidepanel, name):
        """
        Add to interface the side panel chosen in the ComboButton.
        
        @param widget: Reference to the MenuItem clicked.
        @type widget: A MenuItem object.
        
        @param sidepanel: Reference to a side panel.
        @type sidepanel: A side panel object (VBox).
        """
        sidepanel_children = self.sidepanel.get_children()
        if len(sidepanel_children) > 1:
            self.sidepanel.remove(sidepanel_children[1])
        self.sidepanel.pack_start(sidepanel)
        self.combobutton.set_label(name)
        sidepanel.show_all()
        
    def unload(self):
        """
        Unload all side panels.
        """
        for i in self.panels_class:
            i.unload()

    def __get_panels(self):
        """
        Get a list with all files that implement side panels.
        """
        files_dir = os.listdir(SIDEPANELS_DIR)
        files = list(files_dir)
        
        for f in files:
            f_name = f.split('.')
            try:
                if f_name[1] != 'py':
                    continue
                else:
                    self.panels.append(f_name[0])
            except IndexError:
                pass
        
        self.panels.remove('__init__')
        
    #################### Private Methods ####################
    
    def __load_panels(self):
        """
        Load all side panels available.
        """
        try:
            flag = False
            for panel in self.panels:
                #loading class...
                module_path = SIDEPANELS_DIR + '/' + panel + '.py'
                module = imp.load_source(panel, module_path)
                
                plugin_class = [c for c in module.__dict__.values()
                                if isinstance(c, type) 
                                and c.__name__.lower() == module.__name__][0]
                
                sidepanel = plugin_class(self.sidepanel)
                self.panels_class.append(sidepanel)
                
                #add sidepanel to combobutton
                plugin_menu_item = gtk.MenuItem(module.name)
                plugin_menu_item.show()
                plugin_menu_item.connect('activate', self.sidepanel_load,
                                         sidepanel, module.name)
                self.combobutton.append(plugin_menu_item)
                
                if flag == False:
                    self.combobutton.set_active_item(plugin_menu_item)
                    flag = True
        except:
            print "Warning: Error loading sidepanel %s" % (panel)
            raise