
class LaunchpadActions:

    def _init(self, lp):
        print("initLP")
        self.listener = lp

    def changeMode(self, mode):
        self.listener.changeMode(int(mode))