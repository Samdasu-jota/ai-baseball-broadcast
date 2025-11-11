#!/usr/bin/env python3
"""
Test broadcast generation WITH sound effects
Demonstrates the complete audio mixing system
"""

import os
from openai import OpenAI
from pydub import AudioSegment
from fetch_game_data import get_recent_games, get_game_pitch_data
from generate_broadcast import generate_broadcast_script, generate_pitch_description
from audio_mixer import BaseballAudioMixer

def generate_tts(text, output_file="temp_narration.mp3"):
    """Generate TTS narration (without sound effects yet)"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY not set")
        return None

    try:
        client = OpenAI(api_key=api_key)

        print("🎙️  Generating TTS narration...")
        response = client.audio.speech.create(
            model="tts-1-hd",
            voice="onyx",
            speed=0.95,
            input=text
        )

        response.stream_to_file(output_file)
        print(f"✅ Narration saved to {output_file}")

        # Load as AudioSegment
        return AudioSegment.from_mp3(output_file)

    except Exception as e:
        print(f"Error: {e}")
        return None


def main():
    print("=" * 70)
    print("🎙️⚾ BASEBALL BROADCAST WITH SOUND EFFECTS TEST")
    print("=" * 70)

    # Ask user if they want background crowd
    print("\n🎵 Background crowd ambiance:")
    print("   The 'normal croud sound.mp3' will loop continuously at low volume")
    enable_crowd = input("   Enable background crowd? (yes/no): ").strip().lower() in ['yes', 'y']

    # 1. Fetch game data
    print("\n1️⃣  Fetching recent MLB game...")
    recent_games = get_recent_games(days_back=7)
    if not recent_games:
        print("No games found")
        return

    game = recent_games[0]
    game_id = game['game_id']
    away_team = game['away_name']
    home_team = game['home_name']

    print(f"   Selected: {away_team} @ {home_team}")

    # 2. Get pitch data (top of 3rd only for quick test)
    print("\n2️⃣  Fetching pitch data (top of 3rd inning)...")
    pitch_data = get_game_pitch_data(game_id)
    top_3rd = [p for p in pitch_data if p['inning'] == 3 and p['half_inning'] == 'top']
    print(f"   Found {len(top_3rd)} pitches")

    # 3. Generate script
    print("\n3️⃣  Generating broadcast script...")
    script_lines = ["Top of the 3rd inning."]

    prev_batter = None
    prev_pitcher = None

    for pitch in top_3rd:
        mention_pitcher = (prev_pitcher != pitch['pitcher'])
        mention_batter = (prev_batter != pitch['batter'])

        pitch_desc = generate_pitch_description(
            pitch,
            mention_batter=mention_batter,
            mention_pitcher=mention_pitcher
        )
        script_lines.append(pitch_desc)

        result = pitch['result'].lower()
        if 'in play' in result or 'hit' in result:
            prev_batter = None
        else:
            prev_batter = pitch['batter']

        prev_pitcher = pitch['pitcher']

    # Add score
    if top_3rd:
        last = top_3rd[-1]
        away_score = last.get('away_score', 0)
        home_score = last.get('home_score', 0)
        if away_score > home_score:
            script_lines.append(f"After the top of the 3rd, {away_team} leads {away_score} to {home_score}.")
        elif home_score > away_score:
            script_lines.append(f"After the top of the 3rd, {home_team} leads {home_score} to {away_score}.")
        else:
            script_lines.append(f"After the top of the 3rd, we're tied at {away_score}.")

    script = " ".join(script_lines)
    print(f"   Script: {len(script)} characters")

    # Save script
    with open('test_broadcast_sfx_script.txt', 'w') as f:
        f.write(f"# Broadcast with Sound Effects Test\n")
        f.write(f"# {away_team} @ {home_team}\n\n")
        f.write(script)

    # 4. Generate TTS narration
    print("\n4️⃣  Generating TTS narration (HD quality, speed 0.95)...")
    narration_audio = generate_tts(script, "temp_narration.mp3")
    if not narration_audio:
        print("❌ TTS generation failed")
        return

    # 5. Create pitch events for sound effect timing
    print("\n5️⃣  Preparing pitch events for sound effects...")

    # Estimate timing: ~150 words per minute = 2.5 words per second = 400ms per word
    # Rough timing based on script position
    words = script.split()
    pitch_events = []
    current_time_ms = 0
    word_index = 0

    for pitch in top_3rd:
        # Find approximate timestamp for this pitch
        # Each pitch description is ~15-20 words, so roughly 6-8 seconds
        pitch_desc_words = 15
        current_time_ms += pitch_desc_words * 400  # 400ms per word

        pitch_events.append({
            'timestamp_ms': current_time_ms,
            'pitch_type': pitch['pitch_type'],
            'speed': pitch['speed'],
            'result': pitch['result'],
            'at_bat_event': pitch.get('at_bat_event')
        })

    print(f"   Created {len(pitch_events)} pitch events")

    # 6. Mix narration with sound effects
    print("\n6️⃣  Mixing audio with baseball sound effects...")
    mixer = BaseballAudioMixer(enable_background_crowd=enable_crowd)

    output_file = "test_broadcast_with_sfx.mp3"
    final_audio = mixer.mix_broadcast_with_effects(
        narration_audio,
        pitch_events,
        output_file
    )

    print("\n" + "=" * 70)
    print("✅ SUCCESS! Broadcast with sound effects complete!")
    print("=" * 70)
    print(f"\n📝 Script: test_broadcast_sfx_script.txt")
    print(f"🎵 Audio: {output_file}")
    print(f"⏱️  Duration: {len(final_audio) / 1000:.1f} seconds")
    print(f"\n🎧 Listen:")
    print(f"   open '{output_file}'")

    print("\n🔊 Sound effects used:")
    print("   • Fastball catches (>95 mph, fastballs, fast sinkers/cutters)")
    print("   • Slowball catches (all other pitches)")
    print("   • Bat hits (random bat1/bat2/bat3)")
    print("   • Home run bat (bat1 for home runs)")
    print("   • Bunt sounds (for bunts)")
    print("   • Crowd reactions (for hits/home runs)")
    if enable_crowd:
        print("   • Background crowd ambiance (looped at -15 dB)")

    print("\n💡 To disable background crowd, edit:")
    print("   mixer = BaseballAudioMixer(enable_background_crowd=False)")


if __name__ == "__main__":
    main()
