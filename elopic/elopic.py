from PySide.QtCore import QObject, Slot

from ui import MainWindow
from data import EloPicDB


class EloPic(QObject):

    def __init__(self):
        super(EloPic, self).__init__()
        self.ui = MainWindow(
            "D:/Dropbox/Coding/pyside-tutorial/IMG_4812.jpg",
            "D:/Dropbox/Coding/pyside-tutorial/IMG_4816.jpg",
        )
        self.data = EloPicDB()
        self.ui.directory_selected.connect(self.handle_directory_selection)

    def show(self):
        self.ui.show()

    @Slot(unicode)
    def handle_directory_selection(self, directory):
        self.ui.statusBar().showMessage('Selected Dir: ' + directory)
        self.data.load_from_disk(directory)
        left_image, right_image = self.data.get_random_images()
        self.ui.statusBar().showMessage('Left: {} | Right: {}'.format(left_image['path'], right_image['path']))
        self.ui.change_pictures(left_image['path'], right_image['path'])
