import pyautogui as controller


class Standard:

    def new(self):
        controller.hotkey('ctrl', 'n')

    def undo(self):
        controller.hotkey('ctrl', 'z')

    def redoY(self):
        controller.hotkey('ctrl', 'y')

    def redoZ(self):
        controller.hotkey('ctrl', 'shift', 'z')

    def save(self):
        controller.hotkey('ctrl', 's')

    def copy(self):
        controller.hotkey('ctrl', 'c')

    def cut(self):
        controller.hotkey('ctrl', 'x')

    def paste(self):
        controller.hotkey('ctrl', 'v')
