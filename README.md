indicator-eos-workspaces
========================

Provides workspace indicator and switcher for Elementary OS. 
Code highly based on George Dumitrescu's indicator-workspaces for Ubuntu.

Dependecies
------------

python-wnck

    sudo apt-get install python-wnck

dconf-editor

    sudo apt-get install dconf-editor

Usage
------------

    python indicator-eos-workspaces [own-icon-dir]

or

    chmod +x indicator-eos-workspaces
    ./indicator-eos-workspaces [own-icon dir]

To execute it automatically add it at _System settings/Startup Applications_


Notes
------------
Currently dynamic workspaces are not handled. In order to use indicator-eos-workspaces set ``org>>pantheon>>desktop>>gala>>behavior>>dynamic-workspaces`` to false with dconf-editor

or:
 
    dconf write /org/pantheon/desktop/gala/behavior/dynamic-workspaces false

indicator-eos-workspaces is going to search `workspace-x` icons in

- the current themes dir 
(Elementary OS icon themes don't contain any workspace related icon currently, but it gives the possibility to the theme creators.)
- user directory if specified in first argument
- <path to indicator-eos-workspaces>/icons

Setting names of workspaces

Via dconf-tool at ``org>>gnome>>desktop>>wm>>preferences>>num-workspaces`` or:

    dconf write /org/gnome/desktop/wm/preferences/num-workspaces 4
    
Setting number of workspaces

Via dconf-tool at ``org>>gnome>>desktop>>wm>>preferences>>workspace-names`` or:

    dconf write /org/gnome/desktop/wm/preferences/workspace-names ['1','2','3','4']

Todo
------------
- Direct usage of dconf might(should) be replaced Gio module 
- preferences (user icon dir, num of workspaces,workspacenames) do i need this? :)
- Scrolling - later due to https://bugs.launchpad.net/indicator-application/+bug/1075152

