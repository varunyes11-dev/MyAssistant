from datetime import datetime
import subprocess


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
import subprocess


def get_battery_status() -> str:
    """
    Return the current Mac battery percentage and charging status.
    """

    try:
        result = subprocess.run(
            ["pmset", "-g", "batt"],
            capture_output=True,
            text=True,
            check=True,
        )

        output = result.stdout

        battery_line = next(
            (
                line
                for line in output.splitlines()
                if "InternalBattery" in line
            ),
            None,
        )

        if not battery_line:
            return "I couldn't find the battery status."

        parts = [part.strip() for part in battery_line.split(";")]

        # The first section contains the battery percentage.
        first_section = parts[0]

        percentage = next(
            (
                token
                for token in first_section.split()
                if token.endswith("%")
            ),
            None,
        )

        if not percentage:
            return "I couldn't determine the battery percentage."

        status = parts[1] if len(parts) > 1 else "unknown"

        return f"Battery is at {percentage} and {status}."

    except Exception as error:
        return f"I couldn't read the battery status: {error}"