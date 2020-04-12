import pyautogui as controller

class Selection:
    def selectAll(self):
        controller.hotkey('ctrl', 'a')

    def selectWordRight(self):
        controller.hotkey('ctrl', 'shift', 'right')

    def selectSingleRight(self):
        controller.hotkey('shift', 'right')

    def selectWordLeft(self):
        controller.hotkey('ctrl', 'shift', 'left')

    def selectSingleLeft(self):
        controller.hotkey('shift', 'left')