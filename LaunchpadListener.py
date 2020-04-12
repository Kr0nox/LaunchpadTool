import ctypes
import sys
import time
from MidiKey import MidiKey
import pathlib
from typing import List
from Actions import Actions
try:
    import launchpad_py as launchpadManager
except ImportError:
    try:
        import launchpadManager
    except ImportError:
        sys.exit("error loading launchpad.py")
# endregion


class LaunchpadListener:

    currentModeIndex = 0
    buttons: List[MidiKey] = []
    methodNames: str = []
    methodArguments: str = []
    launchpad = None
    filePath = str(pathlib.Path(__file__).parent.absolute()) + "\\"

    def __init__(self, launchpad, UI, profiles):
        if not launchpad.Open():
            print("No Launchpad found")
            return
        self.profiles: List[profiles] = profiles
        self.actions: Actions = Actions(self)
        self.launchpad = launchpad
        self.GUI = UI
        self.setButtons()
        self.GUI.colorUIButtons(self.buttons, True)

    def start(self):
        while not self.GUI.quiting:
            # m = changed Buttons
            buttonData = self.launchpad.ButtonStateXY()
            if not buttonData:
                time.sleep(.05)
                continue
            else:
                # find pressed button
                position = buttonData[0] + buttonData[1] * 9
                pressedKey = self.buttons[position]
                if pressedKey is None:
                    pressedKey = MidiKey({'x': buttonData[0], 'y': buttonData[1], 'red': 0, 'green': 0})

                # give Button new Cor & do action
                pressedKey.changeColor(buttonData[2], self.launchpad)
                if buttonData[2]:
                    self.action(position)

        self.launchpad.Reset()

    def setActions(self, actions):
        self.actions = actions

    def changeMode(self, newMode):
        self.currentModeIndex = newMode
        self.setButtons()

    def setButtons(self):
        # load current data
        data = self.profiles[self.currentModeIndex]
        self.buttons = data.buttons
        self.methodNames = data.methodNames
        self.methodArguments = data.methodArguments

        # set current colors
        self.launchpad.Reset()
        for b in self.profiles[self.currentModeIndex].buttons:
            if b is not None:
                b.changeColor(False, self.launchpad, True)
        self.GUI.colorUIButtons(self.buttons,False)

    def action(self, pressed):
        # ToDo Combine somehow smart
        if self.methodNames[pressed] is None:
            return
        args = []
        if self.methodArguments[pressed] is not None:
            args = str.split(str(self.methodArguments[pressed]), ',')
        getattr(self.actions, str(self.methodNames[pressed]))(*args)
        try:
            self.GUI.pressedOnLaunchpad(pressed, self.buttons[pressed])
        except:
            ctypes.windll.user32.MessageBoxW(0, u"Error", u"Error", 0)


    def setColorXY(self, x, y, r, g):
        self.findButton(x + y * 9).setColor(r, g, self.launchpad)

    def setColorRaw(self, pos, r, g):
        self.buttons[pos].setColor(r, g, self.launchpad)

    def findButton(self, position):
        left = 0
        right = len(self.buttons)
        while left <= right:
            center = int(left + (right - left) / 2)
            if self.buttons[center].position > position:
                right = center - 1
            elif self.buttons[center].position < position:
                left = center + 1
            else:
                return self.buttons[center]
        return None
