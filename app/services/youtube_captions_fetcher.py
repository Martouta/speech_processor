import json
from app.models.duration import Duration
from app.models.recognition_line import RecognitionLine
from app.models.subtitle import Subtitle
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter


class YoutubeCaptionsFetcher:
    @staticmethod
    def call(video_id, language):
        # Get the available captions for the video
        captions_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # Check if the desired captions exist and are not auto-generated
        manual_captions = None
        for transcript in captions_list:
            if transcript.language_code == language[:2] and not transcript.is_generated:
                manual_captions = transcript
                break

        # Raise an error if manual captions do not exist
        if manual_captions is None:
            raise ValueError(
                f"No manual captions found for video ID {video_id} and language {language}")

        # Fetch the captions and convert them to the JSON format
        transcript_json = json.loads(
            JSONFormatter().format_transcript(manual_captions.fetch()))

        # Convert the JSON format to the Subtitle format
        lines = []
        for line in transcript_json:
            start = line['start']
            end = start + line['duration']
            duration = Duration(start, end)
            recognition_line = RecognitionLine(line['text'], duration)
            lines.append(recognition_line)

        return Subtitle(recognition_id=video_id, lines=lines, language=language)
