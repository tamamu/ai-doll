import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QLabel, QApplication)
from PyQt5.QtCore import (Qt, QSize)
from PyQt5.QtGui import (QPixmap, QPainter)

class Body(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.show()

        hbox = QHBoxLayout(self)
        pixmap = QPixmap("rem1.png")
        self.setMask(pixmap.mask())
        lbl = QLabel(self)
        lbl.setPixmap(pixmap)

        hbox.addWidget(lbl)
        self.setLayout(hbox)

    def mousePressEvent(self, event):
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        x=event.globalX()
        y=event.globalY()
        x_w = self.offset.x()
        y_w = self.offset.y()
        self.move(x-x_w, y-y_w)

class MessageBox(QWidget):
    def __init__(self, parent=None):
        super(MessageBox, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 400, 240)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.black)
        painter.setBrush(Qt.white)
        painter.drawRect(20, 20, 380, 220)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    body = Body()
    sys.exit(app.exec_())
