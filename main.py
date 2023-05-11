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

# pylint: disable=no-name-in-module, line-too-long, missing-module-docstring, missing-function-docstring, missing-class-docstring

import datetime
import sys
from time import sleep
import time


# import applescript

from AppKit import NSWorkspace  # E0611: No name 'NSWorkspace' in module 'AppKit'

from Quartz import (
    CGWindowListCopyWindowInfo,  # E0611: No name 'CGWindowListCopyWindowInfo' in module 'Quartz'
    kCGWindowListOptionOnScreenOnly,  # E0611: No name 'kCGWindowListOptionOnScreenOnly' in module 'Quartz'
    kCGNullWindowID,  # E0611: No name 'kCGNullWindowID' in module 'Quartz'
)

from db import Database


db = Database("time_tracker_db.db")


def _get_active_window_win32():
    # TODO: Implement this function when I get code on my Windows machine
    pass


def _get_active_window_darwin():
    curr_pid = NSWorkspace.sharedWorkspace().activeApplication()[
        "NSApplicationProcessIdentifier"
    ]
    options = kCGWindowListOptionOnScreenOnly
    window_list = CGWindowListCopyWindowInfo(options, kCGNullWindowID)

    for window in window_list:
        pid = window["kCGWindowOwnerPID"]
        if curr_pid == pid:
            owner_name = window["kCGWindowOwnerName"]
            window_name = window.get("kCGWindowName", "Unknown")
            # print(
            #     f"DEBUG: {owner_name} - {window_name} (PID: {pid}, WID: {window_number}): {window_name}"
            # )

    return _review_active_info(owner_name, window_name)


def _review_active_info(owner_name, window_name):
    if owner_name == "Safari":
        if " - Safari" in window_name:
            window_name = window_name[: -len(" - Safari")]
    elif owner_name == "Google Chrome":
        if " - Google Chrome" in window_name:
            window_name = window_name[: -len(" - Google Chrome")]
    elif "Code" in owner_name:
        window_name = "Visual Studio Code"
    elif owner_name == "iTerm2":
        window_name = "Terminal"

    return owner_name, window_name


def get_current_window():
    """
    Get the current window

        Parameters:
            event_window_num (int): The number of the window

        Returns:
            str, str: The name of the application and the name of the window
    """
    try:
        if sys.platform == "darwin":
            return _get_active_window_darwin()
        if sys.platform == "win32":
            return _get_active_window_win32()

    except KeyboardInterrupt:
        print("Stopping time tracker")
        sys.exit()

    except SystemExit:
        print("Stopping time tracker")
        sys.exit()

    except NameError:
        print("NameError: %s", sys.exc_info()[0])
        print("error line number: %s", sys.exc_info()[-1].tb_lineno)

    except Exception:
        print("Unexpected error: %s", sys.exc_info()[0])
        print("error line number: %s", sys.exc_info()[-1].tb_lineno)

    return "Unknown", "Unknown"


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
        owner_name, window_name = get_current_window()
        if window_name == "Unknown":
            window_name = owner_name + " - Application"

        if window_name != current_application:
            report(current_application, start_time, time.time())
            current_application = window_name
            start_time = time.time()

        sleep(0.1)


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
