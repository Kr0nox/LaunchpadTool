import pyautogui as controller
import clipboard

class Custom:

    clipboards = [""] * 8
    clipboardMode = 0
    clipboardRow = 7

    def hotkey(self, *args):
        controller.hotkey(*args)

    def write(self, text):
        c = clipboard.paste()
        clipboard.copy(text)
        self.paste()
        clipboard.copy(c)