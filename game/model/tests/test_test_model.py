import unittest
from ..test_model import TestModel


class TestTestModel(unittest.TestCase):

    def test_put_parameter(self):
        TestModel.Meta.host = "http://localhost:8000"

        if not TestModel.exists():
            TestModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)

        # Create an item
        item = TestModel('forum-example', 'thread-example')
        item.view = 1
        item.save()

        # Indexes can be queried easily using the index's hash key
        items = list(TestModel.view_index.query(1))

        self.assertTrue(len(items) > 0)
