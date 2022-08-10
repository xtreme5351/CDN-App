import sys
from PyQt5.QtWidgets import *
from app import CDNApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CDNApp()
    sys.exit(app.exec_())

