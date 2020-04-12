# https://pyautogui.readthedocs.io/en/latest/cheatsheet.html#mouse-functions
import pyautogui as controller
import clipboard
from ActionFiles.Standard import Standard
from ActionFiles.Custom import Custom
from ActionFiles.Krita import Krita
from ActionFiles.Selection import Selection
from ActionFiles.LaunchpadActions import LaunchpadActions
from inspect import signature

methodCategories = []
methodNames = []
attributeCount = []


class Actions(LaunchpadActions, Standard, Selection, Custom, Krita):

    def __init__(self, lp):
        self.listener = lp


    def clipboardAction(self, pos):
        if self.clipboardMode == 0:
            self.copyToClipboard(int(pos))
        else:
            self.pasteFromClipboard(int(pos))

    def changeClipboardMode(self):
        self.clipboardMode = -self.clipboardMode + 1
        print(self.clipboardMode)
        self.listener.setColorXY(8, self.clipboardRow, 3 * self.clipboardMode, -3 * self.clipboardMode + 3)
        for i in range(8):
            self.listener.setColorXY(i, self.clipboardRow,
                                     0 if self.clipboards[i] != "" else 3 - 3 * self.clipboardMode,
                                     3 if self.clipboards[i] != "" else 0)

    def copyToClipboard(self, position):
        c = clipboard.paste()
        self.copy()
        self.clipboards[position] = clipboard.paste()
        clipboard.copy(c)
        self.listener.setColorXY(position, self.clipboardRow, 0, 3)

    def pasteFromClipboard(self, position):
        c = clipboard.paste()
        clipboard.copy(self.clipboards[position])
        self.paste()
        clipboard.copy(c)

    def clearClipboard(self, position):
        print("coming")

    def none(self):
        print("noe")

    def test(self, a, b):
        print(b)
        print(a)



def checkMethods():
    bases = Actions.__bases__
    for b in bases:
        methodCategories.append(b.__name__)
        object_methods = [method_name for method_name in dir(b)
                          if callable(getattr(b, method_name))]
        callables = []
        args = []
        for o in object_methods:
            if o[0] != '_':
                callables.append(o)
                args.append(len(signature(getattr(b, o)).parameters) - 1)
        methodNames.append(callables)
        attributeCount.append(args)

def getParentClass(methodName):
    for count, val in enumerate(methodNames):
        if methodName in val:
            return methodCategories[count]
    return "none"
