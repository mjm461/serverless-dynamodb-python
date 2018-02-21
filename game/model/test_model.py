from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from pynamodb.attributes import NumberAttribute

from .base_meta import BaseMeta


class ViewIndex(GlobalSecondaryIndex):
    class Meta(BaseMeta):
        index_name = "viewIdx"
        read_capacity_units = 1
        write_capacity_units = 1
        projection = AllProjection()

    view = NumberAttribute(default=0, hash_key=True)


class TestModel(Model):
    class Meta(BaseMeta):
        table_name = "TestModel"

    forum = UnicodeAttribute(hash_key=True)
    thread = UnicodeAttribute(range_key=True)
    view_index = ViewIndex()
    view = NumberAttribute(default=0)
