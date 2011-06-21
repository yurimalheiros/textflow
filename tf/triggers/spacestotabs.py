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
This module implements the trigger of "ctrl+shift+2".

Thanks to Tab Convert Gedit Plugin by Frederic Back.
"""

import tf.app

shortcut = "ctrl+shift+@"
sticky = False

class SpacesToTabs(object):

    def activate(self):
        """
        Operations before trigger activation.
        """
        self.document_manager = tf.app.document_manager
        document = self.document_manager.get_active_document() 
        buffer = document.view.buffer
        
        tab_size = document.view.get_tab_width()
        text = document.get_text()
        
        newlines = []
        for line in text.splitlines():

            # count and remove leading whitespace
            #count = 0
            ln = line
            
            if len(ln) > 0:
                while ln[0] == " ":
                    ln = ln[1:]
                    if len(ln) == 0: break
        
        	
            # compare length with/without whitespace
            d = len(line)-len(ln) 

            # add whitespace if count doesn't match
            # example: '    hello'  -> '\thello'
            #          '     hello' -> '\t hello'
            ln = (" " * (d-tab_size*(d/tab_size))) + ln

            tabs = (d/tab_size)*"\t"
            ln = tabs + ln

            newlines.append(ln)
		
        text = "\n".join(newlines)
        
        buffer.begin_user_action()
        
        start_iter = buffer.get_start_iter() 
        end_iter = buffer.get_end_iter()
        
        buffer.delete(start_iter, end_iter)
        buffer.insert(start_iter, text)
        
        buffer.end_user_action()
        
        return True
