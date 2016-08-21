import sys
import socket
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QLabel, QApplication, QGridLayout, QSizePolicy)
from PyQt5.QtCore import (Qt, QSize, QRect, QPoint, QPointF, QPropertyAnimation, QTimer, QByteArray)
from PyQt5.QtGui import (QPixmap, QPainter, QPen, QBrush, QPolygonF, QPolygon)
from PyQt5.QtNetwork import (QUdpSocket, QHostAddress)


class Body(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.mesbox = MessageBox(self)
        self.mesbox.moveFromBase(self.mapFromGlobal(QPoint(0,0)))
        self.socket = QUdpSocket(self)
        self.socket.bind(QHostAddress.LocalHost, 1234)
        self.socket.readyRead.connect(self.receive)
        self.old_node = '0'

    def receive(self):
        while(self.socket.hasPendingDatagrams()):
            datagram = QByteArray()
            size = self.socket.pendingDatagramSize()
            data,addr,port = self.socket.readDatagram(size)
            message = data.strip().decode("utf-8")
            self.mesbox.showMessage(message)

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.show()

        hbox = QHBoxLayout(self)
        pixmap = QPixmap("rem0.png")
        #self.setMask(pixmap.mask())
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
        self.mesbox.moveFromBase(QPoint(x-x_w, y-y_w))

class MessageBox(QWidget):
    def __init__(self, track=None):
        super(MessageBox, self).__init__()
        self.track = track
        self.label = QLabel(self)
        self.anime = QPropertyAnimation(self)
        self.timer = QTimer(self)
        self.initUI()

    def initUI(self):
        self.setFixedSize(200,100)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.anime.setTargetObject(self)
        self.anime.setPropertyName(b"windowOpacity")
        self.anime.setDuration(150)

        layout = QGridLayout(self)
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.setWindowOpacity(0.0)
        self.show()

    def showAnimation(self):
        self.anime.setStartValue(0.0)
        self.anime.setEndValue(1.0)
        self.anime.start()

    def hideAnimation(self):
        self.anime.setStartValue(1.0)
        self.anime.setEndValue(0.0)
        self.anime.start()

    def showMessage(self, message):
        self.label.setText(message)
        self.showAnimation()
        self.timer.singleShot(3000, self.hideAnimation)

    def moveFromBase(self, point):
        self.move(point.x()-self.rect().width(), point.y()+self.rect().height())

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = QRect()
        rect.setX(self.rect().x()+5)
        rect.setY(self.rect().y()+5)
        rect.setWidth(self.rect().width()-10)
        rect.setHeight(self.rect().height()-10)
        painter.setBrush(Qt.white)
        pen = QPen()
        pen.setColor(Qt.black)
        pen.setWidth(3)
        painter.setPen(pen)
        painter.drawRoundedRect(rect, 15, 15)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(Qt.black))
        points = QPolygon([
                QPoint(rect.x(), rect.height()/2-5+3),
                QPoint(rect.x(), rect.height()/2+5+3),
                QPoint(rect.x() - 5, rect.height()/2+3)
        ])
        painter.drawPolygon(points, 3)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    body = Body()
    
    sys.exit(app.exec_())
