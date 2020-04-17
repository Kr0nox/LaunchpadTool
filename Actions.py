# https://pyautogui.readthedocs.io/en/latest/cheatsheet.html#mouse-functions
import inspect
import json
import importlib
import importlib.util
import sys
from inspect import signature
from MidiKey import checkIfKeyExists

# Always imported because they are functions that you need to run the launchpad
from ActionFiles.LaunchpadActions import LaunchpadActions

methodCategories = []
methodNames = []
attributeCount = []
classes = []


def loadClasses():
    global classes
    paths = []
    names = []
    with open("plugins.json") as json_file:
        allData = json.load(json_file)
        plugins = allData["plugins"]
        for p in plugins:
            if not checkIfKeyExists(["path", "name"], p):
                continue
            if not paths.__contains__(p["path"]):
                paths.append(p["path"])
            names.append(p["name"])

    for p in paths:
        sys.path.append(p)

    for n in names:
        importlib.import_module(n)
        for name, obj in inspect.getmembers(sys.modules[n]):
            if inspect.isclass(obj):
                classes.append(obj)


loadClasses()


class Actions(LaunchpadActions, *classes):

    def __init__(self, lp):
        print("initA")
        bases = Actions.__bases__
        for b in bases:
            for method_name in dir(b):
                if callable(getattr(b, method_name)):
                    if method_name == "_init":
                        print(str(b) + " | " + str(len(signature(getattr(b, "_init")).parameters)))
                        if len(signature(getattr(b, "_init")).parameters) == 2:
                            getattr(b, "_init")(self, lp)
        # self.listener = lp


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
