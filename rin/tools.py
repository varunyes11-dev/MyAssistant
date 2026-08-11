from datetime import datetime


def get_current_datetime() -> str:
    """
    Return the current local date and time.
    """

    now = datetime.now()

    return now.strftime(
        "%A, %B %d, %Y at %I:%M %p"
    )
def calculate(expression: str) -> str:
    """
    Safely calculate basic arithmetic expressions.
    """

    allowed = set(
        "0123456789+-*/(). %"
    )

    if not expression or any(
        character not in allowed
        for character in expression
    ):
        return "I can only calculate basic arithmetic expressions."

    try:
        # Evaluate only after restricting the character set.
        result = eval(
            expression,
            {"__builtins__": {}},
            {},
        )

        return str(result)

    except Exception:
        return "I couldn't calculate that expression."