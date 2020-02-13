from typing import List

from database import Base, Session


def save_objects(session: Session, *args: List[Base]) -> None:
    for object in args:
        session.add(object)
    session.commit()
