# AI Baseball Broadcast Generator 🎙️⚾

Generate sleep-friendly AI broadcasts of MLB games with smart pitch selection and professional-quality narration.

## What it does

This program creates concise, AI-narrated baseball broadcasts perfect for bedtime listening. It intelligently selects the most exciting innings and generates natural, professional-quality commentary:

1. **Smart Inning Selection** - Automatically identifies innings with scoring plays
2. **Detailed Pitch Commentary** - Every pitch described with type, speed, and location
3. **Natural Narration** - Reduces repetition, mentions players intelligently
4. **Score Tracking** - Clear announcements of who's leading after each inning
5. **Game Summary** - Professional ending with winning/losing pitcher credits
6. **High-Quality Audio** - OpenAI TTS with calm "onyx" voice

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

### 4. Test Without TTS (No API Key Required)
```bash
python3 test_full_script.py
```

## Example Output

See [Los_Angeles_Dodgers_vs_Toronto_Blue_Jays_script.txt](Los_Angeles_Dodgers_vs_Toronto_Blue_Jays_script.txt) for a complete example broadcast.

**Sample Commentary:**
```
Top of the 3.
Scherzer delivers a 95.0 mile per hour four-seam fastball, down the middle to Hernández, strike.
Delivers a 95.3 mile per hour four-seam fastball, down the middle, ball.
Delivers a 76.5 mile per hour curveball, down the middle, put in play. Fly out.

After that half inning, we're tied at 0.

Bottom of the 3.
Ohtani delivers a 96.3 mile per hour four-seam fastball, down the middle to Springer, strike.
Delivers a 99.2 mile per hour four-seam fastball, down the middle, strike.
Delivers a 88.7 mile per hour slider, down the middle to Bichette, put in play.
It's a home run! That brings in 3 runs.

After that half inning, Toronto Blue Jays leads 3 to 0.
```

**Game Ending:**
```
That's the game. Los Angeles Dodgers wins it in 11 innings, 5 to 4.
Yoshinobu Yamamoto gets the win.
Shane Bieber takes the loss.
```

## File Structure

- `baseball_broadcast_ai.py` - Main program with TTS generation
- `fetch_game_data.py` - MLB data fetching with scoring plays API
- `generate_broadcast.py` - Natural script generation with smart narration
- `test_full_script.py` - Generate text-only broadcasts (no API key needed)
- `Los_Angeles_Dodgers_vs_Toronto_Blue_Jays_script.txt` - Example output
- `broadcast_script.txt` - Generated text output
- `[team]_vs_[team]_broadcast.mp3` - Generated audio

## Features

### ⚾ Smart Game Selection
✅ **Key Innings Only** - Automatically selects innings with scoring plays
✅ **Recent Games** - Finds completed games from last 7 days
✅ **Efficient** - Reduces 300+ pitches to ~200 key moments (56% reduction)

### 🎙️ Professional Commentary
✅ **Detailed Pitches** - Type (fastball, slider, curveball, etc.), speed, and location
✅ **Natural Flow** - Smart pitcher/batter mentions (introduced once per inning/at-bat)
✅ **At-Bat Outcomes** - Strikeouts, home runs, base hits, walks, etc.
✅ **RBI Tracking** - "That brings in 3 runs"

### 📊 Score Management
✅ **Clear Updates** - "Toronto Blue Jays leads 3 to 0"
✅ **Tie Detection** - "We're tied at 4"
✅ **End-of-Inning Summaries** - Score after each half-inning

### 🏆 Game Summary
✅ **Natural Ending** - "That's the game. Dodgers wins it in 11 innings, 5 to 4"
✅ **Winning Pitcher** - Credits the winning pitcher
✅ **Losing Pitcher** - Credits the losing pitcher
✅ **Save Credits** - When applicable

### 🔊 Audio Generation
✅ **High-Quality TTS** - OpenAI's "onyx" voice (deep, calm)
✅ **Sleep-Friendly** - Perfect pacing for bedtime listening
✅ **Natural Speech** - Professional broadcaster quality

## How It Works

### 1. Data Fetching (`fetch_game_data.py`)
- Connects to MLB's free StatsAPI
- Retrieves recent completed games
- Fetches pitch-by-pitch data with full details
- **NEW**: Identifies scoring innings using `game_scoring_plays` API
- **NEW**: Extracts pitch location coordinates (high/low, inside/outside)
- **NEW**: Tracks RBI and score progression

### 2. Script Generation (`generate_broadcast.py`)
- **Smart Selection**: Focuses on innings where runs were scored
- **Pitch Details**: Describes type, speed, and location naturally
- **Smart Mentions**: Introduces pitcher each inning, batter each at-bat
- **At-Bat Results**: Announces strikeouts, home runs, base hits, etc.
- **Score Updates**: Clear "who's leading" after each half-inning
- **Natural Pacing**: Paragraph breaks every 5 pitches

### 3. Audio Generation (`baseball_broadcast_ai.py`)
- Converts script to speech using OpenAI TTS
- Uses "onyx" voice for calm, bedtime-friendly narration
- Saves to MP3 file named `[Away_Team]_vs_[Home_Team]_broadcast.mp3`

## Example Usage

### Generate Full Broadcast with Audio
```bash
python3 baseball_broadcast_ai.py
```
Output: Text script + MP3 audio file

### Generate Text-Only Script
```bash
python3 test_full_script.py
```
Output: Text script with game summary (no API key needed)

### Test Data Fetching
```bash
python3 fetch_game_data.py
```
Output: Lists recent games and shows pitch data sample

### Test Script Generation
```bash
python3 generate_broadcast.py
```
Output: Sample broadcast script from test data

## Cost

- **MLB Data**: Free (official MLB StatsAPI)
- **OpenAI TTS**: ~$0.015 per 1,000 characters
  - Average broadcast: ~15,000 characters = **~$0.23 per game**
  - Typical listening time: 15-20 minutes

## Advanced Features

### Key Innings Selection Algorithm
The system automatically identifies exciting innings by:
1. Querying MLB's `game_scoring_plays` API
2. Parsing scoring play descriptions to find innings with runs
3. Including only those innings in the broadcast
4. Result: Focus on action, skip scoreless innings

### Natural Language Processing
- **Pitcher Tracking**: Mentioned once per inning, then omitted for flow
- **Batter Tracking**: Mentioned at start of at-bat, then omitted
- **Location Parsing**: Converts coordinates to "high and inside", "low and outside", etc.
- **Outcome Mapping**: Translates API events to natural phrases

### Score Intelligence
- Tracks score progression throughout the game
- Determines leader after each half-inning
- Detects tie games
- Formats naturally: "Team X leads Y to Z" vs "We're tied at N"

## Future Enhancements

Potential improvements:
- [ ] Team selection UI
- [ ] Custom game date selection
- [ ] Multiple voice options
- [ ] Highlight detection (no-hitters, perfect games, shutouts)
- [ ] Bullpen day detection
- [ ] Starting pitcher stats (innings pitched)
- [ ] Background music option
- [ ] Multiple language support

## Technical Details

**APIs Used:**
- `statsapi.schedule()` - Get recent games
- `statsapi.game_scoring_plays()` - Identify key innings
- `statsapi.get('game_playByPlay')` - Pitch-by-pitch data
- `statsapi.get('game')` - Winning/losing pitcher decisions
- `openai.audio.speech.create()` - Text-to-speech generation

**Data Processing:**
- Full game: ~300-400 pitches
- Selected: ~150-250 pitches from scoring innings
- Script length: ~13,000-17,000 characters
- Audio duration: 15-20 minutes

## Contributing

Feel free to fork and improve! Some ideas:
- Add more natural language variations
- Improve pitch location descriptions
- Add player statistics integration
- Support live games (real-time updates)

## License

MIT License - Free to use and modify

---

**Enjoy your sleep-friendly baseball broadcasts!** 🌙⚾🎙️
