class RecognitionLine:
    def __init__(self, line_text, duration):
        """
        Initialize the RecognitionLine object with line text and a Duration object
        :param line_text: text of the recognition line
        :param duration: Duration object representing the start and end timestamps of the line
        """
        self.text = line_text
        self.duration = duration

    def __eq__(self, other) -> bool:
        """
        Returns True if the RecognitionLine objects have the same text and duration
        """
        if not isinstance(other, RecognitionLine):
            return False
        return self.text == other.text and self.duration == other.duration

    def __str__(self):
        """
        Returns a string representation of the RecognitionLine object in the format 'duration.ts_start_srt();duration.ts_end_srt();line_text'
        """
        return f"{self.duration_ts_start_srt()};{self.duration_ts_end_srt()};{self.text}"

    def __repr__(self):
        """
        Returns a string representation of the RecognitionLine object
        """
        return f"RecognitionLine(text='{self.text}', duration={repr(self.duration)})"

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

    def duration_ts_srt(self):
        """
        Returns the start and end timestamps of the line's duration in SRT format
        """
        return f"{self.duration_ts_start_srt()} --> {self.duration_ts_end_srt()}"

    def to_dict(self):
        """
        Returns a dictionary representation of the RecognitionLine object with timestamp and text keys
        """
        return {
            'timestamp': self.duration_ts_srt(),
            'text': self.text
        }
