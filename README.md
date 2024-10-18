---
title: Tiger
emoji: 🎥
colorFrom: blue
colorTo: indigo
sdk: streamlit
sdk_version: 1.39.0
app_file: app.py
pinned: false
license: apache-2.0
short_description: Movie transcription for language learners
---

[![Hugging Face space badge]][Hugging Face space URL]
[![Hugging Face sync status badge]][Hugging Face sync status URL]
[![Apache License Badge]][Apache License, Version 2.0]

Tiger
=====

__Tiger__ is an automatic speech recognition application that takes a video file as input and generates a video with
subtitles as well as downloadable .txt, .vtt, .srt transcription files. Tiger generates transcriptions using the
[OpenAI Whisper](https://openai.com/blog/whisper) models.

The app is available on [Hugging Face space][Project Tiger on Hugging Face]. Please check it out.

How Project Tiger Started
-------------------------

I don't believe NLP is inherently AI. [Project Tiger](), however, enlightened me on what way should AI makes NLP more
powerful for people.

Paraphrasing movie lines has been my favorite approach to learn a foreign language. This was why I was able to speak
close-native English in early days. I used this same tactic for German today as well.

One morning I was studying German with the famous German WW2 movie
[_Generation War_](https://youtu.be/8s_0QteDapc?si=usMdIbY5Skfz0u1q). Managing to find its subtitles[^1][^2][^3] were
easy for me. A problem, however, soon arose as I proceeded with them: _the subtitles had errors - missing couple of
phrases every few other lines_. This was a big NO for language learners like me. In old days 10 years ago, I would've
reached a dead end...

[^1]: https://www.opensubtitles.org/en/subtitles/6243166/generation-war-eine-andere-zeit-de
[^2]: https://www.opensubtitles.org/en/subtitles/6243167/generation-war-ein-anderer-krieg-de
[^3]: https://www.opensubtitles.org/en/subtitles/6243168/generation-war-ein-anderes-land-de

Almost immediately, however, I had this idea of having AI figure out those missing words for me; so I tried
[OpenAI's Whisper](https://huggingface.co/spaces/openai/whisper) which, quite surprisingly, yield 100% accurate results.
That was the first occasion where AI produced significant solid values for my life as a language learner.

Being so excited, I decided to industrialize this process and hereby present it as [Project Tiger on Hugging Face], an
__AI movie transcription service that targets specifically for language learners__

> [!NOTE]
>
> On name "__Tiger__"
>
> The project name _tiger_ was taken from the _German heavy tank of World War II -
> [Tiger I](https://tanks-encyclopedia.com/ww2/germany/panzer-vi_tiger.php#index17)_.
>
> I chose this name because the project idea was spawned from the study of German language. More importantly, _Tiger I_
> has been widely recognized as a revolutionary tank being a crown jewels in the history of warfare technology:
>
> > _"It is tempting to view the appearance of the Tiger tank as revolutionary, ... the end result was a machine that
> > represented a quantum leap forward in tank design and changed everything - forever"_[^4]
>
> As _Tiger_ had steered the direction of next-generation heavy tank, this project has also revolutionized my view
> toward AI subconsciously and serves as an empirical guide on how I should make NLP more powerful for people with AI.

[^4]: _[Tiger tank : Panzerkampfwagen VI Tiger I Ausf. E (SdKfz 181): owner's workshop manual](https://a.co/d/28OzPsK)_, The Tank Museum, 2011. p.13

License
-------

The use and distribution terms for [tiger]() are covered by the [Apache License, Version 2.0].

[Apache License Badge]: https://img.shields.io/badge/Apache%202.0-F25910.svg?style=for-the-badge&logo=Apache&logoColor=white
[Apache License, Version 2.0]: https://www.apache.org/licenses/LICENSE-2.0

[Hugging Face space badge]: https://img.shields.io/badge/Hugging%20Face%20Space-tiger-FFD21E?style=for-the-badge&logo=huggingface&logoColor=white
[Hugging Face space URL]: https://huggingface.co/spaces/QubitPi/tiger

[Hugging Face sync status badge]: https://img.shields.io/github/actions/workflow/status/QubitPi/tiger/ci-cd.yaml?branch=master&style=for-the-badge&logo=github&logoColor=white&label=Hugging%20Face%20Sync%20Up
[Hugging Face sync status URL]: https://github.com/QubitPi/tiger/actions/workflows/ci-cd.yaml

[Project Tiger on Hugging Face]: https://huggingface.co/spaces/QubitPi/tiger
