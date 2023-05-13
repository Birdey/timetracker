""" 
This class gets the current window name and application name

Author: Christoffer von Matérn @Birdey

Date: 28-06-2021

Version: 1.0

Version history:
    1.0: Created the class
"""

# pylint: disable=no-name-in-module

import sys
import importlib.util
from time import sleep

if importlib.util.find_spec("win32gui") is not None:
    import win32gui  # pylint: disable=import-error

if importlib.util.find_spec("AppKit") is not None:
    from AppKit import NSWorkspace
    from Quartz import (
        CGWindowListCopyWindowInfo,
        kCGWindowListOptionOnScreenOnly,
        kCGNullWindowID,
    )


class WindowInfoGetter:
    """
    This class gets the current window name and application name

        Example
        -------
            >>> window_name, application_name = WindowInfoGetter.get_current_window()

        Methods
        --------
            >>> get_current_window(): Get the current window
    """

    @staticmethod
    def _get_active_window_win32():
        window = win32gui.GetForegroundWindow()
        window_name = win32gui.GetWindowText(window)
        application_name = win32gui.GetClassName(window)

        return WindowInfoGetter._review_active_info_win32(application_name, window_name)

    @staticmethod
    def _get_active_window_darwin():
        curr_pid = NSWorkspace.sharedWorkspace().activeApplication()[
            "NSApplicationProcessIdentifier"
        ]
        options = kCGWindowListOptionOnScreenOnly
        window_list = CGWindowListCopyWindowInfo(options, kCGNullWindowID)

        for window in window_list:
            pid = window["kCGWindowOwnerPID"]
            if curr_pid == pid:
                application_name = window["kCGWindowOwnerName"]
                window_name = window.get("kCGWindowName", "Unknown")

        return WindowInfoGetter._review_active_info_darwin(
            application_name, window_name
        )

    @staticmethod
    def _review_active_info_darwin(application_name, window_name):
        if application_name == "Safari":
            if " - Safari" in window_name:
                window_name = window_name[: -len(" - Safari")]
        elif application_name == "Google Chrome":
            if " - Google Chrome" in window_name:
                window_name = window_name[: -len(" - Google Chrome")]
        elif "Code" in application_name:
            window_name = "Visual Studio Code"
        elif application_name == "iTerm2":
            window_name = "Terminal"

        return application_name, window_name

    @staticmethod
    def _review_active_info_win32(application_name, window_name):
        window_name = window_name.replace("-", "—")
        window_name_sections = window_name.split("—")
        application_name = window_name_sections.pop(
            len(window_name_sections) - 1
        ).strip()
        window_name = window_name_sections.pop().strip()
        print(f"Application name: {application_name} - Window name: {window_name}")
        return application_name, window_name

    @staticmethod
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
                return WindowInfoGetter._get_active_window_darwin()
            if sys.platform == "win32":
                return WindowInfoGetter._get_active_window_win32()

        except KeyboardInterrupt:
            print("Stopping time tracker")
            sys.exit()

        except SystemExit:
            print("Stopping time tracker")
            sys.exit()

        except NameError as error:
            WindowInfoGetter._print_error_message(error)

        except ModuleNotFoundError as error:
            WindowInfoGetter._print_error_message(error)

        except ValueError as error:
            WindowInfoGetter._print_error_message(error)

        except Exception as error:
            WindowInfoGetter._print_error_message(error)

        return "UnknownApplication", "UnknownWindowName"

    # def _print_exception_message(self, exception: Exception):
    #     """
    #     Print the exception message

    #         Parameters:
    #             exception (Exception): The exception
    #     """
    #     print("===================================")
    #     print(f"{exception.name}: \n'{exception}'")
    #     print(f"file name: {sys.exc_info()[-1].tb_frame.f_code.co_filename}")
    #     print(f"error line number: {sys.exc_info()[-1].tb_lineno}")
    #     print("-----------------------------------")
    #     print(f"Traceback: \n{exception.with_traceback()}"
    #     print("-----------------------------------")
    #     print("===================================")

    @staticmethod
    def _print_error_message(error):
        """
        Print the error message

            Parameters:
                error_message (Error): The error
        """
        print("===================================")
        print(f"{error.name}: \n'{error}'")
        print(f"file name: {sys.exc_info()[-1].tb_frame.f_code.co_filename}")
        print(f"error line number: {sys.exc_info()[-1].tb_lineno}")
        print("-----------------------------------")
        print(f"Traceback: \n{error.with_traceback()}")
        print("-----------------------------------")
        print("===================================")
        sleep(10)
