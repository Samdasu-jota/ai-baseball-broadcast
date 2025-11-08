# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an AI Baseball Broadcast Generator that creates sleep-friendly audio summaries of MLB games. The system fetches pitch-by-pitch data from MLB's free StatsAPI, converts it to natural broadcast commentary, and generates audio using OpenAI's TTS API.

## Dependencies and Setup

Install required packages:
```bash
pip install MLB-StatsAPI openai
```

Set OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

## Running the Application

**Main application:**
```bash
python3 baseball_broadcast_ai.py
```

**Individual components for testing:**
```bash
python3 fetch_game_data.py          # Test MLB data fetching
python3 generate_broadcast.py       # Test script generation
python3 test_tts.py                 # Test TTS with sample text
python3 test_integration.py         # Test data + script generation
```

## Architecture

The system is built with a modular pipeline architecture:

1. **Data Fetching** (`fetch_game_data.py`): Interfaces with MLB StatsAPI to retrieve recent games and pitch-by-pitch data for specific games
2. **Script Generation** (`generate_broadcast.py`): Converts raw pitch data into natural broadcast commentary with inning transitions and pitch descriptions
3. **Audio Generation** (in `baseball_broadcast_ai.py`): Uses OpenAI TTS to convert text to speech with sleep-friendly voice settings
4. **Integration** (`baseball_broadcast_ai.py`): Orchestrates the entire pipeline from game selection to final audio output

## Key Data Flow

- MLB StatsAPI returns pitch data with: inning, batter/pitcher names, pitch type, speed, location, result
- Script generator processes ~40-50 key pitches from a game (279+ total) by sampling first innings, middle game, and final innings
- TTS uses "onyx" voice model optimized for calm, bedtime listening
- Generated files: `broadcast_script.txt` (text) and `[team]_vs_[team]_broadcast.mp3` (audio)

## API Integration Notes

- MLB StatsAPI is free but requires handling of nested JSON structures from `game_playByPlay` endpoint
- OpenAI TTS costs ~$0.015 per 1K characters (~$0.15 per 10-minute broadcast)
- Pitch data extraction relies on `playEvents` filtering for `isPitch: true` events

## Testing Strategy

Use the individual component files to test each part of the pipeline independently before running the full integration. The `test_integration.py` script is useful for validating the data fetching and script generation without using TTS credits.