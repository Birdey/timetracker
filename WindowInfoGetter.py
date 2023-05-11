# pylint: disable=no-name-in-module

import sys

from AppKit import NSWorkspace  # E0611: No name 'NSWorkspace' in module 'AppKit'

from Quartz import (
    CGWindowListCopyWindowInfo,  # E0611: No name 'CGWindowListCopyWindowInfo' in module 'Quartz'
    kCGWindowListOptionOnScreenOnly,  # E0611: No name 'kCGWindowListOptionOnScreenOnly' in module 'Quartz'
    kCGNullWindowID,  # E0611: No name 'kCGNullWindowID' in module 'Quartz'
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
        # TODO: Implement this function when I get code on my Windows machine
        pass

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
                # print(
                #     f"DEBUG: {owner_name} - {window_name} (PID: {pid}, WID: {window_number}): {window_name}"
                # )

        return WindowInfoGetter._review_active_info(application_name, window_name)

    @staticmethod
    def _review_active_info(application_name, window_name):
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

        except NameError:
            print("NameError: %s", sys.exc_info()[0])
            print("error line number: %s", sys.exc_info()[-1].tb_lineno)

        except Exception:
            print("Unexpected error: %s", sys.exc_info()[0])
            print("error line number: %s", sys.exc_info()[-1].tb_lineno)

        return "UnknownApplication", "UnknownWindowName"
