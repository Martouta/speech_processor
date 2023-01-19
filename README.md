# Speech Processor [![Maintainability](https://api.codeclimate.com/v1/badges/152b7d7c3208b39b8b0a/maintainability)](https://codeclimate.com/github/Martouta/speech_processor/maintainability) [![CircleCI](https://circleci.com/gh/Martouta/speech_processor.svg?style=svg)](https://app.circleci.com/pipelines/github/Martouta/speech_processor) [![Coverage Status](https://coveralls.io/repos/github/Martouta/speech_processor/badge.svg?branch=main)](https://coveralls.io/github/Martouta/speech_processor?branch=main)

📗 This project fetches videos and audios from the internet, then it tries to identify their texts through __Google Cloud Speech-To-Text__ and it saves the results.

🧑‍💻 This documentation used to be mostly addressed to non-developers. Now, it is addressed only to developers. Otherwise, it would get crazy how much I would have to explain.

⚠️ The main branch is used for development. It is not a stable branch for usage.
Please, use a release instead. Preferably, the latest.

🐞 When there is an error for any item being processed (non-system-exiting exceptions), it just logs the information of the error/exception and carries on to the next item.

## Table of Contents

- [Speech Processor](#speech-processor)
  - [Table of Contents](#table-of-contents)
  - [Install dependencies](#install-dependencies)
  - [Expected input](#expected-input)
    - [Origin of videos/audios](#origin-of-videos-audios)
      - [Fetch videos/audios from a file](#fetch-videos-audios-from-a-file)
      - [Fetch videos/audios from Kafka](#fetch-videos-audios-from-kafka)
    - [Additional input information through ENV vars](#additional-input-information-through-env-vars)
    - [Input Format](#input-format)
  - [Expected output](#expected-output)
    - [Destination](#destination)
      - [Save in a file](#save-in-a-file)
      - [Save in MongoDB](#save-in-mongodb)
    - [Output Format](#output-format)

## Install dependencies

1. Install [Python version 3.11 or newer](https://www.python.org/downloads/).
2. Install the dependencies (external libraries necessary for this program to work). With this command in the Terminal:
`pip3 install --no-cache-dir -r requirements.txt --user`

You can also use Docker. And the requirements for development/test are in `requirements-dev.txt`

## Expected input

### Origin of videos/audios

The input data can come from either a __file__ or __kafka__ . If the environment variable __INPUT_FILE__ is provided, it assumes it comes from a file. Otherwise, it expects to come from Kafka.
The project for now it is assuming that you pass this data correctly.

#### Fetch videos/audios from a file

The environment variable __INPUT_FILE__ must be the path of the file in your HDD.
The project for now it is assuming that the file is actually there and the program has reading permissions for this file.

#### Fetch videos/audios from Kafka

It uses the environment variables __KAFKA_URL__ (if not provided, it defaults to __localhost:9092__) and it requires __KAFKA_RESOURCE_TOPIC__.
It will read the kafka messages from that URI and that topic and partition/group_id number 1.
If KAFKA is not running in the provided URI, it just sleeps/wait until it is available.

### Additional input information through ENV vars

- __MAX_THREADS__ is how many items run at once. It is optional and by default it is 5.
- __SPEECH_ENV__ is the environment the project is running in. It is required. It must be either __production__, __test__ or __development__ . I'm assuming that it is being passed correctly.

### Input Format

The project for now it is assuming that you pass this data correctly.
Example of a JSON type with multiple items having all possible inputs:

```json
[
  {
    "integration": "youtube",
    "id": "zWQJqt_D-vo",
    "language_code": "ar",
    "resource_id": 1
  },
  {
    "integration": "youtube",
    "id": "CNHe4qXqsck",
    "language_code": "ar",
    "resource_id": 2
  },
  {
    "integration": "tiktok",
    "id": "7105531486224370946",
    "language_code": "en-au",
    "resource_id": 3
  },
  {
    "integration": "hosted",
    "url": "https://scontent-mad1-1.cdninstagram.com/v/t50.16885-16/10000000_4897336923689152_6953647669213471758_n.mp4?efg=eyJ2ZW5jb2RlX3RhZyI6InZ0c192b2RfdXJsZ2VuLjEyODAuaWd0di5iYXNlbGluZSIsInFlX2dyb3VwcyI6IltcImlnX3dlYl9kZWxpdmVyeV92dHNfb3RmXCJdIn0&_nc_ht=scontent-mad1-1.cdninstagram.com&_nc_cat=104&_nc_ohc=OfiUjon4e6AAX8fa1iX&edm=ALQROFkBAAAA&vs=504042498033080_1629363706&_nc_vs=HBksFQAYJEdJQ1dtQURBa0s0YkdtWVJBQTRrc1pDMlVZQmdidlZCQUFBRhUAAsgBABUAGCRHSS1IaXhDdlJKbUlTdHdLQUNYaDgzbUpqb1JWYnZWQkFBQUYVAgLIAQAoABgAGwGIB3VzZV9vaWwBMRUAACbwmrGErMDmPxUCKAJDMywXQFeRBiTdLxsYEmRhc2hfYmFzZWxpbmVfMV92MREAdewHAA%3D%3D&ccb=7-5&oe=62AC1A5F&oh=00_AT9ijqEfW1SCDHUqt3KK79FNnZmlzE9lqGMEegg35y58VQ&_nc_sid=30a2ef",
    "language_code": "en-US",
    "resource_id": 4
  },
  {
    "integration": "hosted",
    "url": "https://lang_src.s3.amazonaws.com/7a.mp3",
    "language_code": "en-US",
    "resource_id": 5
  },
  {
    "integration": "local",
    "path": "tests/fixtures/example.mp3",
    "language_code": "ar",
    "resource_id": 6
  }
]
```

For each item, each of those parameters are mandatory. This is what they mean:

- __integration__ must be one of these options: __youtube__, __tiktok__ or __hosted__. The latter means that it is directly downloadable from that link, and it is either a video (with audio in the video) or an audio.

- __id__ is used for items that are located in either tiktok or youtube. It is the the __id__ of the video in those websites. For example:
  - For __tiktok__, given a URL like `https://www.tiktok.com/@robertirwin/video/7105531486224370946`, the __id__ would be just `7105531486224370946`.
  - For __youtube__, given a URL like `https://www.youtube.com/watch?v=zWQJqt_D-vo`, this would be just `zWQJqt_D-vo`.

- __url__ is provided only for hosted items. It's the URL where you can directly download the item. No scrapping involved. The only supported formats are any format supported by `pydub`'s `AudioSegment.from_file`, like mp4, mp3, wav, m4a and webm.

- __path__ is only provided for local items. It is where you have the resource in the same machine where you are running this program.

- __language_code__ must be a language code from the list in [Documentation of Language Support of Google Cloud Speech-To-Text](https://cloud.google.com/speech-to-text/docs/languages). Plus, for Arabic fus7a is just "ar".

- __resource_id__ is an optional parameter that should not matter to you unless you want the output to be saved in MongoDB. In this case, it must be an integer.

## Expected output

### Destination

The output data can be saved in either a __file__ or __mongodb__ .
The environment variable __SUBS_LOCATION__ can be either __mongodb__ or __file__ and by default it assumes __mongodb__.

#### Save in a file

It saves it inside this same project path, in __resources/subtitles__, in one of its 3 subfolders: __development__, __test__ and __production__ depending on which environment you are in, which it takes from the environment variable __SPEECH_ENV__. It's saved in a SRT file (including the timestamps) in the right format.

#### Save in MongoDB

It uses the environment variables __MONGO_URL__ (if not provided, it defaults to __localhost:27017__) and it requires __MONGO_DB__ for the database collection name.
For mongodb, it assumes that you pass all the data correctly, that it is running and that you can actually connect and write there from this project.

### Output Format

- The format in the __file__ is just the text as it is.
- The format in __mongodb__, it saves it in the following format:

```javascript
{
  'resource_id': 1, // The resource_id provided in the input of the item. If not provided, it default to -1.
  'lines': "example of text processed", // The text processed itself. It is saved in an array of strings.
  'language_code': 'ar', // The same value as the 'language_code' of the input given for this item.
  'created_at': 06/11/2022, 18:54:36 // It is a datetime value type. The current datetime (in UTC) at the moment the text is saved.
}
```
