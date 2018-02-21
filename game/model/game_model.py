from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute
from pynamodb.indexes import LocalSecondaryIndex, GlobalSecondaryIndex, AllProjection

from .base_meta import BaseMeta


class GamePlayerOpponentIndex(LocalSecondaryIndex):
    class Meta(BaseMeta):
        read_capacity_units = 1
        write_capacity_units = 1
        table_name = "GamePlayerOpponentIndex"
        projection = AllProjection()

    player_id = UnicodeAttribute(hash_key=True)
    opponent_id = UnicodeAttribute(range_key=True)


class GameWinnerTimeIndex(GlobalSecondaryIndex):
    class Meta(BaseMeta):
        read_capacity_units = 1
        write_capacity_units = 1
        table_name = "GameWinnerTimeIndex"
        projection = AllProjection()

    winner_id = UnicodeAttribute(hash_key=True)
    created_time = UnicodeAttribute(range_key=True)


class GameModel(Model):
    class Meta(BaseMeta):
        read_capacity_units = 1
        write_capacity_units = 1
        table_name = "GameModel"

    player_id = UnicodeAttribute(hash_key=True)
    created_time = UTCDateTimeAttribute(range_key=True)
    opponent_id = UnicodeAttribute()
    winner_id = UnicodeAttribute()
    notes = UnicodeAttribute(null=True)

    player_opponent_index = GamePlayerOpponentIndex()
    winner_time_index = GameWinnerTimeIndex()
