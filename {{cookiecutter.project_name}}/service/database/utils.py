from sqlalchemy import inspect
from sqlalchemy.dialects.postgresql import insert

from . import Base, Session


def upsert(db: Session, model: Base, **values):
    table = model.__table__
    stmt = insert(table).values(**values)

    primary_keys = [key.name for key in inspect(table).primary_key]
    update_dict = {c: values[c] for c in values if c not in primary_keys}

    if not update_dict:
        raise ValueError('insert_or_update resulted in an empty update_dict')

    stmt = stmt.on_conflict_do_update(index_elements=primary_keys, set_=update_dict)

    db.connection.execute(stmt)
