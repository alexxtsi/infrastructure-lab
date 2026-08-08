#!/usr/bin/python3

import sys
import json


PRIORITIES = [
    "EMERGENCY",
    "ALERT",
    "CRITICAL",
    "ERROR",
    "WARNING",
    "NOTICE",
    "INFO",
    "DEBUG"
]


def parse_log_file(file_path):
    counts = {
        "EMERGENCY": 0,
        "ALERT": 0,
        "CRITICAL": 0,
        "ERROR": 0,
        "WARNING": 0,
        "NOTICE": 0,
        "INFO": 0,
        "DEBUG": 0
    }

    try:
        with open(file_path, "r", encoding="utf-8") as file:

            for line_number, line in enumerate(file, start=1):

                try:
                    log_entry = json.loads(line)

                except json.JSONDecodeError:
                    print(
                        f"Warning: skipping malformed JSON "
                        f"on line {line_number}",
                        file=sys.stderr
                    )
                    continue

                priority = log_entry.get("PRIORITY")

                # Some journal records may not contain PRIORITY.
                if priority is None:
                    print(
                        f"Warning: no PRIORITY on line {line_number}",
                        file=sys.stderr
                    )
                    continue

                try:
                    priority_number = int(priority)
                    severity = PRIORITIES[priority_number]

                except (ValueError, IndexError):
                    print(
                        f"Warning: invalid PRIORITY '{priority}' "
                        f"on line {line_number}",
                        file=sys.stderr
                    )
                    continue

                counts[severity] += 1

    except FileNotFoundError:
        print(
            f"Error: log file '{file_path}' does not exist.",
            file=sys.stderr
        )
        return None

    return counts


def main():
    if len(sys.argv) != 2:
        print(
            f"Usage: {sys.argv[0]} <log-file>",
            file=sys.stderr
        )
        sys.exit(1)

    log_path = sys.argv[1]

    counts = parse_log_file(log_path)

    if counts is None:
        sys.exit(1)

    print("Log severity summary")
    print("--------------------")

    for severity in PRIORITIES:
        print(f"{severity:<10}: {counts[severity]}")


if __name__ == "__main__":
    main()