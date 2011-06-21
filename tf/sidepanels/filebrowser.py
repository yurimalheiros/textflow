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
This module implements a class responsible for the file browser side panel.
"""

import gtk
import gnomevfs
import os
import gettext
import re

import tf.app
from tf.com import files as Files
from tf.widgets.filterwindow import FilterWindow

_ = gettext.gettext

#The name of this side panel
name = _("File Browser")

class FileBrowser(gtk.VBox):
    """
    This class is responsible for the file browser side panel.
    """
    def __init__(self, sidepanel):
        """
        Constructor.
        
        @param sidepanel: Reference to the sidepanels container.
        @type sidepanel: A VBox object.
        """
        super(FileBrowser, self).__init__()
        
        self.document_manager = tf.app.document_manager
        self.sidepanel = sidepanel
        self.preferences_manager = tf.app.preferences_manager
        
        self.expanded_paths = []
        self.history_back = []
        self.history_forward = []
        
        self.set_spacing(6)
        
        self.treestore = gtk.TreeStore(gtk.gdk.Pixbuf, str)
        
        self.treeview = gtk.TreeView(self.treestore)
        self.treeview.set_headers_visible(False)
        
        self.scrolled_window = gtk.ScrolledWindow()
        self.scrolled_window.set_policy(gtk.POLICY_AUTOMATIC,
                                        gtk.POLICY_ALWAYS)
        #self.scrolled_window.set_shadow_type(gtk.SHADOW_IN)
        
        self.tvcolumn = gtk.TreeViewColumn()
        self.cell = gtk.CellRendererPixbuf()
        self.cell2 = gtk.CellRendererText()

        self.tvcolumn.pack_start(self.cell, False)
        self.tvcolumn.pack_start(self.cell2, True)
        self.tvcolumn.add_attribute(self.cell, 'pixbuf', 0)
        self.tvcolumn.add_attribute(self.cell2, 'text', 1)
        
        self.treeview.append_column(self.tvcolumn)
        self.treeview.set_search_column(1)
        
        self.scrolled_window.add(self.treeview)
        
        self.__set_top_bar()
        self.__set_bottom_bar()
        
        self.pack_start(self.top_bar, False, False)
        self.pack_start(self.scrolled_window)
        self.pack_start(self.bottom_bar, False, False)
        
        start_dir = self.preferences_manager.get_value("filebrowser_dir")
        self.flist = Files.FileList(start_dir)
        
        self.treeview.connect('row-expanded', self.expand_folder)
        self.treeview.connect('row-collapsed', self.collapsed_folder)
        self.treeview.connect('row-activated', self.double_click)
        self.treeview.connect('key-press-event', self.key_press)
        self.cell2.connect('edited', self.edit_file_name)
        
        self.__put_files()
        
    def __set_top_bar(self):
        """
        Create the top bar.
        """
        self.top_bar = gtk.HBox()
        
        self.liststore_dir = gtk.TreeStore(gtk.gdk.Pixbuf, str)
        self.combobox_dir = gtk.ComboBox(self.liststore_dir)
        
        cell_image = gtk.CellRendererPixbuf()
        cell_text = gtk.CellRendererText()

        self.combobox_dir.pack_start(cell_image, False)
        self.combobox_dir.pack_start(cell_text, True)
        self.combobox_dir.add_attribute(cell_image, 'pixbuf', 0)
        self.combobox_dir.add_attribute(cell_text, 'text', 1)
        
        image_back = gtk.Image()
        image_back.set_from_stock(gtk.STOCK_GO_BACK, gtk.ICON_SIZE_MENU)
        
        image_forward = gtk.Image()
        image_forward.set_from_stock(gtk.STOCK_GO_FORWARD, gtk.ICON_SIZE_MENU)
        
        self.button_back = gtk.Button()
        self.button_back.set_image(image_back)
        self.button_back.set_property('relief', gtk.RELIEF_NONE)
        self.button_back.set_sensitive(False)
        self.button_back.set_tooltip_text(_("Back"))
        
        self.button_forward = gtk.Button()
        self.button_forward.set_image(image_forward)
        self.button_forward.set_property('relief', gtk.RELIEF_NONE)
        self.button_forward.set_sensitive(False)
        self.button_forward.set_tooltip_text(_("Forward"))
        
        self.top_bar.pack_start(self.combobox_dir)
        self.top_bar.pack_start(self.button_back, False, False)
        self.top_bar.pack_start(self.button_forward, False, False)
        
        self.combobox_dir_signal = self.combobox_dir.connect("changed", self.combobox_dir_changed)
        self.button_back.connect("clicked", self.button_back_clicked)
        self.button_forward.connect("clicked", self.button_forward_clicked)
        
    def __set_bottom_bar(self):
        """
        Create the bottom bar.
        """
        self.bottom_bar = gtk.HBox()
        
        image_new = gtk.Image()
        image_new.set_from_stock(gtk.STOCK_NEW, gtk.ICON_SIZE_MENU)
        
        image_open = gtk.Image()
        image_open.set_from_stock(gtk.STOCK_DIRECTORY, gtk.ICON_SIZE_MENU)
        
        image_refresh = gtk.Image()
        image_refresh.set_from_stock(gtk.STOCK_REFRESH, gtk.ICON_SIZE_MENU)
        
        image_filter = gtk.Image()
        image_filter.set_from_stock(gtk.STOCK_FIND, gtk.ICON_SIZE_MENU)
        
        self.button_new = gtk.Button()
        self.button_new.set_image(image_new)
        self.button_new.set_property('relief', gtk.RELIEF_NONE)
        self.button_new.set_tooltip_text(_("New File"))
        
        self.button_open = gtk.Button()
        self.button_open.set_image(image_open)
        self.button_open.set_property('relief', gtk.RELIEF_NONE)
        self.button_open.set_tooltip_text(_("New Folder"))
        
        self.button_refresh = gtk.Button()
        self.button_refresh.set_image(image_refresh)
        self.button_refresh.set_property('relief', gtk.RELIEF_NONE)
        self.button_refresh.set_tooltip_text(_("Refresh"))
        
        self.button_filter = gtk.Button()
        self.button_filter.set_image(image_filter)
        self.button_filter.set_property('relief', gtk.RELIEF_NONE)
        self.button_filter.set_tooltip_text(_("Filter"))
        
        self.bottom_bar.pack_start(self.button_new, False, False)
        self.bottom_bar.pack_start(self.button_open, False, False)
        self.bottom_bar.pack_start(self.button_refresh, False, False)
        self.bottom_bar.pack_start(self.button_filter, False, False)
        
        self.button_new.connect('clicked', self.new_file)
        self.button_open.connect('clicked', self.new_folder)
        self.button_refresh.connect('clicked', self.refresh_tree)
        self.button_filter.connect('clicked', self.filter)
        
        self.filter_text = ""
        
    def __put_files(self, tree_iter=None, show_hidden=False):
        """
        Put files of the current directory starting in tree_iter.
        
        @param tree_iter: The tree iter where the files will be put.
        @type tree_iter: A TreeIter object.
        
        @param show_hidden: True if this function put hidden files too.
        @type show_hidden: A boolean.
        
        @return: True if the current directory has some files,
        False if the current directory is empty.
        @rtype: A boolean.
        """

        filter = self.filter_text
        
        directory = self.flist.get_current_dir()
        theme = gtk.icon_theme_get_default()
        #self.treeview.set_model(self.treestore)
        
        if tree_iter == None:
            icon = \
            self.treeview.render_icon(gtk.STOCK_DIRECTORY, gtk.ICON_SIZE_MENU)
            
            # Setting combobox elements
            self.liststore_dir.clear()
            
            dir_list = self.__get_dir_list()
            
            for i in dir_list:
                self.liststore_dir.append(None, [icon, i])
                
            self.combobox_dir.handler_block(self.combobox_dir_signal)
            self.combobox_dir.set_active(len(self.liststore_dir) - 1)
            self.combobox_dir.handler_unblock(self.combobox_dir_signal)
            
        dir_info = gnomevfs.get_file_info(directory)
        
        if not (dir_info.permissions & gnomevfs.PERM_USER_EXEC):
            return False
                
        files = self.flist.get_files(show_hidden)        
        
        if len(files) == 0:
            if tree_iter == None:
                self.treestore.append(None, [None, _('(Empty)')])
            return False
        else:
            info = theme.lookup_icon("text-x-generic", gtk.ICON_SIZE_MENU, 0)
            
            if info == None:
                # text-x-generic icon doesn't exist
                icon_f = self.treeview.render_icon(gtk.STOCK_FILE,
                                         gtk.ICON_SIZE_MENU)
            else:
                icon_f = info.load_icon()
            
            for i in files:
                if i.type == gnomevfs.FILE_TYPE_DIRECTORY:
                    icon = self.treeview.render_icon(gtk.STOCK_DIRECTORY,
                                                     gtk.ICON_SIZE_MENU)
                    #direc = self.__get_current_directory(directory)
                    i_iter = self.treestore.append(tree_iter, [icon, i.name])
                    self.treestore.append(i_iter, [None, _('(Empty)')])
                elif i.type == gnomevfs.FILE_TYPE_REGULAR:
                    file_dir = os.path.join(directory, i.name)
                    uri = gnomevfs.get_uri_from_local_path(file_dir)
                    mime = gnomevfs.get_mime_type(uri)
                    t = mime.split("/")
                    
                    #if mime in self.except_mimes or t[0] == "text":
                    if Files.get_language_from_mime(mime) != None \
                    or mime == "" or t[0] == "text":
                        if filter == "":
                            i_iter = self.treestore.append(tree_iter, [icon_f, i.name])
                        else:
                            if self.__parse_filter(i.name, filter) != None:
                                i_iter = self.treestore.append(tree_iter, [icon_f, i.name])
                            
            self.treeview.columns_autosize()

            return True
    
    def combobox_dir_changed(self, widget):
        active_iter = widget.get_active_iter()
        
        if active_iter != None:
            active_path = self.liststore_dir.get_path(active_iter)
            
            dir_list = []
            
            for i in range(1, active_path[0] + 1):
                temp_iter = self.liststore_dir.get_iter((i,))
                dir_list.append(self.liststore_dir.get_value(temp_iter, 1))
                
            directory = "/" + "/".join(dir_list)
            
            self.history_back.append(self.flist.get_current_dir())
            self.history_forward = []
            self.button_back.set_sensitive(True)
            self.button_forward.set_sensitive(False)
            
            self.flist.set_current_dir(directory)
            self.treestore.clear()
            self.__put_files(None)
        
    def button_back_clicked(self, widget):
        directory = self.history_back.pop()
        
        if len(self.history_back) == 0:
            self.button_back.set_sensitive(False)
        
        self.button_forward.set_sensitive(True)
        self.history_forward.append(self.flist.get_current_dir())
        
        self.flist.set_current_dir(directory)
        self.treestore.clear()
        self.__put_files(None)
        
    def button_forward_clicked(self, widget):
        directory = self.history_forward.pop()
        
        if len(self.history_forward) == 0:
            self.button_forward.set_sensitive(False)
            
        self.button_back.set_sensitive(True)
        
        self.history_back.append(self.flist.get_current_dir())
        self.flist.set_current_dir(directory)
        self.treestore.clear()
        self.__put_files(None)

    def refresh(self):
        self.treestore.clear()
        #not_empty = self.__put_files(None)
        self.__put_files(None)
        
        for i in self.expanded_paths:
            self.treeview.expand_row(i, False)
            

    def expand_folder(self, widget, tree_iter, path):
        """
        Show the files of a expanded folder.
        
        @param widget: Reference to the TreeView
        @type widget: A TreeView object.
        
        @param tree_iter: A TreeIter that points to the expanded folder.
        @type tree_iter: A TreeIter object.
        
        @param path: The path for the expanded folder.
        @type path: A tuple.
        """
        child = self.treestore.iter_children(tree_iter)
        
        if not (path in self.expanded_paths):
            self.expanded_paths.append(path)
        
        # Add file only once    
        if (self.treestore.get_value(child, 1) == _('(Empty)')):
            #Setting directory
            current_dir = self.flist.get_current_dir()
            subfolder_dir = current_dir
            
            #Get directory from path
            path = self.treestore.get_path(child)

            for i in range(1, len(path)):
                subfolder = self.treestore.get_iter(path[:i])
                subfolder_dir = os.path.join(subfolder_dir,
                                self.treestore.get_value(subfolder, 1))
                
            self.flist.set_current_dir(subfolder_dir)
            
            #Add files to the expanded folder
            if self.__put_files(tree_iter):
                self.treestore.remove(child)
            
            self.flist.set_current_dir(current_dir)

    def collapsed_folder(self, widget, tree_iter, path):
        self.expanded_paths.remove(path)
    
    def double_click(self, widget, path, view_column):
        """
        Show the files of a expanded folder.
        
        @param widget: Reference to the TreeView
        @type widget: A TreeView object.
        
        @param path: The path for the expanded folder.
        @type path: A tuple.
        
        @param view_column: The column in the activated row.
        @type view_column: A TreeViewColumn object.
        """
#        tree_iter = self.treestore.get_iter(path)
#        folder_name = self.treestore.get_value(tree_iter,1)
        
        #Setting directory
        subfolder_dir = self.flist.get_current_dir()
        #if subfolder_dir == "/":
        #    subfolder_dir = ""
        
        #Get directory from path
        for i in range(1, len(path)+1):
            subfolder = self.treestore.get_iter(path[:i])
            #subfolder_dir += "/" + self.treestore.get_value(subfolder, 1)
            subfolder_dir = os.path.join(subfolder_dir, self.treestore.get_value(subfolder, 1)) 
        
        #if subfolder_dir == "":
        #    subfolder_dir = "/"
            
#        subfolder_name = self.__get_current_directory(subfolder_dir)
        
        file_clicked = gnomevfs.get_file_info(subfolder_dir)
        
        if file_clicked.type == gnomevfs.FILE_TYPE_DIRECTORY:
            self.history_back.append(self.flist.get_current_dir())
            self.history_forward = []
            self.button_back.set_sensitive(True)
            self.button_forward.set_sensitive(False)
            
            self.flist.set_current_dir(subfolder_dir)
            self.treestore.clear()
            self.__put_files(None)
        elif file_clicked.type == gnomevfs.FILE_TYPE_REGULAR:
            self.document_manager.open_tab(subfolder_dir)
    
    #def up_folder(self, widget):
    #    """
    #    Show the files of the upper folder.
    #    
    #    @param widget: Reference to the button
    #    @type widget: A Button object.
    #    """
    #    current_dir_list = self.flist.get_current_dir().split("/")
    #    
    #    current_dir = string.join(current_dir_list[:-1], "/")
    #    print "current dir: " + current_dir
    #    print "current dir 2: " + os.path.split(self.flist.get_current_dir())[0]
    #    
    #    if current_dir == "":
    #        self.flist.set_current_dir("/")
    #    else:
    #        self.flist.set_current_dir(current_dir)
    #    
    #    self.treestore.clear()
    #    self.__put_files(None)
        
    #def go_home(self, widget):
    #    self.flist.set_current_dir(constants.HOME)
    #    self.treestore.clear()
    #    self.__put_files(None)
        
    def new_file(self, widget):
        """
        Create a new file.
        
        @param widget: Reference to the button
        @type widget: A Button object.
        """
        
        sel_model, sel_iter = self.treeview.get_selection().get_selected()
        dir_iter = None
        
        new_file_dir = self.flist.get_current_dir()
        path = None
        
        # If some selection exists
        if sel_iter != None: 
            path = self.treestore.get_path(sel_iter)

            if len(path) == 1: # New file will be created in current folder
                dir_iter = None
            else:
                dir_iter = self.treestore.get_iter(path[0:len(path) - 1])
            
            for i in range(1, len(path)):
                dir_iter = self.treestore.get_iter(path[0:i])
                iter_value = self.treestore.get_value(dir_iter, 1)
                new_file_dir = os.path.join(new_file_dir, iter_value)
                
            #print new_file_dir
            
        # Create file
        i = 1
        new_file_name = _("New File")
        new_file_uri =  os.path.join(new_file_dir, new_file_name)

        while gnomevfs.exists(new_file_uri):
            new_file_uri = \
            os.path.join(new_file_dir, new_file_name + " " + str(i))
            i += 1
        
        old_file_dir = self.flist.get_current_dir()
        self.flist.set_current_dir(new_file_dir)
        
        try:
            files = self.flist.get_files(False)
            new_file = gnomevfs.create(new_file_uri, gnomevfs.OPEN_WRITE)
            new_file.close()
        except gnomevfs.AccessDeniedError:
            main_text = _("<b>You can't create a file.</b>")
            secondary_text = _("You don't have the required permissions to create a file in this directory.") 
            error = ErrorDialog(main_text, secondary_text)
            error_return = error.run()
            
            if error_return == gtk.RESPONSE_DELETE_EVENT:
                error.destroy()
                return
            elif error_return == 1:
                error.destroy()
                return
        
        
        # Verifying if the directory is empty to delete "(Empty)" string.
        if len(files) == 0:
            if dir_iter == None:
                empty_path = (0,)
            else:
                empty_path = list(path)
                empty_path[len(path)-1] = 0
                empty_path = tuple(empty_path)
                
            empty_iter = self.treestore.get_iter(empty_path)
            self.treestore.remove(empty_iter)

        
        theme = gtk.icon_theme_get_default()
        info = theme.lookup_icon("text-x-generic", gtk.ICON_SIZE_MENU, 0)
            
        if info == None:
            # text-x-generic icon doesn't exist
            icon = self.treeview.render_icon(gtk.STOCK_FILE,
                                         gtk.ICON_SIZE_MENU)
        else:
            icon = info.load_icon()
                                         
        name = gnomevfs.URI(new_file_uri).short_name
        new_iter = self.treestore.append(dir_iter, [icon, name])
        
        if len(files) == 0 and dir_iter != None:
            self.treeview.expand_row(path[0:len(path) - 1], False)
            
        self.flist.set_current_dir(old_file_dir)    
        
        path = self.treestore.get_path(new_iter) 
        self.cell2.set_property('editable', True)
        self.treeview.set_cursor_on_cell(path, self.tvcolumn, self.cell2,
                                         start_editing=True)
        self.cell2.set_property('editable', False)
        

    def edit_file_name(self, widget, path, new_text):
        current_dir = self.flist.get_current_dir()
        #root_iter = self.treestore.get_iter_first()
        file_iter = self.treestore.get_iter_from_string(path)
        tuple_path = self.treestore.get_path(file_iter)
        old_file_name = self.treestore.get_value(file_iter, 1)
        file_dir = current_dir
        
#        for i in tuple_path[1:-1]:
#            root_iter = self.treestore.iter_nth_child(root_iter, i)
#            file_dir += '/' + self.treestore.get_value(root_iter, 1)
        
        for i in range(1, len(tuple_path)):
            dir_iter = self.treestore.get_iter(tuple_path[0:i])
            file_dir = os.path.join(file_dir, self.treestore.get_value(dir_iter, 1))
            
        if new_text != old_file_name:

            old_file_uri = os.path.join(file_dir, old_file_name)
            new_file_uri = os.path.join(file_dir, new_text)

            if gnomevfs.exists(new_file_uri):
                secondary_text = _("A file with the same name already exists. Please use a different name.")
                main_text = _("<b>File already exists.</b>") 
                error = ErrorDialog(main_text, secondary_text)
                error_return = error.run()
                
                if error_return == gtk.RESPONSE_DELETE_EVENT:
                    error.destroy()
                    return
                elif error_return == 1:
                    error.destroy()
                    return
            
            old_file_info = gnomevfs.get_file_info(old_file_uri)
            old_file_info.name = new_text
            gnomevfs.set_file_info(old_file_uri, old_file_info,
                                   gnomevfs.SET_FILE_INFO_NAME)
            
            self.treestore.set_value(file_iter, 1, new_text)
        self.refresh()
        
        # Search for the row of the renamed file and select it
        def search_new_file(model, path, iter, new_text):
            file_name = model.get_value(iter, 1)
            
            if file_name == new_text:
                selection = self.treeview.get_selection()
                selection.select_iter(iter)
                return True
                
        self.treestore.foreach(search_new_file, new_text)            

    def new_folder(self, widget):
        """
        Create a new folder in the current directory.
        
        @param widget: Reference to the button.
        @type widget: A Button object.
        """
        
        sel_model, sel_iter = self.treeview.get_selection().get_selected()
        dir_iter = None
        
        new_file_dir = self.flist.get_current_dir()
        path = None
        
        # If some selection exists
        if sel_iter != None:
            path = self.treestore.get_path(sel_iter)

            if len(path) == 1: # New file will be created in current folder
                dir_iter = None
            else:
                dir_iter = self.treestore.get_iter(path[0:len(path) - 1])
            
            for i in range(1, len(path)):
                dir_iter = self.treestore.get_iter(path[0:i])
                iter_value = self.treestore.get_value(dir_iter, 1)
                new_file_dir = os.path.join(new_file_dir, iter_value)
            
        #Create file
        i = 1
        new_file_name = _("New Folder")
        new_file_uri = os.path.join(new_file_dir, new_file_name)

        while gnomevfs.exists(new_file_uri):
            new_file_uri = \
            os.path.join(new_file_dir, new_file_name + " " + str(i))
            i += 1
        
        old_file_dir = self.flist.get_current_dir()
        self.flist.set_current_dir(new_file_dir)
        
        try:
            files = self.flist.get_files(False)
            gnomevfs.make_directory(new_file_uri, 0755)
        except gnomevfs.AccessDeniedError:
            main_text = _("<b>You can't create a folder.</b>")
            secondary_text = _("You don't have the required permissions to create a folder in this directory.") 
            error = ErrorDialog(main_text, secondary_text)
            error_return = error.run()
            
            if error_return == gtk.RESPONSE_DELETE_EVENT:
                error.destroy()
                return
            elif error_return == 1:
                error.destroy()
                return
        
        # Verifying if the directory is empty to delete "(Empty)" string.
        if len(files) == 0:
            if dir_iter == None:
                empty_path = (0,)
            else:
                empty_path = list(path)
                empty_path[len(path)-1] = 0
                empty_path = tuple(empty_path)
                
            empty_iter = self.treestore.get_iter(empty_path)
            self.treestore.remove(empty_iter)
        
        icon = self.treeview.render_icon(gtk.STOCK_DIRECTORY,
                                         gtk.ICON_SIZE_MENU)
        name = gnomevfs.URI(new_file_uri).short_name
        new_iter = self.treestore.append(dir_iter, [icon, name])
        
        if len(files) == 0 and dir_iter != None:
            self.treeview.expand_row(path[0:len(path) - 1], False)
        
        self.flist.set_current_dir(old_file_dir)
        
        path = self.treestore.get_path(new_iter)
        self.cell2.set_property('editable', True)
        self.treeview.set_cursor_on_cell(path, self.tvcolumn, self.cell2,
                                         start_editing=True)
        self.cell2.set_property('editable', False)

    def refresh_tree(self, widget):
        self.refresh()

    def filter(self, widget):
        alloc = widget.get_allocation()
        
        wp_x, wp_y = tf.app.main_window.main_window.get_origin()
        
        filter_window = FilterWindow()
        filter_window.entry.set_text(self.filter_text)
        filter_window.entry.connect('activate', self.filter_activate,
                                    filter_window)
        filter_window.run((alloc.x + wp_x - 80, alloc.y + wp_y - 60))

    def delete_file(self, path, iter):
        #home_dir = constants.HOME
        current_dir = self.flist.get_current_dir()
        #root_iter = self.treestore.get_iter_first()
        file_name = self.treestore.get_value(iter, 1)
        file_dir = current_dir
        
        for i in range(1, len(path)):
            dir_iter = self.treestore.get_iter(path[0:i])
            iter_value = self.treestore.get_value(dir_iter, 1)
            file_dir = os.path.join(file_dir, iter_value)
        
        #file_dir_url = gnomevfs.get_uri_from_local_path(file_dir)
        #file_clicked = gnomevfs.get_file_info(file_dir_url)
        
        #print "gvfs-trash \"" + file_dir + '/' + file_name + "\""
        os.system("gvfs-trash \"" + file_dir + '/' + file_name + "\"")
        self.treestore.remove(iter)
            
        self.refresh()

    def key_press(self, widget, event):
#         print event.keyval
        sel_model, sel_iter = widget.get_selection().get_selected()
        if event.keyval == 65471:
            #F2 to rename
            if sel_iter != None:
                path = self.treestore.get_path(sel_iter)
                self.cell2.set_property('editable', True)
                self.treeview.set_cursor_on_cell(path, self.tvcolumn, 
                                                 self.cell2,
                                                 start_editing=True)
                self.cell2.set_property('editable', False)
        elif event.keyval == 65474:
            #F5 to refresh
            self.refresh()
        elif event.keyval == 65535:
            #Del to delete
            if sel_iter != None:
                path = self.treestore.get_path(sel_iter)
                self.delete_file(path, sel_iter)

    def filter_activate(self, widget, window):
        """
        Apply filter.
        
        @param widget: A reference for a Entry.
        @type widget: A Entry object.
        """
        self.filter_text = widget.get_text()
        window.destroy()
        self.refresh()

    def __parse_filter(self, value, f):
        """
        Verify if f filters value.
        
        @param value: A text that will be filtered
        @type value: A string.
        
        @param f: A text filter.
        @type f: A string.
        
        @return: If value pass through filter returns value, else return "".
        @rtype: A string.
        """
        result = None
		
        f = f.replace("*", ".+")
        f = f.replace("\.+", "\*")
		
        if value != "":
            filter = re.compile("^" + f, re.IGNORECASE)
            matches = filter.findall(value)
            if len(matches) > 0:
                result = matches
            		
        return result
		
    def __get_current_directory(self, dir_path):
        """
        Get the name of the directory of the path defined by dir_path.
        
        @param dir_path: A path for a directory.
        @type dir_path: A string.
        """
        directory = os.path.basename(dir_path)
        
        if directory == "":
            return "/"
        else:
            return directory
    
    def __get_dir_list(self):
        """
        This method returns a list with all directories to "/" from current
        directory. For example, if current dir is "/home/textflow/programming"
        this method returns ["/", "home", "textflow", "programming"]
        """
        directory = self.flist.get_current_dir()
        
        if directory == "/":
            dir_list = ["/"]
        else:
            dir_list = directory.split("/")
            dir_list[0] = "/"
            
        return dir_list
        
    def unload(self):
        c_dir = self.flist.get_current_dir()
        self.preferences_manager.set_value("filebrowser_dir", c_dir)
    
class ErrorDialog(gtk.MessageDialog):
    
    def __init__(self, main_text, secondary_text, parent=None):
        super(ErrorDialog, self).__init__(parent, 0,
                                                gtk.MESSAGE_QUESTION,
                                                gtk.BUTTONS_NONE, None)

        self.format_secondary_text(secondary_text)
        self.set_markup(main_text)
        
        self.add_button(gtk.STOCK_OK, 1)
