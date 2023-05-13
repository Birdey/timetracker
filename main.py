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
import threading
import time
import tkinter
from WindowInfoGetter import WindowInfoGetter
from WindowManager import WindowManager


# import applescript

from db import Database  # Importing from db.py

SCANNING = False

DB = Database("time_tracker_db.db")
BTN_START: tkinter.Button
BTN_STOP: tkinter.Button

WINDOW: WindowManager = None


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
    DB.add_data(application_name, running_time, datetime.date.today())
    total_time = round(DB.total_time_spent_on_app(application_name), 2)
    print(f'App "{application_name}" for {hms}')
    print(f"Total time spent on app: {seconds_to_hms(total_time)}")


def start_button_callback(event: tkinter.Event):
    """
    Start scanning for the current window
    """
    print("Start button was clicked")
    global SCANNING, BTN_START, BTN_STOP

    SCANNING = True
    threading.Thread(target=start_scan).start()
    BTN_START["state"] = "disabled"
    BTN_STOP["state"] = "normal"


def stop_button_callback(event):
    """
    Stop scanning for the current window
    """
    print(event)
    print("Stop button was clicked")
    global SCANNING, BTN_START, BTN_STOP
    SCANNING = False

    BTN_START["state"] = "normal"
    BTN_STOP["state"] = "disabled"


def start_scan():
    """
    Start scanning for the current window
    """
    print("Scanning")
    current_application = ""
    start_time = time.time()
    while SCANNING:
        owner_name, window_name = WindowInfoGetter.get_current_window()
        if window_name == "Unknown":
            window_name = owner_name + " - Application"

        if window_name != current_application:
            report(current_application, start_time, time.time())
            current_application = window_name
            start_time = time.time()

        time.sleep(0.1)


def quit_app():
    """
    Quit the program
    """
    global WINDOW
    if WINDOW is not None:
        if WINDOW.window is not None:
            WINDOW.window.destroy()
        WINDOW = None
    quit()


def start_app():
    """
    Start the program
    """
    global BTN_START, BTN_STOP, WINDOW

    WINDOW = WindowManager("Time Tracker", (1080, 970))

    # Terminate the program when the window is closed
    WINDOW.window.protocol("WM_DELETE_WINDOW", func=quit_app)
    WINDOW.add_text("Time Tracker", (150, 10))
    BTN_START = WINDOW.add_button("Start", (10, 10), (50, 20), start_button_callback)
    BTN_STOP = WINDOW.add_button("Stop", (10, 40), (50, 20), stop_button_callback)

    app_data = DB.view_data()

    x = 20
    y = 70

    app_time_total = {}
    for data in app_data:
        name, app_time, app_date = data
        if name in app_time_total:
            app_time_total[name]["time"] += app_time
            app_time_total[name]["opens"] += 1
        else:
            app_time_total[name] = {
                "time": app_time,
                "opens": 1,
            }

    # Sort app_time_total
    app_time_total = {
        k: v
        for k, v in sorted(
            app_time_total.items(), key=lambda item: item[1]["time"], reverse=True
        )
    }

    # WINDOW.add_text("Total time spent on apps", (x, y))
    WINDOW.add_text("App:", (x, y))
    WINDOW.add_text("Time:", (x + 200, y))
    WINDOW.add_text("Opens:", (x + 300, y))
    y += 20

    for app in app_time_total.items():
        app_name = app[0]
        app_time = seconds_to_hms(int(app[1]["time"]))
        app_opens = app[1]["opens"]
        WINDOW.add_text(f"{app_name}:", (x, y))
        WINDOW.add_text(f"{app_time}", (x + 200, y))
        WINDOW.add_text(f"{app_opens}", (x + 300, y))
        y += 20

    # for app in app_time_total.items():
    #     app_name = app[0]
    #     app_time = seconds_to_hms(int(app[1]))
    #     WINDOW.add_text(f"{app_name}: {app_time}", (x, y))
    #     y += 20

    BTN_STOP["state"] = "disabled"

    WINDOW.show()
    while True:
        WINDOW.update()
        time.sleep(0.01)


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
    start_app()
