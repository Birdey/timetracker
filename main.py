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
import sys
from time import sleep
import time

import applescript

from AppKit import NSWorkspace

from Quartz import (
    CGWindowListCopyWindowInfo,
    kCGWindowListOptionOnScreenOnly,
    kCGNullWindowID,
)


def _get_active_window_win32():
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
            window_number = window["kCGWindowNumber"]
            owner_name = window["kCGWindowOwnerName"]
            window_name = window.get("kCGWindowName", "Unknown")
            # print(
            #     f"DEBUG: {owner_name} - {window_name} (PID: {pid}, WID: {window_number}): {window_name}"
            # )

    return _review_active_info(owner_name, window_name)


def _review_active_info(owner_name, window_name):
    if owner_name == "Google Chrome":
        if " - Google Chrome" in window_name:
            window_name = window_name[: -len(" - Google Chrome")]
        elif " - Firefox" in window_name:
            window_name = window_name[: -len(" - Firefox")]
    elif "Code" in owner_name:
        window_name = "Visual Studio Code"
    elif owner_name == "iTerm2":
        window_name = "Terminal"

    return owner_name, window_name


def get_current_window(event_window_num):
    # Get the current application name on macOS
    try:
        if sys.platform == "darwin":
            return _get_active_window_darwin()
        if sys.platform == "win32":
            return _get_active_window_win32()

    except:
        print("Unexpected error: %s", sys.exc_info()[0])
        print("error line number: %s", sys.exc_info()[-1].tb_lineno)

    return "Unknown", "Unknown"


def report(application_name: str, start_time: int, end_time: int):
    # Report the time spent on a specific application
    running_time = end_time - start_time
    hms = seconds_to_hms(int(running_time))
    print(f'App "{application_name}" for {hms}')


def start():
    # Start the time tracker
    current_application = ""
    start_time = time.time()
    while True:
        pid = NSWorkspace.sharedWorkspace().activeApplication()[
            "NSApplicationProcessIdentifier"
        ]
        owner_name, window_name = get_current_window(pid)
        if window_name == "Unknown":
            window_name = owner_name + " - " + window_name

        if window_name != current_application:
            report(current_application, start_time, time.time())
            current_application = window_name
            start_time = time.time()

        sleep(0.1)


def seconds_to_hms(seconds: int):
    # convert seconds to h:m:s
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


def main():
    start()


if __name__ == "__main__":
    main()
