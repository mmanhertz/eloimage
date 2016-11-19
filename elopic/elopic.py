import os
import sys
from PySide import QtGui

from ui import MainWindow


def run():
    app = QtGui.QApplication(sys.argv)
    main_win = MainWindow(
        "D:/Dropbox/Coding/pyside-tutorial/IMG_4812.jpg",
        "D:/Dropbox/Coding/pyside-tutorial/IMG_4816.jpg"
    )
    sys.exit(app.exec_())
