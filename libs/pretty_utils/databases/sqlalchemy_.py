from typing import List, Union

from sqlalchemy import create_engine, text
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import sessionmaker, Session


class DBException(Exception):
    pass


class DB:
    """
    It's a class that simplifies working with the SQLAlchemy library.
    """

    def __init__(self, db_url: str, **kwargs):
        """
        Initializes a class.

        :param str db_url: a URL containing all the necessary parameters to connect to a DB
        """
        self.db_url = db_url
        self.create_database()
        self.engine = create_engine(self.db_url, **kwargs)
        self.Base = None
        session = sessionmaker(bind=self.engine)
        self.s: Session = session()
        self.conn = self.engine.connect()

    def create_database(self, database: str = ''):
        """
        Creates a database if it doesn't exist.

        :param str database: a database name
        """
        try:
            if not database:
                db_url = self.db_url.split('/')
                database = db_url[-1]
                db_url = '/'.join(db_url[0:-1])

            else:
                db_url = self.db_url

            engine = create_engine(db_url)
            with engine.connect() as conn:
                conn.execute('COMMIT')
                conn.execute(f'CREATE DATABASE {database}')

        except:
            pass

    def create_tables(self, base):
        """
        Creates tables.

        :param base: a base class for declarative class definitions
        """
        self.Base = base
        self.Base.metadata.create_all(self.engine)

    def all(self, entities, *criterion) -> list:
        """
        Fetches all rows.

        :param entities: an ORM entity
        :param criterion: criterion for rows filtering
        :return list: the list of rows
        """
        if criterion:
            return self.s.query(entities).filter(*criterion).all()

        return self.s.query(entities).all()

    def one(self, entities, *criterion, from_the_end: bool = False):
        """
        Fetches one row.

        :param entities: an ORM entity
        :param criterion: criterion for rows filtering
        :param from_the_end: get the row from the end
        :return list: found row or None
        """
        all = self.all(entities, *criterion)
        if all:
            if from_the_end:
                return all[-1]

            return all[0]

        return None

    def execute(self, query, *args):
        """
        Executes SQL query.

        :param query: the query
        :param args: any additional arguments
        """
        result = self.conn.execute(text(query), *args)
        self.commit()
        return result

    def commit(self):
        """
        Commits changes.
        """
        try:
            self.s.commit()

        except DatabaseError:
            self.s.rollback()

    def insert(self, row: Union[object, List[object]]):
        """
        Inserts rows.

        :param Union[object, List[object]] row: an ORM entity or list of entities
        """
        if isinstance(row, list):
            self.s.add_all(row)

        elif isinstance(row, object):
            self.s.add(row)

        else:
            DBException('Wrong type!')

        self.commit()
