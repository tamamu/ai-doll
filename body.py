import os
import sys
import socket
import json
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QLabel, QApplication, QGridLayout, QSizePolicy, QSystemTrayIcon, QMenu)
from PyQt5.QtCore import (Qt, QSize, QRect, QPoint, QPointF, QPropertyAnimation, QTimer, QByteArray, QObject)
from PyQt5.QtGui import (QPixmap, QPainter, QPen, QBrush, QPolygonF, QPolygon, QFont, QIcon)
from PyQt5.QtNetwork import (QUdpSocket, QHostAddress)

_APP_DIR_ = '/.config/ai-doll/'
_MODELS_DIR_ = 'models/'
_MODEL_FILE_ = 'model'
_SETTINGS_FILE_ = 'settings.json'

class Body(QWidget):
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.initUI(self.root.settings['model']['body'])

    def initUI(self, image):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.show()

        hbox = QHBoxLayout(self)
        pixmap = QPixmap(image)
        #self.setMask(pixmap.mask())
        lbl = QLabel(self)
        lbl.setPixmap(pixmap)

        hbox.addWidget(lbl)
        self.setLayout(hbox)

    def positionBox(self):
        for box in self.root.mbs:
            box.moveFromBase(self)

    def mousePressEvent(self, event):
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        x=event.globalX()
        y=event.globalY()
        x_w = self.offset.x()
        y_w = self.offset.y()
        self.move(x-x_w, y-y_w)
        self.positionBox()

class MessageBox(QWidget):
    def __init__(self, font):
        super(MessageBox, self).__init__()
        self.label = QLabel(self)
        self.label.setFont(font)
        self.cnt = 0
        self.closed = False
        self.anime = QPropertyAnimation(self)
        self.anime2 = QPropertyAnimation(self)
        self.timer = QTimer(self)
        self.initUI()

    def initUI(self):
        self.resize(0,64)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setAttribute(Qt.WA_ShowWithoutActivating)

        self.anime.setTargetObject(self)
        self.anime.setPropertyName(b"windowOpacity")
        self.anime.setDuration(150)

        layout = QGridLayout(self)
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.setWindowOpacity(0.0)

    def moveDown(self):
        self.cnt += 1
        self.anime2.setTargetObject(self)
        self.anime2.setPropertyName(b"pos")
        self.anime2.setDuration(200)
        sx = self.pos().x()
        sy = self.pos().y()
        self.anime2.setStartValue(QPoint(sx,sy))
        self.anime2.setEndValue(QPoint(sx,sy+72))
        self.anime2.start()
        self.setWindowOpacity(1.0 - self.cnt*0.2)

    def mousePressEvent(self, event):
        self.anime.stop()
        self.anime2.stop()
        self.setWindowOpacity(0.0)
        self.close()

    def showAnimation(self):
        self.anime.setStartValue(0.0)
        self.anime.setEndValue(1.0)
        self.anime.start()

    def hideAnimation(self):
        self.anime = QPropertyAnimation(self)
        self.anime.setTargetObject(self)
        self.anime.setPropertyName(b"windowOpacity")
        self.anime.setDuration(150)
        self.anime.setStartValue(self.windowOpacity())
        self.anime.setEndValue(0.0)
        self.anime.finished.connect(self.close)
        self.anime.start()

    def close(self):
        self.closed = True

    def showMessage(self, track, message):
        self.show()
        self.label.setText(message)
        lw = self.label.fontMetrics().boundingRect(message).width()
        self.move(track.pos().x()-lw-24, track.pos().y()+100)
        self.showAnimation()
        self.timer.singleShot(9000, self.hideAnimation)

    def moveFromBase(self, track):
        self.anime2.stop()
        lw = self.label.fontMetrics().boundingRect(self.label.text()).width()
        self.move(track.pos().x()-lw-24, track.pos().y()+100+self.cnt*72)

    def enterEvent(self, event):
        self.repaint()

    def leaveEvent(self, event):
        self.repaint()

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = QRect()
        rect.setX(self.rect().x()+5)
        rect.setY(self.rect().y()+5)
        rect.setWidth(self.rect().width()-10)
        rect.setHeight(self.rect().height()-10)
        painter.setBrush(Qt.white)
        pen = QPen()
        if self.underMouse():
            pen.setColor(Qt.gray)
        else:
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

class UdpReceiver(QObject):
    def __init__(self, settings):
        QObject.__init__(self)
        self.settings = settings
        self.font = QFont(self.settings['font'], 16)
        self.initialize()

    def initialize(self):
        self.socket = QUdpSocket(self)
        self.socket.bind(QHostAddress.LocalHost, self.settings['port'])
        self.socket.readyRead.connect(self.receive)
        self.mbs = []
        self.body = Body(self)
        self.mtimer = QTimer(self)
        self.mtimer.setInterval(1000)
        self.mtimer.setSingleShot(False)
        self.mtimer.timeout.connect(self.closeBox)
        self.mtimer.start()

    def closeBox(self):
        for box in self.mbs:
            if box.closed:
                box.deleteLater()
        self.mbs = (list(filter((lambda b: b.closed == False), self.mbs)))

    def receive(self):
        while(self.socket.hasPendingDatagrams()):
            datagram = QByteArray()
            size = self.socket.pendingDatagramSize()
            data,addr,port = self.socket.readDatagram(size)
            message = data.strip().decode("utf-8")
            self.parse(message)

    def parse(self, message):
        if message == 'kill':
            QApplication.exit(0)
        else:
            print(message)
            msgbox = MessageBox(self.font)
            msgbox.showMessage(self.body, message)
            self.closeBox()
            for box in self.mbs:
                box.moveDown()
            self.mbs = (list(filter((lambda b: b.closed == False), self.mbs)))
            self.mbs.append(msgbox)

    def __del__(self):
        self.socket.close()

def model_load(path):
    f = open(path + _MODEL_FILE_, 'r')
    data = json.loads(f.read())
    if data['type'] == 'image':
        data['body'] = path + data['body']
        data['face'] = path + data['face']
        return data
    elif data['type'] == 'live2d':
        print('Not implemented!')
        sys.exit(-1)
    else:
        print('Model type error: use image or live2d')
        sys.exit(-1)

if __name__ == '__main__':

    # Load settings
    app_dir = os.environ.get('HOME') + _APP_DIR_
    if os.path.exists(app_dir + _SETTINGS_FILE_):
        settings_file = open(app_dir + _SETTINGS_FILE_, 'r')
    else:
        settings_file = open(_SETTINGS_FILE_, 'r')
    settings = json.loads(settings_file.read())

    # Load model
    if os.path.exists(app_dir + _MODELS_DIR_ + settings['model'] + '/'):
        settings['model'] = model_load(app_dir + _MODELS_DIR_ + settings['model'] + '/')
    elif os.path.exists(_MODELS_DIR_ + settings['model'] + '/'):
        settings['model'] = model_load(_MODELS_DIR_ + settings['model'] + '/')
    else:
        print('Model not found:', settings['model'])
        sys.exit(-1)

    app = QApplication(sys.argv)
    trayIcon = QSystemTrayIcon(QIcon(QPixmap(settings['model']['face'])), app)
    menu = QMenu()
    exitAction = menu.addAction('Exit')
    exitAction.triggered.connect(app.exit)
    trayIcon.setContextMenu(menu)
    trayIcon.show()

    receiver = UdpReceiver(settings)
    sys.exit(app.exec_())
