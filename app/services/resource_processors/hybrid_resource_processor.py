import logging
from app.services.resource_processors.ai_resource_processor import AiResourceProcessor
from app.services.resource_processors.captions_resource_processor import CaptionsResourceProcessor
from .resource_processor import ResourceProcessor


class HybridResourceProcessor(ResourceProcessor):
    def call(self):
        try:
            return CaptionsResourceProcessor(self.input_item).call()
        except Exception:
            logging.info(f"[Hybrid] CaptionsResourceProcessor failed for '{self.recognition_id()}' ...")
            return AiResourceProcessor(self.input_item).call()
