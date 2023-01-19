class Duration:
    def __init__(self, ts_start, ts_end):
        self.ts_start = ts_start
        self.ts_end = ts_end

    def __str__(self):
        attributes_str = f'ts_start = {self.ts_start_srt()}\n'
        attributes_str += f'ts_end = {self.ts_end_srt()}\n'
        return str(self.__class__) + '\n' + attributes_str

    def __eq__(self, other):
        if isinstance(other, Duration):
            return self.ts_start == other.ts_start and self.ts_end == other.ts_end
        return False

    def ts_start_srt(self):
        return Duration.ms_to_srt_timestamp(self.ts_start)

    def ts_end_srt(self):
        return Duration.ms_to_srt_timestamp(self.ts_end)

    def export(self, filepath, index):
        with open(filepath, 'w') as file:
            file.write(f"{index};{self.ts_start_srt()};{self.ts_end_srt()}")

    @staticmethod
    def ms_to_srt_timestamp(ms):
        hours, remainder = divmod(ms, 3600000)
        minutes, remainder = divmod(remainder, 60000)
        seconds, ms = divmod(remainder, 1000)

        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{int(ms):03}"

    @staticmethod
    def srt_timestamp_to_ms(srt_timestamp):
        hours, minutes, seconds_ms = srt_timestamp.split(":")
        seconds, ms = seconds_ms.split(",")

        time_in_ms = (int(hours) * 3600000 +
                                int(minutes) * 60000 +
                                int(seconds) * 1000 +
                                int(ms))
        return time_in_ms
