#!/usr/bin/env python3
"""
Ultra-short TTS test - just TOP of inning 3 only (30 seconds test!)
"""

import os
from openai import OpenAI
from fetch_game_data import get_recent_games, get_game_pitch_data, get_key_innings_from_scoring
from generate_broadcast import generate_broadcast_script

def text_to_speech(text, output_file="test_broadcast_ultra_short.mp3"):
    """Convert text to speech using OpenAI TTS API"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        return False

    try:
        client = OpenAI(api_key=api_key)

        print("Generating speech audio...")
        print(f"Script length: {len(text)} characters")
        estimated_cost = (len(text) / 1000) * 0.015
        print(f"Estimated cost: ${estimated_cost:.4f}")

        response = client.audio.speech.create(
            model="tts-1",
            voice="onyx",
            speed=0.8,  # 20% slower for relaxed, sleep-friendly pacing
            input=text
        )
        response.stream_to_file(output_file)
        print(f"✅ Audio saved to {output_file}")
        return True

    except Exception as e:
        print(f"Error generating speech: {e}")
        return False

def main():
    print("=" * 60)
    print("🎙️  ULTRA-SHORT TTS TEST - Top of 3rd Inning Only!")
    print("=" * 60)

    # Get recent games
    print("\n1. Fetching recent games...")
    recent_games = get_recent_games(days_back=7)

    if not recent_games:
        print("No recent games found")
        return

    # Use first game
    game = recent_games[0]
    away_team = game.get('away_name', 'Unknown')
    home_team = game.get('home_name', 'Unknown')
    game_id = game.get('game_id', '')

    print(f"\n2. Selected game: {away_team} @ {home_team}")

    # Get pitch data
    print("\n3. Fetching pitch data...")
    pitch_data = get_game_pitch_data(game_id)

    # Filter for ONLY top of 3rd inning
    print("\n4. Filtering for TOP of 3rd inning only...")
    top_3rd_pitches = [
        p for p in pitch_data
        if p['inning'] == 3 and p['half_inning'] == 'top'
    ]

    print(f"   Found {len(top_3rd_pitches)} pitches in top of 3rd")

    if not top_3rd_pitches:
        print("   No pitches found for top of 3rd")
        return

    # Generate script for just top of 3rd
    print("\n5. Generating ULTRA-SHORT broadcast script...")

    # Manually build a simple script
    script_lines = []
    script_lines.append("Top of the 3rd inning.")
    script_lines.append("")

    prev_batter = None
    for i, pitch in enumerate(top_3rd_pitches):
        pitcher = pitch['pitcher'].split()[-1]
        batter = pitch['batter'].split()[-1]

        # Build pitch description
        pitch_type = pitch['pitch_type'].lower() if pitch['pitch_type'] != 'Unknown' else 'pitch'
        speed = pitch['speed']
        result = pitch['result'].lower()

        # Determine outcome
        if "ball" in result:
            outcome = "ball"
        elif "strike" in result or "foul" in result:
            outcome = "strike"
        elif "in play" in result or "hit" in result:
            outcome = "put in play"
        else:
            outcome = result

        # Mention batter only when they change
        # Add comma after pitcher name and separate outcome with period for natural pauses
        if batter != prev_batter:
            if i == 0:
                desc = f"{pitcher}, delivers a {int(round(speed))} mile per hour {pitch_type} to {batter}. {outcome.capitalize()}."
            else:
                desc = f"Delivers a {int(round(speed))} mile per hour {pitch_type} to {batter}. {outcome.capitalize()}."
        else:
            desc = f"Delivers a {int(round(speed))} mile per hour {pitch_type}. {outcome.capitalize()}."

        script_lines.append(desc)

        # Add paragraph break when at-bat ends (ball put in play)
        if "put in play" in outcome:
            script_lines.append("")
            prev_batter = None  # Reset for next batter
        else:
            prev_batter = batter

    # Get final score for this half-inning
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

    # Save script
    script_file = "test_broadcast_ultra_short.txt"
    with open(script_file, 'w') as f:
        f.write(f"# ULTRA-SHORT TEST - Top of 3rd Inning Only\n")
        f.write(f"# {away_team} @ {home_team}\n\n")
        f.write(script)

    print(f"   ✅ Script saved to {script_file}")
    print(f"   Script length: {len(script)} characters")
    estimated_cost = (len(script) / 1000) * 0.015
    print(f"   💰 Estimated TTS cost: ${estimated_cost:.4f}")

    # Preview
    print("\n" + "=" * 60)
    print("PREVIEW:")
    print("=" * 60)
    print(script[:400] + "..." if len(script) > 400 else script)
    print("=" * 60)

    # Auto-generate audio (no prompt needed for this short test)
    print(f"\n6. Generating audio...")
    print(f"   Cost: ~${estimated_cost:.4f}")
    print(f"   Duration: ~1 minute")

    audio_file = "test_broadcast_ultra_short.mp3"

    if text_to_speech(script, audio_file):
        print(f"\n✅ SUCCESS! Ultra-short audio test complete!")
        print(f"\n🎧 Play your test broadcast:")
        print(f"   open '{audio_file}'")
        print(f"\n📝 Text script: {script_file}")
    else:
        print("\n❌ Audio generation failed")
        print(f"📝 Text script available: {script_file}")

if __name__ == "__main__":
    main()
