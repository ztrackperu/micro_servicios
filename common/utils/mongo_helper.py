from pymongo.collection import Collection
from pymongo import ASCENDING, DESCENDING

def ensure_indexes(col: Collection, indexes: list[tuple[str, int]], unique: list[str] | None = None):
    unique = unique or []
    for field, order in indexes:
        if field in unique:
            col.create_index([(field, order)], unique=True)
        else:
            col.create_index([(field, order)])
