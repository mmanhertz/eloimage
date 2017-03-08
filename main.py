if __name__ == '__main__':

    import sys
    from PySide import QtGui
    from elopic.elopic import EloPic

    app = QtGui.QApplication(sys.argv)
    main = EloPic()
    main.show()
    sys.exit(app.exec_())