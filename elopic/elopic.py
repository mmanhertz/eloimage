from __future__ import unicode_literals

from PySide.QtCore import QObject, Slot

from ui import MainWindow
from data import EloPicDB
from logic import EloRating

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
        self.ui.change_pictures(left_image['path'], right_image['path'])

    @Slot(unicode, unicode)
    def handle_picture_chosen(self, winner, loser):
        # TODO: Actually assign ELO scores
        self._calculate_new_scores(winner, loser)
        self._randomize_picture()

    @Slot(unicode)
    def handle_picture_deleted(self, pic_deleted):
        # TODO: Actually "delete" picture
        self._randomize_picture(pic_deleted)

    def _randomize_picture(self, pic_to_randomize=None):
        left_image, right_image = self.data.get_random_images(2)
        if pic_to_randomize == None:
            self.ui.change_pictures(left_image['path'], right_image['path'])
        elif pic_to_randomize == self.ui.left_path:
            self.ui.change_pictures(left_image['path'], self.ui.right_path)
        elif pic_to_randomize == self.ui.right_path:
            self.ui.change_pictures(self.ui.left_path, right_image['path'])
        else:
            raise ValueError(
                '{} cannot be replaced. It does not match the displayed images.'
            )

    def _calculate_new_scores(self, winner, loser):
        elo = EloRating()
        winner_rating, loser_rating = elo.calculate_new_rating(
            self.data.get_rating(winner),
            self.data.get_rating(loser),
            1
        )
        self.data.update_rating(winner, winner_rating)
        self.data.update_rating(loser, loser_rating)

