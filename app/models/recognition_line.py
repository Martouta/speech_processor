class RecognitionLine:
    def __init__(self, line_text, duration):
        """
        Initialize the RecognitionLine object with line text and a Duration object
        :param line_text: text of the recognition line
        :param duration: Duration object representing the start and end timestamps of the line
        """
        self.text = line_text
        self.duration = duration

    def __str__(self):
        """
        Returns a string representation of the RecognitionLine object in the format 'duration.ts_start_srt();duration.ts_end_srt();line_text'
        """
        return f"{self.duration.ts_start_srt()};{self.duration.ts_end_srt()};{self.text}"

    def duration_ts_start_srt(self):
        """
        Returns the start timestamp of the line's duration in SRT format
        """
        return self.duration.ts_start_srt()

    def duration_ts_end_srt(self):
        """
        Returns the end timestamp of the line's duration in SRT format
        """
        return self.duration.ts_end_srt()
