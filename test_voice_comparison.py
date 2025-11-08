#!/usr/bin/env python3
"""
Test TTS with different voices for comparison
Generates 3 ultra-short test files with onyx, fable, and echo voices
"""

import os
from openai import OpenAI
from fetch_game_data import get_recent_games, get_game_pitch_data
from generate_broadcast import generate_broadcast_script

def text_to_speech_with_voice(text, voice_name, output_file):
    """Convert text to speech using specified voice"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print(f"Error: OPENAI_API_KEY environment variable not set")
        return False

    try:
        client = OpenAI(api_key=api_key)

        print(f"  Generating with {voice_name} voice...")
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice_name,
            speed=0.8,  # 20% slower for relaxed pacing
            input=text
        )
        response.stream_to_file(output_file)
        print(f"  ✅ Saved to {output_file}")
        return True

    except Exception as e:
        print(f"  ❌ Error with {voice_name}: {e}")
        return False

def main():
    print("=" * 60)
    print("🎙️  VOICE COMPARISON TEST - onyx vs fable vs echo")
    print("=" * 60)

    # Get recent game
    print("\n1. Fetching game data...")
    recent_games = get_recent_games(days_back=7)
    if not recent_games:
        print("No recent games found")
        return

    game = recent_games[0]
    away_team = game.get('away_name', 'Unknown')
    home_team = game.get('home_name', 'Unknown')
    game_id = game.get('game_id', '')

    print(f"   Selected: {away_team} @ {home_team}")

    # Get pitch data for top of 3rd inning only
    print("\n2. Generating ultra-short script (top of 3rd)...")
    pitch_data = get_game_pitch_data(game_id)

    # Filter for top of 3rd only
    top_3rd_pitches = [p for p in pitch_data if p['inning'] == 3 and p['half_inning'] == 'top']
    print(f"   Found {len(top_3rd_pitches)} pitches")

    # Manually build simple script for top of 3rd
    script_lines = []
    script_lines.append("Top of the 3rd inning.")
    script_lines.append("")

    prev_batter = None
    for i, pitch in enumerate(top_3rd_pitches):
        pitcher = pitch['pitcher'].split()[-1]
        batter = pitch['batter'].split()[-1]

        from generate_broadcast import format_pitch_type, format_pitch_location
        import random

        pitch_type = format_pitch_type(pitch['pitch_type'])
        speed = int(round(pitch['speed']))
        result = pitch['result'].lower()
        location = format_pitch_location(pitch.get('pX'), pitch.get('pZ'), pitch.get('zone'))

        # Use action verbs
        verbs = ["fires", "deals", "throws", "comes with"]
        verb = random.choice(verbs)

        # Determine outcome
        if "ball" in result:
            outcome = "ball"
        elif "called" in result and "strike" in result:
            outcome = "got him looking, strike"
        elif "strike" in result or "foul" in result:
            outcome = "strike"
        elif "in play" in result or "hit" in result:
            outcome = "in play"
        else:
            outcome = result

        # Build description
        if batter != prev_batter:
            if i == 0:
                if location:
                    desc = f"{pitcher} {verb} a {speed} mile per hour {pitch_type}, {location}, to {batter}. {outcome.capitalize()}."
                else:
                    desc = f"{pitcher} {verb} a {speed} mile per hour {pitch_type} to {batter}. {outcome.capitalize()}."
            else:
                if location:
                    desc = f"Here's the pitch to {batter}... {pitch_type}, {speed}, {location}. {outcome.capitalize()}."
                else:
                    desc = f"Here's the pitch to {batter}... {pitch_type}, {speed}. {outcome.capitalize()}."
        else:
            if location:
                desc = f"The {pitch_type}, {speed}, {location}. {outcome.capitalize()}."
            else:
                desc = f"The {pitch_type}, {speed}. {outcome.capitalize()}."

        script_lines.append(desc)

        if "put in play" in outcome or "in play" in outcome:
            script_lines.append("")
            prev_batter = None
        else:
            prev_batter = batter

    # Get final score
    if top_3rd_pitches:
        last_pitch = top_3rd_pitches[-1]
        away_score = last_pitch.get('away_score', 0)
        home_score = last_pitch.get('home_score', 0)

        script_lines.append("")
        if away_score > home_score:
            script_lines.append(f"After the top of the 3rd, {away_team} leads {away_score} to {home_score}.")
        elif home_score > away_score:
            script_lines.append(f"After the top of the 3rd, {home_team} leads {home_score} to {away_score}.")
        else:
            script_lines.append(f"After the top of the 3rd, we're tied at {away_score}.")

    script = " ".join(script_lines)

    print(f"   Script length: {len(script)} characters")
    print(f"   Estimated cost per voice: ${(len(script) / 1000) * 0.015:.4f}")
    print(f"   Total cost for 3 voices: ${(len(script) / 1000) * 0.015 * 3:.4f}")

    # Save script
    with open('voice_comparison_script.txt', 'w') as f:
        f.write(script)

    print("\n3. Generating audio with 3 different voices...")
    print(f"   Total cost: ~${(len(script) / 1000) * 0.015 * 3:.4f}\n")

    # Generate with each voice
    voices = [
        ("onyx", "test_voice_onyx.mp3"),
        ("fable", "test_voice_fable.mp3"),
        ("echo", "test_voice_echo.mp3")
    ]

    success_count = 0
    for voice_name, output_file in voices:
        if text_to_speech_with_voice(script, voice_name, output_file):
            success_count += 1

    print(f"\n{'=' * 60}")
    if success_count == 3:
        print("✅ All 3 voices generated successfully!")
        print("\n🎧 Listen and compare:")
        print("   1. test_voice_onyx.mp3  (deep, calm)")
        print("   2. test_voice_fable.mp3 (energetic, masculine)")
        print("   3. test_voice_echo.mp3  (dynamic, engaging)")
        print("\nPick the one that sounds most like a baseball broadcaster!")
    elif success_count > 0:
        print(f"⚠️  {success_count} out of 3 voices generated")
    else:
        print("❌ All voice generation failed")
        print("📝 Script saved to: voice_comparison_script.txt")

if __name__ == "__main__":
    main()
