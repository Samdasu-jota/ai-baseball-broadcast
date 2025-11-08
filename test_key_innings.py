#!/usr/bin/env python3
"""
Test script to verify key innings detection works correctly
"""

from fetch_game_data import get_recent_games, get_game_pitch_data, get_key_innings_from_scoring
from generate_broadcast import generate_broadcast_script

def main():
    print("=" * 60)
    print("Testing Key Innings Detection")
    print("=" * 60)

    # Get a recent game
    print("\n1. Fetching recent games...")
    recent_games = get_recent_games(days_back=7)

    if not recent_games:
        print("No recent games found")
        return

    # Use first game
    test_game = recent_games[0]
    away_team = test_game.get('away_name', 'Unknown')
    home_team = test_game.get('home_name', 'Unknown')
    game_id = test_game.get('game_id', '')
    score = f"{test_game.get('away_score', 0)}-{test_game.get('home_score', 0)}"

    print(f"\n2. Testing with game: {away_team} @ {home_team}")
    print(f"   Final Score: {score}")
    print(f"   Game ID: {game_id}")

    # Get key innings
    print("\n3. Fetching key innings with scoring...")
    key_innings = get_key_innings_from_scoring(game_id)

    if key_innings:
        print(f"   ✅ Found scoring in innings: {key_innings}")
    else:
        print("   ⚠️  No scoring plays detected")

    # Get pitch data
    print("\n4. Fetching pitch data...")
    pitch_data = get_game_pitch_data(game_id)
    print(f"   Total pitches in game: {len(pitch_data)}")

    # Count pitches per inning
    from collections import Counter
    inning_counts = Counter(p['inning'] for p in pitch_data)
    print(f"\n5. Pitches per inning:")
    for inning in sorted(inning_counts.keys()):
        is_scoring = "📍 SCORING" if inning in key_innings else ""
        print(f"   Inning {inning}: {inning_counts[inning]} pitches {is_scoring}")

    # Generate script with key innings
    print("\n6. Generating broadcast script with key innings only...")
    script = generate_broadcast_script(pitch_data, key_innings=key_innings)

    print(f"\n7. Script Preview (first 500 characters):")
    print("=" * 60)
    print(script[:500] + "...")
    print("=" * 60)

    print(f"\n✅ Test Complete!")
    print(f"   - Full game had {len(pitch_data)} pitches")
    print(f"   - Selected {len([p for p in pitch_data if p['inning'] in key_innings])} pitches from scoring innings")
    print(f"   - Script length: {len(script)} characters")

if __name__ == "__main__":
    main()
