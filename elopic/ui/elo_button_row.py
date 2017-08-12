from PySide import QtGui
from PySide.QtCore import Signal

from elopic.utils import resource_path


class EloButtonRow(QtGui.QWidget):

    DEL_ICON = resource_path('icons/delete.png')
    CHECK_ICON = resource_path('icons/check.png')

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
        self._init_signals()

    def _init_ui(self):

        hbox = QtGui.QHBoxLayout(self)

        self._btn_del_left = self._init_button(
            layout=hbox,
            icon_path=self.DEL_ICON,
            tooltip_text='Delete Left Picture'
        )
        hbox.addStretch(1)

        self._btn_left = self._init_button(
            layout=hbox,
            icon_path=self.CHECK_ICON,
            tooltip_text='Choose Left Picture'
        )
        self._btn_right = self._init_button(
            layout=hbox,
            icon_path=self.CHECK_ICON,
            tooltip_text='Choose Right Picture'
        )

        hbox.addStretch(1)
        self._btn_del_right = self._init_button(
            layout=hbox,
            icon_path=self.DEL_ICON,
            tooltip_text='Delete Right Picture'
        )

        self.setLayout(hbox)

    def _init_signals(self):
        self._btn_del_left.clicked.connect(self.left_deleted)
        self._btn_left.clicked.connect(self.left_chosen)
        self._btn_right.clicked.connect(self.right_chosen)
        self._btn_del_right.clicked.connect(self.right_deleted)

    def _init_button(self, layout, icon_path, tooltip_text):
        button = QtGui.QPushButton('', self)
        button.setToolTip(tooltip_text)
        button.setIcon(QtGui.QIcon(icon_path))
        layout.addWidget(button)
        return button
