# Speech Processor

[![Maintainability](https://api.codeclimate.com/v1/badges/152b7d7c3208b39b8b0a/maintainability)](https://codeclimate.com/github/Martouta/speech_processor/maintainability)

[![Test Coverage](https://api.codeclimate.com/v1/badges/152b7d7c3208b39b8b0a/test_coverage)](https://codeclimate.com/github/Martouta/speech_processor/test_coverage)

[![CircleCI](https://circleci.com/gh/Martouta/speech_processor.svg?style=svg)](https://app.circleci.com/pipelines/github/Martouta/speech_processor)

📗 This project fetches videos and audios from the internet, then it tries to identify their texts through __Google Cloud Speech-To-Text__ and it saves the results.

🧑‍💻 This documentation used to be mostly addressed to non-developers. Now, it is addressed only to developers. Otherwise, it would get crazy how much I would have to explain.

⚠️ The main branch is used for development. It is not a stable branch for usage.
Please, use a release instead. Preferably, the latest.

🐞 When there is an error for any item being processed (non-system-exiting exceptions), it just logs the information of the error/exception and carries on to the next item.

## How does it work

### Install dependencies
Install [Python version 3.10 or newer](https://www.python.org/downloads/).
Python is already installed by default in Linux and Mac but no idea about Windows. To know the version, run in the Terminal: `python3 -V` or `python -V`.
Then install the dependencies (external libraries necessary for this program to work). With this command in the Terminal:
`pip3 install --no-cache-dir -r requirements.txt --user`

For developers, you can also use Docker. And the requirements for development/test are in `requirements-dev.txt`

### Run the program
Have a file with extension `.json` in your computer with the following format:
```json
[
  {"id": "yt_zWQJqt_D-vo", "youtube_reference_id": "zWQJqt_D-vo", "language_code": "ar"},
  {"id": "yt_CNHe4qXqsck", "youtube_reference_id": "CNHe4qXqsck", "language_code": "ar"},
  {"id": "tiktok_7105531486224370946", "tiktok_reference_id": "7105531486224370946", "language_code": "en-au"},
  {
    "id": "example_mp4",
    "video": {
      "url": "https://file-examples-com.github.io/uploads/2017/04/file_example_MP4_480_1_5MG.mp4",
      "filename": "example_mp4",
      "extension": "mp4"
    },
    "language_code": "en-US"
  },
  {
    "id": "example_mp3",
    "audio": {
      "url": "https://file-examples-com.github.io/uploads/2017/11/file_example_MP3_700KB.mp3",
      "filename": "example_mp3",
      "extension": "mp3"
    },
    "language_code": "en-US"
  }
]
```
Each line there is a resource (video or audio) that you want to be processed.
It must follow these characteristics:

- **id** can be whatever you want as long as it is not empty and it is unique for each video/audio for all those resources running at the same time.

- **language_code** must be a language code from the list in [Documentation of Language Support of Google Cloud Speech-To-Text](https://cloud.google.com/speech-to-text/docs/languages). Plus, for Arabic fus7a is just "ar".

- **tiktok_reference_id** must only be provided for tiktok videos and it is the *id* of the video. For example, for a URL like `https://www.tiktok.com/@robertirwin/video/7105531486224370946`, this would be just `7105531486224370946`.

- **youtube_reference_id** must only be provided for youtube videos and it is the *id* of the video. For example, for a URL like `https://www.youtube.com/watch?v=zWQJqt_D-vo`, this would be just `zWQJqt_D-vo`.

- **video** is only provided when the resource is a video that you can directly 'save' from the URL and it must be a 'mp4'. Then it contains **url** with the URL, **filename** with whatever unique name you want and **extension** 'mp4'.

- **audio** is exactly like *video* but for an audio. The extension must be either 'mp3' or 'wav'.

Then run the following command in the Terminal from the directory where you have this program, given that MAX_THREADS is the number of videos/audios you want to be processed at once and that INPUT_FILE is the path/location of the JSON file mentioned above.
```bash
MAX_THREADS=8 INPUT_FILE='example_input.json' SPEECH_ENV='production' SUBS_LOCATION='file' python3 -u . --user
```

They will be saved inside this program folder, in `subtitles/production`.

For developers:

- The input can either be a json file as shown or it can be listening through kafka with the url `KAFKA_URL` and the topic `KAFKA_RESOURCE_TOPIC`.

- The output can be either a file as shown or MongoDB with the url `MONGO_URL` and the database `MONGO_DB`.
