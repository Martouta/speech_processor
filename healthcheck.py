import os
from datetime import datetime, timedelta

LIVENESS_THRESHOLD = timedelta(minutes=5)
READINESS_LOG_LINE = "Connection to kafka established"


def get_last_log_line():
    with open(f"log/{os.environ['SPEECH_ENV']}.log", "r") as log_file:
        lines = log_file.readlines()
        return lines[-1] if lines else None


def log_timestamp(log_line):
    timestamp_str = log_line.split(" - ")[0]
    return datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")


def is_liveness_ok(log_line):
    if not log_line:
        return False

    log_parts = log_line.split(" - ")
    log_level = log_parts[1].strip()
    log_timestamp = datetime.strptime(log_parts[0], "%Y-%m-%d %H:%M:%S.%f")

    if log_level == "ERROR" and datetime.now() - log_timestamp > LIVENESS_THRESHOLD:
        return False

    return True


def is_readiness_ok(log_line):
    return READINESS_LOG_LINE in log_line


def main():
    last_log_line = get_last_log_line()

    probe_type = os.environ.get("PROBE_TYPE")

    if probe_type == "liveness":
        is_ok = is_liveness_ok(last_log_line)
    elif probe_type == "readiness":
        is_ok = is_readiness_ok(last_log_line)
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
