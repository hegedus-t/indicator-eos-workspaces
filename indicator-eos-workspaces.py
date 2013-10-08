#!/usr/b        in/env python
#
# [SNIPPET_NAME:        Workspace Switcher Application Indicator for Elementary OS            ]
# [SNIPPET_CATEGORIES:  Application Indicator                                                 ]
# [SNIPPET_DESCRIPTION: Simple workspace switcher for Elementary OS                           ]
# [SNIPPET_AUTHOR:      Tamas Hegedus <hegedus.t@gmail.com>                                   ]
# [SNIPPET_BASED_ON:    George Dumitrescu's indicator-workspaces                              ]
# [                     https://launchpad.net/indicator-workspaces                            ]
# [                     Icons from (some gnome package): tbd                                  ]
# [SNIPPET_DOCS:        https://wiki.ubuntu.com/DesktopExperienceTeam/ApplicationIndicators   ]
# [SNIPPET_LICENSE:     GPL]

import pygtk
pygtk.require('2.0')
import gtk
import appindicator
import wnck
import time
import math
import tempfile
import os
import sys
import subprocess


ICON_THEME = gtk.icon_theme_get_default()
OWN_ICON_DIR = '~/indicator-eos-workspaces/icons/';

class AppIndicatorWorkspace:
    
    def __init__(self):
        
        self.lockfile = os.path.normpath(tempfile.gettempdir() + '/' + os.path.basename(__file__) + '.lock')
        import fcntl
        self.fp = open(self.lockfile, 'w')
        try:
            fcntl.lockf(self.fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except IOError:
            print "\nAnother instance is already running, quitting."
            sys.exit(-1)

        if self._which('dconf') == None:
            print "dconf-editor is missing\nTo install use Software manager or \n'sudu apt-get install dconf-editor' from command line"
            sys.exit(-1)

        self.ind = appindicator.Indicator("indicator-eos-workspaces", "", appindicator.CATEGORY_APPLICATION_STATUS)

        self.ind.set_status (appindicator.STATUS_ACTIVE)
        
        self.scr = wnck.screen_get_default()
        self.scr.force_update()

        while gtk.events_pending():
            gtk.main_iteration()
            
        self.initialize()
        self.set_icon(self.active_desktop)

        self.scr.connect('active-workspace-changed', self.ws_changed)

    def set_icon(self, ws = None):
        ic = "workspace-%d" % (ws+1)
        if ICON_THEME.lookup_icon(ic, 24, 0):
            self.ind.set_icon(ic)
        else:
            self.ind.set_icon_theme_path (self.icon_directory(OWN_ICON_DIR))
            self.ind.set_icon(ic)

    def icon_directory(self, icon_path = __file__):
         return os.path.realpath(os.path.expanduser(icon_path)) + os.path.sep

    def _get_active_desktop(self):
        ws = self.scr.get_active_workspace()
        return ws.get_number()
    active_desktop = property(_get_active_desktop)

    def _get_num_desktops(self):
        return self.num_workspaces
    num_desktops = property(_get_num_desktops)
    
    def update(self):
        self.ws = self.scr.get_active_workspace()
        self.num_workspaces = self.scr.get_workspace_count()
    
    def _which(self,program):

        def is_exe(fpath):
            return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

        fpath, fname = os.path.split(program)
        if fpath:
            if is_exe(program):
                return program
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                path = path.strip('"')
                exe_file = os.path.join(path, program)
                if is_exe(exe_file):
                    return exe_file

        return None
    
    def _dconf(self, action, dconf_path, value  ):

        out = subprocess.check_output(["dconf" ,action,dconf_path,value], shell=False)
        return out
        
    def initialize(self):
        
        # variable init
        self.update()        
        
        # create a menu
        self.menu = gtk.Menu()
        self.aradio = []

        # xlib way:   
        # workspace_list = get_property(display.Display(), '_NET_DESKTOP_NAMES').value.split('\x00')[:-1]
        # cur_ws = get_property(display.Display(), '_NET_CURRENT_DESKTOP').value[0]

        workspace_list = self._dconf("read", "/org/gnome/desktop/wm/preferences/workspace-names","")[2:-3].split('\', \'')
        
        # generate list if empty
        if workspace_list[0] == '':
            workspace_list = []
            for number in range(self.num_desktops):
                label = "Workspace %d" % (number+1)
                workspace_list.append(label)
        
            # write dconf
            self._dconf("write","/org/gnome/desktop/wm/preferences/workspace-names", "[\"" + "\",\"".join(workspace_list) + "\"]")
        
        # create items for the menu 
        for number,workspace_name in enumerate(workspace_list):
            if number == 0:
                self.aradio.append(gtk.RadioMenuItem(None, workspace_name))

            else:
                self.aradio.append(gtk.RadioMenuItem(self.aradio[number-1], workspace_name))
            if number == self.ws:
                self.aradio[number].set_active(True)
            self.aradio[number].connect("activate", self.switch_to_desktop, number)
            self.aradio[number].show()
            self.menu.append(self.aradio[number])
                    
        self.menu.show()
        self.ind.set_menu(self.menu)
        # bug : https://bugs.launchpad.net/indicator-application/+bug/1075152
        #self.ind.connect("scroll-event", self.scroll_to_desktop)

    def clear(self):
        self.aradio = []
        self.initialize()
        
    def scroll_to_desktop(self, arg1, arg2, arg3):
        self.update()
        if arg3 == 0:
            if (self.active_desktop > 0):
                self.set_desktop(self.active_desktop-1)
        else:
            if (self.active_desktop < self.num_desktops-1):
                self.set_desktop(self.active_desktop+1)
            
        
    def switch_to_desktop(self, obj, number):
        self.update()
        if self.aradio[number].get_active():
            timestamp = int(time.time())
            self.scr.get_workspace(number).activate(timestamp)
            
    def set_desktop (self, number):
        timestamp = int(time.time())
        self.scr.get_workspace(number).activate(timestamp) 
        
    def ws_changed(self, scrm, opt = False):
        self.clear()
        self.set_icon(self.active_desktop)
        if not self.aradio[self.active_desktop].get_active():
            self.aradio[self.active_desktop].set_active(True)
        
    def preferences(self, opt):
        subprocess.Popen("indicator-workspaces-preferences")
    
    def quit(self, widget, data=None):
        gtk.main_quit()
        
def main():
    gtk.main()

if __name__ == "__main__":
    indicator = AppIndicatorWorkspace()
    main()
