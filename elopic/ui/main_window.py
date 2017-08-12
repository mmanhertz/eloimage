from PySide import QtGui
from PySide.QtCore import Signal, Slot, QEvent, Qt

from central_widget import CentralWidget
from table_window import TableWindow
from elopic.utils import resource_path


class MainWindow(QtGui.QMainWindow):

    directory_selected = Signal(unicode)
    picture_chosen = Signal(unicode, unicode)  # winner, loser
    picture_deleted = Signal(unicode)
    export_top_x_selected = Signal(int)

    def __init__(self, left_image_path, right_image_path):
        super(MainWindow, self).__init__()
        self.left_path = ""  # left_image_path
        self.right_path = ""  # right_image_path
        self.central_widget = None
        self.init_ui()

    def init_ui(self):

        self.central_widget = CentralWidget(
            self.left_path,
            self.right_path,
            parent=self
        )
        self.setCentralWidget(self.central_widget)

        self.central_widget.left_chosen.connect(self._left_chosen)
        self.central_widget.left_deleted.connect(self._left_deleted)
        self.central_widget.right_chosen.connect(self._right_chosen)
        self.central_widget.right_deleted.connect(self._right_deleted)
        self.central_widget.installEventFilter(self)

        self.statusBar()

        self.menubar = self.menuBar()
        self.file_menu = self._init_filemenu()
        self.help_menu = self._init_help_menu()
        self.ranking = TableWindow([('', 0)], ('path', 'rating'))
        self.ranking.export_top_x_clicked.connect(self.handle_export_top_x)

        self.setGeometry(100, 100, 1600, 900)
        self.setWindowTitle('EloPic')

    def eventFilter(self, widget, event):
        if event.type() == QEvent.KeyPress and widget is self.central_widget:
            key = event.key()
            if key == Qt.Key_A:
                self._left_chosen()
            elif key == Qt.Key_D:
                self._right_chosen()
            return True
        return QtGui.QMainWindow.eventFilter(self, widget, event)

    def _init_filemenu(self):
        exit_action = QtGui.QAction(
            QtGui.QIcon(resource_path('icons/exit.png')),
            '&Exit',
            self,
            shortcut='Ctrl+Q',
            statusTip='Exit Elopic',
            triggered=self.close,
        )
        select_dir_action = QtGui.QAction(
            QtGui.QIcon(resource_path('icons/folder.png')),
            '&Open...',
            self,
            shortcut='Ctrl+D',
            statusTip='Select a directory',
            triggered=self._select_dir,
        )
        show_list_action = QtGui.QAction(
            QtGui.QIcon(resource_path('icons/ranking.png')),
            '&Ranking...',
            self,
            shortcut='Ctrl+R',
            statusTip='Show Ranking',
            triggered=self._show_ranking,
        )

        file_menu = self.menubar.addMenu('&File')
        file_menu.addAction(exit_action)
        file_menu.addAction(select_dir_action)
        file_menu.addAction(show_list_action)
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

    def _show_ranking(self):
        self.ranking.show()

    @Slot()
    def _left_chosen(self):
        self.statusBar().showMessage('Left picture was chosen')
        self.picture_chosen.emit(self.left_path, self.right_path)

    @Slot()
    def _left_deleted(self):
        self.picture_deleted.emit(self.left_path)

    @Slot()
    def _right_chosen(self):
        self.statusBar().showMessage('Right picture was chosen')
        self.picture_chosen.emit(self.right_path, self.left_path)

    @Slot()
    def _right_deleted(self):
        self.picture_deleted.emit(self.right_path)

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

    @Slot()
    def handle_rating_updated(self, new_ratings):
        self.ranking.update(new_ratings)

    @Slot(int)
    def handle_export_top_x(self, x):
        self.statusBar().showMessage('Exporting Top {}'.format(x))
        self.export_top_x_selected.emit(x)



