# AI Baseball Broadcast Generator 🎙️⚾

Generate sleep-friendly AI broadcasts of MLB games focusing on pitch-by-pitch action.

## What it does

This program creates concise, AI-narrated baseball broadcasts perfect for bedtime listening. It:

1. Fetches recent MLB game data including every pitch
2. Converts pitch data into natural broadcast commentary
3. Generates high-quality audio using OpenAI's TTS
4. Creates ~10-15 minute summaries of full games

## Quick Start

### 1. Install Dependencies
```bash
pip install MLB-StatsAPI openai
```

### 2. Set OpenAI API Key
```bash
export OPENAI_API_KEY='your-api-key-here'
```

### 3. Run the Generator
```bash
python3 baseball_broadcast_ai.py
```

## Example Output

**Text:** "Top of the 1st. deGrom delivers a 98.5 mile per hour fastball to Trout, ball. deGrom delivers a 84.2 mile per hour slider to Trout, strike..."

**Audio:** High-quality speech with calm, deep voice perfect for bedtime.

## File Structure

- `baseball_broadcast_ai.py` - Main program (complete MVP)
- `fetch_game_data.py` - MLB data fetching
- `generate_broadcast.py` - Script generation
- `test_tts.py` - TTS testing
- `broadcast_script.txt` - Generated text output
- `[team]_vs_[team]_broadcast.mp3` - Generated audio

## Features

✅ **Free MLB Data** - Uses MLB's official StatsAPI  
✅ **Natural Speech** - OpenAI TTS with calm "onyx" voice  
✅ **Sleep-Friendly** - Focuses on pure baseball action, no fluff  
✅ **Recent Games** - Automatically finds completed games from last 7 days  
✅ **Pitch Focus** - Every pitch described with speed, type, and outcome  

## Next Steps

- Add team selection
- Support custom game dates
- Add different voice options
- Include key game moments (home runs, strikeouts)
- Add background music

## Cost

- MLB data: **Free**
- OpenAI TTS: ~$0.015 per 1K characters (~$0.15 per 10-minute broadcast)