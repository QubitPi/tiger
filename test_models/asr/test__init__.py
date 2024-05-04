import time
import unittest

from . import random_filename

class TestASR(unittest.TestCase):

    def test_same_file_has_different_random_name_at_different_times(self):
        first = random_filename("foo.mp3")
        time.sleep(1)
        second = random_filename("foo.mp3")
        self.assertNotEquals(first, second)
