import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QFileDialog, QAction
from PyQt5.QtGui import QPixmap

class MainWindow(QMainWindow):

    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        editMenu = menubar.addMenu('Edit')
        self.resize(500, 500)

        openAction = QAction('Open Image', self)  
        openAction.triggered.connect(self.openImage) 
        fileMenu.addAction(openAction)

        closeAction = QAction('Exit', self)  
        closeAction.triggered.connect(self.close) 
        fileMenu.addAction(closeAction)
        self.label = QLabel()
        self.setCentralWidget(self.label)

    def openImage(self):
        imagePath, _ = QFileDialog.getOpenFileName()
        pixmap = QPixmap(imagePath)
        self.label.setPixmap(pixmap)
        self.resize(pixmap.size())
        self.adjustSize()

def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    return app.exec_()

if __name__ == '__main__':
    sys.exit(main()) 