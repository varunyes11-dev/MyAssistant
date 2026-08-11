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
        result = eval(
            expression,
            {"__builtins__": {}},
            {},
        )

        return str(result)

    except Exception:
        return "I couldn't calculate that expression."


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

        parts = [
            part.strip()
            for part in battery_line.split(";")
        ]

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

        status = (
            parts[1]
            if len(parts) > 1
            else "unknown"
        )

        return f"Battery is at {percentage} and {status}."

    except Exception as error:
        return (
            f"I couldn't read the battery status: {error}"
        )


def get_system_info(key: str | None = None) -> str:
    """
    Return useful non-sensitive information about this Mac.
    """

    try:
        hardware_result = subprocess.run(
            ["system_profiler", "SPHardwareDataType"],
            capture_output=True,
            text=True,
            check=True,
        )

        software_result = subprocess.run(
            ["sw_vers"],
            capture_output=True,
            text=True,
            check=True,
        )

        computer_result = subprocess.run(
            ["scutil", "--get", "ComputerName"],
            capture_output=True,
            text=True,
            check=True,
        )

        hardware = hardware_result.stdout
        software = software_result.stdout
        computer_name = computer_result.stdout.strip()

        def get_value(text: str, field: str) -> str:
            for line in text.splitlines():
                if line.strip().startswith(f"{field}:"):
                    return line.split(":", 1)[1].strip()

            return "Unknown"

        model = get_value(
            hardware,
            "Model Name",
        )

        chip = get_value(
            hardware,
            "Chip",
        )

        memory = get_value(
            hardware,
            "Memory",
        )

        macos_version = get_value(
            software,
            "ProductVersion",
        )

        return (
            f"Computer: {computer_name}\n"
            f"Model: {model}\n"
            f"Chip: {chip}\n"
            f"Memory: {memory}\n"
            f"macOS: {macos_version}"
        )

    except Exception as error:
        return (
            f"I couldn't read the system information: {error}"
        )