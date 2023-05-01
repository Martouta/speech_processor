import logging
from app.muted_stdout_stderr import muted_stdout_stderr
import speech_recognition as sr


class GoogleSpeechRecognizer:
    @staticmethod
    def call(filepath, language):
        try:
            with sr.AudioFile(filepath) as audiofile:
                recognizer = sr.Recognizer()
                audio = recognizer.record(audiofile)
                with muted_stdout_stderr():
                    text = recognizer.recognize_google(
                        audio, language=language)
                return text if text else None
        except (sr.RequestError, sr.UnknownValueError) as error:
            logging.getLogger(__name__).error(f"{type(error)} - {error}")
            return
