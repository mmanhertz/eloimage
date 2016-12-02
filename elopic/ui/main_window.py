from PySide import QtGui

from picture_area import PictureArea
from elo_button_row import EloButtonRow


class MainWindow(QtGui.QMainWindow):
    def __init__(self, left_image_path, right_image_path):
        super(MainWindow, self).__init__()
        self.left_path = left_image_path
        self.right_path = right_image_path
        self.pic_area = None
        self.init_ui()

    def init_ui(self):

        self.pic_area = CentralWidget(self.left_path, self.right_path, parent=self)
        self.setCentralWidget(self.pic_area)

        # btn1 = QtGui.QPushButton("Button 1", self)
        # btn1.clicked.connect(self.button_clicked)

        self.statusBar()

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('EloPic')
        self.show()

    def button_clicked(self):
        sender = self.sender()
        self.statusBar().showMessage(sender.text() + ' was pressed')
        self.pic_area.set_pictures(self.right_path, self.left_path)


class CentralWidget(QtGui.QWidget):
    def __init__(self, left_image_path, right_image_path, parent=None):

        super(CentralWidget, self).__init__(parent=parent)
        self.init_ui(left_image_path, right_image_path)

    def init_ui(self, left_image_path, right_image_path):

        vbox = QtGui.QVBoxLayout(self)

        self.pic_area = PictureArea(left_image_path, right_image_path, parent=self)
        self.buttons = EloButtonRow(parent=self)

        vbox.addWidget(self.pic_area, stretch=100)
        vbox.addWidget(self.buttons, stretch=1)
        self.setLayout(vbox)
