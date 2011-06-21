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
This module has the constants used on TextFlow.
"""

import gettext
import gtk
import gtk.glade
import os
import distutils.sysconfig
from tf.com import files as Files

_ = gettext.gettext

def get_path(default, destination):
    if not os.path.exists(destination):
        return os.path.abspath(default)
    else:
        return os.path.abspath(destination)

# Python Lib Dir
#PYTHON_LIB_DIR = distutils.sysconfig.get_python_lib()
PYTHON_LIB_DIR = os.path.split(os.path.split(os.path.dirname(__file__))[0])[0]

# User dirs
HOME = os.getenv("HOME")
COLORS_DIR = Files.mkdir(os.path.expanduser('~/.textflow/colors'))

BASE_PATH = os.path.abspath(os.curdir)

LANGUAGES_USER_DIR = get_path(os.path.expanduser('~/.textflow/languages'), 
                                       os.path.join(BASE_PATH ,'tf/languages'))


MAIN_WINDOW_GLADE = get_path('/usr/share/textflow/glade/main_window.glade',
                       os.path.join(BASE_PATH ,'tf/glade/main_window.glade'))
                       
PREFERENCES_WINDOW = get_path('/usr/share/textflow/glade/preferences.glade',
                       os.path.join(BASE_PATH ,'tf/glade/preferences.glade'))

SNIPPET_WINDOW = get_path('/usr/share/textflow/glade/snippetbrowser.glade',
                       os.path.join(BASE_PATH ,'tf/glade/snippetbrowser.glade'))

                       
SIDEPANELS_DIR = get_path('/usr/share/textflow/sidepanels',
                          os.path.join(BASE_PATH ,'tf/sidepanels'))
                          
TRIGGER_DIR = get_path('/usr/share/textflow/triggers',
                        os.path.join(BASE_PATH ,'tf/triggers'))

LANGUAGES_DIR = get_path(os.path.join(PYTHON_LIB_DIR, 'tf', 'languages'),
                        os.path.join(BASE_PATH ,'tf/languages'))
                        
print LANGUAGES_DIR

SCALABLE_ICON = get_path('/usr/share/textflow/icons/scalable/apps/textflow.svg',
                         os.path.join(BASE_PATH ,'icons/scalable/apps/textflow.svg'))

# Internationalization stuff...
APP = 'textflow'
DIR = '/usr/share/locale'

gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

gtk.glade.bindtextdomain(APP, DIR)
gtk.glade.textdomain(APP)
# End of internationalization stuff

# Strings
MESSAGE_0001 = _("New File")
MESSAGE_0002 = _("Save")
MESSAGE_0003 = _("Open")
MESSAGE_0004 = _("If you don't save it, your changes will be permanently lost.")
MESSAGE_0005 = _("<b>Save the changes to this document before closing?</b>")
MESSAGE_0006 = _("Close without saving")
MESSAGE_0007 = _("<b>Save the changes of unsaved tabs before closing?</b>")
MESSAGE_0008 = _("Save selected files")
MESSAGE_0009 = _("Search:")
MESSAGE_0010 = _("Replace:")
MESSAGE_0011 = _("<b>Cannot load snippet file</b>")
MESSAGE_0012 = _("The snippet xml file has errors and can't be loaded.")
MESSAGE_0013 = _("If you don't save they, your changes will be permanently lost.")
MESSAGE_0014 = _("<b>Save the changes of this document before change encode?</b>")
MESSAGE_0015 = _("No Document Open")
MESSAGE_0016 = _("Line: ")
MESSAGE_0017 = _("Column: ")
MESSAGE_0018 = _("<b>Could not save the file.</b>")
MESSAGE_0019 = _("You do not have the permissions necessary to save the file.")
MESSAGE_0020 = _("<b>TextFlow cannot decode this file with default encoding</b>")
MESSAGE_0021 = _("Select a character encoding from the menu and try again.")
MESSAGE_0022 = _("Character encoding: ")
MESSAGE_0023 = _("Other encoding")
MESSAGE_0024 = _("<b>Select a character encoding from the list.</b>")
MESSAGE_0025 = _("TextFlow cannot save this file with current encoding, please change current encoding and try again.")
MESSAGE_0026 = _("Tab Size:")
MESSAGE_0027 = _("Filter:")
MESSAGE_0028 = _("Goto line:")
MESSAGE_0029 = _('Could not connect to dbus session bus. Dbus will be unavailable.')
MESSAGE_0030 = _('The file %s is too large, you want really open it?')
MESSAGE_0031 = _('Press Return to close terminal')
MESSAGE_0032 = _("The file <b>%s</b> has been changed on disk.")
MESSAGE_0033 = _("<b>The file %s doesn't exists.</b>")
MESSAGE_0034 = _("You tried to open a inexistent file, please check if you typed the file path correctly and try again.")
MESSAGE_0035 = _("<b>Can not store tabs.</b>")
MESSAGE_0036 = _("You do not have permissions to store tabs. Check your textflow configuration directory in your home folder.")
MESSAGE_0037 = _('<b>Enter a custom tab size value.</b>')
MESSAGE_0038 = _('Tab size: ')


# Application info
APPNAME = "TextFlow"
APPVERSION = "0.3.2"
COPYRIGHTS = _("TextFlow - Copyright (c) 2007-2010\n Yuri Malheiros <ymalheiros@gmail.com>")
WEBSITE = "www.textflowproject.org"
AUTHORS = [
    _('Developers:'),
    'Yuri Malheiros <ymalheiros@gmail.com>',
    'Waldecir Santos <waldecir@gmail.com>',
    '',
    _('Contributors:'),
    'Andrews Medina <andrewsmedina@gmail.com>',
    'Bastian Kennel <bastian.kennel@gmail.com>',
    'Dickson Guedes <guediz@gmail.com>',
    'Elyézer Rezende <elyezermr@gmail.com>',
    'Gaëtan Podevijn <gpodevij@gmail.com>',
    'Laudeci Oliveira <laudeci@gmail.com>',
    'Luiz Armesto <luiz.armesto@gmail.com>',
    'Og Maciel <ogmaciel@gnome.org>',
    'Rafael Proença <cypherbios@gmail.com>',
]

ARTISTS = [
    'Marcelo Silva <celobox@gmail.com>'
]

TRANSLATORS = _("translator-credits")

LICENSE = """TextFlow is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 only.

TextFlow is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
"""
