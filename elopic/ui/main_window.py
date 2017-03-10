from PySide import QtGui
from PySide.QtCore import Signal, Slot

from central_widget import CentralWidget

LEFT = 0
RIGHT = 1


class MainWindow(QtGui.QMainWindow):

    directory_selected = Signal(unicode)
    picture_chosen = Signal(int)
    picture_deleted = Signal(int)

    def __init__(self, left_image_path, right_image_path):
        super(MainWindow, self).__init__()
        self.left_path = left_image_path
        self.right_path = right_image_path
        self.central_widget = None
        self.init_ui()

    def init_ui(self):

        self.central_widget = CentralWidget(self.left_path, self.right_path, parent=self)
        self.setCentralWidget(self.central_widget)

        self.central_widget.left_chosen.connect(self._left_chosen)
        self.central_widget.left_deleted.connect(self._left_deleted)
        self.central_widget.right_chosen.connect(self._right_chosen)
        self.central_widget.right_deleted.connect(self._right_deleted)

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

    @Slot()
    def _left_chosen(self):
        self.picture_chosen.emit(LEFT)

    @Slot()
    def _left_deleted(self):
        self.picture_deleted.emit(LEFT)

    @Slot()
    def _right_chosen(self):
        self.picture_chosen.emit(RIGHT)

    @Slot()
    def _right_deleted(self):
        self.picture_deleted.emit(RIGHT)

    def _about_dialog(self):
        QtGui.QMessageBox.information(
            self,
            'About Elopic',
            'Elopic by Matthias Manhertz\nIcons by https://icons8.com/',
        )

    @Slot()
    def button_clicked(self):
        sender = self.sender()
        self.statusBar().showMessage(sender.toolTip() + ' was pressed')
        self.change_pictures(self.right_path, self.left_path)

    def change_pictures(self, left_image_path, right_image_path):
        self.left_path = left_image_path
        self.right_path = right_image_path
        self.central_widget.change_pictures(left_image_path, right_image_path)


