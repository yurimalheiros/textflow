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
import pango
import shutil
import tf.core.constants as constants
import tf.app
from tf.widgets.filedialog import ChooseFileDialog


class Preferences(object):
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
        self.document_manager = main_window.document_manager
        self.preferences_manager = tf.app.preferences_manager
        self.styles = {}
        
        self.gladefile = constants.PREFERENCES_WINDOW
        self.widgets_tree = gtk.glade.XML(self.gladefile)
        
        self.__set_all_widgets()
        self.__set_all_signals()
        self.__get_colors_styles()
        
    #################### Public Methods ####################
        
    def run(self):
        """
        Open the dialog.
        """
        pm = self.preferences_manager
        
        #Set widgets values
        self.check_highlight_current_line.set_active(pm.get_value("highlight_current_line"))
        self.check_use_spaces.set_active(pm.get_value("indentation/use_spaces"))
        self.check_auto_indent.set_active(pm.get_value("indentation/automatic"))
        self.check_text_wrapping.set_active(pm.get_value("text_wrapping"))
        self.check_right_margin.set_active(pm.get_value("right_margin/display"))
        self.check_brackets_matching.set_active(pm.get_value("brackets_matching"))
        self.spin_right_margin.set_value(pm.get_value("right_margin/position"))
        self.fontbutton.set_font_name(pm.get_value("font"))
        
        default_encoding_value = pm.get_value("open_save/encoding")
        
        if default_encoding_value == "utf-7":
            self.combobox_default_encoding.set_active(0)
        elif default_encoding_value == "utf-8":
            self.combobox_default_encoding.set_active(1)
        elif default_encoding_value == "utf-16":
            self.combobox_default_encoding.set_active(2)
        elif default_encoding_value == "iso-8859-1":
            self.combobox_default_encoding.set_active(3)
        elif default_encoding_value == "iso-8859-2":
            self.combobox_default_encoding.set_active(4)
        elif default_encoding_value == "iso-8859-4":
            self.combobox_default_encoding.set_active(5)
        elif default_encoding_value == "iso-8859-5":
            self.combobox_default_encoding.set_active(6)
        elif default_encoding_value == "iso-8859-6":
            self.combobox_default_encoding.set_active(7)
        elif default_encoding_value == "iso-8859-7":
            self.combobox_default_encoding.set_active(8)
        elif default_encoding_value == "iso-8859-9":
            self.combobox_default_encoding.set_active(9)
        elif default_encoding_value == "iso-8859-15":
            self.combobox_default_encoding.set_active(10)
        elif default_encoding_value == "gb2312":
            self.combobox_default_encoding.set_active(11)
        
        line_end_value = pm.get_value("open_save/line_ending")
        
        if line_end_value == "LF":
            self.combobox_line_ending.set_active(0)
        elif line_end_value == "CR LF":
            self.combobox_line_ending.set_active(1)
        
        self.checkbutton_autosave.set_active(pm.get_value("open_save/auto_save"))
        self.spinbutton_autosave.set_value(pm.get_value("open_save/auto_save_minutes"))
        self.checkbutton_reopen_tabs.set_active(pm.get_value("open_save/reopen_tabs"))
        self.checkbutton_backup_file.set_active(pm.get_value("open_save/save_copy"))
        
        dialog_run = self.dialog_preferences.run()
        
        if dialog_run == gtk.RESPONSE_DELETE_EVENT:
            self.dialog_preferences.hide()
        elif dialog_run == 0:
            self.dialog_preferences.hide()
    
    #################### Private Methods ####################
    
    def __get_colors_styles(self):
        """
        Get properties from color styles id.
        """
        ssm = self.document_manager.style_manager
        ssm.force_rescan()
        styles = ssm.get_scheme_ids()
        
        for i in styles:
            scheme = ssm.get_scheme(i)
            name = scheme.get_name()
            description = scheme.get_description()
            self.styles[name] = i
            self.liststore.append((name, description,))
            
    def __set_all_widgets(self):
        """
        Initialize all widgets used by the preferences window.
        """
        wt = self.widgets_tree
        
        self.dialog_preferences = wt.get_widget("dialog_preferences")

        #Editor tab
        #self.check_show_toolbar = wt.get_widget("check_show_toolbar")
        #self.check_show_line_numbers = wt.get_widget("check_show_line_numbers")
        self.check_highlight_current_line = wt.get_widget("check_highlight_current_line")
        self.check_use_spaces = wt.get_widget("check_use_spaces")
        self.check_auto_indent = wt.get_widget("check_auto_indent")
        self.check_text_wrapping = wt.get_widget("check_text_wrapping")
        self.check_right_margin = wt.get_widget("check_right_margin")
        self.check_brackets_matching = wt.get_widget("check_brackets_matching")
        self.spin_right_margin = wt.get_widget("spin_right_margin")
        self.fontbutton = wt.get_widget("fontbutton")
        
        #Colors tab
        self.button_colors_add = wt.get_widget("button_colors_add")
        self.button_colors_remove = wt.get_widget("button_colors_remove")
        self.scrolledwindow_colors = wt.get_widget("scrolledwindow_colors")
        self.liststore = gtk.ListStore(str, str)
        self.treeview = gtk.TreeView(self.liststore)
        self.treeview.show()
        self.scrolledwindow_colors.add(self.treeview)
        
        self.tvcolumn = gtk.TreeViewColumn()
        self.cell = gtk.CellRendererText()
        self.cell.set_property("weight", pango.WEIGHT_BOLD)
        self.cell2 = gtk.CellRendererText()
        
        self.treeview.set_headers_visible(False)
        self.tvcolumn.pack_start(self.cell, False)
        self.tvcolumn.pack_start(self.cell2, False)
        self.tvcolumn.add_attribute(self.cell, 'text', 0)
        self.tvcolumn.add_attribute(self.cell2, 'text', 1)
        
        self.treeview.append_column(self.tvcolumn)
        self.treeview.set_search_column(0)
        
        self.button_colors_remove.set_sensitive(False)
        
        #Open and Save tab
        self.combobox_default_encoding = wt.get_widget("combobox_default_encoding")
        self.combobox_line_ending = wt.get_widget("combobox_line_ending")
        self.checkbutton_reopen_tabs = wt.get_widget("checkbutton_reopen_tabs")
        self.checkbutton_autosave = wt.get_widget("checkbutton_autosave")
        self.spinbutton_autosave = wt.get_widget("spinbutton_autosave")
        self.checkbutton_backup_file = wt.get_widget("checkbutton_backup_file")
        
    def __set_all_signals(self):
        """
        Set all signals used by the preferences window.
        """
        dic = {
               #"on_check_show_toolbar_toggled" :
               #self.on_check_show_toolbar_toggled,
               
               #"on_check_show_line_numbers_toggled" :
               #self.on_check_show_line_numbers_toggled,
               
               "on_check_highlight_current_line_toggled" :
               self.on_check_highlight_current_line_toggled,
               
               "on_check_use_spaces_toggled" :
               self.on_check_use_spaces_toggled,
               
               "on_check_auto_indent_toggled" :
               self.on_check_auto_indent_toggled,
               
               "on_check_text_wrapping_toggled" :
               self.on_check_text_wrapping_toggled,
               
               "on_check_right_margin_toggled" :
               self.on_check_right_margin_toggled,
               
               "on_check_brackets_matching_toggled" :
               self.on_check_brackets_matching_toggled,
               
               "on_spin_right_margin_value_changed" :
               self.on_spin_right_margin_value_changed,
               
               "on_fontbutton_font_set" :
               self.on_fontbutton_font_set,
               
               "on_button_colors_add_clicked" :
               self.on_button_colors_add_clicked,
               
               "on_button_colors_remove_clicked" :
               self.on_button_colors_remove_clicked,
               
               "on_combobox_default_encoding_changed" :
               self.on_combobox_default_encoding_changed,
               
               "on_combobox_line_ending_changed" :
               self.on_combobox_line_ending_changed,
               
               "on_checkbutton_autosave_toggled" :
               self.on_checkbutton_autosave_toggled,
               
               "on_spinbutton_autosave_value_changed" :
               self.on_spinbutton_autosave_value_changed,
               
               "on_checkbutton_backup_file_toggled" :
               self.on_checkbutton_backup_file_toggled,
               
               "on_checkbutton_reopen_tabs_toggled" :
               self.on_checkbutton_reopen_tabs_toggled
               }
               
        self.widgets_tree.signal_autoconnect(dic)
        
        self.treeview.connect("cursor-changed", self.row_clicked)
        
    #################### Signals ####################
    
    def on_check_highlight_current_line_toggled(self, widget):
        value = widget.get_active()
        pages = self.document_manager.get_n_pages()
        
        self.preferences_manager.set_value("highlight_current_line", value)
        for i in range(pages):
            view = self.document_manager.get_nth_page(i).view
            #self.document_manager.set_highlight_current_line(view, value)
            view.set_highlight_current_line(value)
            
    def on_check_use_spaces_toggled(self, widget):
        value = widget.get_active()
        pages = self.document_manager.get_n_pages()
        
        self.preferences_manager.set_value("indentation/use_spaces", value)
        for i in range(pages):
            view = self.document_manager.get_nth_page(i).view
            #self.document_manager.set_use_spaces(view, value)
            view.set_insert_spaces_instead_of_tabs(value)
    
    def on_check_auto_indent_toggled(self, widget):
        value = widget.get_active()
        pages = self.document_manager.get_n_pages()

        self.preferences_manager.set_value("indentation/automatic",
                                           widget.get_active())
        for i in range(pages):
            view = self.document_manager.get_nth_page(i).view
            #self.document_manager.set_auto_indent(view, value)
            view.set_auto_indent(value)
    
    def on_check_text_wrapping_toggled(self, widget):
        value = widget.get_active()
        pages = self.document_manager.get_n_pages()
        
        self.preferences_manager.set_value("text_wrapping",
                                           widget.get_active())
        for i in range(pages):
            document = self.document_manager.get_nth_page(i)
            document.set_text_wrapping(value)
            
    
    def on_check_right_margin_toggled(self, widget):
        value = widget.get_active()
        pages = self.document_manager.get_n_pages()
        
        self.preferences_manager.set_value("right_margin/display",
                                           widget.get_active())
        for i in range(pages):
            view = self.document_manager.get_nth_page(i).view
            #self.document_manager.set_show_right_margin(view, value)
            view.set_show_right_margin(value)
    
    def on_check_brackets_matching_toggled(self, widget):
        value = widget.get_active()
        pages = self.document_manager.get_n_pages()
        
        self.preferences_manager.set_value("brackets_matching",
                                           widget.get_active())
        for i in range(pages):
            view = self.document_manager.get_nth_page(i).view
            #self.document_manager.set_brackets_matching(view, value)
            view.buffer.set_highlight_matching_brackets(value)
    
    def on_spin_right_margin_value_changed(self, widget):
        value = widget.get_value_as_int()
        pages = self.document_manager.get_n_pages()
        
        self.preferences_manager.set_value("right_margin/position",
                                            widget.get_value_as_int())
        for i in range(pages):
            view = self.document_manager.get_nth_page(i).view
            #self.document_manager.set_right_margin_position(view, value)
            view.set_right_margin_position(value)
    
    def on_fontbutton_font_set(self, widget):
        value = widget.get_font_name()
        pages = self.document_manager.get_n_pages()
        
        self.preferences_manager.set_value("font", widget.get_font_name())
#        print widget.get_font_name()
        for i in range(pages):
            view = self.document_manager.get_nth_page(i).view
            #self.document_manager.set_font(view, value)
            view.modify_font(pango.FontDescription(value))
            
    def row_clicked(self, widget):
        selection = widget.get_selection()
        model, iter = selection.get_selected()
        name = model.get_value(iter, 0)
        pages = self.document_manager.get_n_pages()
        
        self.preferences_manager.set_value("color_style", self.styles[name])
        
        for i in range(pages):
            view = self.document_manager.get_nth_page(i).view
            self.document_manager.set_style(view, self.styles[name])
            
        ssm = self.document_manager.style_manager
        scheme = ssm.get_scheme(self.styles[name])
        filename = scheme.get_filename()
        
        if filename.split("/")[1] == "home":
            self.button_colors_remove.set_sensitive(True)
        else:
            self.button_colors_remove.set_sensitive(False)
    
    def on_button_colors_add_clicked(self, widget):
        scheme = ChooseFileDialog("escolher tema", self.dialog_preferences,
                                  "Color Scheme File", '*.xml',
                                  False, constants.HOME)
        files = scheme.run()
        scheme.destroy()
        
        if len(files):
            file_name = files[0].split("/")[-1]
#            dist = constants.home + "/.textflow/colors/" + file_name
            dist = constants.HOME + constants.COLORS_DIR + file_name
            shutil.copyfile(files[0], dist)
            
        self.liststore.clear()
        self.__get_colors_styles()
        
    def on_button_colors_remove_clicked(self, widget):
        selection = self.treeview.get_selection()
        model, iter = selection.get_selected()
        name = model.get_value(iter, 0)
        filename = self.document_manager.get_style_filename(self.styles[name])
        shutil.move(filename, constants.HOME + "/.Trash/" + filename.split("/")[-1])
        model.remove(iter)
    
    def on_combobox_default_encoding_changed(self, widget):
        self.preferences_manager.set_value("open_save/encoding",
                                           widget.get_active_text())
    
    def on_combobox_line_ending_changed(self, widget):
        self.preferences_manager.set_value("open_save/line_ending",
                                           widget.get_active_text())
                                           
    def on_checkbutton_reopen_tabs_toggled(self, widget):
        self.preferences_manager.set_value("open_save/reopen_tabs",
                                           widget.get_active())
                                           
    def on_checkbutton_autosave_toggled(self, widget):
        value = widget.get_active()
        self.preferences_manager.set_value("open_save/auto_save", value)

        pages = self.document_manager.get_n_pages()
        
        for i in range(pages):
            document = self.document_manager.get_nth_page(i)
            
            if document.file_uri != "":
                if value:
                    self.document_manager.add_to_autosave(document)
                else:
                    self.document_manager.remove_from_autosave(document)
    
    def on_spinbutton_autosave_value_changed(self, widget):
        value = widget.get_value_as_int()
        
        self.preferences_manager.set_value("open_save/auto_save_minutes", value)
        
    def on_checkbutton_backup_file_toggled(self, widget):
        value = widget.get_active()
        self.preferences_manager.set_value("open_save/save_copy", value)
