from __future__ import unicode_literals

import os

import shutil

import errno
from PySide.QtCore import QObject, Slot
from PySide.QtCore import Signal

from ui import MainWindow
from data import EloPicDB
from logic import EloRating

LEFT = 0
RIGHT = 1
BOTH = 2


class EloPic(QObject):

    EXPORT_DIR_NAME = 'EloPic Top {}'

    rating_updated = Signal(list)

    def __init__(self):
        super(EloPic, self).__init__()
        self.ui = MainWindow(
            "D:/Dropbox/Coding/pyside-tutorial/IMG_4812.jpg",
            "D:/Dropbox/Coding/pyside-tutorial/IMG_4816.jpg",
        )
        self.data = EloPicDB()
        self.current_directory = ''
        self.ui.directory_selected.connect(self.handle_directory_selection)
        self.ui.picture_chosen.connect(self.handle_picture_chosen)
        self.ui.picture_deleted.connect(self.handle_picture_deleted)
        self.ui.export_top_x_selected.connect(self.handle_export_top_x)
        self.rating_updated.connect(self.ui.handle_rating_updated)

    def show(self):
        self.ui.show()

    @Slot(unicode)
    def handle_directory_selection(self, directory):
        self.current_directory = directory
        self.ui.statusBar().showMessage('Selected Dir: ' + directory)
        self.data.load_from_disk(directory)
        self.rating_updated.emit(self.data.to_list())
        left_image, right_image = self.data.get_random_images(2)
        self.ui.change_pictures(left_image['path'], right_image['path'])

    @Slot(unicode, unicode)
    def handle_picture_chosen(self, winner, loser):
        self._calculate_new_scores(winner, loser)
        self._randomize_picture()

    @Slot(unicode)
    def handle_picture_deleted(self, pics_deleted):
        self.data.ignore_pictures(pics_deleted)
        if len(pics_deleted) > 1:
            self._randomize_picture()
        else:
            self._randomize_picture(pics_deleted[0])

    @Slot(int)
    def handle_export_top_x(self, x):
        try:
            export_basepath = self._get_export_base_path(x)
            os.makedirs(export_basepath)
        except OSError as e:
            if e.errno == errno.EEXIST:
                self._clean_up_directory(export_basepath)
            else:
                raise
        try:
            top_x = self.data.get_top_x_filepaths_by_rating(x)
            for i, original_filepath in enumerate(top_x):
                export_filepath = self._get_export_path(original_filepath, export_basepath, i+1)
                shutil.copyfile(original_filepath, export_filepath)
        except IOError:
            self.ui.statusBar().showMessage('Error while exporting!')

    def _get_export_base_path(self, x):
        return os.path.join(self.current_directory, self.EXPORT_DIR_NAME.format(x))

    @staticmethod
    def _clean_up_directory(path):
        for item in os.listdir(path):
            file_path = os.path.join(path, item)
            if os.path.isfile(file_path):
                os.unlink(file_path)

    def _get_export_path(self, original_path, export_basepath, rank):
        base, filename = os.path.split(original_path)
        filename = self._add_rank_to_filename(filename, rank)
        return os.path.join(export_basepath, filename)

    def _add_rank_to_filename(self, filename, rank):
        return '{}_{}'.format(str(rank).zfill(4), filename)

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
        self.rating_updated.emit(self.data.to_list())

