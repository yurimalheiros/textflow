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
This module implements a class responsible for manage the TextFlow preferences.
"""

import gconf

class Preferences(object):
    """
    This class is responsible for get the preferences of TextFlow stored in gconf.
    """
    
    def __init__(self):
        """
        Constructor.
        """

        self.dir = "/apps/textflow/preferences/"
        
        #default preferences values
        self.preferences = {"interface/show_toolbar" : True,
                            "interface/show_sidepanel" : True,
                            "interface/width" : 700,
                            "interface/height" : 650,
                            "font" : "Bitstream Vera Sans Mono 10",
                            "indentation/tab_width" : 4,
                            "indentation/use_spaces" : False,
                            "indentation/automatic" : True,
                            "right_margin/display" : False,
                            "right_margin/position" : 72,
                            "line_numbers" : True,
                            "highlight_current_line" : True,
                            "text_wrapping" : True,
                            "brackets_matching" : True,
                            "filebrowser_dir" : "",
                            "color_style": "classic",
                            "open_save/encoding" : "utf-8",
                            "open_save/line_ending" : "LF",
                            "open_save/auto_save" : False,
                            "open_save/auto_save_minutes" : 10,
                            "open_save/reopen_tabs" : True,
                            "open_save/save_copy" : False,
                            "open_save/recent" : False }
        
        self.client = gconf.client_get_default()
        self.__check_values()

    #################### Public Methods ####################
        
    def get_value(self, item):
        """
        Get a value of a item of the preferences.
        
        @param item: The preferences' item.
        @type item: A string.
        
        @return: The value of the item.
        @rtype: The return type is variable.
        """
        path = self.dir + item
        value = self.client.get(path)
        
        if value == None:
            raise ValueError
        if value.type == gconf.VALUE_LIST:
            list_type = value.get_list_type()
            return self.client.get_list(path, list_type)
        else:
            return self.client.get_value(path)
    
    def set_value(self, item, value):
        """
        Set a value of a item of the preferences.
        
        @param item: The preferences' item.
        @type item: A string.
        
        @param value: The new value of the preferences' item.
        @type value: The value type is variable.
        """
        path = self.dir + item
        if type(value) == list:
            item_type = type(value[0])
            
            if item_type == str:
                self.client.set_list(path, gconf.VALUE_STRING, value)
            elif item_type == int:
                self.client.set_list(path, gconf.VALUE_INT, value)
            elif item_type == bool:
                self.client.set_list(path, gconf.VALUE_BOOL, value)
            elif item_type == float:
                self.client.set_list(path, gconf.VALUE_FLOAT, value)
        else:    
            self.client.set_value(path, value)
    
    #################### Private Methods ####################
    
    def __check_values(self):
        """
        Check if all preferences items exist and
        set default value if some item doesn't exist.
        """
        for i in self.preferences.keys():
            try:
                #self.client.get_value(self.dir + i)
                self.get_value(i)
            except ValueError:
                value = self.preferences[i]
                #self.client.set_value(self.dir + i, value)
                self.set_value(i, value)

