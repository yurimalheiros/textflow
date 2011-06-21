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
This module implements a class responsible for manager all triggers available.
"""

import os
import imp

from tf.core.constants import TRIGGER_DIR

class TriggerManager(object):
    """
    This class is responsible for loading of all triggers available.
    """
    
    def __init__(self):
        """
        Constructor.
        """
        self.triggers = []
        self.shortcuts = {}
        self.language_shortcuts = {}
        self.sticky_shortcuts = {}
        self.sticky_keys = {}
        self.last_shortcut = None
        
        self.__get_triggers()
        self.__load_triggers()
    
    #################### Public Methods ####################
    
    def add_trigger(self, trigger, directory=TRIGGER_DIR):
        """
        Add a trigger to trigger manager.
        
        @param trigger: Trigger name.
        @type trigger: A String.
        
        @param directory: Trigger file directory.
        @type directory: A String.
        """
        
        module_path = directory + '/' + trigger + '.py'
        module = imp.load_source(trigger, module_path)
        
        # Get the class with the same name of file (case unsensitive)
        trigger_class = [c for c in module.__dict__.values()
                         if isinstance(c, type)
                         and c.__name__.lower() == module.__name__][0]

        shortcut = module.shortcut
        #trigger_obj = trigger_class(self.document_manager)
        trigger_obj = trigger_class()
        self.shortcuts[shortcut] = trigger_obj.activate
        
        if module.sticky:
            self.sticky_shortcuts[shortcut] = trigger_obj.sticky_release
            self.sticky_keys[shortcut] = module.sticky_keys
            
        return shortcut
        
        
    #################### Private Methods ####################
    
    def __get_triggers(self):
        """
        Get a list with all files that implement triggers.
        """
        
        files = os.listdir(TRIGGER_DIR)
        
        for f in files:
            f_name = f.split('.')
            
            try:
                if f_name[1] != 'py':
                    continue
                else:
                    self.triggers.append(f_name[0])
            except IndexError:
                pass
        
        self.triggers.remove('__init__')
        
    def __load_triggers(self):
        """
        Load all triggers available.
        """
        
        for trigger in self.triggers:
            self.add_trigger(trigger)
