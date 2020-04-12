import json
import math
from MidiKey import MidiKey, checkIfKeyExists


class KeyProfile:

    def __init__(self, path):
        self.buttons = [None] * 81
        self.methodNames = [None] * 81
        self.methodArguments = [None] * 81
        self.path = path
        with open(path) as json_file:
            data = json.load(json_file)
            self.name = data['name']
            for d in data['keys']:
                if not checkIfKeyExists(['x', 'y', 'red', 'green', 'function_name'], d):
                    continue
                mk = MidiKey(d)
                position = d['x'] + d['y'] * 9
                self.methodNames[position] = d['function_name']
                if checkIfKeyExists('arguments', d):
                    self.methodArguments[position] = d['arguments']
                self.buttons[position] = mk

    def returnAll(self):
        return [self.buttons, self.methodNames, self.methodArguments]

    def saveToFile(self):
        data = {"name": self.name, "keys": []}
        for b in self.buttons:
            data["keys"].append(self.keyToJson(b))
        file = open(self.path, "r+")
        file.truncate(0)
        json.dump(data, file)
        file.close()

    def changeKey(self, index, red, green, function, args = None):
        data = {'function_name': function, 'x': index%9, 'y': math.floor(index/9), 'red': red, 'green': green}
        if args is not None:
            data['arguments'] = args
            self.methodArguments[index] = args
        mk = MidiKey(data)
        self.buttons[index] = mk
        self.methodNames[index] = function

    def keyToJson(self, b):
        if b is None:
            return {}

        index = self.buttons.index(b)
        data = {'x': b.x, 'y': b.y, 'red': b.uRed, 'green': b.uGreen, 'function_name': self.methodNames[index]}
        if self.methodArguments[index] is not None:
            data['arguments'] = self.methodArguments[index]
        return data
