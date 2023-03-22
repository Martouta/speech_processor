import speech_recognition as sr
import os


class MicrosoftAzureSpeechRecognizer:
    @staticmethod
    def call(filepath, language):
        try:
            api_key = os.environ.get('MS_AZURE_SPEECH_API_KEY')
            recognizer = sr.Recognizer()
            with sr.AudioFile(filepath) as source:
                audio = recognizer.record(source)
            text, _ = recognizer.recognize_azure(
                audio, key=api_key, language=language)
            return text if text else None
        except Exception as e:
            print(f"Error recognizing speech: {e}")
            return None
