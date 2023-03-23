class Duration:
    def __init__(self, ts_start, ts_end):
        """
        Initialize the Duration object with start and end timestamps in milliseconds
        :param ts_start: start timestamp in milliseconds
        :param ts_end: end timestamp in milliseconds
        """
        self.ts_start = ts_start
        self.ts_end = ts_end

    def __str__(self):
        """
        Returns a string representation of the Duration object
        """
        attributes_str = f'ts_start = {self.ts_start_srt()}\n'
        attributes_str += f'ts_end = {self.ts_end_srt()}\n'
        return str(self.__class__) + '\n' + attributes_str

    def __eq__(self, other) -> bool:
        """
        Compare two Duration objects for equality
        :param other: other Duration object to compare to
        :return: True if both objects are equal, False otherwise
        """
        if isinstance(other, Duration):
            return self.ts_start == other.ts_start and self.ts_end == other.ts_end
        return False

    def ts_start_srt(self):
        """
        Returns the start timestamp in SRT format
        """
        return Duration.ms_to_srt_timestamp(self.ts_start)

    def ts_end_srt(self):
        """
        Returns the end timestamp in SRT format
        """
        return Duration.ms_to_srt_timestamp(self.ts_end)

    def export(self, filepath, index):
        """
        Export the Duration object to a file in the format 'index;ts_start_srt;ts_end_srt'
        :param filepath: filepath to export the object to
        :param index: index of the duration object
        """
        with open(filepath, 'w') as file:
            file.write(f"{index};{self.ts_start_srt()};{self.ts_end_srt()}")

    @staticmethod
    def from_srt(start, end):
        """
        Create a Duration object from start and end timestamps in SRT format
        :param start: start timestamp in SRT format
        :param end: end timestamp in SRT format
        :return: the created Duration object
        """
        ts_start = Duration.srt_timestamp_to_ms(start)
        ts_end = Duration.srt_timestamp_to_ms(end)
        return Duration(ts_start, ts_end)

    @staticmethod
    def ms_to_srt_timestamp(ms):
        """
        Convert timestamp from milliseconds to SRT format
        :param ms: timestamp in milliseconds
        :return: timestamp in SRT format
        """
        hours, remainder = divmod(ms, 3600000)
        minutes, remainder = divmod(remainder, 60000)
        seconds, ms = divmod(remainder, 1000)

        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{int(ms):03}"

    @staticmethod
    def srt_timestamp_to_ms(srt_timestamp):
        """
        Convert timestamp from SRT format to milliseconds
        :param srt_timestamp: timestamp in SRT format
        :return: timestamp in milliseconds
        """
        hours, minutes, seconds_ms = srt_timestamp.split(":")
        seconds, ms = seconds_ms.split(",")

        time_in_ms = (int(hours) * 3600000 +
                      int(minutes) * 60000 +
                      int(seconds) * 1000 +
                      int(ms))
        return time_in_ms
