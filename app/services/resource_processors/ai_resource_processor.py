import logging

from app.models.resource_audio import ResourceAudio
from app.services.temporary_files_cleaner import TemporaryFilesCleaner
from .resource_processor import ResourceProcessor


class AiResourceProcessor(ResourceProcessor):
    def call(self):
        self.log_step(0)
        filepath = self.input_item.save()
        self.log_step(1)
        audio = ResourceAudio.save_as_wav(self.recognition_id(), filepath)
        self.log_step(2)
        audio.split_into_chunks()
        self.log_step(3)
        subtitle = audio.recognize_all_chunks(self.input_item.recognizer_data)
        self.log_step(4)
        subs_location = subtitle.save_subs(self.input_item.resource_id)
        self.log_step(5)
        TemporaryFilesCleaner.call(self.recognition_id(), filepath)
        self.log_step(6)
        return self.response(subs_location)

    def log_step(self, step_number):
        total_steps = 6
        steps = [
            f"[1/{total_steps}] Downloading multimedia from URL ... [{self.recognition_id()}]",
            f"[2/{total_steps}] Saving audio as WAP ... [{self.recognition_id()}]",
            f"[3/{total_steps}] Spliting into chunks ... [{self.recognition_id()}]",
            f"[4/{total_steps}] Recognizing chunks ... [{self.recognition_id()}]",
            f"[5/{total_steps}] Saving subtitles ... [{self.recognition_id()}]",
            f"[6/{total_steps}] Cleaning up temporary generated files ... [{self.recognition_id()}]",
            f"[DONE] [{self.recognition_id()}]"
        ]
        logging.info(steps[step_number])
