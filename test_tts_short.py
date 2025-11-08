#!/usr/bin/env python3
"""
Test OpenAI TTS with a short broadcast script (1-2 innings only)
This limits the cost to just a few cents for testing
"""

import os
from openai import OpenAI
from fetch_game_data import get_recent_games, get_game_pitch_data, get_key_innings_from_scoring
from generate_broadcast import generate_broadcast_script

def text_to_speech(text, output_file="test_broadcast_short.mp3"):
    """Convert text to speech using OpenAI TTS API (handles 4096 char limit)"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        print("Please set your OpenAI API key:")
        print("export OPENAI_API_KEY='your-api-key-here'")
        return False

    try:
        client = OpenAI(api_key=api_key)

        print("Generating speech audio...")
        print(f"Script length: {len(text)} characters")
        estimated_cost = (len(text) / 1000) * 0.015
        print(f"Estimated cost: ${estimated_cost:.4f}")

        # OpenAI TTS limit is 4096 characters per request
        MAX_CHARS = 4000  # Leave some buffer

        # Split text into chunks if needed
        if len(text) <= MAX_CHARS:
            # Single request
            print("Generating audio (single chunk)...")
            response = client.audio.speech.create(
                model="tts-1",
                voice="onyx",
                input=text
            )
            response.stream_to_file(output_file)
        else:
            # Multiple chunks needed
            import re

            # Split on double newlines (inning boundaries) to keep context
            chunks = []
            current_chunk = ""

            paragraphs = text.split('\n\n')

            for para in paragraphs:
                if len(current_chunk) + len(para) + 2 <= MAX_CHARS:
                    current_chunk += para + '\n\n'
                else:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = para + '\n\n'

            if current_chunk:
                chunks.append(current_chunk.strip())

            print(f"Splitting into {len(chunks)} chunks...")

            # Generate audio for each chunk
            temp_files = []
            for i, chunk in enumerate(chunks):
                print(f"  Generating chunk {i+1}/{len(chunks)} ({len(chunk)} chars)...")
                temp_file = f"temp_chunk_{i}.mp3"

                response = client.audio.speech.create(
                    model="tts-1",
                    voice="onyx",
                    input=chunk
                )
                response.stream_to_file(temp_file)
                temp_files.append(temp_file)

            # Combine audio files using pydub
            print("Combining audio chunks...")
            try:
                from pydub import AudioSegment

                combined = AudioSegment.empty()
                for temp_file in temp_files:
                    audio = AudioSegment.from_mp3(temp_file)
                    combined += audio

                combined.export(output_file, format="mp3")

                # Clean up temp files
                import os as os_module
                for temp_file in temp_files:
                    os_module.remove(temp_file)

            except ImportError:
                print("\n⚠️  Warning: pydub not installed. Saving chunks separately.")
                print("To combine, install: pip install pydub")
                print(f"Chunk files: {', '.join(temp_files)}")
                print(f"\nYou can play them in order, or install pydub to combine.")
                return True

        print(f"✅ Audio saved to {output_file}")
        return True

    except Exception as e:
        print(f"Error generating speech: {e}")
        return False

def main():
    print("=" * 60)
    print("🎙️  ULTRA-SHORT TTS TEST - 1 Inning Only")
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
    score = f"{game.get('away_score', 0)}-{game.get('home_score', 0)}"

    print(f"\n2. Selected game: {away_team} @ {home_team}")
    print(f"   Final Score: {score}")

    # Get key innings
    print("\n3. Identifying scoring innings...")
    key_innings = get_key_innings_from_scoring(game_id)

    if key_innings:
        print(f"   Found scoring in innings: {key_innings}")
        # LIMIT TO FIRST 1 SCORING INNING ONLY FOR TESTING (even shorter!)
        test_innings = key_innings[:1]
        print(f"   📝 TEST: Using only first 1 inning: {test_innings}")
    else:
        print("   No scoring data found")
        return

    # Get pitch data
    print("\n4. Fetching pitch data...")
    pitch_data = get_game_pitch_data(game_id)
    print(f"   Total pitches in game: {len(pitch_data)}")

    # Generate script with LIMITED innings
    print(f"\n5. Generating SHORT broadcast script (innings {test_innings} only)...")
    script = generate_broadcast_script(
        pitch_data,
        key_innings=test_innings,  # Only first 2 innings!
        away_team=away_team,
        home_team=home_team
    )

    # Add simple game summary
    script += f"\n\nThat's the end of our test broadcast. This was a sample from {away_team} versus {home_team}."

    # Save script
    script_file = "test_broadcast_short.txt"
    with open(script_file, 'w') as f:
        f.write(f"# SHORT TEST BROADCAST - Innings {test_innings} only\n")
        f.write(f"# {away_team} @ {home_team}\n")
        f.write(f"# Final Score: {score}\n\n")
        f.write("=" * 60 + "\n")
        f.write("BROADCAST SCRIPT (SHORT TEST)\n")
        f.write("=" * 60 + "\n\n")
        f.write(script)

    print(f"   ✅ Script saved to {script_file}")
    print(f"   Script length: {len(script)} characters")
    estimated_cost = (len(script) / 1000) * 0.015
    print(f"   💰 Estimated TTS cost: ${estimated_cost:.4f}")

    # Preview
    print("\n" + "=" * 60)
    print("PREVIEW (first 500 characters):")
    print("=" * 60)
    print(script[:500] + "...")
    print("=" * 60)

    # Ask for confirmation
    print(f"\n6. Ready to generate audio?")
    print(f"   Cost: ~${estimated_cost:.4f}")
    print(f"   Duration: ~{len(script.split()) // 150} minutes")

    user_input = input("\n   Continue with TTS? (yes/no): ").strip().lower()

    if user_input in ['yes', 'y']:
        print("\n7. Generating audio...")
        audio_file = f"test_broadcast_short.mp3"

        if text_to_speech(script, audio_file):
            print(f"\n✅ SUCCESS! Audio test complete!")
            print(f"\n🎧 Play your test broadcast:")
            print(f"   open '{audio_file}'")
            print(f"\n📝 Text script: {script_file}")
        else:
            print("\n❌ Audio generation failed")
            print(f"📝 Text script available: {script_file}")
    else:
        print("\n⏸️  Skipped TTS generation")
        print(f"📝 Text script available: {script_file}")

if __name__ == "__main__":
    main()
