# region import
from Actions import checkMethods
import sys
from GUI import GUI
from KeyProfile import KeyProfile
from typing import List
try:
    import launchpad_py as launchpadManager
except ImportError:
    try:
        import launchpadManager
    except ImportError:
        sys.exit("error loading launchpad.py")

profiles: List[KeyProfile] = []
paths = ["Profiles\\modeChangeKeys.json",
         "Profiles\\programmingKeys.json",
         "Profiles\\kritaKeys.json"]


def main():
    launchpad = launchpadManager.Launchpad()
    for path in paths:
        k = KeyProfile(path)
        profiles.append(k)

    UI = GUI(launchpad, profiles)


if __name__ == '__main__':
    main()


