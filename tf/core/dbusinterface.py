# -*- coding: utf-8 -*-

#######################################################################
# Copyright © 2007-2009 Waldecir Santos.
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

import dbus
import dbus.service
import dbus.glib

dbus.glib.threads_init()

class DaemonDBus(dbus.service.Object):
    def __init__(self, bus_name, TextFlow_instance):
        self.TextFlow = TextFlow_instance
        object_path = '/org/textflowproject/TextFlow'
        super(DaemonDBus, self).__init__(bus_name, object_path)

    @dbus.service.method('org.textflowproject.TextFlow')
    def open_file_tab(self, path):
        self.TextFlow.document_manager.open_tab(path)
        self.TextFlow.main_window.deiconify()

def TextFlow_dbus_init(TextFlow_instance):
    try:
        session_bus = dbus.SessionBus()
        name = dbus.service.BusName('org.textflowproject.TextFlow', bus=session_bus)
        return DaemonDBus(name, TextFlow_instance)
    except dbus.DBusException:
        return None
