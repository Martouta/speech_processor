from app.models.duration import Duration
from app.models.recognition_line import RecognitionLine
from app.models.subtitle import Subtitle
from app.muted_stdout_stderr import muted_stdout_stderr
from youtube_transcript_api import YouTubeTranscriptApi


class YoutubeCaptionsFetcher:
    @staticmethod
    def call(recognition_id, video_id, language):
        with muted_stdout_stderr():
            captions_list = YoutubeCaptionsFetcher._get_available_captions(video_id)
            manual_captions = YoutubeCaptionsFetcher._manual_captions(captions_list, language)

        if manual_captions is None:
            raise ValueError(
                f"No manual captions found for video ID {video_id} and language {language}")

        transcript_json = YoutubeCaptionsFetcher._captions_to_json(
            manual_captions)

        subtitle = YoutubeCaptionsFetcher._json_to_subtitles(
            transcript_json, recognition_id, language)

        return subtitle

    @staticmethod
    def _get_available_captions(video_id):
        return YouTubeTranscriptApi.list_transcripts(video_id)

    @staticmethod
    def _manual_captions(captions_list, language):
        for transcript in captions_list:
            if transcript.language_code == language[:2] and not transcript.is_generated:
                return transcript
        return None

    @staticmethod
    def _captions_to_json(captions):
        return captions.fetch()

    @staticmethod
    def _json_to_subtitles(transcript_json, recognition_id, language):
        lines = []
        for line in transcript_json:
            start = line['start']
            end = start + line['duration']
            duration = Duration(start, end)
            recognition_line = RecognitionLine(line['text'], duration)
            lines.append(recognition_line)

        return Subtitle(recognition_id=recognition_id, lines=lines, language=language)
