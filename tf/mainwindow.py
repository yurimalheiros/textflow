# -*- coding: utf-8 -*-

#######################################################################
# Copyright © 2007-2009 Yuri Malheiros.
# Copyright © 2009 TextFlow Team.
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
This module implements a class
responsible for creating the main window of TextFlow.

@author Yuri Malheiros
@copyright: Copyright © 2007-2008 Yuri Malheiros
"""

import gtk
import gtk.glade
import gettext
import os
import gtksourceview2

import tf.app
from tf.core.sidepanelmanager import SidePanelManager
from tf.core import constants
from tf.widgets.filedialog import *
from tf.widgets.closeprogramalertdialog import CloseProgramAlertDialog
#from tf.widgets.searchbar import SearchBar
from tf.widgets.gotobar import GotoBar
from tf.widgets.searchreplacebar import SearchReplaceBar
from tf.widgets.statusbar import StatusBar
from tf.widgets.combobutton import ComboButton
from tf.widgets.closebutton import CloseButton
from tf.ui.preferences import Preferences
from tf.ui.aboutdialog import AboutDialog

_ = gettext.gettext

class MainWindow(object):
    """
    This class creates the main window of TextFlow.
    """
    
    def __init__(self, argv=None, tests=False):
        """
        Constructor.
        """
        self.gladefile = constants.MAIN_WINDOW_GLADE
        self.widgets_tree = gtk.glade.XML(self.gladefile)
        
        self.clipboard = gtk.Clipboard()
#        self.tooltip = gtk.Tooltips()
        
        self.__set_all_widgets()
        self.__set_all_signals()
        self.__set_all_accelerators()        

        self.preferences = Preferences(self)                            
        self.preferences_manager = tf.app.preferences_manager          

        
    #################### Public Methods ####################
    
    def run(self, argv, tests):
        """
        Run main window.
        """
        arg_path = argv is not None and os.path.isdir(argv[0])

        if arg_path:
          self.last_dir = argv[0]
          self.preferences_manager.set_value("filebrowser_dir", self.last_dir)
        else:
          self.last_dir = constants.HOME     

        self.sidepanel_manager = SidePanelManager(self.side_panel_vbox, self.combobutton)     

       
        # Set window size
        w = self.preferences_manager.get_value("interface/width")
        h = self.preferences_manager.get_value("interface/height")
        self.main_window.resize(w, h)
        
        if self.preferences_manager.get_value("open_save/reopen_tabs") and not arg_path:
            self.document_manager.open_stored_tabs()
        
        if not tests:
           self.main_window.show()
           self.side_panel_vbox.show_all()
           self.main_vbox.show()
           self.statusbar.show_all()
           self.document_manager.show()
           
           #self.search_bar.hide()
           self.search_replace_bar.hide()
           self.goto_bar.hide()
        
        self.__apply_preferences()
        
        # Open or not a file with TextFlow
        if argv == None:
            if self.document_manager.get_n_pages() == 0:
                self.document_manager.open_tab()
        elif arg_path:
            self.document_manager.open_tab()
            self.show_sidepanel(True)
        else:
            for i in argv:
                self.document_manager.open_tab(i)

        self.document_manager.get_active_view().grab_focus()
    
    def show_toolbar(self, state):
        """
        Define if the toolbar will be showed or not.
        
        @param state: True to show the toolbar or False to hide the toolbar.
        @type state: A boolean.
        """
        if state:
            self.toolbar.show_all()
        else:
            self.toolbar.hide()
            
        self.preferences_manager.set_value("interface/show_toolbar", state)
            
    def show_sidepanel(self, state):
        """
        Define if the sidepanel will be showed or not.
        
        @param state: True to show the toolbar or False to hide the sidepanel.
        @type state: A boolean.
        """
        if state:
            self.side_panel_vbox.show_all()
        else:
            self.side_panel_vbox.hide()
        self.preferences_manager.set_value("interface/show_sidepanel", state)
        
    def quit(self):
        can_quit = self.__verify_unsaved_tabs()
        if can_quit:
            w, h = self.main_window.get_size()
            self.preferences_manager.set_value("interface/width", w)
            self.preferences_manager.set_value("interface/height", h)
            self.sidepanel_manager.unload()
            
            if self.preferences_manager.get_value("open_save/reopen_tabs"):
                self.document_manager.store_tabs()
                
            gtk.main_quit()
        else:
            return True
    
    #################### Private Methods ####################
    
    def __set_all_widgets(self):
        """
        Initialize all widgets used by MainWindow.
        """
        wt = self.widgets_tree
        
        self.main_window = wt.get_widget("main_window")
        self.main_window.set_icon_from_file(constants.SCALABLE_ICON)
        
        self.hpaned = wt.get_widget("hpaned")
        self.toolbar = wt.get_widget("toolbar")
        self.interface_vbox = wt.get_widget("main_vbox")
        
        self.toolbutton_new = wt.get_widget("toolbutton_new")
        self.toolbutton_open = wt.get_widget("toolbutton_open")
        self.toolbutton_save = wt.get_widget("toolbutton_save")
        self.toolbutton_undo = wt.get_widget("toolbutton_undo")
        self.toolbutton_redo = wt.get_widget("toolbutton_redo")
        self.toolbutton_search = wt.get_widget("toolbutton_search")
        #self.toolbutton_replace = wt.get_widget("toolbutton_replace")
        self.toolbutton_preferences = wt.get_widget("toolbutton_preferences")
        
#        self.tooltip.set_tip(self.toolbutton_new, _("New"))
#        self.tooltip.set_tip(self.toolbutton_open, _("Open"))
#        self.tooltip.set_tip(self.toolbutton_save, _("Save"))
#        self.tooltip.set_tip(self.toolbutton_undo, _("Undo"))       
#        self.tooltip.set_tip(self.toolbutton_redo, _("Redo"))
#        self.tooltip.set_tip(self.toolbutton_search, _("Search"))
#        self.tooltip.set_tip(self.toolbutton_replace, _("Replace"))
#        self.tooltip.set_tip(self.toolbutton_preferences, _("Preferences"))
        
        self.toolbutton_new.set_tooltip_text(_("New"))   
        self.toolbutton_open.set_tooltip_text(_("Open"))
        self.toolbutton_save.set_tooltip_text(_("Save"))
        self.toolbutton_undo.set_tooltip_text(_("Undo"))
        self.toolbutton_redo.set_tooltip_text(_("Redo"))
        self.toolbutton_search.set_tooltip_text(_("Search"))
        #self.toolbutton_replace.set_tooltip_text(_("Replace"))
        self.toolbutton_preferences.set_tooltip_text(_("Preferences"))
        
        self.toolbutton_undo.set_sensitive(False)
        self.toolbutton_redo.set_sensitive(False)
        
        for i in range(self.toolbar.get_n_items() - 1):
            item = self.toolbar.get_nth_item(i)
            item.set_homogeneous(False)
        
        self.menu_file = wt.get_widget("menu_file")
        
        #for item in recent_chooser.get_children():
        #    self.menu_file.append(item)
        
        self.imagemenuitem_closetab = wt.get_widget("imagemenuitem_closetab")
        self.menuitem_duplicateline = wt.get_widget("menuitem_duplicateline")
        self.menuitem_deleteline = wt.get_widget("menuitem_deleteline")
        
        self.imagemenuitem_save_as = wt.get_widget("imagemenuitem_save_as")
        self.menuitem_save_all = wt.get_widget("menuitem_save_all")
        self.imagemenuitem_undo = wt.get_widget("imagemenuitem_undo")
        self.imagemenuitem_redo = wt.get_widget("imagemenuitem_redo")

        # Workaround to put pseudo Ctrl+D accelerator
        deleteline_child = self.menuitem_deleteline.get_child()
        self.menuitem_deleteline.remove(deleteline_child)
        
        hbox_deleteline = gtk.HBox()
        hbox_deleteline.pack_start(gtk.Label("Delete Line"), False)
        
        label_ctrld = gtk.Label("Ctrl+D")
        label_ctrld.set_alignment(1, 0.5)
        
        hbox_deleteline.pack_start(label_ctrld)
        # End of workaround
        
        self.menuitem_deleteline.add(hbox_deleteline)
        self.menuitem_deleteline.show_all()
        
        self.menuitem_uppercase = wt.get_widget("menuitem_uppercase")
        self.menuitem_lowercase = wt.get_widget("menuitem_lowercase")
        
        self.menuitem_tabs_to_spaces = wt.get_widget("menuitem_tabs_to_spaces")
        self.menuitem_spaces_to_tabs = wt.get_widget("menuitem_spaces_to_tabs")
        
        self.checkmenuitem_sidepanel = wt.get_widget("checkmenuitem_sidepanel")
        self.checkmenuitem_toolbar = wt.get_widget("checkmenuitem_toolbar")
        self.checkmenuitem_line_numbers = wt.get_widget("checkmenuitem_line_numbers")
        self.imagemenuitem_search_bar = wt.get_widget("imagemenuitem_search_bar")
        #self.imagemenuitem_replace_bar = wt.get_widget("imagemenuitem_replace_bar")

        self.menuitem_search_next = wt.get_widget("menuitem_search_next")
        self.menuitem_search_previous = wt.get_widget("menuitem_search_previous")
        
        self.menuitem_replace = wt.get_widget("menuitem_replace")
        self.menuitem_replace_all = wt.get_widget("menuitem_replace_all")
        self.menuitem_goto_bar = wt.get_widget("menuitem_goto_bar") 
        
        self.menuitem_language = wt.get_widget("menuitem_language")       

        self.document_manager = tf.app.document_manager
        
        self.statusbar = StatusBar(self.document_manager)
        
        self.combobutton = ComboButton("", True)
        self.combobutton.set_text_center(False)
        
        self.side_panel_vbox = gtk.VBox()
        combobutton_hbox = gtk.HBox(False, 4)
        self.main_vbox = gtk.VBox()
        self.main_vbox.pack_end(self.statusbar, False, False, 0)
        self.hpaned.add1(self.side_panel_vbox)
        self.hpaned.add2(self.main_vbox)

        self.main_vbox.pack_start(self.document_manager)

        combobutton_hbox.pack_start(self.combobutton, True, True, 0)
        self.side_panel_vbox.pack_start(combobutton_hbox, False, False, 0)

        self.close_sidepanel_button = CloseButton()

        close_button_vbox = gtk.VBox()
        close_button_vbox.pack_start(self.close_sidepanel_button,
                                     True, False, 0)
        combobutton_hbox.pack_start(close_button_vbox, False, False, 0)
        combobutton_hbox.set_child_packing(close_button_vbox, False,
                                           False, 0, gtk.PACK_END)
                                           
        #self.search_bar = SearchBar(self.document_manager)
        #self.main_vbox.pack_start(self.search_bar, False, False, 0)
        
        self.search_replace_bar = SearchReplaceBar(self.document_manager)
        self.main_vbox.pack_start(self.search_replace_bar, False, False, 0)
        
        self.goto_bar = GotoBar(self.document_manager)
        self.main_vbox.pack_start(self.goto_bar, False, False, 0)
            
    def __set_all_signals(self):
        """
        Set all signals used by MainWindow.
        """
        dic = {"on_toolbutton_new_clicked" :
                self.on_toolbutton_new_clicked,
                
               "on_toolbutton_open_clicked" :
               self.on_toolbutton_open_clicked,
               
               "on_toolbutton_save_clicked" :
               self.on_toolbutton_save_clicked,
               
               "on_toolbutton_undo_clicked" :
               self.on_toolbutton_undo_clicked,
               
               "on_toolbutton_redo_clicked" :
               self.on_toolbutton_redo_clicked,                            
               
               "on_toolbutton_search_clicked" :
               self.on_toolbutton_search_clicked,
               
               #"on_toolbutton_replace_clicked" :
               #self.on_toolbutton_replace_clicked,                            
               
               "on_toolbutton_preferences_clicked" :
               self.on_toolbutton_preferences_clicked,
               
               "on_imagemenuitem_new_activate" :
               self.on_imagemenuitem_new_activate,
               
               "on_imagemenuitem_open_activate" :
               self.on_imagemenuitem_open_activate,
               
               "on_imagemenuitem_closetab_activate" :
               self.on_imagemenuitem_closetab_activate,
               
               "on_imagemenuitem_save_activate" :
               self.on_imagemenuitem_save_activate,
               
               "on_imagemenuitem_save_as_activate" :
               self.on_imagemenuitem_save_as_activate,
               
               "on_menuitem_save_all_activate" :
               self.on_menuitem_save_all_activate,
               
               "on_imagemenuitem_quit_activate" :
               self.on_imagemenuitem_quit_activate,
               
               "on_imagemenuitem_undo_activate" :
               self.on_imagemenuitem_undo_activate,
               
               "on_imagemenuitem_redo_activate" :
               self.on_imagemenuitem_redo_activate,
               
               "on_imagemenuitem_cut_activate" :
               self.on_imagemenuitem_cut_activate,
               
               "on_imagemenuitem_copy_activate" :
               self.on_imagemenuitem_copy_activate,
               
               "on_imagemenuitem_paste_activate" :
               self.on_imagemenuitem_paste_activate,
               
               "on_menuitem_duplicateline_activate" :
               self.on_menuitem_duplicateline_activate,
               
               "on_menuitem_deleteline_activate" :
               self.on_menuitem_deleteline_activate,
               
               "on_menuitem_uppercase_activate" :
               self.on_menuitem_uppercase_activate,
               
               "on_menuitem_lowercase_activate" :
               self.on_menuitem_lowercase_activate,
               
               "on_menuitem_tabs_to_spaces_activate" :
               self.on_menuitem_tabs_to_spaces_activate,
               
               "on_menuitem_spaces_to_tabs_activate" :
               self.on_menuitem_spaces_to_tabs_activate,
               
               "on_imagemenuitem_preferences_activate" :
               self.on_imagemenuitem_preferences_activate,
               
               "on_imagemenuitem_about_activate" :
               self.on_imagemenuitem_about_activate,
               
               "on_imagemenuitem_help_activate" :
               self.on_imagemenuitem_help_activate,
               
               "on_checkmenuitem_sidepanel_toggled" :
               self.on_checkmenuitem_sidepanel_toggled,
               
               "on_checkmenuitem_toolbar_toggled" :
               self.on_checkmenuitem_toolbar_toggled,
               
               "on_checkmenuitem_line_numbers_toggled" :
               self.on_checkmenuitem_line_numbers_toggled,
               
               "on_imagemenuitem_search_bar_activate" :
               self.on_imagemenuitem_search_bar_activate,

               "on_menuitem_goto_bar_activate" :
               self.on_menuitem_goto_bar_activate,
               
               #"on_imagemenuitem_replace_bar_activate" :
               #self.on_imagemenuitem_replace_bar_activate,
               
               "on_menuitem_search_next_activate" :
               self.on_menuitem_search_next_activate,
               
               "on_menuitem_search_previous_activate" :
               self.on_menuitem_search_previous_activate,
               
               "on_menuitem_replace_activate" :
               self.on_menuitem_replace_activate,
               
               "on_menuitem_replace_all_activate" :
               self.on_menuitem_replace_all_activate,
               
               "on_main_window_delete_event" :
               self.delete_event }
               
        self.widgets_tree.signal_autoconnect(dic)
        self.close_sidepanel_button.connect("clicked", self.close_sidepanel)
        
    def __set_all_accelerators(self):
        """
        Set all Main Window accelerators
        """
        accel_group = gtk.AccelGroup()
        self.main_window.add_accel_group(accel_group)
        
        # Ctrl+J
        self.menuitem_duplicateline.add_accelerator("activate", accel_group, 106, gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        
        # Ctrl+D
        
        #self.menuitem_deleteline.add_accelerator("activate", accel_group, 100, gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        
        
        
        # Ctrl+2
        self.menuitem_tabs_to_spaces.add_accelerator("activate", accel_group, 50, gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        
        # Ctrl+Shift+2
        self.menuitem_spaces_to_tabs.add_accelerator("activate", accel_group, 50, gtk.gdk.CONTROL_MASK | gtk.gdk.SHIFT_MASK, gtk.ACCEL_VISIBLE)
        
        # Ctrl+U
        self.menuitem_uppercase.add_accelerator("activate", accel_group, 117, gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        
        # Ctrl+Shift+U
        self.menuitem_lowercase.add_accelerator("activate", accel_group, 117, gtk.gdk.CONTROL_MASK | gtk.gdk.SHIFT_MASK, gtk.ACCEL_VISIBLE)
        
        # F9 to show/hide side panel
        self.checkmenuitem_sidepanel.add_accelerator("activate", accel_group, 
                                                     65478, 0,
                                                     gtk.ACCEL_VISIBLE)
        # Ctrl+F to show/hide search bar
        self.imagemenuitem_search_bar.add_accelerator("activate", accel_group,
                                                      102, gtk.gdk.CONTROL_MASK,
                                                      gtk.ACCEL_VISIBLE)

        # Ctrl+H to show/hide goto bar
        self.menuitem_goto_bar.add_accelerator("activate", accel_group,
                                                      104, gtk.gdk.CONTROL_MASK,
                                                      gtk.ACCEL_VISIBLE)
        
        # Ctrl+G to search next
        self.menuitem_search_next.add_accelerator("activate", accel_group, 103,
                                                  gtk.gdk.CONTROL_MASK,
                                                  gtk.ACCEL_VISIBLE)
        
        # Shift+Ctrl+G to search previous
        self.menuitem_search_previous.add_accelerator("activate", accel_group,
                                                      103, gtk.gdk.CONTROL_MASK
                                                      | gtk.gdk.SHIFT_MASK,
                                                      gtk.ACCEL_VISIBLE)
        
        # Ctrl+R to show/hide replace bar
        #self.imagemenuitem_replace_bar.add_accelerator("activate", accel_group,
        #                                               114, gtk.gdk.CONTROL_MASK,
        #                                               gtk.ACCEL_VISIBLE)
        
        # Ctrl+T to replace
        self.menuitem_replace.add_accelerator("activate", accel_group, 116,
                                              gtk.gdk.CONTROL_MASK,
                                              gtk.ACCEL_VISIBLE)
        
        # Ctrl+Alt+T to replace all
        self.menuitem_replace_all.add_accelerator("activate", accel_group, 116,
                                                  gtk.gdk.CONTROL_MASK
                                                  | gtk.gdk.MOD1_MASK,
                                                  gtk.ACCEL_VISIBLE)
                                                  
        # Ctrl+W to close tab
        self.imagemenuitem_closetab.add_accelerator("activate", accel_group,
                                                    119, gtk.gdk.CONTROL_MASK,
                                                    gtk.ACCEL_VISIBLE)
                                                    
        # Ctrl+Shift+S to save as
        self.imagemenuitem_save_as.add_accelerator("activate", accel_group, 115,
                                                   gtk.gdk.CONTROL_MASK
                                                   | gtk.gdk.SHIFT_MASK,
                                                   gtk.ACCEL_VISIBLE)

        # Ctrl+Alt+S to save all
        self.menuitem_save_all.add_accelerator("activate", accel_group, 115,
                                               gtk.gdk.CONTROL_MASK
                                               | gtk.gdk.MOD1_MASK,
                                               gtk.ACCEL_VISIBLE)
                                                   
        # Ctrl+Z to undo
        self.imagemenuitem_undo.add_accelerator("activate", accel_group, 122,
                                                gtk.gdk.CONTROL_MASK,
                                                gtk.ACCEL_VISIBLE)

        # Ctrl+Shift+Z to redo
        self.imagemenuitem_redo.add_accelerator("activate", accel_group, 122,
                                               gtk.gdk.CONTROL_MASK
                                               | gtk.gdk.SHIFT_MASK,
                                               gtk.ACCEL_VISIBLE)
                                                   
    def __apply_preferences(self):
        """
        Apply the preferences defined.
        """
        value = self.preferences_manager.get_value("interface/show_toolbar")
        self.show_toolbar(value)
        
        value = self.preferences_manager.get_value("interface/show_sidepanel")
        self.checkmenuitem_sidepanel.set_active(value)
        
        value = self.preferences_manager.get_value("interface/show_toolbar")
        self.checkmenuitem_toolbar.set_active(value)
        
        value = self.preferences_manager.get_value("line_numbers")
        self.checkmenuitem_line_numbers.set_active(value)
        
    def __verify_unsaved_tabs(self):
        """
        This method verifies every tab to know if they are saved.
        """
        num_pages = self.document_manager.get_n_pages()
#        flag = 0
        files = []
        
        for i in range(num_pages):
            document = self.document_manager.get_nth_page(i) 
            
            if not document.is_updated():
                file_uri = document.get_file_uri()
                if file_uri == "":
                    file_uri = constants.MESSAGE_0001
                
                files.append(file_uri)
                
        if len(files) > 0:
            dialog = CloseProgramAlertDialog(files)
            dialog_return = dialog.run()
            
            if dialog_return == gtk.RESPONSE_DELETE_EVENT:
                dialog.destroy()
                return False
            elif dialog_return == 1:
                dialog.destroy()
                return True
            elif dialog_return == 2:
                dialog.destroy()
                return False
            elif dialog_return == 3:
                dialog.destroy()
                
                checks = dialog.get_checkboxes()
                
                for i in range(len(checks)):
                    if checks[i]:
                        if files[i] != constants.MESSAGE_0001:
                            self.document_manager.save_file_tab(files[i])
                        else:
                            file_save = SaveFileDialog(constants.MESSAGE_0002, None,
                                                       "", "*", False)
                            new_file = file_save.run()
                            file_save.destroy()
                    
                            if len(new_file):
                                self.document_manager.save_file_tab(new_file[0])
                            else:
                                return False
                
#                self.save_all()
                return True
        return True
        
        
    def __save_all_possible_tabs(self):
        """
        Save all possible tabs. Save tabs without show dialogs.
        """
        num_pages = self.document_manager.get_n_pages()
        
        for i in range(num_pages):
            init_page = self.document_manager.get_current_page()

            self.document_manager.set_current_page(i)
            document = self.document_manager.get_active_document()
            file_uri = document.get_file_uri()
        
            if file_uri != "":
                self.document_manager.save_file_tab(file_uri, False)
            else:
                return
            
            self.document_manager.set_current_page(init_page)
            
    #################### Signals ####################
    
    def delete_event(self, event, x):
        """
        This method does some operations when TextFlow quit.
        """
        return self.quit()
    
    # Toolbar
    def on_toolbutton_new_clicked(self, widget):
        """
        Open a new empty tab.

        @param widget: Reference to a Button.
        @type widget: A Button object.
        """
        self.document_manager.open_tab()
    
    def on_toolbutton_open_clicked(self, widget):
        """
        Open a new file in a tab.

        @param widget: Reference to a Button.
        @type widget: A Button object.
        """
        document = self.document_manager.get_active_document()
        
        if document == None:
            direc = self.last_dir
        elif document.file_uri == "":
            direc = self.last_dir
        else:
            direc = "/".join(document.file_uri.split("/")[:-1])
            self.last_dir = direc
        
        file_add = ChooseFileDialog(constants.MESSAGE_0003, self.main_window,
                                    "", '*', True, direc)
        files = file_add.run()
        file_add.destroy()
        
        for i in range(len(files)):
            self.document_manager.open_tab(files[i])
        
    def on_toolbutton_save_clicked(self, widget):
        """
        Save the current tab in a file.

        @param widget: Reference to a Button.
        @type widget: A Button object.
        """
        document = self.document_manager.get_active_document()
        
        if document is not None:
            self.document_manager.save_active_tab()
            file_uri = document.get_file_uri()
            self.last_dir = "/".join(file_uri.split("/")[:-1])
    
    def on_toolbutton_undo_clicked(self, widget):
        """
        Undo.

        @param widget: Reference to a Button.
        @type widget: A Button object.
        """
        self.document_manager.undo()
            
    def on_toolbutton_redo_clicked(self, widget):
        """
        Redo.

        @param widget: Reference to a Button.
        @type widget: A Button object.
        """
        self.document_manager.redo()

    def on_toolbutton_search_clicked(self, widget):
        """
        Show search bar.

        @param widget: Reference to a Button.
        @type widget: A Button object.
        """
        self.search_replace_bar.show_bar()
        #self.search_replace_bar.hide()
        
#    def on_toolbutton_replace_clicked(self, widget):
#        """
#        Show replace bar.
#
#        @param widget: Reference to a Button.
#        @type widget: A Button object.
#        """
#        self.search_replace_bar.show_bar()
#        self.search_bar.hide()
        
    def on_toolbutton_preferences_clicked(self, widget):
        """
        Open the preference window.

        @param widget: Reference to a Button.
        @type widget: A Button object.
        """
        self.preferences.run()
        
    
    # File Menu
    def on_imagemenuitem_new_activate(self, widget):
        """
        Open a new empty tab.

        @param widget: Reference to a ImageMenuItem.
        @type widget: A ImageMenuItem object.
        """
        self.document_manager.open_tab()
    
    def on_imagemenuitem_open_activate(self, widget):
        """
        Open a new file in a tab.

        @param widget: Reference to a ImageMenuItem.
        @type widget: A ImageMenuItem object.
        """
        document = self.document_manager.get_active_document()
        
        if document is None:
            direc = self.last_dir
        elif document.file_uri == "":
            direc = self.last_dir
        else:
            direc = "/".join(document.file_uri.split("/")[:-1])
            self.last_dir = direc
        
        file_add = ChooseFileDialog(constants.MESSAGE_0003, self.main_window,
                                    "", '*', True, direc)
        files = file_add.run()
        file_add.destroy()
        
        for i in range(len(files)):
            self.document_manager.open_tab(files[i])
    
    def on_imagemenuitem_closetab_activate(self, widget):
        page_num = self.document_manager.get_current_page()
        
        if page_num != -1:
            swindow = self.document_manager.get_nth_page(page_num)
            self.document_manager.close_tab(swindow)
    
    def on_imagemenuitem_save_activate(self, widget):
        """
        Save the current tab in a file.

        @param widget: Reference to a ImageMenuItem.
        @type widget: A ImageMenuItem object.
        """
        document = self.document_manager.get_active_document()
        
        if document is not None:
            self.document_manager.save_active_tab()
            file_uri = document.get_file_uri()
            self.last_dir = "/".join(file_uri.split("/")[:-1])
    
    def on_imagemenuitem_save_as_activate(self, widget):
        """
        Save the current tab in a new file.

        @param widget: Reference to a ImageMenuItem.
        @type widget: A ImageMenuItem object.
        """
        document = self.document_manager.get_active_document()
        
        if document is not None:
            self.document_manager.save_as_tab(document)
            file_uri = document.get_file_uri()
            self.last_dir = "/".join(file_uri.split("/")[:-1])
    
    def save_all(self, show_error=True):
        """
        Save all tabs.
        """
        self.document_manager.save_all_tabs()
    
    def on_menuitem_save_all_activate(self, widget):
        """
        Save all open tabs.
        
        @param widget: Reference to a ImageMenuItem.
        @type widget: A ImageMenuItem object.
        """
        self.save_all()
    
    def on_imagemenuitem_quit_activate(self, widget):
        """
        Quit TextFlow.
        
        @param widget: Reference to a ImageMenuItem.
        @type widget: A ImageMenuItem object.
        """
        return self.quit()
    
    # Edit Menu
    def on_imagemenuitem_cut_activate(self, widget):
        """
        Cut selected text.

        @param widget: Reference to a ImageMenuItem.
        @type widget: A ImageMenuItem object.
        """
        focus = self.main_window.focus_widget
        
        if isinstance(focus, gtksourceview2.View):
            focus.buffer.cut_clipboard(self.clipboard, True)
        elif isinstance(focus, gtk.Entry):
            focus.cut_clipboard()
    
    def on_imagemenuitem_undo_activate(self, widget):
        """
        Undo.

        @param widget: Reference to a ImageMenuItem.
        @type widget: A ImageMenuItem object.
        """
        self.document_manager.undo()
    
    def on_imagemenuitem_redo_activate(self, widget):
        """
        Undo.

        @param widget: Reference to a ImageMenuItem.
        @type widget: A ImageMenuItem object.
        """
        self.document_manager.redo()
        
    def on_imagemenuitem_copy_activate(self, widget):
        """
        Copy selected text.

        @param self: Reference to MainWindow.
        @type self: A MainWindow object.
        
        @param widget: Reference to a ImageMenuItem.
        @type widget: A ImageMenuItem object.
        """
        focus = self.main_window.focus_widget
        
        if isinstance(focus, gtksourceview2.View):
            focus.buffer.copy_clipboard(self.clipboard)
        elif isinstance(focus, gtk.Entry):
            focus.copy_clipboard()
    
    def on_imagemenuitem_paste_activate(self, widget):
        """
        Paste text.
        
        @param widget: Reference to a ImageMenuItem.
        @type widget: A ImageMenuItem object.
        """
        focus = self.main_window.focus_widget
        
        if isinstance(focus, gtksourceview2.View):
            focus.buffer.paste_clipboard(self.clipboard, None, True)
        elif isinstance(focus, gtk.Entry):
            focus.paste_clipboard()
    
    def on_menuitem_duplicateline_activate(self, widget):
        """
        Duplicate a line.

        @param widget: Reference to a Button.
        @type widget: A Button object.
        """
        self.document_manager.trigger_manager.shortcuts[u'ctrl+j']()
        
    def on_menuitem_deleteline_activate(self, widget):
        """
        Delete line.

        @param widget: Reference to a Button.
        @type widget: A Button object.
        """
        
        view = self.document_manager.get_active_view()
        buffer = view.buffer

        buffer.begin_user_action()
        itstart = buffer.get_iter_at_mark(buffer.get_insert())
        start_line = itstart.get_line()
        itstart = buffer.get_iter_at_line(start_line)
        itend = buffer.get_iter_at_mark(buffer.get_insert())
        itend.forward_line()

        buffer.delete(itstart, itend)
        buffer.end_user_action()
        
    
    def on_menuitem_uppercase_activate(self, widget):
        """
        Upper case.

        @param widget: Reference to a Button.
        @type widget: A Button object.
        """
        self.document_manager.trigger_manager.shortcuts[u'ctrl+u']()
        
    def on_menuitem_lowercase_activate(self, widget):
        """
        Lower case.

        @param widget: Reference to a Button.
        @type widget: A Button object.
        """
        self.document_manager.trigger_manager.shortcuts[u'ctrl+shift+u']()

    def on_menuitem_tabs_to_spaces_activate(self, widget):
        """
        Convert tabs to spaces.

        @param widget: Reference to a Button.
        @type widget: A Button object.
        """
        self.document_manager.trigger_manager.shortcuts[u'ctrl+2']()
        
    def on_menuitem_spaces_to_tabs_activate(self, widget):
        """
        Convert spaces to tabs.

        @param widget: Reference to a Button.
        @type widget: A Button object.
        """
        self.document_manager.trigger_manager.shortcuts[u'ctrl+shift+@']()

    def on_imagemenuitem_preferences_activate(self, widget):
        """
        Open the preference window.

        @param widget: Reference to a Button.
        @type widget: A Button object.
        """
        self.preferences.run()
    
    # View Menu
    def on_checkmenuitem_sidepanel_toggled(self, widget):
        """
        Show or hide side panel.
        
        @param widget: Reference to a ImageMenuItem.
        @type widget: A ImageMenuItem object.
        """
        value = widget.active
        self.show_sidepanel(value)
        
    def on_checkmenuitem_toolbar_toggled(self, widget):
        """
        Show or hide toolbar.
        
        @param widget: Reference to a ImageMenuItem.
        @type widget: A ImageMenuItem object.
        """
        self.show_toolbar(widget.get_active())
        
    def on_checkmenuitem_line_numbers_toggled(self, widget):
        """
        Show or hide toolbar.
        
        @param widget: Reference to a ImageMenuItem.
        @type widget: A ImageMenuItem object.
        """
        value = widget.get_active()
        pages = self.document_manager.get_n_pages()
        
        self.preferences_manager.set_value("line_numbers", value)
        for i in range(pages):
            view = self.document_manager.get_nth_page(i).view
            view.set_show_line_numbers(value)

    # Search Menu
    def on_imagemenuitem_search_bar_activate(self, widget):
        """
        Show or hide search bar.
        
        @param widget: Reference to a ImageMenuItem.
        @type widget: A ImageMenuItem object.
        """
        self.search_replace_bar.show_bar()
        #self.search_replace_bar.hide()
        self.goto_bar.hide()
    
    def on_menuitem_search_next_activate(self, widget):
        """
        Find next match.
        
        @param widget: Reference to a ImageMenuItem.
        @type widget: A ImageMenuItem object.
        """
        self.document_manager.search_functions.next()
        
    def on_menuitem_search_previous_activate(self, widget):
        """
        Find previous match.
        
        @param widget: Reference to a ImageMenuItem.
        @type widget: A ImageMenuItem object.
        """
        self.document_manager.search_functions.previous()
        
    #def on_imagemenuitem_replace_bar_activate(self, widget):
    #    """
    #    Show or hide replace bar.
    #    
    #    @param widget: Reference to a ImageMenuItem.
    #    @type widget: A ImageMenuItem object.
    #    """
    #    self.search_replace_bar.show_bar()
    #    self.search_bar.hide()
    #    self.goto_bar.hide()
        
    def on_menuitem_replace_activate(self, widget):
        """
        Replace the current current match.
        
        @param widget: Reference to a ImageMenuItem.
        @type widget: A ImageMenuItem object.
        """
        self.document_manager.search_functions.replace()
        
    def on_menuitem_replace_all_activate(self, widget):
        """
        Replace all matches.
        
        @param widget: Reference to a ImageMenuItem.
        @type widget: A ImageMenuItem object.
        """
        self.document_manager.search_functions.replace_all()
    
    # Help Menu
    def on_imagemenuitem_help_activate(self, widget):
        """
        Open TextFlow documentation in a browser.

        @param widget: Reference to a ImageMenuItem.
        @type widget: A ImageMenuItem object.
        """
        gtk.show_uri(gtk.gdk.Screen(), "http://docs.textflowproject.org", 0)
    
    def on_imagemenuitem_about_activate(self, widget):
        """
        Show the about window.

        @param widget: Reference to a ImageMenuItem.
        @type widget: A ImageMenuItem object.
        """
        about = AboutDialog()
        ret = about.run()
        about.destroy()

        return ret

    def on_menuitem_goto_bar_activate(self, widget):
        """
        Show or hide search bar.
        
        @param widget: Reference to a ImageMenuItem.
        @type widget: A ImageMenuItem object.
        """
        self.search_replace_bar.hide()
        #self.search_bar.hide()
        self.goto_bar.show_bar()

    # Close Sidepanel
    def close_sidepanel(self, widget):
        """
        Hide side panel.
        
        @param widget: Reference to a ImageMenuItem.
        @type widget: A ImageMenuItem object.
        """
        self.show_sidepanel(False)
        self.checkmenuitem_sidepanel.set_active(False)
        
