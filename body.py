import sys
import socket
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QLabel, QApplication, QGridLayout)
from PyQt5.QtCore import (Qt, QSize, QRect, QPoint, QPointF, QPropertyAnimation, QTimer)
from PyQt5.QtGui import (QPixmap, QPainter, QPen, QBrush, QPolygonF, QPolygon)
from PyQt5.QtNetwork import (QTcpServer, QHostAddress)


class Body(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.mesbox = MessageBox(self)
        self.mesbox.moveFromBase(self.mapFromGlobal(QPoint(0,0)))
        self.server = QLocalServer(self)
        self.server.listen(QHostAddress("127.0.0.1"), 8888)
        self.connect(self.server, SIGNAL("newConnection()"), self.newConection)
        self.connections = []

    def newConnection(self):
        client = self.server.nextPendingConnection()
        client.nextBlockSize = 0
        self.connections.append(client)

        self.connect(client, SIGNAL("readyRead()"), self.receiveMessage)
        self.connect(client, SIGNAL("disconnected()"), self.removeConnection)
        self.connect(client, SIGNAL("error()"), self.socketError)

    def receiveMessage(self):



    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
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
        self.mesbox.moveFromBase(QPoint(x-x_w, y-y_w))

class MessageBox(QWidget):
    def __init__(self, track=None):
        super(MessageBox, self).__init__()
        self.track = track
        self.label = QLabel(self)
        self.anime = QPropertyAnimation(self)
        self.timer = QTimer(self)
        self.initUI()
        self.showMessage("あいうえお")

    def initUI(self):
        self.resize(200,100)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.anime.setTargetObject(self)
        self.anime.setPropertyName(b"windowOpacity")
        self.anime.setDuration(150)

        layout = QGridLayout(self)
        self.label.setText("Hogehoge")
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.setWindowOpacity(0.0)
        self.showAnimation()
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
        self.timer.singleShot(6000, self.hideAnimation)

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
