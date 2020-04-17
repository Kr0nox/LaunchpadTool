class MidiKey:
    x = 0
    y = 0
    position = 0
    uRed = 0
    uGreen = 0
    pRed = 0
    pGreen = 0
    disabled = False
    pressed = False

    def __init__(self, d):
        self.x = d['x']
        self.y = d['y']
        self.position = self.x + self.y * 9
        self.uRed = d['red']
        self.uGreen = d['green']
        if checkIfKeyExists('disable', d):
            self.disabled = bool(d['disable'])
        self.pRed = 0 if not self.uGreen >= self.uRed else 3
        self.pGreen = 0 if not self.uRed > self.uGreen else 3

    def changeColor(self, pressedState, launchpad, force=False):
        if self.disabled and not force:
            return

        if pressedState:
            launchpad.LedCtrlXY(self.x, self.y, self.pRed, self.pGreen)
        else:
            launchpad.LedCtrlXY(self.x, self.y, self.uRed, self.uGreen)

    def setColor(self, r, g, launchpad):
        launchpad.LedCtrlXY(self.x, self.y, r, g)

    def setDefaultColor(self, launchpad):
        launchpad.LedCtrlXY(self.x, self.y, self.uRed, self.uGreen)

def checkIfKeyExists(key, data):
    if data == {}:
        return False
    if isinstance(key, list):
        for k in key:
            if k not in data:
                return False
        return True
    return key in data
