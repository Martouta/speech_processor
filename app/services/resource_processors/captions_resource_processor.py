import logging

from app.services.youtube_captions_fetcher import YoutubeCaptionsFetcher
from .resource_processor import ResourceProcessor


class CaptionsResourceProcessor(ResourceProcessor):
    def call(self):
        self.log_step(0)
        logging.info(f"Fetching captions for {self.input_item.id} ...")
        subtitle = YoutubeCaptionsFetcher.call(
            self.input_item.recognition_id, self.input_item.id, self.input_item.language_code())
        subs_location = subtitle.save_subs(self.input_item.resource_id)
        self.log_step(1)
        return self.response(subs_location)

    def log_step(self, step_number):
        total_steps = 2
        steps = [
            f"[1/{total_steps}] Fetching captions from YouTube ... [{self.recognition_id()}]",
            f"[2/{total_steps}] Saving subtitles ... [{self.recognition_id()}]",
            f"[DONE] [{self.recognition_id()}]",
        ]
        logging.info(steps[step_number])
