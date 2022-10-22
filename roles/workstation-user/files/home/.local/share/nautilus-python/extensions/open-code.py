# -*- coding: utf-8 -*-
#
# Add context menu to open Visual Studio Code to Nautilus
#
# Copyright (c) Zhangyuan Nie. All rights reserved. MIT license.

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Nautilus", "4.0")
from gi.repository import Nautilus, GObject
from subprocess import run


class OpenCodeExtension(GObject.GObject, Nautilus.MenuProvider):
    def _open_code(self, menu, file):
        run(["code", file.get_location().get_path()])

    def get_background_items(self, dir):
        item = Nautilus.MenuItem(
            name="NautilusPython::opencode",
            label="Open in Code",
            tip="Open the current directory in Code",
        )
        item.connect("activate", self._open_code, dir)

        return (item,)
