import os
from datetime import timedelta

STARTUP_LOG_LINE = "Fetching input messages"


def get_all_log_lines():
    with open(f"log/{os.environ['SPEECH_ENV']}.log", "r") as log_file:
        lines = log_file.readlines()
        return lines


def is_startup_ok(log_lines):
    for line in log_lines:
        if STARTUP_LOG_LINE in line:
            return True
    return False


def main():
    log_lines = get_all_log_lines()

    probe_type = os.environ.get("PROBE_TYPE")

    if probe_type == "startup":
        is_ok = is_startup_ok(log_lines)
    else:
        print("Unknown probe type")
        exit(1)

    if is_ok:
        print("OK")
        exit(0)
    else:
        print("Not OK")
        exit(1)


if __name__ == "__main__":
    main()
