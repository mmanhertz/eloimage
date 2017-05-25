from PySide import QtGui
from PySide.QtCore import Signal
from elo_button_row import EloButtonRow
from picture_area import PictureArea


class CentralWidget(QtGui.QWidget):

    left_chosen = Signal()
    right_chosen = Signal()
    left_deleted = Signal()
    right_deleted = Signal()

    def __init__(self, left_image_path, right_image_path, parent=None):

        super(CentralWidget, self).__init__(parent=parent)
        self._init_ui(left_image_path, right_image_path)
        self._init_signals()

    def _init_ui(self, left_image_path, right_image_path):

        vbox = QtGui.QVBoxLayout(self)

        self.pic_area = PictureArea(
            left_image_path,
            right_image_path,
            parent=self
        )
        self.buttons = EloButtonRow(parent=self)

        vbox.addWidget(self.pic_area, stretch=100)
        vbox.addWidget(self.buttons, stretch=1)
        self.setLayout(vbox)

    def _init_signals(self):
        self.buttons.left_deleted.connect(self.left_deleted)
        self.buttons.left_chosen.connect(self.left_chosen)
        self.buttons.right_chosen.connect(self.right_chosen)
        self.buttons.right_deleted.connect(self.right_deleted)

    def change_pictures(self, left_image_path, right_image_path):
        self.pic_area.change_pictures(left_image_path, right_image_path)
