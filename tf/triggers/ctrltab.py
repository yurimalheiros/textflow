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
This module implements the trigger of "shift+tab".
"""

import tf.app

shortcut = "ctrl+" + u'\uff09'
sticky = False

class CtrlTab(object):
        
    def activate(self):
        """
        Operations after trigger activation.
        """
        self.document_manager = tf.app.document_manager
        total_pages = self.document_manager.get_n_pages()
        page_num = self.document_manager.get_current_page()
        
        if page_num != -1 and total_pages > 1:
            if page_num == (total_pages - 1):
                self.document_manager.set_current_page(0)
            else:
                self.document_manager.next_page()
        return True
