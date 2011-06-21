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
This module implements a About Dialog.
"""

import gtk

from tf.core import constants

class AboutDialog(gtk.AboutDialog):
    """
    About dialog class.
    """
    def __init__(self, parent=None):
        gtk.AboutDialog.__init__(self)

        # Set up the UI
        self.__initialize_dialog_widgets()

    #################### Private Methods ####################
    
    def __initialize_dialog_widgets(self):
        self.set_name(constants.APPNAME)
        self.set_version(constants.APPVERSION)
        self.set_copyright(constants.COPYRIGHTS)
        self.set_logo(gtk.gdk.pixbuf_new_from_file(constants.SCALABLE_ICON))
        self.set_translator_credits(constants.TRANSLATORS)
        self.set_license(constants.LICENSE)
        self.set_website("http://" + constants.WEBSITE)
        self.set_website_label(constants.WEBSITE)
        self.set_authors(constants.AUTHORS)
        self.set_artists(constants.ARTISTS)

        # Show all widgets
        self.show_all()
