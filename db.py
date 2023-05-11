"""
Database module
---------------
This module contains the class for interacting with the database.

Classes
-------
Database
    Class for interacting with the database
"""

from datetime import date as Date
import sqlite3


class Database:
    """
    Class for interacting with the database

    Attributes
    ----------
    >>> database_name : str
        The name of the database

    Methods
    -------
    >>> create_database() -> None
        Create the database

    >>> add_data(application: str, time: int, date: Date) -> None
        Add data to the database

    >>> insert_data(application: str, time: int, date: Date) -> None
        Insert data into the database

    >>> view_data() -> None
        View the data in the database

    >>> delete_data(application: str) -> None
        Delete data from the database

    >>> update_data(application: str, time: int, date: Date) -> None
        Update data in the database

    >>> total_time_spent() -> int
        Get the total time spent on all applications

    >>> total_time_spent_on_app(application: str) -> int
        Get the total time spent on a specific application

    >>> total_time_spent_on_app_on_date(application: str, date: Date) -> int
        Get the total time spent on a specific application on a specific date

    >>> total_time_spent_on_app_for_dates(application: str, start_date: Date, end_date: Date) -> int
        Get the total time spent on a specific application for specific dates
    """

    def __init__(self, database_name):
        self.database_name = database_name
        self.create_database()

    def _query_commit(self, sql_statement: str, variables: tuple = None) -> None:
        connection = sqlite3.connect(self.database_name)
        cursor = connection.cursor()
        if variables:
            cursor.execute(sql_statement, variables)
        else:
            cursor.execute(sql_statement)
        connection.commit()
        connection.close()

    def _query_fetch(self, sql_statement: str, variables: tuple = None) -> list:
        connection = sqlite3.connect(self.database_name)
        cursor = connection.cursor()
        if variables:
            cursor.execute(sql_statement, variables)
        else:
            cursor.execute(sql_statement)
        data = cursor.fetchall()
        connection.close()
        return data

    def _query_execute(self, sql_statement: str, variables: tuple = None) -> None:
        connection = sqlite3.connect(self.database_name)
        cursor = connection.cursor()
        if variables:
            cursor.execute(sql_statement, variables)
        else:
            cursor.execute(sql_statement)
        connection.close()

    def create_database(self) -> None:
        """
        Create the database
        """
        sql_statement = "CREATE TABLE IF NOT EXISTS time_tracker (application_name text, time_spent integer, date_used text)"
        self._query_execute(sql_statement)

    def add_data(self, application: str, time: int, date: Date) -> None:
        """
        Add data to the database

            Parameters:
                application (str): The name of the application
                time (int): The time spent on the application
                date (date): The date when the application was used
        """
        sql_statement = "INSERT INTO time_tracker VALUES (?, ?, ?)"
        data = (application, time, date)
        self._query_commit(sql_statement, data)

    def insert_data(self, application: str, time: int, date: Date) -> None:
        """
        Insert data into the database

            Parameters:
                application (str): The name of the application
                time (int): The time spent on the application
                date (date): The date when the application was used
        """
        sql_statement = "INSERT INTO time_tracker VALUES (?, ?, ?)"
        data = (application, time, date)
        self._query_commit(sql_statement, data)

    def view_data(self):
        """
        View the data in the database

            Returns:
                list: The data from the database
        """
        sql_statement = "SELECT * FROM time_tracker"
        data = self._query_fetch(sql_statement)
        return data

    def delete_data(self, application):
        """
        Delete data from the database

            Parameters:
                application (str): The name of the application
        """
        sql_statement = "DELETE FROM time_tracker WHERE application_name = (?)"
        self._query_commit(sql_statement, (application,))

    def update_data(self, application, time, date):
        """
        Update data in the database

            Parameters:
                application (str): The name of the application
                time (int): The time spent on the application
                date (date): The date when the application was used
        """
        sql_statement = "UPDATE time_tracker SET time_spent = (?), date_used = (?) WHERE application_name = (?)"
        self._query_commit(sql_statement, (time, date, application))

    def total_time_spent(self):
        """
        Get the total time spent on all applications

            Returns:
                int: The total time spent on all applications
        """
        sql_statement = "SELECT SUM(time_spent) FROM time_tracker"
        data = self._query_fetch(sql_statement)
        return data

    def total_time_spent_on_app(self, application):
        """
        Get the total time spent on a specific application

            Parameters:
                application (str): The name of the application

            Returns:
                int: The total time spent on a specific application
        """
        sql_statement = (
            "SELECT SUM(time_spent) FROM time_tracker WHERE application_name = (?)"
        )
        data = self._query_fetch(sql_statement, (application,))
        return data[0][0]

    def total_time_spent_on_app_on_date(self, application, date):
        """
        Get the total time spent on a specific application on a specific date

            Parameters:
                application (str): The name of the application
                date (date): The date when the application was used

            Returns:
                int: The total time spent on a specific application on a specific date
        """
        sql_statement = "SELECT SUM(time_spent) FROM time_tracker WHERE application_name = (?) AND date_used = (?)"
        data = self._query_fetch(sql_statement, (application, date))
        return data

    def total_time_spent_on_app_for_dates(self, application, start_date, end_date):
        """
        Get the total time spent on a specific application for specific dates

            Parameters:
                application (str): The name of the application
                start_date (date): The start date when the application was used
                end_date (date): The end date when the application was used

            Returns:
                int: The total time spent on a specific application for specific dates
        """
        sql_statement = "SELECT SUM(time_spent) FROM time_tracker WHERE application_name = (?) AND date_used BETWEEN (?) AND (?)"
        data = self._query_fetch(sql_statement, (application, start_date, end_date))
        return data
