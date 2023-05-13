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


from TimeTracker import TimeTracker


def main():
    """
    This is the main function.
    """
    time_tracker = TimeTracker()
    time_tracker.run()


if __name__ == "__main__":
    main()
