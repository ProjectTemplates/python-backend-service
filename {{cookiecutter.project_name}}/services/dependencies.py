from typing import Generator

from database import Session


# FastAPI Dependency for db session management
def get_db() -> Generator[Session, None, None]:
    db = None
    try:
        db = Session()
        yield db
    finally:
        if db:
            db.close()
