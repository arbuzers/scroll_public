import sqlite3
from typing import Optional, Union


class DBException(Exception):
    pass


class DB:
    """
    It's a class to interact with a SQLite3 database via SQL queries.
    """

    def __init__(self, database_file: str, **kwargs):
        """
        Initializes a class.

        :param str database_file: a path to the database
        :param **kwargs: other arguments for connecting
        """
        self.database_file = database_file
        self.kwargs = kwargs
        if not kwargs:
            self.db = sqlite3.connect(self.database_file, isolation_level=None)

        else:
            self.db = sqlite3.connect(self.database_file, **kwargs)

        try:
            self.cursor = self.db.cursor()

        except Exception as e:
            raise DBException(f'\n{str(e)}')

    def execute(self, query: str, data: Optional[tuple] = None, fetchone: bool = False, with_column_names: bool = False,
                return_class: bool = True):
        """
        Executes SQL queries.

        :param str query: a query
        :param str data: a data for query
        :param str fetchone: if True uses fetchone, otherwise uses fetchall in SELECT queries (False)
        :param str with_column_names: if True returns column names in SELECT queries (False)
        :param str return_class: if True returns dynamic class, otherwise returns tuple (True)
        """
        while True:
            try:
                if data:
                    self.cursor.execute(query, data)

                else:
                    self.cursor.execute(query)

                response = []
                try:
                    headers = tuple([description[0] for description in self.cursor.description])

                except:
                    headers = ()

                if with_column_names:
                    response.append(headers)

                if fetchone:
                    try:
                        if return_class:
                            return dynamic_class('data', headers, self.cursor.fetchone())

                        else:
                            if with_column_names:
                                response.append(self.cursor.fetchone())

                            else:
                                response = self.cursor.fetchone()

                    except:
                        pass

                else:
                    if return_class:
                        response = []
                        for row in self.cursor.fetchall():
                            response.append(dynamic_class('data', headers, row))

                    else:
                        response += self.cursor.fetchall()

                return response

            except sqlite3.ProgrammingError as e:
                if 'Cannot operate on a closed cursor' in str(e):
                    self.__init__(self.database_file, **self.kwargs)

                else:
                    raise DBException(f'\n{str(e)}')

            except Exception as e:
                raise DBException(f'\n{str(e)}')


def dynamic_class(class_name: str, variables: Union[list, tuple], values: Union[list, tuple]) -> object:
    """
    Dynamically creates a class for received data similar to the one in SQLAlchemy,
    but without explicitly specifying instance variables.

    :param str class_name: a class name
    :param Union[list, tuple] variables: variables of the class
    :param Union[list, tuple] values: values of the specified variables
    :return object: a created class
    """
    class_dict = dict(zip(variables, values))
    class_format = f'{class_name}('
    for i in range(len(variables)):
        class_format += f'{variables[i]}={repr(values[i])}, '

    metaclass = type(class_name, (type,), {'__repr__': lambda cls: class_format[:-2] + ')'})
    return metaclass(class_name, (object,), class_dict)


def make_sql(query: str, data: tuple = None, ret1: bool = False, ret_class: bool = True,
             with_column_names: bool = False, database_file: str = 'database.db'):
    """
    Function was deprecated, use DB class.
    """
    with sqlite3.connect(database_file) as db:
        try:
            cursor = db.cursor()
            if data:
                try:
                    cursor.execute(query, data)

                except Exception as e:
                    raise DBException(f'\n{str(e)}')

            else:
                try:
                    cursor.execute(query)

                except Exception as e:
                    raise DBException(f'\n{str(e)}')

            db.commit()
            response = []
            try:
                headers = tuple([description[0] for description in cursor.description])

            except:
                headers = ()

            if with_column_names:
                response.append(headers)

            if ret1:
                try:
                    if ret_class:
                        return dynamic_class('data', headers, cursor.fetchone())

                    else:
                        if with_column_names:
                            response.append(cursor.fetchone())

                        else:
                            response = cursor.fetchone()

                except:
                    pass

            else:
                if ret_class:
                    response = []
                    for row in cursor.fetchall():
                        response.append(dynamic_class('data', headers, row))
                else:
                    response += cursor.fetchall()

            return response

        except Exception as e:
            raise DBException(f'\n{str(e)}')
