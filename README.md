indicator-eos-workspaces
========================

Provides workspace indicator and switcher for Elementary OS. 
Code highly based on George Dumitrescu's indicator-workspaces for Ubuntu.

Dependecies
------------

python-wnck
dconf-editor

Notes
------------
Currently dynamic workspaces are not handled. In order to use indicator-eos-workspaces set ``org>>pantheon>desktop>>gala>>behavior>>dynamic-workspaces`` to false with dconf-editor

or::
 
    dconf write /org/pantheon/desktop/gala/behavior/dynamic-workspaces false

Todo
------------
    Direct usage of dconf might be replaced Gio module
