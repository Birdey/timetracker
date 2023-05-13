# pylint: disable=no-name-in-module

import sys
import importlib.util


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
        spam_spec = importlib.util.find_spec("win32gui")
        if spam_spec is None:
            raise ModuleNotFoundError(
                "You must have pywin32 installed to use this module"
            )

        import win32gui

        window = win32gui.GetForegroundWindow()
        window_name = win32gui.GetWindowText(window)
        application_name = win32gui.GetClassName(window)

        return WindowInfoGetter._review_active_info_win32(application_name, window_name)

    @staticmethod
    def _get_active_window_darwin():
        spam_spec = importlib.util.find_spec("AppKit")
        if spam_spec is None:
            raise ModuleNotFoundError(
                "You must have pyobjc installed to use this module"
            )

        from AppKit import (
            NSWorkspace,
        )  # E0611: No name 'NSWorkspace' in module 'AppKit'

        from Quartz import (
            CGWindowListCopyWindowInfo,  # E0611: No name 'CGWindowListCopyWindowInfo' in module 'Quartz'
            kCGWindowListOptionOnScreenOnly,  # E0611: No name 'kCGWindowListOptionOnScreenOnly' in module 'Quartz'
            kCGNullWindowID,  # E0611: No name 'kCGNullWindowID' in module 'Quartz'
        )

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

        except NameError:
            print("NameError: %s", sys.exc_info()[0])
            print("error line number: %s", sys.exc_info()[-1].tb_lineno)
            print("file name: %s", sys.exc_info()[-1].tb_frame.f_code.co_filename)

        except ModuleNotFoundError as error:
            print("ModuleNotFoundError: %s", error)
            print("error line number: %s", sys.exc_info()[-1].tb_lineno)
            print("file name: %s", sys.exc_info()[-1].tb_frame.f_code.co_filename)
            print(error.with_traceback())
            print("Please install the missing module and try again")
            exit(1)

        except ValueError:
            print("ValueError: %s", sys.exc_info()[0])
            print("error line number: %s", sys.exc_info()[-1].tb_lineno)
            print("file name: %s", sys.exc_info()[-1].tb_frame.f_code.co_filename)

        except Exception:
            print("Unexpected error: %s", sys.exc_info()[0])
            print("error line number: %s", sys.exc_info()[-1].tb_lineno)
            print("file name: %s", sys.exc_info()[-1].tb_frame.f_code.co_filename)

        return "UnknownApplication", "UnknownWindowName"
