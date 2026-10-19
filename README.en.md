# Narrative Video Engine

**[Português](README.md) · [English](README.en.md) · [Español](README.es.md)**

[![Narrative Video Engine](guia/assets/banner-en.jpg)](https://inematds.github.io/motor-videos-narrativos/guia/en/)

## What it is

A Python tool for planning educational and narrative videos. Starting from a topic, it organizes scenes, estimated timings and guidance for images, voice and music into two files. Local history helps vary choices between projects. All you need is Python 3.9 or later: plans are created offline, without an API key. The final script, audio and video are produced later using other tools.

## User guide

[Open the complete guide](https://inematds.github.io/motor-videos-narrativos/guia/en/).

```bash
git clone https://github.com/inematds/motor-videos-narrativos.git
cd motor-videos-narrativos
python3 motor_video.py --tema "Como o café chegou ao Brasil" --duracao 60 --formato 9:16
```

Outputs: `jobs/<id>/plano.json` and `jobs/<id>/prompt_pack.md`. Local history in `history.json` is created automatically and is not tracked in version control. The supplied examples are in `exemplos/`, including the original history. The engine interface, generated text, original documents and examples are in Portuguese.

- Python 3.9+, standard library only; no APIs or external packages.
- `--help`: lists all options; duration ranges from 20 to 600 seconds.
- `--voz informative_warm`: selects a catalog profile; it does not synthesize audio.
- `--seed`: repeats choices only with the same arguments, configuration and input history; date metadata varies.
- `--out`: choose a new folder to avoid overwriting previous outputs.
- Choices are random draws constrained by history; there is no semantic analysis of the topic.
- The engine generates guidance and script placeholders. It does not research facts, write the final script or render MP4 files.

## Materials

- [Audiovisual DNA](reference_analysis.md): supplied analysis, with reported measurements of the reference.
- [Original proposal](docs/proposta-original.md): the full workflow vision; includes steps still handled outside the code.
- [Coffee](exemplos/demo_cafe/prompt_pack.md) and [rivers](exemplos/demo_rios/prompt_pack.md): supplied examples in Portuguese.
- `engine_config.json`: narrative structures, visual styles, voices, music and production rules.

The supplied ZIP contains the same engine and configuration as the individual files; its examples were incorporated without changing the code. The reference video and transcript were not included in the package. References to those files in the original documents are preserved for context.
