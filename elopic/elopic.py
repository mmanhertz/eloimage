from PySide.QtCore import QObject, Slot

from ui import MainWindow
from data import EloPicDB

LEFT = 0
RIGHT = 1
BOTH = 2


class EloPic(QObject):

    def __init__(self):
        super(EloPic, self).__init__()
        self.ui = MainWindow(
            "D:/Dropbox/Coding/pyside-tutorial/IMG_4812.jpg",
            "D:/Dropbox/Coding/pyside-tutorial/IMG_4816.jpg",
        )
        self.data = EloPicDB()
        self.ui.directory_selected.connect(self.handle_directory_selection)
        self.ui.picture_chosen.connect(self.handle_picture_chosen)
        self.ui.picture_deleted.connect(self.handle_picture_deleted)

    def show(self):
        self.ui.show()

    @Slot(unicode)
    def handle_directory_selection(self, directory):
        self.ui.statusBar().showMessage('Selected Dir: ' + directory)
        self.data.load_from_disk(directory)
        left_image, right_image = self.data.get_random_images(2)
        #self.ui.statusBar().showMessage('Left: {} | Right: {}'.format(left_image['path'], right_image['path']))
        self.ui.change_pictures(left_image['path'], right_image['path'])

    @Slot(int)
    def handle_picture_chosen(self, pic_chosen):
        # TODO: Actually assign ELO scores
        self._randomize_picture(BOTH)

    @Slot(int)
    def handle_picture_deleted(self, pic_deleted):
        # TODO: Actually "delete" picture
        self._randomize_picture(pic_deleted)


    def _randomize_picture(self, pic_to_randomize=BOTH):
        left_image, right_image = self.data.get_random_images(2)
        if pic_to_randomize == LEFT:
            self.ui.change_pictures(left_image['path'], self.ui.right_path)
        elif pic_to_randomize == RIGHT:
            self.ui.change_pictures(self.ui.left_path, right_image['path'])
        else:
            self.ui.change_pictures(left_image['path'], right_image['path'])

