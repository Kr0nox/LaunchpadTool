import tkinter as tk
import webbrowser
from LaunchpadListener import LaunchpadListener
import time
import threading
import math
from typing import List
from KeyProfile import KeyProfile
import Actions

launchpad = None
profiles: List[KeyProfile] = []
UI = None

UNCLICKED = "#bbb"
BACKGROUND = "#111"
BUTTON_SETTINGS_SELECTION_WIDTH = 26
DEFAULT_COLORS = {'fg': "#fff", 'bg': BACKGROUND}
INTERACTABLE_COLORS = {'fg': "#fff", 'bg': "#222"}
SELECTION_SETTINGS = {**DEFAULT_COLORS, 'bd': 0, 'highlightthickness': 1, 'highlightbackground': "#000"}
COLOR_SLIDER_SETTINGS = {'from_': 0, 'to': 3, 'orient': "horizontal", **DEFAULT_COLORS,
                         'highlightthickness': 1,
                         'highlightbackground': "#000", 'showvalue': False, 'activebackground': BACKGROUND,
                         'troughcolor': "#222", 'bd': 0, 'length': 195}
ATTRIBUTEROW = 6
LBL_INFO_PACK = {'fill': "x", 'expand': True, 'padx': 5, 'pady': 2, 'side': "top", 'anchor': "n"}
HEIGHT = 470

class GUI:
    uIButtons = []
    root = None
    buttonCanvas = None
    currentlyWorkingOnButton = [None, None]
    quiting = False

    def __init__(self, lp, p):
        global launchpad
        global profiles
        profiles = p
        launchpad = lp
        self.root = tk.Tk()
        self.root.title("Launchpad Shortcuts")
        canvas = tk.Canvas(self.root, bg="#222", bd=0, highlightthickness=0)
        canvas.pack()
        self.root.resizable(False, False)
        self.selected = 0

        # region Launchpad Display Matrix as Buttons
        buttonCanvas = tk.Canvas(canvas, width=450, height=450, bg=BACKGROUND, highlightthickness=2,
                                 highlightbackground="#000")
        buttonCanvas.pack(padx=10, pady=10, side="left", ipadx=1, ipady=1)
        for y in range(9):
            for x in range(9):
                if x == 8 and y == 0:
                    self.uIButtons.append("None")
                    continue
                tag = "clickable" + str(len(self.uIButtons))
                if x == 8 or y == 0:
                    c = buttonCanvas.create_oval(5 + x * 50, 5 + y * 50, 50 + x * 50, 50 + y * 50, fill=UNCLICKED,
                                                 width=0, tags=tag)
                    # self.uIButtons.append(c)
                else:
                    c = self.round_rectangle(buttonCanvas, tag, 5 + x * 50, 5 + y * 50, 50 + x * 50, 50 + y * 50, 15)
                buttonCanvas.tag_bind(tag, "<Button-1>",
                                      lambda event, pos=x + y * 9: self.pressedUiLpKey(event, pos))

                self.uIButtons.append(c)
        # endregion

        settingsCanvas = tk.Canvas(canvas, width=270, height=HEIGHT, bg="#222", highlightthickness=0)
        settingsCanvas.pack(side="left")

        # region Settings for File
        fileSettingsCanvas = tk.Canvas(settingsCanvas, width=250, height=100, bg=BACKGROUND, highlightthickness=2,
                                       highlightbackground="#000")
        fileSettingsCanvas.pack_propagate(0)
        fileSettingsCanvas.pack(padx=10, pady=10, side="top", ipadx=5, ipady=5, fill="both")

        self.profilesChoices = ["Display Current"]
        for p in profiles:
            self.profilesChoices.append(p.name)

        # Drop-Down Selection
        self.profilesChoice = tk.StringVar(fileSettingsCanvas)
        self.profilesChoice.set(self.profilesChoices[0])
        self.profilesSelection = tk.OptionMenu(fileSettingsCanvas, self.profilesChoice, *self.profilesChoices)
        self.profilesSelection.configure(**SELECTION_SETTINGS)
        self.profilesSelection.pack(fill="x", expand=True, padx=5, pady=5, side="top", anchor="n")
        self.profilesChoice.trace_variable("w", self.profileSelectionChanged)

        # Name Changing
        self.changeNameCanvas = tk.Canvas(fileSettingsCanvas, bg=BACKGROUND, highlightthickness=0)
        self.changeNameCanvasPackSettings = {'fill': "x", 'expand': True, 'padx': 2}
        self.changeNameCanvas.pack(**self.changeNameCanvasPackSettings)
        txtName = tk.Label(self.changeNameCanvas, text="New Name:", **DEFAULT_COLORS)
        txtName.pack(side="left", padx=3, pady=3)
        self.inputText = tk.StringVar(self.changeNameCanvas, "asdasd")
        self.inputName = tk.Entry(self.changeNameCanvas, textvariable=self.inputText, **DEFAULT_COLORS,
                                  borderwidth=0, highlightthickness=1,
                                  highlightbackground="#000")
        self.inputName.pack(fill="x", expand=True, padx=3, pady=3, side="right")

        # Buttons
        self.fileButtonCanvas = tk.Canvas(fileSettingsCanvas, bg=BACKGROUND, highlightthickness=0)
        self.fileButtonCanvasPackSettings = {'fill': "x", 'expand': True, 'padx': 2, 'pady': 2, 'anchor': "s"}
        self.fileButtonCanvas.pack(**self.fileButtonCanvasPackSettings)
        saveButton = tk.Button(self.fileButtonCanvas, text="Save", **INTERACTABLE_COLORS, borderwidth=0,
                               command=self.saveNameChange)
        saveButton.pack(padx=3, pady=3, expand=True, fill="x", side="left")
        cancelButton = tk.Button(self.fileButtonCanvas, text="Cancel", **INTERACTABLE_COLORS, borderwidth=0,
                                 command=self.cancelNameChange)
        cancelButton.pack(padx=3, pady=3, expand=True, fill="x", side="right")
        # endregion

        # region Settings for Key
        # Canvas Structure
        buttonSettings = tk.Canvas(settingsCanvas, width=250, height=210, bg=BACKGROUND, highlightthickness=2,
                                   highlightbackground="#000")
        buttonSettings.pack_propagate(0)
        buttonSettings.pack(padx=10, pady=10, side="top", ipadx=5, ipady=5)
        self.buttonSettingsCanvasOuter = tk.Canvas(buttonSettings, bg=BACKGROUND, highlightthickness=2,
                                                   highlightbackground="#000")
        self.buttonSettingsCanvasOuterPackSettings = {'fill': "both", 'expand': True}
        self.buttonSettingsCanvasOuter.pack(**self.buttonSettingsCanvasOuterPackSettings)
        buttonSettingsCanvas = tk.Canvas(self.buttonSettingsCanvasOuter, bg=BACKGROUND, highlightthickness=0, width=240)
        buttonSettingsCanvas.pack(padx=5, pady=5, fill="both", expand=True)

        # X und Y Coordinates
        self.lblX = tk.Label(buttonSettingsCanvas, text="X:  ", **DEFAULT_COLORS)
        self.lblX.grid(column=0, row=0)
        self.lblY = tk.Label(buttonSettingsCanvas, text="Y:  ", **DEFAULT_COLORS)
        self.lblY.grid(column=1, row=0, sticky="w")

        # Red Slider
        lblRed = tk.Label(buttonSettingsCanvas, text="Red:", **DEFAULT_COLORS)
        lblRed.grid(column=0, row=1)
        self.sliderRed = tk.Scale(buttonSettingsCanvas, **COLOR_SLIDER_SETTINGS, command=self.colorSliderChange)
        self.sliderRed.grid(column=1, row=1)

        # Green Slider
        lblGreen = tk.Label(buttonSettingsCanvas, text="Green:", **DEFAULT_COLORS)
        lblGreen.grid(column=0, row=2, sticky="ew")
        self.sliderGreen = tk.Scale(buttonSettingsCanvas, **COLOR_SLIDER_SETTINGS, command=self.colorSliderChange)
        self.sliderGreen.grid(column=1, row=2)

        # Display Color
        lblCol = tk.Label(buttonSettingsCanvas, text="Color:", **DEFAULT_COLORS)
        lblCol.grid(column=0, row=3)
        self.lblColor = tk.Label(buttonSettingsCanvas, **DEFAULT_COLORS, width=BUTTON_SETTINGS_SELECTION_WIDTH)
        self.lblColor.grid(column=1, row=3, sticky="w")

        # Function
        lblFunc = tk.Label(buttonSettingsCanvas, text="Function:", **DEFAULT_COLORS)
        lblFunc.grid(column=0, row=4)


        Actions.checkMethods()
        self.funcCatChoices = Actions.methodCategories
        self.funcCatChoices.append("none")
        self.funcCatValue = tk.StringVar(buttonSettingsCanvas)
        self.funcCatValue.set("none")
        self.funcCatSelection = tk.OptionMenu(buttonSettingsCanvas, self.funcCatValue, *self.funcCatChoices)
        self.funcCatSelection.configure(**SELECTION_SETTINGS, width=BUTTON_SETTINGS_SELECTION_WIDTH)
        self.funcCatSelection.grid(column=1, row=4)
        self.funcCatValue.trace_variable("w", self.funcCatSelectionChanged)

        self.funcChoices = ["none"]
        self.funcValue = tk.StringVar(buttonSettingsCanvas)
        self.funcValue.set("none")
        self.funcSelection = tk.OptionMenu(buttonSettingsCanvas, self.funcValue, *self.funcChoices)
        self.funcSelection.configure(**SELECTION_SETTINGS, width=BUTTON_SETTINGS_SELECTION_WIDTH)
        self.funcSelection.grid(column=1, row=5)
        self.funcValue.trace_variable("w", self.funcSelectionChanged)

        self.txtAtt = tk.Label(buttonSettingsCanvas, text="Params:", **DEFAULT_COLORS)
        self.txtAtt.grid(column=0, row=ATTRIBUTEROW)
        self.attString = tk.StringVar(buttonSettingsCanvas, "")
        self.inputAtt = tk.Entry(buttonSettingsCanvas, textvariable=self.attString, **DEFAULT_COLORS,
                                 borderwidth=0, highlightthickness=1, width=32,
                                 highlightbackground="#000")
        self.inputAtt.grid(column=1, row=ATTRIBUTEROW)

        buttonSettingsCanvas.columnconfigure(1, weight=1)
        for i in range(5):
            buttonSettingsCanvas.rowconfigure(i, pad=5)
        # Buttons
        saveButtonB = tk.Button(self.buttonSettingsCanvasOuter, text="Save", **INTERACTABLE_COLORS, borderwidth=0,
                                command=self.saveKeyChange)
        saveButtonB.pack(padx=5, pady=5, expand=True, fill="x", side="left")
        cancelButtonB = tk.Button(self.buttonSettingsCanvasOuter, text="Cancel", **INTERACTABLE_COLORS, borderwidth=0,
                                  command=self.cancelKeyChange)
        cancelButtonB.pack(padx=5, pady=5, expand=True, fill="x", side="right")
        # endregion

        # Spacer
        spacerCanvas = tk.Canvas(settingsCanvas, width=250, height=64, bg=BACKGROUND, highlightthickness=2,
                                 highlightbackground="#000")
        spacerCanvas.pack_propagate(0)
        spacerCanvas.pack(padx=10, pady=10, side="bottom", ipadx=5, ipady=5)
        lblInfo1 = tk.Label(spacerCanvas, text="Open Source Project on ", **DEFAULT_COLORS)
        lblInfo2 = tk.Label(spacerCanvas, text="GitHub", bg=BACKGROUND, fg="#5af")
        lblInfo3 = tk.Label(spacerCanvas, text="Tested with Novation Launchpad Mini", **DEFAULT_COLORS)
        lblInfo1.pack(**LBL_INFO_PACK)
        lblInfo2.pack(**LBL_INFO_PACK)
        lblInfo2.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/AlexV-KX/LaunchpadTool"))
        lblInfo3.pack(**LBL_INFO_PACK)

        self.buttonSettingsCanvasOuter.pack_forget()
        self.changeNameCanvas.pack_forget()
        self.fileButtonCanvas.pack_forget()
        self.inputAtt.grid_forget()
        self.txtAtt.grid_forget()
        self.buttonCanvas = buttonCanvas
        self.listener = LaunchpadListener(launchpad, self, profiles)
        global UI
        UI = self
        t = threading.Thread(target=self.startPad)
        t.start()
        self.root.protocol("WM_DELETE_WINDOW", self.closing)
        self.root.mainloop()

    # UI Changes
    def profileSelectionChanged(self, *args):
        value = self.profilesChoice.get()
        self.selected = self.profilesChoices.index(value) - 1
        if value == self.profilesChoices[0]:
            self.buttonSettingsCanvasOuter.pack_forget()
            self.changeNameCanvas.pack_forget()
            self.fileButtonCanvas.pack_forget()
            self.colorUIButtons(self.listener.buttons)
        else:
            self.buttonSettingsCanvasOuter.pack(**self.buttonSettingsCanvasOuterPackSettings)
            self.changeNameCanvas.pack(**self.changeNameCanvasPackSettings)
            self.fileButtonCanvas.pack(**self.fileButtonCanvasPackSettings)
            self.inputText.set(profiles[self.selected].name)
            self.colorUIButtons(profiles[self.selected].buttons, True)

    def funcCatSelectionChanged(self, *args):
        index = self.funcCatChoices.index(self.funcCatValue.get())
        menu = self.funcSelection.children['menu']
        for i in range(len(self.funcChoices)):
            menu.delete(0)
        if self.funcCatValue.get() != 'none':
            for t in Actions.methodNames[index]:
                menu.add_command(label=t, command=lambda v=self.funcValue, l=t: v.set(l))
            self.funcChoices = Actions.methodNames[index]
        else:
            self.attString.set("")
            self.inputAtt.grid_forget()
            self.txtAtt.grid_forget()
            self.funcChoices = ['none']

        self.funcValue.set(self.funcChoices[0])

    def funcSelectionChanged(self, *args):
        if self.funcCatValue.get() == 'none':
            return
        catIndex = Actions.methodCategories.index(self.funcCatValue.get())
        nameIndex = Actions.methodNames[catIndex].index(self.funcValue.get())
        if Actions.attributeCount[catIndex][nameIndex] > 0:
            self.txtAtt.grid(column=0, row=ATTRIBUTEROW)
            self.inputAtt.grid(column=1, row=ATTRIBUTEROW)
        else:
            self.txtAtt.grid_forget()
            self.inputAtt.grid_forget()

    def colorSliderChange(self, event):
        self.lblColor.config(bg=self.returnHexColor(self.sliderRed.get(), self.sliderGreen.get()))

    @staticmethod
    def onEnter(e, o):
        o['background'] = "#000"

    @staticmethod
    def onLeave(e, o):
        o['background'] = "#222"

    # Called if a key in the UI gets pressed
    def pressedUiLpKey(self, event, i):
        if self.selected != -1:
            self.resetButtonSettings()
            x = (i % 9)
            y = math.floor(i / 9)
            self.lblX.config(text="X: " + str(x))
            self.lblY.config(text="Y: " + str(y))
            self.currentlyWorkingOnButton = [x, y]
            button = profiles[self.selected].buttons[i]
            if button is not None:
                self.sliderRed.set(button.uRed)
                self.sliderGreen.set(button.uGreen)
                methodName = profiles[self.selected].methodNames[i]
                self.funcCatValue.set(Actions.getParentClass(methodName))
                self.funcValue.set(methodName)
                self.attString.set(profiles[self.selected].methodArguments[i])
            else:
                self.sliderRed.set(0)
                self.sliderGreen.set(0)

    # Save functions
    def saveNameChange(self):
        profiles[self.selected].name = self.inputText.get()
        profiles[self.selected].saveToFile()

    def cancelNameChange(self):
        self.inputText.set(profiles[self.selected].name)

    def saveKeyChange(self):
        if self.currentlyWorkingOnButton[0] is None:
            return
        index = self.currentlyWorkingOnButton[0] + self.currentlyWorkingOnButton[1] * 9
        attr = None
        if self.funcCatValue.get() != 'none':
            catIndex = Actions.methodCategories.index(self.funcCatValue.get())
            nameIndex = Actions.methodNames[catIndex].index(self.funcValue.get())
            attr = self.attString.get() if Actions.attributeCount[catIndex][nameIndex] > 0 else None
        profiles[self.selected].changeKey(index,
                                          self.sliderRed.get(), self.sliderGreen.get(), self.funcValue.get(), attr)
        profiles[self.selected].saveToFile()
        self.setButtonColor(index, self.returnHexColor(self.sliderRed.get(), self.sliderGreen.get()))

        self.resetButtonSettings()
        self.listener.setButtons()
        self.currentlyWorkingOnButton = [None, None]

    # Cancel functions
    def cancelKeyChange(self):
        self.resetButtonSettings()
        self.currentlyWorkingOnButton = [None, None]

    def resetButtonSettings(self):
        self.lblX.config(text="X: ")
        self.lblY.config(text="Y: ")
        self.sliderRed.set(0)
        self.sliderGreen.set(0)
        self.funcCatValue.set("none")
        menu = self.funcSelection.children['menu']
        for i in range(len(self.funcChoices)):
            menu.delete(0)
        self.funcValue.set("none")
        self.txtAtt.grid_forget()
        self.inputAtt.grid_forget()
        self.attString.set("")

    # Makes square with rounded corners
    @staticmethod
    def round_rectangle(holder, tags, x1, y1, x2, y2, radius=25):
        points = [x1 + radius, y1,
                  x1 + radius, y1,
                  x2 - radius, y1,
                  x2 - radius, y1,
                  x2, y1,
                  x2, y1 + radius,
                  x2, y1 + radius,
                  x2, y2 - radius,
                  x2, y2 - radius,
                  x2, y2,
                  x2 - radius, y2,
                  x2 - radius, y2,
                  x1 + radius, y2,
                  x1 + radius, y2,
                  x1, y2,
                  x1, y2 - radius,
                  x1, y2 - radius,
                  x1, y1 + radius,
                  x1, y1 + radius,
                  x1, y1]
        return holder.create_polygon(points, smooth=True, fill=UNCLICKED, tags=tags)

    # Gives the UI the corresponding colors
    def colorUIButtons(self, lpButtons, ignore=False):
        if (self.selected < 0) or ignore:
            self.resetUIPad()
            for i in range(81):
                b = lpButtons[i]
                if b is not None:
                    self.setButtonColor(i, self.returnHexColor(b.uRed, b.uGreen))

    # Sets the color of a single button on the UI
    def setButtonColor(self, n, c):
        self.buttonCanvas.itemconfig(self.uIButtons[n], fill=c)

    # creates a Hexcode through  red and green values form 0 to 3
    @staticmethod
    def returnHexColor(r, g):
        if r == 0 and g == 0:
            return UNCLICKED
        col = ["0", "9", "c", "f"]
        return "#" + col[r] + col[g] + "0"

    # Makes the UI buttons blank
    def resetUIPad(self):
        for i in range(81):
            self.setButtonColor(i, UNCLICKED)

    # Reacts to a pressed key on the Launchpad
    def pressedOnLaunchpad(self, p, button):
        if button is not None and self.selected < 0:
            self.setButtonColor(p, self.returnHexColor(button.pRed, button.pGreen))
            time.sleep(0.5)
            self.setButtonColor(p, self.returnHexColor(button.uRed, button.uGreen))

    def startPad(self):
        self.listener.start()

    def closing(self):
        self.quiting = True
        self.root.destroy()

    def none(self, *args):
        pass
