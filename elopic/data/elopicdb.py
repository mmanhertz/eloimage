import sys
from os import path, listdir
from tinydb import TinyDB

ELOPIC_DB_NAME = 'elopic.db'
ELOPIC_SUPPORTED_EXTENSIONS = ['.jpg', '.jpeg']


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

        If an `elopic.db` file from a previous run exists in the directory, read
        from there (doing a consistency check for moved / added / deleted
        files).
        Otherwise read the images in the directory and create an initial
        `elopic.db`.
        :param directory: Filesystem path to the directory holding the image
        files.
        """
        assert path.isdir(directory)
        self._dir = directory
        db_path = path.join(self._dir, ELOPIC_DB_NAME)
        try:
            self._db = TinyDB(db_path)
        except ValueError as err:
            err.message = 'Unable to read {}: {}\n'.format(db_path, err.message)
            raise
        try:
            self.validate()
        except Exception as err:
            err.message = 'Error while validating elopic.db in {}: {}'.format(
                self._dir, err.message
            )

    def validate(self):
        """
        Makes sure exactly the files in `self._dir` are mapped in self._db.

        Files that are not (any longer) in the directory are removed from the
        db. Files that have been added to the directory are added to the db with
        initial values.
        """
        # TODO: Flag missing files instead of removing them from the db.
        # TODO: Use os.walk to find files recursively in subdirs.
        # TODO: Use hash values instead of filenames to distinguish images,
        #       possibly find similar / duplicate images
        for img in listdir(self._dir):
            if any(img.endswith(ext) for ext in ELOPIC_SUPPORTED_EXTENSIONS):
                try:
                    self._validate_image(img)
                except Exception as err:
                    err.message = 'Error while validating {}: {}'.format(
                        img, err.message
                    )

    def _validate_image(self, image_path):
        raise NotImplementedError
