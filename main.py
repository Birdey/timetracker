"""
This is a project to keep track of time spent in applications and websites.

For example:
- How much time do I spend on YouTube?
- How much time did I spend on YouTube yesterday?
- How much time did I spend on YouTube this week?
- How much time did I spend on YouTube last week?


Features:
- Create a database that tracks time spent on applications and websites.
- Create a GUI that allows you to enter the name of the application or website.

The database should be able to store the following information:
- Name of the application or website
- Time spent on the application or website
- Date of when the application or website was used

The GUI should allow you to:
- Input the name of the application or website
- Input the time spent on the application or website
- Input the date of when the application or website was used

The GUI should also allow you to:
- View the total amount of time spent on the application or website
- View the total amount of time spent on the application or website on a specific date
- View the total amount of time spent on the application or website on a specific week
"""

import datetime
import time
from WindowInfoGetter import WindowInfoGetter


# import applescript

from db import Database  # Importing from db.py


db = Database("time_tracker_db.db")


def report(application_name: str, start_time: int, end_time: int):
    """
    Saves reported data to the database

        Parameters:
            application_name (str): The name of the application
            start_time (int): The start time
            end_time (int): The end time
    """
    if application_name.strip() == "":
        print("Not reporting app because it's empty.")
        print(f"time: {seconds_to_hms(end_time - start_time)}")
        return
    running_time = end_time - start_time
    hms = seconds_to_hms(int(running_time))
    db.add_data(application_name, running_time, datetime.date.today())
    total_time = round(db.total_time_spent_on_app(application_name), 2)
    print(f'App "{application_name}" for {hms}')
    print(f"Total time spent on app: {seconds_to_hms(total_time)}")


def start():
    """
    Start the program
    """
    current_application = ""
    start_time = time.time()
    while True:
        owner_name, window_name = WindowInfoGetter.get_current_window()
        if window_name == "Unknown":
            window_name = owner_name + " - Application"

        if window_name != current_application:
            report(current_application, start_time, time.time())
            current_application = window_name
            start_time = time.time()

        time.sleep(0.1)


def seconds_to_hms(seconds: int):
    """
    Convert seconds to hours, minutes and seconds

        Parameters:
            seconds (int): The number of seconds

        Returns:
            str: The hours, minutes and seconds in a string
    """
    hours = int(seconds / 3600)
    seconds = seconds % 3600
    minutes = int(seconds / 60)
    seconds = seconds % 60

    r_string = ""
    if hours != 0:
        r_string += f"{hours}h "
    if minutes != 0:
        r_string += f"{minutes}m "
    if seconds != 0:
        r_string += f"{seconds}s"

    return r_string


if __name__ == "__main__":
    start()
