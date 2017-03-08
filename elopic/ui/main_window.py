from PySide import QtGui
from PySide.QtCore import Signal

from picture_area import PictureArea
from elo_button_row import EloButtonRow


class MainWindow(QtGui.QMainWindow):

    directory_selected = Signal(unicode)

    def __init__(self, left_image_path, right_image_path):
        super(MainWindow, self).__init__()
        self.left_path = left_image_path
        self.right_path = right_image_path
        self.pic_area = None
        self.init_ui()

    def init_ui(self):

        self.pic_area = CentralWidget(self.left_path, self.right_path, parent=self)
        self.setCentralWidget(self.pic_area)

        self.statusBar()

        self.menubar = self.menuBar()
        self.file_menu = self._init_filemenu()
        self.help_menu = self._init_help_menu()

        self.setGeometry(100, 100, 1600, 900)
        self.setWindowTitle('EloPic')

    def _init_filemenu(self):
        exit_action = QtGui.QAction(
            QtGui.QIcon('elopic/ui/icons/exit.png'),
            '&Exit',
            self,
            shortcut='Ctrl+Q',
            statusTip='Exit Elopic',
            triggered=self.close,
        )
        select_dir_action = QtGui.QAction(
            QtGui.QIcon('elopic/ui/icons/folder.png'),
            '&Open...',
            self,
            shortcut='Ctrl+D',
            statusTip='Select a directory',
            triggered=self._select_dir,
        )

        file_menu = self.menubar.addMenu('&File')
        file_menu.addAction(exit_action)
        file_menu.addAction(select_dir_action)
        return file_menu

    def _init_help_menu(self):
        about_action = QtGui.QAction(
            '&About',
            self,
            triggered=self._about_dialog,
        )

        about_menu = self.menubar.addMenu('&Help')
        about_menu.addAction(about_action)
        return about_menu

    def _select_dir(self):
        dialog = QtGui.QFileDialog()
        dialog.setFileMode(QtGui.QFileDialog.Directory)
        dialog.setOption(QtGui.QFileDialog.ShowDirsOnly)
        if dialog.exec_():
            selected_dir = dialog.selectedFiles()
        self.directory_selected.emit(selected_dir[0])

    def _about_dialog(self):
        QtGui.QMessageBox.information(
            self,
            'About Elopic',
            'Elopic by Matthias Manhertz\nIcons by https://icons8.com/',
        )

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
