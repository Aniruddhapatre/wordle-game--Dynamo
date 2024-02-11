import sys
from json import load
from random import randint
from collections import defaultdict
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtCore 
from PyQt5 import QtGui

from mainGui import Ui_mainWindow
from keymap import keydata 

wordArr = []
DEBUG = True
MAX_TRIALS = 6

STYLE_SHEET_STR = """
*:disabled {
	background-color:rgb(30, 30, 30);	
	color: rgb(127, 127, 127);
}
*{
	background-color: rgb(90, 90, 90);
	color: white;
}
"""

with open("./formattingTools/english_words.json", "r", encoding="utf-8") as fil:
    wordArr = load(fil)["data"]
    WORD_COU = len(wordArr)
    
class myWindow(QtWidgets.QMainWindow):
    keyPressed = QtCore.pyqtSignal(QtCore.QEvent)
    def __init__(self):
        super(myWindow, self).__init__()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('img.png'))
        self.keyPressed.connect(self.on_key)
        self.wordsLabelLayouts = [self.ui.word_1, self.ui.word_2, self.ui.word_3, self.ui.word_4, self.ui.word_5, self.ui.word_6]

        self.initApp()


    def keyPressEvent(self, event):
        super(myWindow, self).keyPressEvent(event)
        self.keyPressed.emit(event) 

    def on_key(self, event):
        if self.userStr and event.key() == QtCore.Qt.Key_Backspace:
            self.userStr = self.userStr[:-1]
        elif event.text().isalpha() and len(self.userStr) < 5:
            self.userStr += event.text()
        elif event.key() == QtCore.Qt.Key_Return:
            if DEBUG:
                print("Enter pressed")
            if len(self.userStr)  == 5:
                self.game()
            else:
                self.errorMessage("mistake", "Enter a 5 project word")
        
        self.printWord()
        
        if DEBUG:
            print(self.userStr)
        
    def clear(self):
        for layout in self.wordsLabelLayouts:
            labels = [layout.itemAt(i).widget() for i in range(layout.count()) if type(layout.itemAt(i).widget()) == QtWidgets.QLabel]
            for label in labels:
                label.setText("_")
                label.setStyleSheet("")

        for object in self.keyboardKeys.values():
            object.setStyleSheet("")      

    def printWord(self):
        layout = self.wordsLabelLayouts[self.iWLL]
        labels = [layout.itemAt(i).widget() for i in range(layout.count()) if type(layout.itemAt(i).widget()) == QtWidgets.QLabel]
        for label in labels:
            label.setText("_")
        for (char, label) in zip(self.userStr, labels):
            label.setText(char)

    def colorize(self):
        layout = self.wordsLabelLayouts[self.iWLL]
        labels = [layout.itemAt(i).widget() for i in range(layout.count()) if type(layout.itemAt(i).widget()) == QtWidgets.QLabel]
        for (label, color) in zip(labels, self.colorPatternArr):
            label.setStyleSheet(color)

    def colorizeKeyboard(self):
        for object, color in zip(self.keyboardKeys.values(), self.keyboardStyles.values()):
            object.setStyleSheet(color)                     

    def inputWord(self):
        if len(self.userStr) == 5:
            if self.userStr in wordArr:
                return self.userStr
            else:
                self.warningMessage(title=self.userStr, text="This word is not in the list ..guess again.")
                self.userStr = ""
                self.printWord()
                return None     

    def initApp(self):
        self.colorPatternArr = []
        mykeydata = keydata(self.ui)
        self.keyboardKeys = mykeydata.keyData
        self.keyboardStyles = {keyboardLetter: "" for keyboardLetter in self.keyboardKeys.keys()}
        self.userStr = ""
        self.iWLL = 0 # indice for self.wordsLabelLayouts
        self.word = wordArr[randint(0, WORD_COU-1)]
        self.attemptCou = 0
        self.clear()

    def play(self, selectedWord):
        global wordArr
        if self.inputWord() != None:
            if self.checkWord(self.inputWord(), selectedWord):
                return True
            else:
                self.attemptCou += 1
                self.iWLL += 1
                return False
        else:
            return None

    def checkWord(self, userWord, selectedWord):
        self.colorPatternArr = []
        self.prohibitedIndexes = []
        # Get the number of occurence each letter
        letters = defaultdict(int)
        for letter in selectedWord:
            letters[letter] += 1
        
        for i, (letterUser, letterSelected) in enumerate(zip(userWord, selectedWord)):
            if DEBUG:
                print(f"{i} {letterUser} {letterSelected}")
            
            if letterUser == letterSelected:
                self.colorPatternArr.append("color: rgb(56,118,29)")
                self.keyboardStyles[letterUser] = "background-color: rgb(56,118,29)"
                letters[letterUser] -= 1
                self.prohibitedIndexes.append(i)
            else:
                self.colorPatternArr.append("color: rgb(54, 51, 51)")
                self.keyboardStyles[letterUser] = "background-color: rgb(54, 51, 51)"

        for i, (letterUser, letterSelected) in enumerate(zip(userWord, selectedWord)):
            if letters[letterUser] > 0 and not (i in self.prohibitedIndexes):
                self.colorPatternArr[i] = "color: rgb(241,194,50)"
                self.keyboardStyles[letterUser] = "background-color: rgb(241,194,50)"
                letters[letterUser] -= 1

        self.colorize()
        self.colorizeKeyboard()

        if selectedWord == userWord:
            return True

    def infoMessage(self, title="Info", text="Text text"):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setWindowIcon(QtGui.QIcon('img.png'))
        msg.setText(text)
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        btnOk = msg.button(QMessageBox.Ok)
        btnOk.setText("OK")
        msg.setStyleSheet(STYLE_SHEET_STR)
        msg.exec_()

    def warningMessage(self, title="Info", text="Text text"):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setWindowIcon(QtGui.QIcon('img.png'))
        msg.setText(text)
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Ok)
        btnOk = msg.button(QMessageBox.Ok)
        btnOk.setText("ok")
        msg.setStyleSheet(STYLE_SHEET_STR)
        msg.exec_()

    def errorMessage(self, title="Error", text="An error occured"):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setWindowIcon(QtGui.QIcon('img.png'))
        msg.setText(text)
        msg.setIcon(QMessageBox.Critical)
        msg.setStandardButtons(QMessageBox.Ok)
        btnOk = msg.button(QMessageBox.Ok)
        btnOk.setText("Word puzzle game")
        msg.setStyleSheet(STYLE_SHEET_STR)
        msg.exec_()

    def confirmationMsg(self, title="Question", text="Are you sure doing xyz?"):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setWindowIcon(QtGui.QIcon('img.png'))
        msg.setText(text)
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.Yes)
        btnYes = msg.button(QMessageBox.Yes)
        btnYes.setText("YESS")
        btnNo = msg.button(QMessageBox.No)
        btnNo.setText("NO")
        msg.setStyleSheet(STYLE_SHEET_STR)
        answer = msg.exec_()
        return answer == QMessageBox.Yes

    def game(self):
        try:
            if self.play(self.word):
                self.infoMessage(title="you won ..yay", text=f"{self.word} you have succesfully found the word .")
                if self.confirmationMsg(title="Wordle", text="would you like to play again?"):
                    self.initApp()
                else:
                    sys.exit()
            elif self.attemptCou < MAX_TRIALS:
                self.userStr = ""
            elif self.attemptCou >= MAX_TRIALS:
                self.errorMessage(title="sorry you lost", text=f"selected word: {self.word} is the word.")
                if self.confirmationMsg(title="Wordle", text="would you like to play again ?"):
                    self.initApp()
                else:
                    sys.exit()
        except Exception as ex:
            self.errorMessage(text=str(ex))

def app():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    win = myWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    app()