class RecognitionLine:
    def __init__(self, line_text, duration):
        self.text = line_text
        self.duration = duration

    def __str__(self):
        return f"{self.duration.ts_start_srt()};{self.duration.ts_end_srt()};{self.text}"
