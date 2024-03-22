import logging
from typing import Optional

import mysql.connector


class DBException(Exception):
    pass


class DB:
    """
    It's a class to interact with a MySQL database via SQL queries.
    """

    def __init__(self, database: str = "database", host: str = "localhost", user: str = "root",
                 passwd: Optional[str] = None, **kwargs):
        """
        Initializes a class.

        :param str database: a database name (database)
        :param str host: IP:port for connection to DB (localhost)
        :param str user: a username for connection (root)
        :param str passwd: a password for connection
        :param **kwargs: other arguments for connecting
        """
        self.database = database
        if not self.database:
            self.conn = mysql.connector.connect(
                host=host,
                user=user,
                passwd=passwd,
                autocommit=True,
                **kwargs
            )

        else:
            self.conn = mysql.connector.connect(
                host=host,
                user=user,
                passwd=passwd,
                database=self.database,
                autocommit=True,
                **kwargs
            )

        try:
            self.cursor = self.conn.cursor()

        except Exception as e:
            raise DBException(f'\n{str(e)}')

    def execute(self, query: str, data: Optional[tuple] = None, fetchone: bool = False):
        """
        Executes SQL queries.

        :param str query: a query
        :param str data: a data for query
        :param str fetchone: if True uses fetchone, otherwise uses fetchall in SELECT queries (False)
        """
        try:
            if not self.conn:
                self.__init__(self.database)

            else:
                if data:
                    self.cursor.execute(query, data)

                else:
                    self.cursor.execute(query)

                if 'INSERT' in query or 'UPDATE' in query or 'DELETE' in query or 'DROP' in query:
                    self.conn.commit()

                elif 'SELECT' in query:
                    if fetchone:
                        return self.cursor.fetchone()

                    else:
                        return self.cursor.fetchall()

        except Exception as e:
            logging.error('connection', exc_info=True)
            raise DBException(f'\n{str(e)}')
