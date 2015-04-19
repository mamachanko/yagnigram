import os
import unittest

from yagnigram.image import UnicodeImage


class ImageTest(unittest.TestCase):

    def test_dimensions(self):
        sample_image = self._get_sample_image(width=25, height=25)
        print(unicode(sample_image))
        rows = sample_image.get_rows()
        self.assertEqual(100, len(rows[0]))
        self.assertEqual(100, len(rows))

    def _get_sample_image(self, width, height):
        tests_dir = os.path.dirname(os.path.abspath(__file__))
        sample_image_filename = os.path.join(tests_dir, 'sample.jpg')
        return UnicodeImage.from_filename(
            sample_image_filename, width=width, height=height
        )

