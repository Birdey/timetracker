"""
String utilities

Author: Christoffer von Matérn @Birdey

Created: 2020-09-25

Examples:
    >>> seconds_to_hms_str(3600)
    '1h'
"""


def seconds_to_hms_str(seconds: int):
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

    return r_string.strip()
