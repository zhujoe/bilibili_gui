# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\bilibili.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

import sys
import webbrowser
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from bili import *


class workTread(QThread):
    trigger = pyqtSignal(list)

    def __init__(self):
        super(workTread, self).__init__()
        self.lists = []

    def run(self):
        self.lists = get_bili()
        self.trigger.emit(self.lists)


class Ui_MainWindow(QWidget):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.lists = []
        self.listItem = []
        self.del_item = None
        print('路过__init__')
        self.setupUi()

    def setupUi(self):
        # self.setObjectName("window")
        self.resize(392, 810)
        self.setWindowTitle("小工具")
        self.central()
        self.build_tray()

        # 窗口样式设置
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.verticalLayoutWidget = QWidget(self)
        self.verticalLayoutWidget.setGeometry(QRect(15, 22, 362, 764))
        # self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")

        # 垂直布局
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        # self.verticalLayout.setObjectName("verticalLayout")

        # 标签
        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setTextFormat(Qt.AutoText)
        self.label.setAlignment(Qt.AlignCenter)
        # self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label.setText( "…… bili一下 ……")
        self.label.setFont(QFont("微软雅黑", 14, QFont.Bold))

        # 列表
        self.listWidget = QListWidget(self.verticalLayoutWidget)
        # self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        # 打开排序开关
        # self.listWidget.setSortingEnabled(True)
        # 设置为图标模式（默认应该是列表模式）
        self.listWidget.setViewMode(QListView.IconMode)
        # Listview显示状态不可拖动
        self.listWidget.setMovement(QListView.Static)
        # 设置图标的大小和间距
        self.listWidget.setIconSize(QSize(160, 220))
        # self.listWidget.setIconSize(QSize(320, 440))
        self.setlistwidget()

        # 按钮
        self.pushbotton = QPushButton(self.verticalLayoutWidget)
        # self.pushbotton.setObjectName("btm")
        self.pushbotton.setGeometry(10, 4, 25, 25)
        self.pushbotton.setIcon(QIcon('logo.png'))
        self.pushbotton.setIconSize(QSize(25, 25))
        self.pushbotton.clicked.connect(self.on_btm_clicked)

        # 水平布局
        self.hLayout = QHBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.addLayout(self.hLayout)
        self.hLayout.setSpacing(20)

        self.pub1 = QPushButton(self.verticalLayoutWidget)
        self.hLayout.addWidget(self.pub1)
        self.pub1.clicked.connect(self.listdel)

        self.pub2 = QPushButton(self.verticalLayoutWidget)
        self.hLayout.addWidget(self.pub2)

        # 暂时不可知是否在pyqt中能够使用，所以注释掉了
        # 此函数应该是声明信号与槽相关
        # QMetaObject.connectSlotsByName(self)

    def setlistwidget(self):
        if self.lists:
            self.item = []
            self.ico = []
        else:
            return
        for i in range(0, 50):
            # self.item.append(self.lists[i]['name'][0:10])
            self.item.append(self.lists[i]['name'])
            self.ico.append('./img/' + str(i) + '.jpg')
        for i in range(len(self.item)):
            self.listItem.append(QListWidgetItem(QIcon(self.ico[i]), self.item[i]))
        # 添加进列表中
        for i in range(len(self.listItem)):
            self.listWidget.insertItem(i, self.listItem[i])
        # 相应点击事件
        self.listWidget.itemDoubleClicked.connect(self.clickitem)

    # 列表点击响应
    def clickitem(self, obj):
        print(obj.text())
        foundflg = 0
        num = 0
        for name in self.item:
            if name == obj.text():
                foundflg = 1
                break
            else:
                num += 1
        if foundflg:
            webbrowser.open(self.lists[num]['url'])
        else:
            print('未找到')

    def on_btm_clicked(self):
        self.label.setText('数据收集中……')
        QMessageBox.warning(self, "提示", '已经开始数据收集\n请勿重复点击更新按钮', QMessageBox.Yes)
        workTread.start()
        workTread.trigger.connect(self.getover)

    def getover(self, getlists):
        self.label.setText('…… bili一下 ……')
        self.lists = getlists
        self.setlistwidget()

    def listdel(self):
        count = self.listWidget.count()
        print(count)
        if count != 0:
            del self.listItem[:]
            for i in range(0, count):
                self.del_item = self.listWidget.takeItem(i)
                print(self.del_item)
                self.del_item = None

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = QMouseEvent.globalPos()-self.pos()
            QMouseEvent.accept()
            self.label.setText('你敢动我一下试试……')

    def mouseMoveEvent(self, QMouseEvent):
        if QMouseEvent.buttons() and Qt.LeftButton:
            self.move(QMouseEvent.globalPos()-self.m_DragPosition)
            QMouseEvent.accept()
            self.label.setText('…… 好吧，让你动 ……')

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag = False
        self.label.setText('…… bili一下 ……')

    def central(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(screen.width() - size.width(), 0)

    def build_tray(self):
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(QIcon('logo.png'))
        self.trayIcon.show()
        self.trayIcon.setToolTip('bili')
        self.trayIcon.activated.connect(self.trayClick)

        menu = QMenu()

        # 菜单选项
        normal = menu.addAction('显示到桌面')
        mini = menu.addAction('最小化到托盘')
        initxy = menu.addAction('回到右上角')
        offtop = menu.addAction('取消置顶')
        ontop = menu.addAction('置顶')
        exitA = menu.addAction('退出')

        # 事件
        normal.triggered.connect(self.showNormal)
        mini.triggered.connect(self.showMinimized)
        initxy.triggered.connect(self.showinitxy)
        offtop.triggered.connect(self.ushowtop)
        ontop.triggered.connect(self.showtop)
        exitA.triggered.connect(self.exit)

        self.trayIcon.setContextMenu(menu)

    def showinitxy(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        x = screen.width() - size.width()
        x1 = self.pos().x()
        y1 = self.pos().y()
        if x1 < x+1:
            for xy_x in range(x1, x+1, 2):
                self.move(xy_x, y1)
        else:
            for xy_x in range(x1, x+1, -2):
                self.move(xy_x, y1)
        if y1 > 1:
            for xy_y in range(y1, 1, -2):
                self.move(xy_x, xy_y)
        else:
            for xy_y in range(y1, 1, 2):
                self.move(xy_x, xy_y)

    def exit(self):
        self.trayIcon.setVisible(False)
        sys.exit(0)

    def showNormal(self):
        super(Ui_MainWindow, self).showNormal()
        self.repaint()

    def trayClick(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.showNormal()
            self.repaint()

    def showtop(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        super(Ui_MainWindow, self).showNormal()
        self.label.setText('…… 置顶 ……')

    def ushowtop(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        super(Ui_MainWindow, self).showNormal()
        self.label.setText('…… 取消置顶 ……')

    def drawShadow(self, painter):
        # 阴影宽度
        self.SHADOW_WIDTH = 15
        # 绘制左上角、左下角、右上角、右下角、上、下、左、右边框
        self.pixmaps = list()
        self.pixmaps.append(str("./img/shadow/left_top.png"))
        self.pixmaps.append(str("./img/shadow/left_bottom.png"))
        self.pixmaps.append(str("./img/shadow/right_top.png"))
        self.pixmaps.append(str("./img/shadow/right_bottom.png"))
        self.pixmaps.append(str("./img/shadow/top_mid.png"))
        self.pixmaps.append(str("./img/shadow/bottom_mid.png"))
        self.pixmaps.append(str("./img/shadow/left_mid.png"))
        self.pixmaps.append(str("./img/shadow/right_mid.png"))

        painter.drawPixmap(0, 0, self.SHADOW_WIDTH, self.SHADOW_WIDTH, QPixmap(self.pixmaps[0]))   #左上角
        painter.drawPixmap(self.width()-self.SHADOW_WIDTH, 0, self.SHADOW_WIDTH, self.SHADOW_WIDTH, QPixmap(self.pixmaps[2]))   #右上角
        painter.drawPixmap(0,self.height()-self.SHADOW_WIDTH, self.SHADOW_WIDTH, self.SHADOW_WIDTH, QPixmap(self.pixmaps[1]))   #左下角
        painter.drawPixmap(self.width()-self.SHADOW_WIDTH, self.height()-self.SHADOW_WIDTH, self.SHADOW_WIDTH, self.SHADOW_WIDTH, QPixmap(self.pixmaps[3]))  #右下角
        painter.drawPixmap(0, self.SHADOW_WIDTH, self.SHADOW_WIDTH, self.height()-2*self.SHADOW_WIDTH, QPixmap(self.pixmaps[6]).scaled(self.SHADOW_WIDTH, self.height()-2*self.SHADOW_WIDTH)) #左
        painter.drawPixmap(self.width()-self.SHADOW_WIDTH, self.SHADOW_WIDTH, self.SHADOW_WIDTH, self.height()-2*self.SHADOW_WIDTH, QPixmap(self.pixmaps[7]).scaled(self.SHADOW_WIDTH, self.height()- 2*self.SHADOW_WIDTH)) #右
        painter.drawPixmap(self.SHADOW_WIDTH, 0, self.width()-2*self.SHADOW_WIDTH, self.SHADOW_WIDTH, QPixmap(self.pixmaps[4]).scaled(self.width()-2*self.SHADOW_WIDTH, self.SHADOW_WIDTH)) #上
        painter.drawPixmap(self.SHADOW_WIDTH, self.height()-self.SHADOW_WIDTH, self.width()-2*self.SHADOW_WIDTH, self.SHADOW_WIDTH, QPixmap(self.pixmaps[5]).scaled(self.width()-2*self.SHADOW_WIDTH, self.SHADOW_WIDTH))   #下

    def paintEvent(self, event):
        painter = QPainter(self)
        self.drawShadow(painter)
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.white)
        painter.drawRect(QRect(self.SHADOW_WIDTH, self.SHADOW_WIDTH, self.width()-2*self.SHADOW_WIDTH, self.height()-2*self.SHADOW_WIDTH))

workTread = workTread()
