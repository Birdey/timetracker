import sqlite3


class Database:
    def __init__(self, database_name):
        self.database_name = database_name

    def add_data(self, application, time, date):
        # insert data into the database
        SQL_statement = "INSERT INTO time_tracker VALUES (?, ?, ?)"
        data = (application, time, date)

        # create connection
        connection = sqlite3.connect(self.database_name)

        # create cursor
        cursor = connection.cursor()

        # execute SQL statement
        cursor.execute(SQL_statement, data)

        # commit changes
        connection.commit()

        # close connection
        connection.close()

    def create_database():
        # create a local database using sqlite3
        database_name = "time_tracker.db"

        # create connection
        connection = sqlite3.connect(database_name)

        # create cursor
        cursor = connection.cursor()

        # create table
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS time_tracker (
            application_name text,
            time_spent integer,
            date_used text
        )"""
        )

        # close connection
        connection.close()

    def insert_data(application, time, date):
        # insert data into the database
        SQL_statement = "INSERT INTO time_tracker VALUES (?, ?, ?)"
        data = (application, time, date)

        # create connection
        connection = sqlite3.connect("time_tracker.db")

        # create cursor
        cursor = connection.cursor()

        # execute SQL statement
        cursor.execute(SQL_statement, data)

        # commit changes
        connection.commit()

        # close connection
        connection.close()

    def view_data():
        # view data from the database
        # create connection
        connection = sqlite3.connect("time_tracker.db")

        # create cursor
        cursor = connection.cursor()

        # execute SQL statement
        cursor.execute("SELECT * FROM time_tracker")

        # fetch data
        data = cursor.fetchall()

        # print data
        print(data)

        # close connection
        connection.close()

    def delete_data(application):
        # delete data from the database
        # create connection
        connection = sqlite3.connect("time_tracker.db")

        # create cursor
        cursor = connection.cursor()

        # execute SQL statement
        cursor.execute(
            "DELETE FROM time_tracker WHERE application_name = (?)", (application,)
        )

        # commit changes
        connection.commit()

        # close connection
        connection.close()

    def update_data(application, time, date):
        # update data from the database
        # create connection
        connection = sqlite3.connect("time_tracker.db")

        # create cursor
        cursor = connection.cursor()

        # execute SQL statement
        cursor.execute(
            "UPDATE time_tracker SET time_spent = (?), date_used = (?) WHERE application_name = (?)",
            (time, date, application),
        )

        # commit changes
        connection.commit()

        # close connection
        connection.close()

    def total_time_spent():
        # calculate the total time spent on all applications
        # create connection
        connection = sqlite3.connect("time_tracker.db")

        # create cursor
        cursor = connection.cursor()

        # execute SQL statement
        cursor.execute("SELECT SUM(time_spent) FROM time_tracker")

        # fetch data
        data = cursor.fetchall()

        # print data
        print(data)

        # close connection
        connection.close()

    def total_time_spent_on_app(application):
        # calculate the total time spent on a specific application
        # create connection
        connection = sqlite3.connect("time_tracker.db")

        # create cursor
        cursor = connection.cursor()

        # execute SQL statement
        cursor.execute(
            "SELECT SUM(time_spent) FROM time_tracker WHERE application_name = (?)",
            (application,),
        )

        # fetch data
        data = cursor.fetchall()

        # print data
        print(data)

        # close connection
        connection.close()

    def total_time_spent_on_app_on_date(application, date):
        # calculate the total time spent on a specific application on a specific date
        # create connection
        connection = sqlite3.connect("time_tracker.db")

        # create cursor
        cursor = connection.cursor()

        # execute SQL statement
        cursor.execute(
            "SELECT SUM(time_spent) FROM time_tracker WHERE application_name = (?) AND date_used = (?)",
            (application, date),
        )

        # fetch data
        data = cursor.fetchall()

        # print data
        print(data)

        # close connection
        connection.close()

    def total_time_spent_on_app_for_dates(application, start_date, end_date):
        # calculate the total time spent on a specific application on a specific week
        # create connection
        connection = sqlite3.connect("time_tracker.db")

        # create cursor
        cursor = connection.cursor()

        # execute SQL statement
        cursor.execute(
            "SELECT SUM(time_spent) FROM time_tracker WHERE application_name = (?) AND date_used BETWEEN (?) AND (?)",
            (application, start_date, end_date),
        )

        # fetch data
        data = cursor.fetchall()

        # print data
        print(data)

        # close connection
        connection.close()
