import random
import sys
from os import path, listdir

from tinydb import Query
from tinydb import TinyDB

from logic.elo import INITIAL_ELO_SCORE

ELOPIC_DB_NAME = 'elopic.data'
ELOPIC_SUPPORTED_EXTENSIONS = ['.jpg', '.jpeg']


class EloPicDBError(Exception):
    pass


# TODO: Add tests for the DB
class EloPicDB:
    """
    Simple wrapper class for elopic's underlying database. Abstracts all data
    related functions so replacing TinyDB in the future would be easy.
    """
    def __init__(self):
        self._db = None
        self._dir = ''

    def load_from_disk(self, directory):
        """
        Reads the EloImages from `directory`.

        If an `elopic.data` file from a previous run exists in the directory, read
        from there (doing a consistency check for moved / added / deleted
        files).
        Otherwise read the images in the directory and create an initial
        `elopic.data`.
        :param directory: Filesystem path to the directory holding the image
        files.
        """
        assert path.isdir(directory)
        self._dir = path.abspath(directory)
        db_path = path.join(self._dir, ELOPIC_DB_NAME)
        try:
            self._db = TinyDB(db_path)
        except ValueError as err:
            err.message = 'Unable to read {}: {}\n'.format(db_path, err.message)
            raise
        try:
            self.validate()
        except Exception as err:
            err.message = 'Error while validating elopic.data in {}: {}'.format(
                self._dir, err.message
            )

    def validate(self):
        """
        Makes sure all the files in `self._dir` are present in self._db.

        Files that have been added to the directory are added to the data with
        initial values.
        """
        # TODO: Flag missing files instead of removing them from the data.
        # TODO: Use os.walk to find files recursively in subdirs.
        # TODO: Use hash values instead of filenames to distinguish images,
        #       possibly find similar / duplicate images
        # TODO: Files that are not (any longer) in the directory are removed from the data?
        for img in listdir(self._dir):
            if any(img.lower().endswith(ext) for ext in ELOPIC_SUPPORTED_EXTENSIONS):
                try:
                    self._validate_image(path.join(self._dir, img))
                except Exception as err:
                    err.message = 'Error while validating {}: {}'.format(
                        img, err.message
                    )

    def _validate_image(self, image_path):
        Image = Query()
        result = self._db.search(Image.path == image_path)
        if len(result) == 0:
            # Image not in DB yet -> add it
            self._db.insert({'path': image_path, 'rating': INITIAL_ELO_SCORE})

        if len(result) > 1:
            # Image in DB more than once -> raise
            raise EloPicDBError('Multiple entry for the same image: "{}".'.format(image_path))

        # Image already in DB. -> we are fine
        return

    def get_random_images(self, count):
        return random.sample(self._db.all(), count)
