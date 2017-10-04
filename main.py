# -*- coding: utf-8 -*-
# ----------------------------
# 作者：朱旭晖
# 时间：2017.8.16
# ----------------------------
import sys
from PyQt5.QtWidgets import *
from windows import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())
