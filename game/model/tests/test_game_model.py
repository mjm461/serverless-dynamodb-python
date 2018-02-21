import unittest
import datetime
import uuid

from ..game_model import GameModel


class TestGameModel(unittest.TestCase):

    def test_put_parameter(self):

        GameModel.Meta.host = "http://localhost:8000"

        if not GameModel.exists():
            GameModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)

        if not GameModel.exists():
            GameModel.create_table(wait=True)

        winner_uuid = str(uuid.uuid4())

        # Create an item
        item = GameModel('1234', datetime.datetime.utcnow())
        item.winner_id = winner_uuid
        item.save()

        # Count on an index
        self.assertTrue(len(list(
            GameModel.player_opponent_index.query('1234', GameModel.winner_id == winner_uuid))) == 1)
