import pytest
from sqlalchemy import create_engine

from conf import DB_URI, make_db_uri
from database import Base, Session


@pytest.fixture(scope='session', autouse=True)
def test_db(request):
    print('Creating test database')

    test_db = 'test'

    tmp_engine = create_engine(DB_URI)
    conn = tmp_engine.connect()
    conn.execute('COMMIT')
    conn.execute(f'CREATE DATABASE {test_db}')

    engine = create_engine(make_db_uri(db=test_db))
    # Execute setup here - create extensions, additional dbs, types, etc.
    # engine.execute('')

    Base.metadata.create_all(engine)
    Session.configure(bind=engine)

    def teardown():
        print('Tearing down test database')

        engine.dispose()

        conn.execute('COMMIT')
        conn.execute(f'DROP DATABASE {test_db}')
        conn.close()

    request.addfinalizer(teardown)


@pytest.fixture(scope='function', autouse=True)
def clear_db(request):
    engine = Session().get_bind()

    def reset_db():
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

    request.addfinalizer(reset_db)
