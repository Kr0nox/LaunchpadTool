from ActionFiles.Custom import Custom
import pyautogui as controller


class Krita:
    def eraser(self):
        controller.hotkey('e')

    def selectToolKrita(self, name):
        x, y = controller.position()
        controller.click(1390, 670)
        controller.hotkey('a')
        controller.hotkey('enter')
        self.kritaClearWritingArea()
        Custom.write(None, name)
        controller.click(1390, 710)
        self.kritaClearWritingArea()
        controller.moveTo(x, y)

    def newSceneKrita(self):
        x, y = controller.position()
        controller.click(1350, 580)
        controller.moveTo(x, y)

    def kritaClearWritingArea(self):
        controller.click(1360, 860)
        controller.hotkey('ctrl', 'a')
        controller.hotkey('delete')
