#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import socket
import json

from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import *

_APP_DIR_ = '/.config/ai-doll/'
_MODELS_DIR_ = 'models/'
_MODEL_FILE_ = 'model'
_SETTINGS_FILE_ = 'settings.json'

class Body(QWidget):
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.image = QImage(self.root.settings['model']['body'])
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)

        mask = QPixmap(self.image)
        self.setFixedSize(mask.width(), mask.height())
        self.setMask(mask.mask())

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(0, 0, self.image)

    def positionBox(self):
        for box in self.root.mbs:
            box.moveFromBase(self)

    def showAnimation(self):
        for box in self.root.mbs:
            box.show()
        self.positionBox()
        self.setWindowOpacity(0.0)
        self.show()
        anime = QPropertyAnimation(self)
        anime.setTargetObject(self)
        anime.setPropertyName(b"windowOpacity")
        anime.setDuration(200)
        anime.setStartValue(0.0)
        anime.setEndValue(1.0)
        anime.start()

    def hideAnimation(self):
        self.setWindowOpacity(0.0)
        anime = QPropertyAnimation(self)
        anime.setTargetObject(self)
        anime.setPropertyName(b"windowOpacity")
        anime.setDuration(200)
        anime.setStartValue(1.0)
        anime.setEndValue(0.0)
        anime.finished.connect(self.hide)
        anime.start()

    def mousePressEvent(self, event):
        self.offset = event.pos()
        if event.button() == Qt.RightButton:
            self.root.toggle()

    def mouseMoveEvent(self, event):
        x=event.globalX()
        y=event.globalY()
        x_w = self.offset.x()
        y_w = self.offset.y()
        self.move(x-x_w, y-y_w)
        self.positionBox()

class Badge(QWidget):
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.image = QImage(self.root.settings['model']['badge'])
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)

        mask = QPixmap(self.image)
        self.setFixedSize(mask.width(), mask.height())
        self.setMask(mask.mask())

        g = QDesktopWidget().screenGeometry(-1)
        self.move(g.right() - self.width()*1.25, g.bottom() - self.height()*1.25)

    def positionBox(self):
        for box in self.root.mbs:
            box.moveFromBase(self)

    def showAnimation(self):
        self.positionBox()
        for box in self.root.mbs:
            if box.cnt > 0:
                box.hide()
        self.setWindowOpacity(0.0)
        self.show()
        anime = QPropertyAnimation(self)
        anime.setTargetObject(self)
        anime.setPropertyName(b"windowOpacity")
        anime.setDuration(200)
        anime.setStartValue(0.0)
        anime.setEndValue(1.0)
        anime.start()

    def hideAnimation(self):
        self.setWindowOpacity(0.0)
        anime = QPropertyAnimation(self)
        anime.setTargetObject(self)
        anime.setPropertyName(b"windowOpacity")
        anime.setDuration(200)
        anime.setStartValue(1.0)
        anime.setEndValue(0.0)
        anime.finished.connect(self.hide)
        anime.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(0, 0, self.image)

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.root.toggle()

class MessageBox(QWidget):
    def __init__(self, font, parent=None, fixed=False, fid=None):
        super(MessageBox, self).__init__()
        self.label = QLabel(self)
        self.label.setFont(font)
        self.cnt = 0
        self.parent = parent
        self.fid = fid
        self.fixed = fixed
        self.closed = False
        self.anime = QPropertyAnimation(self)
        self.anime2 = QPropertyAnimation(self)
        self.timer = QTimer(self)
        self.initUI()

    def initUI(self):
        self.resize(0,64)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
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

    def moveByCount(self, track):
        self.anime2.setTargetObject(self)
        self.anime2.setPropertyName(b"pos")
        self.anime2.setDuration(200)
        sx = self.pos().x()
        sy = self.pos().y()
        self.anime2.setStartValue(QPoint(sx,sy))
        self.anime2.setEndValue(QPoint(sx,track.pos().y()+self.cnt*72))
        self.anime2.start()
        if self.fixed:
            self.setWindowOpacity(1.0)
        else:
            self.setWindowOpacity(1.0 - self.cnt*0.2)

    def inc(self):
        if not self.fixed:
            self.cnt+=1

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
        self.parent.boxCloseEvent()

    def showMessage(self, track, message):
        self.show()
        self.label.setText(message)
        lw = self.label.fontMetrics().boundingRect(message).width()
        self.move(track.pos().x()-lw-48, track.pos().y())
        self.showAnimation()
        if self.fixed == False:
            self.timer.singleShot(9000, self.hideAnimation)

    def updateMessage(self, track, message):
        if self.label.text() == message:
            return
        self.setFixedSize(0, 64)
        self.label.setText(message)
        lw = self.label.fontMetrics().boundingRect(message).width()
        self.move(track.pos().x()-lw-48, track.pos().y())

    def moveFromBase(self, track):
        self.anime2.stop()
        lw = self.label.fontMetrics().boundingRect(self.label.text()).width()
        self.move(track.pos().x()-lw-48, track.pos().y()+self.cnt*72)

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
        if self.settings['init_style'] == 'body':
            self.isBadge = False
        elif self.setings['init_style'] == 'badge':
            self.isBadge = True
        else:
            print('Settings parse error: use body or badge for init_style')
            QApplication.exit(-1)
        self.isBadge = False
        self.initialize()

    def initialize(self):
        self.socket = QUdpSocket(self)
        self.socket.bind(QHostAddress.LocalHost, self.settings['port'])
        self.socket.readyRead.connect(self.receive)
        self.mbs = []
        self.body = Body(self)
        self.badge = Badge(self)
        self.mtimer = QTimer(self)
        self.mtimer.setInterval(1000)
        self.mtimer.setSingleShot(False)
        self.mtimer.timeout.connect(self.closeBox)
        self.mtimer.start()
        if self.isBadge:
            self.badge.show()
        else:
            self.body.show()

    def toggle(self):
        if self.isBadge:
            self.isBadge = False
            self.badge.hideAnimation()
            self.body.showAnimation()
        else:
            self.isBadge = True
            self.body.hideAnimation()
            self.badge.showAnimation()

    def boxCloseEvent(self):
        self.closeBox()
        self.sortByFixed()
        if self.isBadge:
            if len(self.mbs) > 0:
                self.mbs[0].show()
                self.mbs[0].moveByCount(self.badge)
                for i in range(1,len(self.mbs)):
                    self.mbs[i].hide()
        else:
            for box in self.mbs:
                box.moveByCount(self.body)

    def sortByFixed(self):
        fixed = (list(filter((lambda b: b.fixed == True), self.mbs)))
        nonFixed = (list(filter((lambda b: b.fixed == False), self.mbs)))
        fixed.extend(nonFixed)
        self.mbs = fixed
        for i in range(len(self.mbs)):
            self.mbs[i].cnt = i

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
        req = json.loads(message)
        if req['type'] == 'kill':
            QApplication.exit(0)
        elif req['type'] == 'update':
            for box in self.mbs:
                if box.fid == req['id']:
                    if self.isBadge:
                        box.updateMessage(self.badge, req['data'])
                    else:
                        box.updateMessage(self.body, req['data'])
                    break
        else:
            if req['type'] == 'message':
                fixed = False
                fid = None
            elif req['type'] == 'fixed':
                fixed = True
                fid = req['id']
            msgbox = MessageBox(self.font, self, fixed, fid)
            for box in self.mbs:
                box.inc()
            self.closeBox()
            self.mbs.insert(0, msgbox)
            self.sortByFixed()
            if self.isBadge:
                for box in self.mbs:
                    box.hide()
                msgbox.showMessage(self.badge, req['data'])
            else:
                msgbox.showMessage(self.body, req['data'])
                for box in self.mbs:
                    box.moveByCount(self.body)

    def __del__(self):
        self.socket.close()

def model_load(path):
    f = open(path + _MODEL_FILE_, 'r')
    data = json.loads(f.read())
    if data['type'] == 'image':
        data['body'] = path + data['body']
        data['badge'] = path + data['badge']
        return data
    elif data['type'] == 'live2d':
        print('Model type error: live2d is not implemented!')
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
    trayIcon = QSystemTrayIcon(QIcon(QPixmap(settings['model']['badge'])), app)
    menu = QMenu()
    exitAction = menu.addAction('Exit')
    exitAction.triggered.connect(app.exit)
    trayIcon.setContextMenu(menu)
    trayIcon.show()

    receiver = UdpReceiver(settings)
    sys.exit(app.exec_())
