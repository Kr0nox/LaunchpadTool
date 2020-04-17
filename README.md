# LaunchpadTool
Custom Shortcuts on a Launchpad

### How to use
1. Install libraries (requirements.txt) 
2. Connect Launchpad to PC over USB
3. Start *app.py*
4. Configure your hotkeys and shortcuts

### Add new Profile
At the moment you will have to add a new json file (or copy an already existing) and then link to it in the paths array in *app.py*.


### Plug Ins
You can develop your own Plug Ins for this tool.

Every function has to be declared inside a class.
If reference to the launchpad listener is needed add the following
```python
def _init(self, lp):
    self.listener = lp
```
This function replaces the normal ```__init__```, so everything you want to call in init is writen in their.
Methods, that should not show up in the UI and shouldn´t be bound to a button are marked with an underscore in the front,
like the following:
```python
def _functionname:
    # Stuff to do in private method
```
Every other function will be shown in the UI.

A UI for adding Plug Ins will be added shortly. At the moment you can add your Plug Ins by adding them to the *plugins.json*.