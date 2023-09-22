from unittest import TestCase

from theresa.common import remove_duplicates


class TestCommon(TestCase):

    def test_deduplicating_nodes_by_id(self):
        self.assertEqual(
            [{"id": "china"}, {"id": "us"}],
            remove_duplicates([{"id": "china"}, {"id": "us"}, {"id": "china"}])
        )
