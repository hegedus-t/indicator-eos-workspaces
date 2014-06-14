indicator-eos-workspaces
========================

Provides workspace indicator and switcher for Elementary OS. 
Code highly based on George Dumitrescu's indicator-workspaces for Ubuntu.

Dependecies
------------

python-wnck

    sudo apt-get install python-wnck

Usage
------------

    python indicator-eos-workspaces [own-icon-dir]

or

    chmod +x indicator-eos-workspaces
    ./indicator-eos-workspaces [own-icon dir]

To execute it automatically add it at _System settings/Startup Applications_


Notes
------------
Currently dynamic workspaces are not handled. In order to use indicator-eos-workspaces:
 
    gsettings set org.pantheon.desktop.gala.behavior dynamic-workspaces false

indicator-eos-workspaces is going to search `workspace-x` icons in

- the current themes dir 
(Elementary OS icon themes don't contain any workspace related icon currently, but it gives the possibility to the theme creators.)
- user directory if specified in first argument
- <path to indicator-eos-workspaces>/icons

Setting number of workspaces:

    gsettings set org.gnome.desktop.wm.preferences num-workspaces 4
    
Setting names of workspaces:

    gsettings set org.gnome.desktop.wm.preferences workspace-names "['1','2','3','4']"

Todo
------------
- preferences (user icon dir, num of workspaces,workspacenames) do i need this? :)
- Scrolling - later due to https://bugs.launchpad.net/indicator-application/+bug/1075152

