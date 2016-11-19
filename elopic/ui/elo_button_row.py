from PySide import QtGui
from PySide.QtCore import Signal


class EloButtonRow(QtGui.QWidget):

    left_chosen = Signal()
    right_chosen = Signal()
    left_deleted = Signal()
    right_deleted = Signal()

    def __init__(self, parent):

        super(EloButtonRow, self).__init__(parent=parent)

        self._btn_left = None
        self._btn_right = None
        self._btn_del_left = None
        self._btn_del_right = None

        self._init_ui()

    def _init_ui(self):

        hbox = QtGui.QHBoxLayout(self)

        self._btn_del_left = self._init_button(hbox, 'icons/delete.png', self.left_deleted)
        hbox.addStretch(1)
        self._btn_left = self._init_button(hbox, 'icons/check.png', self.left_chosen)
        self._btn_right = self._init_button(hbox, 'icons/check.png', self.right_chosen)
        hbox.addStretch(1)
        self._btn_del_right = self._init_button(hbox, 'icons/delete.png', self.right_deleted)

        self.setLayout(hbox)

    def _init_button(self, layout, icon_path, signal):
        button = QtGui.QPushButton('', self)
        button.clicked.connect(signal.emit)
        button.setIcon(QtGui.QIcon(icon_path))
        layout.addWidget(button)
        return button
