from datetime import datetime


def get_current_datetime() -> str:
    """
    Return the current local date and time.
    """

    now = datetime.now()

    return now.strftime(
        "%A, %B %d, %Y at %I:%M %p"
    )