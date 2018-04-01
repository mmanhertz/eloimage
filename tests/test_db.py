from __future__ import unicode_literals

import os
import shutil
import tempfile
import unittest

from elopic.data.elopicdb import EloPicDB, EloPicDBError
from elopic.logic.elo import INITIAL_ELO_SCORE
from tests.utils import copy_all_files, delete_files_matching_pattern


class TestDatabase(unittest.TestCase):
    """Test cases for the data package"""

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.picdir = 'testdata/pics1'
        copy_all_files(self.picdir, self.tempdir)
        self._initDB()

    def tearDown(self):
        self.db.close()
        shutil.rmtree(self.tempdir)

    def _initDB(self):
        self.db = EloPicDB()
        self.db.load_from_disk(self.tempdir)

    def _assert_db_matches_dir(self, dir):
        expected = self._get_imagepaths_in_dir(dir)
        result = self.db.to_list()
        self.assertEquals(len(result), len(expected), 'Number of pictures does not match.')
        self.assertListEqual(
            [r[0] for r in result],
            expected,
            'Paths do not match'
        )
        for r in result:
            self.assertEqual(r[1], 0)
            self.assertEqual(r[2], INITIAL_ELO_SCORE)
            self.assertEqual(r[3], 0)

    def _get_imagepaths_in_dir(self, dir):
        return [os.path.join(self.tempdir, e) for e in os.listdir(dir) if e.endswith('.jpg')]

    def test_load_from_disk_new_folder(self):
        self._assert_db_matches_dir(self.tempdir)

    def test_load_additional_files(self):
        self.db.close()
        # delete_files_matching_pattern(self.tempdir, r'^\d+\.jpg$')
        copy_all_files('testdata/pics2', self.tempdir)
        self._initDB()

        self._assert_db_matches_dir(self.tempdir)

    @unittest.skip('Support for deleted files is not in yet')
    def test_load_deleted_files(self):
        self.db.close()
        delete_files_matching_pattern(self.tempdir, r'^\d+\.jpg$')
        copy_all_files('testdata/pics2', self.tempdir)
        self._initDB()

        self._assert_db_matches_dir(self.tempdir)

    def test_rating(self):
        images = self._get_imagepaths_in_dir(self.tempdir)
        for path in images:
            self.assertEqual(INITIAL_ELO_SCORE, self.db.get_rating(path))
        for idx, path in enumerate(images):
            self.db.update_rating(path, idx)
        for idx, path in enumerate(images):
            self.assertEqual(idx, self.db.get_rating(path))
        self.assertListEqual(images[:-4:-1], self.db.get_top_x_filepaths_by_rating(3))

    def test_headers(self):
        expected = [
            'ignore',
            'path',
            'rating',
            'seen_count',
        ]
        result = self.db.get_headers()
        result.sort()
        self.assertEqual(expected, result)

    def test_ignore(self):
        images = self._get_imagepaths_in_dir(self.tempdir)
        self.db.ignore_pictures(images[:3])
        self.db.ignore_pictures(images[-1:])
        self.maxDiff = None
        self.assertListEqual(images[3:-1], [i['path'] for i in self.db.get_all()])
