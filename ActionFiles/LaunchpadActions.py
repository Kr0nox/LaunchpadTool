
class LaunchpadActions:

    def __init__(self, lp):
        self.listener = lp

    def changeMode(self, mode):
        self.listener.changeMode(int(mode))