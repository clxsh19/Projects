from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog
from PyQt5 import QtCore, QtGui, QtWidgets
from PIL import Image
import sys

from cache import json_file
from photomosaics import start, Add_all_pixels


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(100, 100, 800, 500)
        self.setWindowTitle("Photomosaics")

        self.Image_box()
        self.File_button()
        self.Folder_button()
        self.Submit_button()

    def Image_box(self):
        self.label = QtWidgets.QLabel('', self)
        self.label.setGeometry(QtCore.QRect(140, 0, 656, 480))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(None))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

    def File_button(self):
        self.button = QtWidgets.QPushButton(self)
        self.button.setText('Choose a File')
        self.button.setGeometry(20, 20, 100, 40)
        self.button.clicked.connect(self.chooseFile)

    def Folder_button(self):
        self.button2 = QtWidgets.QPushButton(self)
        self.button2.setText('Choose Folder')
        self.button2.setGeometry(20, 80, 100, 40)
        self.button2.clicked.connect(self.chooseFolder)

    def Submit_button(self):
        self.button3 = QtWidgets.QPushButton(self)
        self.button3.setText('Submit')
        self.button3.setGeometry(20, 400, 100, 40)
        self.button3.clicked.connect(self.submit)

    def chooseFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if file:
            self.filePath = file
            self.image = Image.open(self.filePath)

    def chooseFolder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        folder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if folder:
            self.folderPath = folder

    def submit(self):
        SIDE = 10
        DIV = SIDE*SIDE
        WIDTH, HEIGHT = self.image.size
        NEW_IMAGE = Image.new(mode = "RGB", size = (WIDTH ,HEIGHT), color = None)

        json_file(self.folderPath, DIV)
        start(self.image, NEW_IMAGE, WIDTH, HEIGHT, SIDE, DIV, self.folderPath)
        NEW_IMAGE.save("photomosaic.jpg")
        self.label.setPixmap(QtGui.QPixmap('photomosaic.jpg'))
        
def main():
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())

main()