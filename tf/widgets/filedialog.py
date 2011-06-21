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
This module implements a class responsible create a file chooser dialog.
"""

import gtk
import gettext
_ = gettext.gettext

class ChooseFileDialog(gtk.FileChooserDialog):
    """
    A dialog selection for folders.
    """
    def __init__(self, title, parent, filter_name, pattern,
                 select_multiples = True, initial_dir = None):
        """
        Constructor.
        """
        
        super(ChooseFileDialog, self).__init__(title = title, parent = parent,
                                               action = gtk.FILE_CHOOSER_ACTION_OPEN,
                                               buttons = (gtk.STOCK_CANCEL,
                                               gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN,
                                               gtk.RESPONSE_OK))
        if initial_dir:
            self.set_current_folder(initial_dir)

        self.set_local_only(True)
        self.set_select_multiple(select_multiples)
        
        self.__creater_filters()

    #################### Public Methods ####################

    def run(self):
        """
        Run the dialog.
        """
        
        resp = super(ChooseFileDialog, self).run()
        fns = self.get_filenames()
        if resp == gtk.RESPONSE_OK:
            return fns
        else:
            return []
    
    #################### Private Methods ####################
    
    def __creater_filters(self):
        """
        Create the list file filters.
        """
        
        dic = (("C", "*.c"), ("C++", "*.cpp"),  
               ("C#", "*.cs"), ("HTML", "*.html"), ("Java", "*.java"), 
               ("Javascript", "*.js"), ("Perl", "*.pl"), ("PHP", "*.php"), 
               ("Python", "*.py"), ("Ruby", "*.rb"), ("Shell Script", "*.sh"), 
               ("Vala", "*.vala"), ("XML", "*.xml"))
        
        all_files_filter = gtk.FileFilter()
        all_files_filter.set_name(_("All Files"))
        all_files_filter.add_pattern("*")
        self.add_filter(all_files_filter)
        self.set_filter(all_files_filter)
        
        for i in dic:
            file_filter = gtk.FileFilter()
            file_filter.set_name(i[0])
            file_filter.add_pattern(i[1])
            self.add_filter(file_filter)

class SaveFileDialog(gtk.FileChooserDialog):
    def __init__(self, title, parent, filter_name, pattern,
                 select_multiples = True, initial_dir = None):
        """
        Constructor.
        """
        
        super(SaveFileDialog, self).__init__(title = title, parent = parent,
                                             action = gtk.FILE_CHOOSER_ACTION_SAVE,
                                             buttons = (gtk.STOCK_CANCEL,
                                             gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE,
                                             gtk.RESPONSE_OK))
        if initial_dir:
            self.set_current_folder(initial_dir)

        self.set_local_only(True)
        self.set_select_multiple(select_multiples)
        
    #################### Public Methods ####################

    def run(self):
        """
        Run the dialog.
        """
        resp = super(SaveFileDialog, self).run()
        fns = self.get_filenames()
        if resp == gtk.RESPONSE_OK:
            return fns
        else:
            return []

