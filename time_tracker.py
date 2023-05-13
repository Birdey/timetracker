"""
The main class for the TimeTracker

Author: Christoffer von Matérn @Birdey

Date: 28-06-2021

Version: 1.0

Version history:
    1.0: Created the class
"""

import datetime
import threading
import time
import tkinter
from window_info_graber import WindowInfoGetter

from WindowManager import WindowManager
from db import Database
from utils.StringUtils import seconds_to_hms_str


class TimeTracker:
    """
    The main class for the TimeTracker
    """

    main_window: tkinter.Tk
    window_manager: WindowManager
    database: Database

    start_button: tkinter.Button
    stop_button: tkinter.Button
    stats_button: tkinter.Button

    scanning: bool

    def run(self) -> None:
        """
        Run the program
        """
        self.main_window = WindowManager("Time Tracker", (1080, 970))

        # Terminate the program when the window is closed
        self.main_window.window.protocol("WM_DELETE_WINDOW", func=self.quit_app)

        # set WINDOW background to a light gray
        self.main_window.window.configure(
            padx=10,
            pady=10,
            borderwidth=2,
            relief="groove",
            bd=2,
            highlightthickness=2,
            highlightbackground="#a0a0a0",
            highlightcolor="#a0a0a0",
        )
        # WINDOW.window.configgure(bd=2)
        self.main_window.add_text("Time Tracker", (150, 10))
        self.start_button = self.main_window.add_button(
            "Start", (10, 10), (50, 20), self.start_button_callback
        )
        self.stop_button = self.main_window.add_button(
            "Stop", (10, 40), (50, 20), self.stop_button_callback
        )
        self.stats_button = self.main_window.add_button(
            "Stats", (10, 70), (50, 20), self.show_stats_window
        )

        self.stop_button["state"] = "disabled"

        self.main_window.show()

    def show_stats_window(self, event) -> None:
        """
        Creates a new window that shows the stats for the application
        """
        print(event)
        app_data = self.database.view_data()

        pos_x = 20
        pos_y = 70

        app_time_total = {}
        for data in app_data:
            name, app_time, _ = data
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

        stats_window = WindowManager("Stats", (600, 700))

        stats_window.add_text("Stats", (150, 10))

        stats_window.add_text("App:", (pos_x, pos_y))
        stats_window.add_text("Time:", (pos_x + 200, pos_y))
        stats_window.add_text("Opens:", (pos_x + 300, pos_y))

        pos_y += 20

        for app in app_time_total.items():
            app_name = app[0]
            app_time = seconds_to_hms_str(int(app[1]["time"]))
            app_opens = app[1]["opens"]
            stats_window.add_text(f"{app_name}:", (pos_x, pos_y))
            stats_window.add_text(f"{app_time}", (pos_x + 200, pos_y))
            stats_window.add_text(f"{app_opens}", (pos_x + 300, pos_y))
            pos_y += 20

        stats_window.show()

    def show_stats(self, event):
        """
        Show the stats window
        """

        print(event)
        app_data = self.database.view_data()

        pos_x = 20
        pos_y = 70

        app_time_total = {}
        for data in app_data:
            name, app_time, _ = data
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

        stats_window = WindowManager("Stats", (600, 700))

        stats_window.add_text("Stats", (150, 10))

        stats_window.add_text("App:", (pos_x, pos_y))
        stats_window.add_text("Time:", (pos_x + 200, pos_y))
        stats_window.add_text("Opens:", (pos_x + 300, pos_y))

        pos_y += 20

        for app in app_time_total.items():
            app_name = app[0]
            app_time = seconds_to_hms_str(int(app[1]["time"]))
            app_opens = app[1]["opens"]
            stats_window.add_text(f"{app_name}:", (pos_x, pos_y))
            stats_window.add_text(f"{app_time}", (pos_x + 200, pos_y))
            stats_window.add_text(f"{app_opens}", (pos_x + 300, pos_y))
            pos_y += 20

        stats_window.show()

    def report(self, application_name: str, start_time: int, end_time: int):
        """
        Saves reported data to the database

            Parameters:
                application_name (str): The name of the application
                start_time (int): The start time
                end_time (int): The end time
        """
        if application_name.strip() == "":
            print("Not reporting app because it's empty.")
            print(f"time: {seconds_to_hms_str(end_time - start_time)}")
            return
        running_time = end_time - start_time
        self.database.add_data(application_name, running_time, datetime.date.today())

    def start_button_callback(self, event):  # pylint: disable=unused-argument
        """
        Start scanning for the current window
        """

        self.scanning = True
        threading.Thread(target=self.start_scan).start()
        self.start_button["state"] = "disabled"
        self.stop_button["state"] = "normal"

    def stop_button_callback(self, event):  # pylint: disable=unused-argument
        """
        Stop scanning for the current window
        """
        self.scanning = False

        self.start_button["state"] = "normal"
        self.stop_button["state"] = "disabled"

    def start_scan(self):
        """
        Start scanning for the current window
        """
        print("Scanning")
        current_application = ""
        start_time = time.time()
        while self.scanning:
            owner_name, window_name = WindowInfoGetter.get_current_window()
            if window_name == "Unknown":
                window_name = owner_name + " - Application"

            if window_name != current_application:
                self.report(current_application, start_time, time.time())
                current_application = window_name
                start_time = time.time()

            time.sleep(0.1)

    def quit_app(self):
        """
        Quit the program
        """
        if self.main_window is not None:
            self.main_window.destroy()

        quit()

    def update(self) -> None:
        """
        Update the main window
        """
        self.window_manager.update()
