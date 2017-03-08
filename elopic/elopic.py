from PySide.QtCore import QObject, Slot

from ui import MainWindow


class EloPic(QObject):

    def __init__(self):
        super(EloPic, self).__init__()
        self.ui = MainWindow(
            "D:/Dropbox/Coding/pyside-tutorial/IMG_4812.jpg",
            "D:/Dropbox/Coding/pyside-tutorial/IMG_4816.jpg"
        )

        self.ui.directory_selected.connect(self.handle_directory_selection)

    def show(self):
        self.ui.show()

    @Slot(unicode)
    def handle_directory_selection(self, directory):
        self.ui.statusBar().showMessage('Selected Dir: ' + directory)
