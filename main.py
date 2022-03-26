import sys
from json import load
from random import randint
from collections import defaultdict

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtCore 
from PyQt5 import QtGui
from matplotlib.pyplot import text 
from mainGui import Ui_mainWindow

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

with open("words.json", "r", encoding="utf-8") as fil:
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

    def keyPressEvent(self, event):
        super(myWindow, self).keyPressEvent(event)
        self.keyPressed.emit(event) 

    def on_key(self, event):
        layout = self.ui.word_1
        for i in range(layout.count()):
            item = layout.itemAt(i).widget()
            if type(item) == QtWidgets.QLabel:
                item.setText(event.text())
            print(item)
        self.warningMessage()

    def play(self, selectedWord):
        global wordArr
        for i in range(1, MAX_TRIALS + 1):
            guess = ""
            while True:
                guess = input(f"{i}. Tahmininiz:\n-> ")
                if guess in wordArr:
                    break
                else:
                    self.warningMessage(title=guess, text="Bu kelime listede yok. Tekrar tahmin yapın.")
            if self.checkWord(guess, selectedWord):
                return True
        return False

    def checkWord(self, userWord, selectedWord):
        colorPatternArr = []
        # Get th number of occurence each letter
        letters = defaultdict(int)
        for letter in selectedWord:
            letters[letter] += 1
        
        for i, (letterUser, letterSelected) in enumerate(zip(userWord, selectedWord)):
            if DEBUG:
                print(f"{i} {letterUser} {letterSelected}")

            if letterUser == letterSelected:
                colorPatternArr.append("color: green")
                letters[letterUser] -= 1
            elif letters[letterUser]:
                colorPatternArr.append("color: yellow")
                letters[letterUser] -= 1
            else:
                colorPatternArr.append("color: red")
            
        # for (letter, color) in zip(userWord, colorPatternArr):
        #     print(color, end='')
        #     print(letter + " ", end='')


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
        btnOk.setText("Tamam")
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
        btnOk.setText("Tamam")
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
        btnOk.setText("Tamam")
        msg.setStyleSheet(STYLE_SHEET_STR)
        msg.exec_()

    def confirmationMsg(self, title="Question", text="Are you sure doing xyz?"):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setWindowIcon(QtGui.QIcon('img.png'))
        msg.setText(text)
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        btnYes = msg.button(QMessageBox.Yes)
        btnYes.setText("Evet")
        btnNo = msg.button(QMessageBox.No)
        btnNo.setText("Hayır")
        msg.setStyleSheet(STYLE_SHEET_STR)
        answer = msg.exec_()
        return answer == QMessageBox.Yes

    def game(self):
        try:
            word = wordArr[randint(0, WORD_COU-1)]
            if self.play(word):
                self.infoMessage(title="Kazandınız", text=f"{word} kelimesini başarıyla buldunuz.")
            else:
                self.errorMessage(title="Kaybettiniz", text=f"Seçilen kelime: {word} idi.")
        except KeyboardInterrupt:
            sys.exit()
        finally:
            if self.confirmationMsg(title="Wordle", text="Tekrar oynamak ister misiniz?"):
                self.game()
            else:
                sys.exit()


def app():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    win = myWindow()
    win.show()
    win.game()
    sys.exit(app.exec_())

if __name__ == "__main__":
    app()

