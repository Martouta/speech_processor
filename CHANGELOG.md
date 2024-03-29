# Changelog

## [v3.0.0](https://github.com/Martouta/speech_processor/tree/v3.0.0) (2023-04-08)

[Full Changelog](https://github.com/Martouta/speech_processor/compare/v2.0.1...v3.0.0)

**Fixed bugs:**

- \[Bug\] Error trying to download tiktok - Browser closed unexpectedly [\#103](https://github.com/Martouta/speech_processor/issues/103)
- 🐛 🐞 Fix bugs of \#61 [\#184](https://github.com/Martouta/speech_processor/pull/184) ([Martouta](https://github.com/Martouta))

**Closed issues:**

- Do not save subtitles if the whole thing is empty 😂 [\#161](https://github.com/Martouta/speech_processor/issues/161)
- Support audio .m4a [\#135](https://github.com/Martouta/speech_processor/issues/135)
- Support webm [\#130](https://github.com/Martouta/speech_processor/issues/130)
- Allow to run resources with local paths [\#129](https://github.com/Martouta/speech_processor/issues/129)
- For YouTube, get the subtitles/captions when they are already in Youtube [\#61](https://github.com/Martouta/speech_processor/issues/61)
- Save timestamp in subtitles [\#57](https://github.com/Martouta/speech_processor/issues/57)
- Remove support for Google Cloud Speech-To-Text if they carry on with Project Nimbus \(apartheid support\) 🇵🇸 💪🏽 [\#15](https://github.com/Martouta/speech_processor/issues/15)
- Add support for other Speech-to-Text AI platforms 🗣️  [\#14](https://github.com/Martouta/speech_processor/issues/14)

**Merged pull requests:**

- Make ResourceAudio.save\_as\_wav more memory-friendly 🐘 [\#189](https://github.com/Martouta/speech_processor/pull/189) ([Martouta](https://github.com/Martouta))
- Import only very minimal stuff if \_\_init\_\_ to 'app' [\#186](https://github.com/Martouta/speech_processor/pull/186) ([Martouta](https://github.com/Martouta))
- Allow for "captions" to try if present manual captions, otherwise go for IA 🏗️ [\#185](https://github.com/Martouta/speech_processor/pull/185) ([Martouta](https://github.com/Martouta))
- Bump google-cloud-speech from 2.18.0 to 2.19.0 [\#180](https://github.com/Martouta/speech_processor/pull/180) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump pytube from 12.1.2 to 12.1.3 [\#179](https://github.com/Martouta/speech_processor/pull/179) ([dependabot[bot]](https://github.com/apps/dependabot))
- \[Refactor\] Clean up issue \#61 [\#177](https://github.com/Martouta/speech_processor/pull/177) ([Martouta](https://github.com/Martouta))
- Add \_\_eq\_\_ to Subtitle and RecognitionLine [\#176](https://github.com/Martouta/speech_processor/pull/176) ([Martouta](https://github.com/Martouta))
- Get the manual subtitles/captions from Youtube \(optionally\) - if not present, do nothing [\#175](https://github.com/Martouta/speech_processor/pull/175) ([Martouta](https://github.com/Martouta))
- Save timestamps in MongoDB [\#174](https://github.com/Martouta/speech_processor/pull/174) ([Martouta](https://github.com/Martouta))
- Don't save Subtitles with empty lines [\#173](https://github.com/Martouta/speech_processor/pull/173) ([Martouta](https://github.com/Martouta))
- Use PyTube 12.1.2 [\#172](https://github.com/Martouta/speech_processor/pull/172) ([Martouta](https://github.com/Martouta))
- \[Snyk\] Security upgrade setuptools from 39.0.1 to 65.5.1 [\#171](https://github.com/Martouta/speech_processor/pull/171) ([Martouta](https://github.com/Martouta))
- \[Snyk\] Security upgrade setuptools from 39.0.1 to 65.5.1 [\#170](https://github.com/Martouta/speech_processor/pull/170) ([Martouta](https://github.com/Martouta))
- Support language param in Speech Recognizer\(s\) [\#169](https://github.com/Martouta/speech_processor/pull/169) ([Martouta](https://github.com/Martouta))
- \[Refactor\] Fix LoD in TestResourceJSONToInputItem [\#168](https://github.com/Martouta/speech_processor/pull/168) ([Martouta](https://github.com/Martouta))
- Add Microsoft Azure Speech Recognizer [\#167](https://github.com/Martouta/speech_processor/pull/167) ([Martouta](https://github.com/Martouta))
- \[Doc\] Rename ASSEMBLYAI\_SECRET\_KEY -\> ASSEMBLYAI\_API\_KEY [\#166](https://github.com/Martouta/speech_processor/pull/166) ([Martouta](https://github.com/Martouta))
- \[Doc\] Add support for other Speech-to-Text AI platforms [\#165](https://github.com/Martouta/speech_processor/pull/165) ([Martouta](https://github.com/Martouta))
- Add AssemblyAI Speech Recognizer [\#164](https://github.com/Martouta/speech_processor/pull/164) ([Martouta](https://github.com/Martouta))
- Add OpenAI Whisper Speech Recognizer [\#163](https://github.com/Martouta/speech_processor/pull/163) ([Martouta](https://github.com/Martouta))
- Add Gladia Speech Recognizer [\#162](https://github.com/Martouta/speech_processor/pull/162) ([Martouta](https://github.com/Martouta))
- Add RecognizerData [\#160](https://github.com/Martouta/speech_processor/pull/160) ([Martouta](https://github.com/Martouta))
- Rename SpeechProcessor -\> GoogleSpeechProcessor [\#159](https://github.com/Martouta/speech_processor/pull/159) ([Martouta](https://github.com/Martouta))
- Add support for other Speech-to-Text AI platforms 🗣️  [\#158](https://github.com/Martouta/speech_processor/pull/158) ([Martouta](https://github.com/Martouta))
- Bump pytest from 7.2.1 to 7.2.2 [\#155](https://github.com/Martouta/speech_processor/pull/155) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump google-cloud-speech from 2.17.3 to 2.18.0 [\#154](https://github.com/Martouta/speech_processor/pull/154) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump google-cloud-speech from 2.17.2 to 2.17.3 [\#151](https://github.com/Martouta/speech_processor/pull/151) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump google-cloud-speech from 2.17.1 to 2.17.2 [\#150](https://github.com/Martouta/speech_processor/pull/150) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump google-cloud-speech from 2.17.0 to 2.17.1 [\#149](https://github.com/Martouta/speech_processor/pull/149) ([dependabot[bot]](https://github.com/apps/dependabot))
- \[Doc\] Add docstring descriptions to the public functions in RecognitionLine Model [\#147](https://github.com/Martouta/speech_processor/pull/147) ([Martouta](https://github.com/Martouta))
- \[Doc\] Add docstring descriptions to the public functions in 'resource\_message\_to\_json' converter [\#146](https://github.com/Martouta/speech_processor/pull/146) ([Martouta](https://github.com/Martouta))
- \[Doc\] Add docstring descriptions to the public functions in InputItemLocal [\#144](https://github.com/Martouta/speech_processor/pull/144) ([Martouta](https://github.com/Martouta))
- \[Doc\] Add docstring descriptions to the public functions in Duration model [\#143](https://github.com/Martouta/speech_processor/pull/143) ([Martouta](https://github.com/Martouta))
- \[Refactor\] Extract Network requests into a Service class [\#142](https://github.com/Martouta/speech_processor/pull/142) ([Martouta](https://github.com/Martouta))
- Do not save empty lines in subs [\#141](https://github.com/Martouta/speech_processor/pull/141) ([Martouta](https://github.com/Martouta))
- Add models Duration & RecognitionLine [\#140](https://github.com/Martouta/speech_processor/pull/140) ([Martouta](https://github.com/Martouta))
- Bump google-cloud-speech from 2.16.2 to 2.17.0 [\#139](https://github.com/Martouta/speech_processor/pull/139) ([dependabot[bot]](https://github.com/apps/dependabot))
- Save timestamp in SRT subtitles \(in files\) - even empty lines 😂 [\#138](https://github.com/Martouta/speech_processor/pull/138) ([Martouta](https://github.com/Martouta))
- Support any extension/format allowed by AudioSegment [\#136](https://github.com/Martouta/speech_processor/pull/136) ([Martouta](https://github.com/Martouta))
- Bump pytest from 7.2.0 to 7.2.1 [\#134](https://github.com/Martouta/speech_processor/pull/134) ([dependabot[bot]](https://github.com/apps/dependabot))
- Decrease ResourceAudio's min\_silence\_len 500-\>400 [\#133](https://github.com/Martouta/speech_processor/pull/133) ([Martouta](https://github.com/Martouta))
- Allow to run resources with local paths [\#131](https://github.com/Martouta/speech_processor/pull/131) ([Martouta](https://github.com/Martouta))
- Bump speechrecognition from 3.8.1 to 3.9.0 [\#127](https://github.com/Martouta/speech_processor/pull/127) ([dependabot[bot]](https://github.com/apps/dependabot))
- Revert "\[Doc\] It does not require a headless browser" [\#126](https://github.com/Martouta/speech_processor/pull/126) ([Martouta](https://github.com/Martouta))
- \[Doc\] It does not require a headless browser [\#125](https://github.com/Martouta/speech_processor/pull/125) ([Martouta](https://github.com/Martouta))
- Bump mako from 1.2.3 to 1.2.4 [\#124](https://github.com/Martouta/speech_processor/pull/124) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump pymongo from 4.3.2 to 4.3.3 [\#123](https://github.com/Martouta/speech_processor/pull/123) ([dependabot[bot]](https://github.com/apps/dependabot))
- Update Python to 3.11 [\#122](https://github.com/Martouta/speech_processor/pull/122) ([Martouta](https://github.com/Martouta))
- Bump pytest from 7.1.3 to 7.2.0 [\#121](https://github.com/Martouta/speech_processor/pull/121) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump pymongo from 4.2.0 to 4.3.2 [\#120](https://github.com/Martouta/speech_processor/pull/120) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump google-cloud-speech from 2.16.1 to 2.16.2 [\#119](https://github.com/Martouta/speech_processor/pull/119) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump google-cloud-speech from 2.16.0 to 2.16.1 [\#118](https://github.com/Martouta/speech_processor/pull/118) ([dependabot[bot]](https://github.com/apps/dependabot))
- Add .coverage to .gitignore [\#117](https://github.com/Martouta/speech_processor/pull/117) ([Martouta](https://github.com/Martouta))
- Bump google-cloud-speech from 2.15.1 to 2.16.0 [\#116](https://github.com/Martouta/speech_processor/pull/116) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump coverage from 6.4.4 to 6.5.0 [\#115](https://github.com/Martouta/speech_processor/pull/115) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump mako from 1.2.2 to 1.2.3 [\#114](https://github.com/Martouta/speech_processor/pull/114) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump pytest from 7.1.2 to 7.1.3 [\#113](https://github.com/Martouta/speech_processor/pull/113) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump mako from 1.2.1 to 1.2.2 [\#112](https://github.com/Martouta/speech_processor/pull/112) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump requests-mock from 1.9.3 to 1.10.0 [\#111](https://github.com/Martouta/speech_processor/pull/111) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump coverage from 6.4.3 to 6.4.4 [\#110](https://github.com/Martouta/speech_processor/pull/110) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump google-cloud-speech from 2.15.0 to 2.15.1 [\#109](https://github.com/Martouta/speech_processor/pull/109) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump coverage from 6.4.2 to 6.4.3 [\#108](https://github.com/Martouta/speech_processor/pull/108) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v2.0.1](https://github.com/Martouta/speech_processor/tree/v2.0.1) (2022-07-28)

[Full Changelog](https://github.com/Martouta/speech_processor/compare/v2.0.0...v2.0.1)

**Fixed bugs:**

- \[Bugfix\] Error trying to download tiktok - Browser closed unexpectedly [\#107](https://github.com/Martouta/speech_processor/pull/107) ([Martouta](https://github.com/Martouta))

**Merged pull requests:**

- Bump pymongo from 4.1.1 to 4.2.0 [\#106](https://github.com/Martouta/speech_processor/pull/106) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump google-cloud-speech from 2.14.1 to 2.15.0 [\#105](https://github.com/Martouta/speech_processor/pull/105) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump coverage from 6.4.1 to 6.4.2 [\#104](https://github.com/Martouta/speech_processor/pull/104) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump mako from 1.2.0 to 1.2.1 [\#102](https://github.com/Martouta/speech_processor/pull/102) ([dependabot[bot]](https://github.com/apps/dependabot))
- \[Docker Compose\] Remove ports from SpeechProcessor [\#101](https://github.com/Martouta/speech_processor/pull/101) ([Martouta](https://github.com/Martouta))

## [v2.0.0](https://github.com/Martouta/speech_processor/tree/v2.0.0) (2022-06-16)

[Full Changelog](https://github.com/Martouta/speech_processor/compare/v1.0.7...v2.0.0)

**Fixed bugs:**

- \[Bug\] \[YouTube\] pytube.exceptions.RegexMatchError: \_\_init\_\_: could not find match for ^\w+\W [\#66](https://github.com/Martouta/speech_processor/issues/66)
- \[Bugfix\] \[YouTube\] pytube.exceptions.RegexMatchError: \_\_init\_\_: could not find match for ^\w+\W [\#72](https://github.com/Martouta/speech_processor/pull/72) ([Martouta](https://github.com/Martouta))

**Closed issues:**

- Check and do or discard the optional tasks of \#75 [\#80](https://github.com/Martouta/speech_processor/issues/80)
- Add a changelog for version 2.0.0 [\#74](https://github.com/Martouta/speech_processor/issues/74)
- With the requirements pointing to forked repos, point to a tag instead of a branch [\#73](https://github.com/Martouta/speech_processor/issues/73)
- Set up Test Coverage [\#7](https://github.com/Martouta/speech_processor/issues/7)
- Clarify what 'GOOGLE\_LOCAL' means. [\#1](https://github.com/Martouta/speech_processor/issues/1)

**Merged pull requests:**

- Rename type -\> integration [\#100](https://github.com/Martouta/speech_processor/pull/100) ([Martouta](https://github.com/Martouta))
- Set up CHANGELOG 💃🏻 [\#99](https://github.com/Martouta/speech_processor/pull/99) ([Martouta](https://github.com/Martouta))
- Test Youtube download params & Fix YT Tests [\#98](https://github.com/Martouta/speech_processor/pull/98) ([Martouta](https://github.com/Martouta))
- \[Refactor\] Remove unused imports from TestResourceAudio + Use GOOGLE\_API\_URL [\#97](https://github.com/Martouta/speech_processor/pull/97) ([Martouta](https://github.com/Martouta))
- Test exceptions of recognising an audio [\#96](https://github.com/Martouta/speech_processor/pull/96) ([Martouta](https://github.com/Martouta))
- Ensure and test \_\_str\_\_ for models [\#95](https://github.com/Martouta/speech_processor/pull/95) ([Martouta](https://github.com/Martouta))
- Remove extension and get it from the URL for hosted [\#94](https://github.com/Martouta/speech_processor/pull/94) ([Martouta](https://github.com/Martouta))
- \[Refactor\] Use InputItems instead of the downloaders [\#93](https://github.com/Martouta/speech_processor/pull/93) ([Martouta](https://github.com/Martouta))
- \[CircleCI\] Upgrade to a next-gen Docker convenience image. [\#92](https://github.com/Martouta/speech_processor/pull/92) ([Martouta](https://github.com/Martouta))
- \[Refactor\] Remove json\_input\_resources file in favor of fetch\_input\_messages [\#91](https://github.com/Martouta/speech_processor/pull/91) ([Martouta](https://github.com/Martouta))
- Replace hosted\_audio|video in JSONs [\#90](https://github.com/Martouta/speech_processor/pull/90) ([Martouta](https://github.com/Martouta))
- Add Makefile to execute locally some common commands [\#89](https://github.com/Martouta/speech_processor/pull/89) ([Martouta](https://github.com/Martouta))
- Replace hosted\_audio|video for just 'hosted' and remove filename param [\#88](https://github.com/Martouta/speech_processor/pull/88) ([Martouta](https://github.com/Martouta))
- \[Refactor\] Use resources/multimedia path instead of resources/videos|audios [\#87](https://github.com/Martouta/speech_processor/pull/87) ([Martouta](https://github.com/Martouta))
- \[Refactor\] Extract fetch\_input\_messages from \_\_main\_\_ into its own file [\#86](https://github.com/Martouta/speech_processor/pull/86) ([Martouta](https://github.com/Martouta))
- In requirements\*.txt, point to git tags/releases instead of branches [\#85](https://github.com/Martouta/speech_processor/pull/85) ([Martouta](https://github.com/Martouta))
- \[CircleCI\] Do not install python-dev or gcc [\#84](https://github.com/Martouta/speech_processor/pull/84) ([Martouta](https://github.com/Martouta))
- Organise project \(app\) and resources into some subfolders [\#83](https://github.com/Martouta/speech_processor/pull/83) ([Martouta](https://github.com/Martouta))
- Upload Test Coverage to Coveralls [\#82](https://github.com/Martouta/speech_processor/pull/82) ([Martouta](https://github.com/Martouta))
- Set up test coverage [\#81](https://github.com/Martouta/speech_processor/pull/81) ([Martouta](https://github.com/Martouta))
- Recognise chunks in Google Cloud only through default credentials [\#79](https://github.com/Martouta/speech_processor/pull/79) ([Martouta](https://github.com/Martouta))
- \[Doc\] Add project description and a few extra initial info to README [\#78](https://github.com/Martouta/speech_processor/pull/78) ([Martouta](https://github.com/Martouta))
- Adapt code to new input format for initial expectations of version 2.0.0 [\#77](https://github.com/Martouta/speech_processor/pull/77) ([Martouta](https://github.com/Martouta))
- Raise ValueError in Subtitle\#save\_subs if ENV SUBS\_LOCATION value is not supported [\#76](https://github.com/Martouta/speech_processor/pull/76) ([Martouta](https://github.com/Martouta))
- Document README for initial expectations of version 2.0.0 [\#75](https://github.com/Martouta/speech_processor/pull/75) ([Martouta](https://github.com/Martouta))
- \[CircleCI\] Run Tests verbosely and with warnings [\#71](https://github.com/Martouta/speech_processor/pull/71) ([Martouta](https://github.com/Martouta))
- Support TikTok videos \(through PyTikTokAPI==0.0.5 - no playwright required\) [\#70](https://github.com/Martouta/speech_processor/pull/70) ([Martouta](https://github.com/Martouta))
- Bump google-cloud-speech from 2.14.0 to 2.14.1 [\#69](https://github.com/Martouta/speech_processor/pull/69) ([dependabot[bot]](https://github.com/apps/dependabot))
- Skip test\_download\_multimedia\_for\_youtube only in CircleCI [\#68](https://github.com/Martouta/speech_processor/pull/68) ([Martouta](https://github.com/Martouta))
- Rename download\_multimedia\_from\_url -\> download\_multimedia [\#67](https://github.com/Martouta/speech_processor/pull/67) ([Martouta](https://github.com/Martouta))
- Remove port in ProcessResource test [\#65](https://github.com/Martouta/speech_processor/pull/65) ([Martouta](https://github.com/Martouta))
- Order pip requirements/dependencies alphabetically [\#64](https://github.com/Martouta/speech_processor/pull/64) ([Martouta](https://github.com/Martouta))
- Bump protobuf from 3.20.1 to 4.21.1 [\#62](https://github.com/Martouta/speech_processor/pull/62) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump google-cloud-speech from 2.13.1 to 2.14.0 [\#60](https://github.com/Martouta/speech_processor/pull/60) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v1.0.7](https://github.com/Martouta/speech_processor/tree/v1.0.7) (2022-05-14)

[Full Changelog](https://github.com/Martouta/speech_processor/compare/v1.0.6...v1.0.7)

**Closed issues:**

- For pytube, use only audio [\#56](https://github.com/Martouta/speech_processor/issues/56)

**Merged pull requests:**

- Download only audio for YouTube [\#58](https://github.com/Martouta/speech_processor/pull/58) ([Martouta](https://github.com/Martouta))
- Bump google-cloud-speech from 2.12.0 to 2.13.1 [\#45](https://github.com/Martouta/speech_processor/pull/45) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v1.0.6](https://github.com/Martouta/speech_processor/tree/v1.0.6) (2022-05-09)

[Full Changelog](https://github.com/Martouta/speech_processor/compare/v1.0.5...v1.0.6)

**Merged pull requests:**

- Bump pytube from 12.0.0 to 12.1.0 [\#55](https://github.com/Martouta/speech_processor/pull/55) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump pytest from 7.1.1 to 7.1.2 [\#53](https://github.com/Martouta/speech_processor/pull/53) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump protobuf from 3.20.0 to 3.20.1 [\#52](https://github.com/Martouta/speech_processor/pull/52) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump pymongo from 4.1.0 to 4.1.1 [\#51](https://github.com/Martouta/speech_processor/pull/51) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump pymongo from 4.0.2 to 4.1.0 [\#50](https://github.com/Martouta/speech_processor/pull/50) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump protobuf from 3.19.4 to 3.20.0 [\#49](https://github.com/Martouta/speech_processor/pull/49) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump pytest from 7.1.0 to 7.1.1 [\#48](https://github.com/Martouta/speech_processor/pull/48) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump pytest from 7.0.1 to 7.1.0 [\#47](https://github.com/Martouta/speech_processor/pull/47) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump mako from 1.1.6 to 1.2.0 [\#46](https://github.com/Martouta/speech_processor/pull/46) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump pymongo from 4.0.1 to 4.0.2 [\#44](https://github.com/Martouta/speech_processor/pull/44) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v1.0.5](https://github.com/Martouta/speech_processor/tree/v1.0.5) (2022-02-15)

[Full Changelog](https://github.com/Martouta/speech_processor/compare/v1.0.4...v1.0.5)

**Fixed bugs:**

- 2022-02-07 04:02:25,086 - root - ERROR - \<class 'AttributeError'\> : 'NoneType' object has no attribute 'span' [\#39](https://github.com/Martouta/speech_processor/issues/39)

**Merged pull requests:**

- Bump pytube from 11.0.2 to 12.0.0 [\#42](https://github.com/Martouta/speech_processor/pull/42) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump pytest from 7.0.0 to 7.0.1 [\#41](https://github.com/Martouta/speech_processor/pull/41) ([dependabot[bot]](https://github.com/apps/dependabot))
- \[Documentation\] Use local user's Python [\#40](https://github.com/Martouta/speech_processor/pull/40) ([Martouta](https://github.com/Martouta))

## [v1.0.4](https://github.com/Martouta/speech_processor/tree/v1.0.4) (2022-02-07)

[Full Changelog](https://github.com/Martouta/speech_processor/compare/v1.0.3...v1.0.4)

**Closed issues:**

- AttributeError: 'NoneType' object has no attribute 'span'; File "/usr/local/lib/python3.10/site-packages/pytube/parser.py" [\#33](https://github.com/Martouta/speech_processor/issues/33)

**Merged pull requests:**

- Bump pytest from 6.2.5 to 7.0.0 [\#38](https://github.com/Martouta/speech_processor/pull/38) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump protobuf from 3.19.3 to 3.19.4 [\#37](https://github.com/Martouta/speech_processor/pull/37) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump google-cloud-speech from 2.11.1 to 2.12.0 [\#36](https://github.com/Martouta/speech_processor/pull/36) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump protobuf from 3.19.1 to 3.19.3 [\#35](https://github.com/Martouta/speech_processor/pull/35) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v1.0.3](https://github.com/Martouta/speech_processor/tree/v1.0.3) (2021-12-16)

[Full Changelog](https://github.com/Martouta/speech_processor/compare/v1.0.2...v1.0.3)

**Merged pull requests:**

- Bump pytube from 11.0.1 to 11.0.2 [\#34](https://github.com/Martouta/speech_processor/pull/34) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v1.0.2](https://github.com/Martouta/speech_processor/tree/v1.0.2) (2021-12-13)

[Full Changelog](https://github.com/Martouta/speech_processor/compare/v1.0.1...v1.0.2)

**Merged pull requests:**

- Bump pymongo from 4.0 to 4.0.1 [\#32](https://github.com/Martouta/speech_processor/pull/32) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump pymongo from 3.12.1 to 4.0 [\#31](https://github.com/Martouta/speech_processor/pull/31) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump mako from 1.1.5 to 1.1.6 [\#30](https://github.com/Martouta/speech_processor/pull/30) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v1.0.1](https://github.com/Martouta/speech_processor/tree/v1.0.1) (2021-11-03)

[Full Changelog](https://github.com/Martouta/speech_processor/compare/v1.0.0...v1.0.1)

**Fixed bugs:**

- Bug: urllib.error.URLError: urlopen error \[SSL: CERTIFICATE\_VERIFY\_FAILED\] certificate verify failed: unable to get local issuer certificate [\#21](https://github.com/Martouta/speech_processor/issues/21)

**Closed issues:**

- Setup Python linters: flake8 + mypy + pydocstyle [\#10](https://github.com/Martouta/speech_processor/issues/10)
- \[CircleCI\] Do not always hold tests [\#8](https://github.com/Martouta/speech_processor/issues/8)
- Fix CodeClimate 1s code smells [\#5](https://github.com/Martouta/speech_processor/issues/5)
- Test JSON input/output [\#4](https://github.com/Martouta/speech_processor/issues/4)
- Setup Kafka in CircleCI [\#3](https://github.com/Martouta/speech_processor/issues/3)

**Merged pull requests:**

- Bump google-cloud-speech from 2.11.0 to 2.11.1 [\#29](https://github.com/Martouta/speech_processor/pull/29) ([dependabot[bot]](https://github.com/apps/dependabot))
- Process resource input JSON with and without wrapping [\#28](https://github.com/Martouta/speech_processor/pull/28) ([Martouta](https://github.com/Martouta))
- Update/Upgrade MongoDB to 5.0.3 [\#27](https://github.com/Martouta/speech_processor/pull/27) ([Martouta](https://github.com/Martouta))
- Bump protobuf from 3.19.0 to 3.19.1 [\#26](https://github.com/Martouta/speech_processor/pull/26) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump google-cloud-speech from 2.10.0 to 2.11.0 [\#25](https://github.com/Martouta/speech_processor/pull/25) ([dependabot[bot]](https://github.com/apps/dependabot))
- pyenv local 3.10.0 [\#24](https://github.com/Martouta/speech_processor/pull/24) ([Martouta](https://github.com/Martouta))
- Remove code quality local chekers \(Pylint\) [\#23](https://github.com/Martouta/speech_processor/pull/23) ([Martouta](https://github.com/Martouta))
- Do not hold CircleCI tests [\#22](https://github.com/Martouta/speech_processor/pull/22) ([Martouta](https://github.com/Martouta))
- \[CodeClimate\] Clean 1st code smells [\#20](https://github.com/Martouta/speech_processor/pull/20) ([Martouta](https://github.com/Martouta))
- Setup Kafka in CircleCI [\#19](https://github.com/Martouta/speech_processor/pull/19) ([Martouta](https://github.com/Martouta))
- Bump pymongo from 3.12.0 to 3.12.1 [\#18](https://github.com/Martouta/speech_processor/pull/18) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump protobuf from 3.18.1 to 3.19.0 [\#17](https://github.com/Martouta/speech_processor/pull/17) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v1.0.0](https://github.com/Martouta/speech_processor/tree/v1.0.0) (2021-10-15)

[Full Changelog](https://github.com/Martouta/speech_processor/compare/45f9872db26596ebd386332a6ec8ef3cd358ef3d...v1.0.0)

**Fixed bugs:**

- Add code to Docker image. [\#11](https://github.com/Martouta/speech_processor/pull/11) ([Martouta](https://github.com/Martouta))

**Merged pull requests:**

- \[Snyk\] Security upgrade python from 3.10.0rc1-slim to 3.10-slim [\#16](https://github.com/Martouta/speech_processor/pull/16) ([snyk-bot](https://github.com/snyk-bot))
- Bump google-cloud-speech from 2.9.3 to 2.10.0 [\#13](https://github.com/Martouta/speech_processor/pull/13) ([dependabot[bot]](https://github.com/apps/dependabot))
- Refactor Dockerfile for a safer and simplest Production-ready image. [\#12](https://github.com/Martouta/speech_processor/pull/12) ([Martouta](https://github.com/Martouta))
- Add 1st badges to README. [\#6](https://github.com/Martouta/speech_processor/pull/6) ([Martouta](https://github.com/Martouta))



\* *This Changelog was automatically generated by [github_changelog_generator](https://github.com/github-changelog-generator/github-changelog-generator)*
