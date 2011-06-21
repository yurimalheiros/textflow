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
This module implements a class for responsible for the language system.
"""

import os
import imp
import gtk

import tf.app
from tf.core import constants

class LanguageManager(object):
    """
    This class manage the load and the change of language configurations.
    """
    
    def __init__(self):
        """
        Constructor.
        """
        #self.document_manager = document_manager
        #self.main_window = document_manager.main_window
        
        self.main_window = tf.app.main_window
        
        #self.preferences = self.document_manager.preferences_manager
        #self.trigger_manager = self.document_manager.trigger_manager
        self.preferences = tf.app.preferences_manager
        self.trigger_manager = tf.app.trigger_manager
        self.language = None
        self.triggers = {}
        self.loaded_configs = {}
        self.configs = {}
        
    def change_mode(self, language):
        """
        Change the current language.
        
        @param language: A language id.
        @type language: A String.
        """
        
        # Remove current language trigger menu accelgroup 
        if self.language != None:
            try:
                accel_group = self.loaded_configs[self.language]["accelgroup"]
            except KeyError:
                pass
            else:
                #self.main_window.remove_accel_group(accel_group)
                if tf.app.main_window is not None:
                    tf.app.main_window.main_window.remove_accel_group(accel_group)
        
        # Load language configurations
        self.language = language
                
        
        
        if language == None:
            #self.trigger_manager.language_shortcuts = {}
            tf.app.trigger_manager.language_shortcuts = {}
            if tf.app.main_window is not None:
                tf.app.main_window.menuitem_language.hide()
        else:
            # Load configs
            if not self.loaded_configs.has_key(self.language):
                self.__load_configs(self.language)
            
            self.configs = self.loaded_configs[self.language]

            # Load triggers
            if not self.triggers.has_key(self.language):
                self.__load_triggers(self.language)

            self.trigger_manager.language_shortcuts = self.triggers[language]
            
            
            
            if self.loaded_configs[language].has_key("accelgroup"):
                if tf.app.main_window is not None:
                    tf.app.main_window.main_window.add_accel_group(self.loaded_configs[language]["accelgroup"])
            
            # Change the language trigger menu
            try:
                menu = self.loaded_configs[language]["menu"]
            except KeyError:
                tf.app.main_window.menuitem_language.hide()
            else:
                if len(menu) == 0:
                    tf.app.main_window.menuitem_language.hide()
                else:
                    menu_title = self.loaded_configs[language]["menu-title"]
                    tf.app.main_window.menuitem_language.get_children()[0].set_label(menu_title)
                    tf.app.main_window.menuitem_language.remove_submenu()
                    tf.app.main_window.menuitem_language.set_submenu(menu)
                    tf.app.main_window.menuitem_language.show_all()
                    
            
            
    def __load_configs(self, language):
        """
        Load configs from language configuration file.
        
        @param language: A language id.
        @type language: A String.
        """
        configs = {}
        
        config_file = os.path.join(constants.LANGUAGES_USER_DIR,
                                   language, "config.py")
        
                      
        try:
            module = imp.load_source(language + "config", config_file)
        except IOError:
            tab_size = self.preferences.get_value("indentation/tab_width")
            menu_mask = ()
            menu_title = None
        else:
            try:
                tab_size = module.tab_size
            except AttributeError:
                tab_size = self.preferences.get_value("indentation/tab_width")
                
            try:
                menu_mask = module.menu
            except AttributeError:
                menu_mask = ()
                
            try:
                menu_title = module.menu_title
            except AttributeError:                
                menu_title = language
            
        configs["tab-size"] = tab_size
        configs["menu-mask"] = menu_mask
        configs["menu-title"] = menu_title
        
        self.loaded_configs[language] = configs
        
    def __load_triggers(self, language):
        """
        Load all language triggers and build the language menu.
        
        @param language: A language id.
        @type language: A String.
        """
        
        # Getting trigger files
        triggers = []
        lang_triggers = self.triggers[language] = {}
        trigger_dir = os.path.join(constants.LANGUAGES_DIR,
                                   self.language, "triggers")
        
        try:
            files = os.listdir(trigger_dir)
        except OSError:
            #print "language triggers directory not found."
            return
        
        for f in files:
            f_name = f.split('.')
            try:
                if f_name[1] != 'py':
                    continue
                else:
                    triggers.append(f_name[0])
            except IndexError:
                pass
        
        triggers.remove('__init__')
        
        shortcuts = {}
        menu_callbacks = {}
        
        # Add files to trigger manager
        try:
            for p in triggers:
                module_path = os.path.join(trigger_dir, p + '.py')
                module = imp.load_source(p, module_path)
                
                trigger_class = [c for c in module.__dict__.values() if isinstance(c, type) and c.__name__.lower() == module.__name__][0]
                
                shortcut = module.shortcut
                shortcuts[p] = shortcut
                
                #trigger_obj = trigger_class(self.document_manager)
                trigger_obj = trigger_class()
                lang_triggers[shortcut] = trigger_obj.activate
                
                menu_callbacks[p] = trigger_obj.activate
                
            
            # Build menu
            menu = self.__build_menu(triggers, shortcuts, menu_callbacks)
            self.loaded_configs[language]["menu"] = menu
            
            self.trigger_manager.language_shortcuts = lang_triggers
        except ImportError:
            print "Warning: error importing %s" % (os.path.join(trigger_dir, p + '.py'))
        
            
    #def __unload_triggers(self):
    #    for trigger in self.triggers:
    #        self.trigger_manager.shortcuts.pop(trigger)
    #        
    #    self.triggers = {}
        
    def __build_menu(self, triggers, shortcuts, callbacks):
        """
        Build the language triggers menu.
        
        @param triggers: A list with triggers module names without .py
        @type triggers: A List.
        
        @param shortcuts: A dictionary with format
                          trigger module name => shortcut
        @type shortcuts: A Dict.
        
        @param callbacks: A dictionary with format
                          trigger module name => callback function
        @type callbacks: A Dict.
        """
        
        menu = gtk.Menu()
        accelgroup = gtk.AccelGroup()
        
        self.loaded_configs[self.language]["accelgroup"] = accelgroup
        
        menu_item = None
        
        # Build menu according menu mask
        for i in self.loaded_configs[self.language]["menu-mask"]:
            try:
                if i[0] == "-":
                    menu_item = gtk.SeparatorMenuItem()
                    menu.append(menu_item)
                    
                elif i[0] in triggers:
                    menu_item = gtk.MenuItem(i[1])
                    
                    shortcut_tokens = shortcuts[i[0]].split("+")
                    
                    mask = 0
                    
                    if "ctrl" in shortcut_tokens:
                        mask = mask | gtk.gdk.CONTROL_MASK
                    
                    if "shift" in shortcut_tokens:
                        mask = mask | gtk.gdk.SHIFT_MASK
                        
                    if "alt" in shortcut_tokens:
                        mask = mask | gtk.gdk.MOD1_MASK
                    
                    
                    key_number = ord(shortcut_tokens[-1])
                    menu_item.add_accelerator("activate", accelgroup, 
                                              key_number, mask,
                                              gtk.ACCEL_VISIBLE)
                                              
                    callback = self.__get_callback(callbacks[i[0]])
                    
                    menu_item.connect("activate", callback)
                    menu.append(menu_item)
            
            except IndexError:
                continue
            except TypeError:
                continue
        
        
        return menu
    
    def __get_callback(self, function):
        """
        Create a MenuItem activate callback function.
        
        @param function: A function without parameters.
        @type function: A function.
        
        @return: a new function with correct parameters to be used as
                 a MenuItem activate callback function.
        @rtype: A function. 
        """
        
        def callback(widget):
            function()
        
        return callback
