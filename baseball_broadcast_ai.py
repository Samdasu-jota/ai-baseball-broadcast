#!/usr/bin/env python3
"""
AI Baseball Broadcast Generator
Generate sleep-friendly AI broadcasts of MLB games focusing on pitch-by-pitch action
"""

import os
from openai import OpenAI

# Import functions from our modules instead of duplicating them!
from fetch_game_data import get_recent_games, get_game_pitch_data, get_key_innings_from_scoring
from generate_broadcast import generate_broadcast_script

# === AUDIO GENERATION ===

def text_to_speech(text, output_file="broadcast_audio.mp3"):
    """Convert text to speech using OpenAI TTS API"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        print("Please set your OpenAI API key:")
        print("export OPENAI_API_KEY='your-api-key-here'")
        return False
    
    try:
        client = OpenAI(api_key=api_key)
        
        print("Generating speech audio...")
        response = client.audio.speech.create(
            model="tts-1-hd",  # HD model for better prosody and naturalness
            voice="onyx",  # Deep, calm voice for baseball broadcasting
            speed=0.95,  # Slightly slower for clear, natural pacing
            input=text
        )
        
        response.stream_to_file(output_file)
        print(f"Audio saved to {output_file}")
        return True
        
    except Exception as e:
        print(f"Error generating speech: {e}")
        return False

# === MAIN APPLICATION ===

def main():
    print("🎙️  AI Baseball Broadcast Generator")
    print("=" * 50)
    
    # Get recent games
    print("Fetching recent games...")
    recent_games = get_recent_games(days_back=7)
    
    if not recent_games:
        print("No recent games found")
        return
    
    # Show available games
    print(f"Found {len(recent_games)} recent games:")
    for i, game in enumerate(recent_games[:5]):
        away = game.get('away_name', 'Unknown')
        home = game.get('home_name', 'Unknown')
        score = f"{game.get('away_score', 0)}-{game.get('home_score', 0)}"
        print(f"{i+1}. {away} @ {home} ({score})")
    
    # Use first game for now
    selected_game = recent_games[0]
    away_team = selected_game.get('away_name', 'Unknown')
    home_team = selected_game.get('home_name', 'Unknown')
    game_id = selected_game.get('game_id', '')
    
    print(f"\nGenerating broadcast for: {away_team} @ {home_team}")
    
    # Get pitch data
    pitch_data = get_game_pitch_data(game_id)

    if not pitch_data:
        print("No pitch data found for this game")
        return

    print(f"Processing {len(pitch_data)} total pitches...")

    # Get key innings (innings with scoring)
    print("Identifying key innings with scoring plays...")
    key_innings = get_key_innings_from_scoring(game_id)

    if key_innings:
        print(f"Found scoring in innings: {key_innings}")
    else:
        print("No scoring plays found, using all pitches")

    # Generate script using key innings
    script = generate_broadcast_script(pitch_data, max_pitches=40, key_innings=key_innings, away_team=away_team, home_team=home_team)
    
    # Save script
    script_file = "broadcast_script.txt"
    with open(script_file, 'w') as f:
        f.write(script)
    print(f"Script saved to {script_file}")
    
    # Preview script
    print("\n" + "="*60)
    print("BROADCAST PREVIEW (first 200 chars):")
    print("="*60)
    print(script[:200] + "...")
    print("="*60)
    
    # Generate audio
    audio_file = f"{away_team.replace(' ', '_')}_vs_{home_team.replace(' ', '_')}_broadcast.mp3"
    print(f"\nGenerating audio broadcast...")
    
    if text_to_speech(script, audio_file):
        print(f"✅ Success! Audio broadcast saved to: {audio_file}")
        print(f"🎧 Play your bedtime baseball broadcast:")
        print(f"   open '{audio_file}'")
    else:
        print("❌ Audio generation failed. Set OPENAI_API_KEY to enable TTS.")
        print(f"📝 Text script available in: {script_file}")

if __name__ == "__main__":
    main()