#!/usr/bin/env python3
"""
Learning Script: Understanding MLB StatsAPI
Follow along with the comments to understand each step
"""

import statsapi
from datetime import datetime, timedelta

print("="*60)
print("LEARNING MLB STATSAPI - Step by Step")
print("="*60)

# ============================================================
# STEP 1: Get Recent Games (Simple Version)
# ============================================================
print("\n--- STEP 1: Getting Recent Games ---")

# First, let's understand dates
# We want games from the last 3 days
today = datetime.now()
print(f"Today's date: {today.strftime('%m/%d/%Y')}")

three_days_ago = today - timedelta(days=3)
print(f"Three days ago: {three_days_ago.strftime('%m/%d/%Y')}")

# Now let's get games using statsapi.schedule()
# This function asks MLB: "Give me all games between these dates"
start_date = three_days_ago.strftime('%m/%d/%Y')
end_date = today.strftime('%m/%d/%Y')

print(f"\nAsking MLB API for games between {start_date} and {end_date}...")
all_games = statsapi.schedule(start_date=start_date, end_date=end_date)

print(f"Found {len(all_games)} total games")

# Let's look at what ONE game looks like
if all_games:
    print("\n--- What does ONE game look like? ---")
    first_game = all_games[0]

    # Print all the information we get about a game
    for key, value in first_game.items():
        print(f"  {key}: {value}")

# ============================================================
# STEP 2: Filter for COMPLETED Games Only
# ============================================================
print("\n--- STEP 2: Filtering for Completed Games ---")

# Not all games are finished - some might be scheduled, postponed, etc.
# We only want games that are "Final"
completed_games = []
for game in all_games:
    if game['status'] == 'Final':
        completed_games.append(game)

# This is the same as the "list comprehension" you see in the real code:
# completed_games = [game for game in all_games if game['status'] == 'Final']

print(f"Found {len(completed_games)} completed games")

# Show the completed games
for i, game in enumerate(completed_games[:5]):  # Show first 5
    away = game.get('away_name', 'Unknown')
    home = game.get('home_name', 'Unknown')
    away_score = game.get('away_score', 0)
    home_score = game.get('home_score', 0)
    game_id = game.get('game_id', '')

    print(f"\n{i+1}. {away} @ {home}")
    print(f"   Score: {away_score} - {home_score}")
    print(f"   Game ID: {game_id} (we'll need this for pitch data!)")

# ============================================================
# STEP 3: Get Pitch-by-Pitch Data for ONE Game
# ============================================================
print("\n" + "="*60)
print("--- STEP 3: Getting Pitch-by-Pitch Data ---")
print("="*60)

if completed_games:
    # Pick the first completed game
    selected_game = completed_games[0]
    game_id = selected_game.get('game_id', '')

    print(f"\nGetting pitch data for game ID: {game_id}")
    print("This might take a few seconds...")

    # This is the key function - it gets ALL the details about a game
    playbyplay = statsapi.get('game_playByPlay', {'gamePk': game_id})

    # Let's see what we got back
    print(f"\nWhat's in the playbyplay data?")
    print(f"Keys: {playbyplay.keys()}")

    # The important part is 'allPlays' - this has every at-bat
    all_plays = playbyplay.get('allPlays', [])
    print(f"Total plays (at-bats) in this game: {len(all_plays)}")

    # ============================================================
    # STEP 4: Understanding ONE Play (At-Bat)
    # ============================================================
    print("\n--- STEP 4: Looking Inside ONE Play ---")

    if all_plays:
        # Let's examine the first play in detail
        first_play = all_plays[0]

        print("\nWhat information is in ONE play?")
        print(f"Keys: {first_play.keys()}")

        # Get inning information
        inning = first_play.get('about', {}).get('inning', 0)
        half_inning = first_play.get('about', {}).get('halfInning', '')
        print(f"\nInning: {inning} ({half_inning})")

        # Get player information
        matchup = first_play.get('matchup', {})
        batter_name = matchup.get('batter', {}).get('fullName', 'Unknown')
        pitcher_name = matchup.get('pitcher', {}).get('fullName', 'Unknown')
        print(f"Batter: {batter_name}")
        print(f"Pitcher: {pitcher_name}")

        # Get all the pitch events in this at-bat
        play_events = first_play.get('playEvents', [])
        print(f"\nThis at-bat had {len(play_events)} events")

        # ============================================================
        # STEP 5: Looking at Individual PITCHES
        # ============================================================
        print("\n--- STEP 5: Looking at Individual Pitches ---")

        pitch_count = 0
        for event in play_events:
            # Some events are pitches, some are other things (pickoffs, etc.)
            if event.get('isPitch'):
                pitch_count += 1

                # Get pitch details
                pitch_data = event.get('pitchData', {})
                pitch_details = event.get('details', {})

                speed = pitch_data.get('startSpeed', 0)
                pitch_type = pitch_data.get('details', {}).get('type', {}).get('description', 'Unknown')
                result = pitch_details.get('description', 'Unknown')

                # Get the count
                count = event.get('count', {})
                balls = count.get('balls', 0)
                strikes = count.get('strikes', 0)

                print(f"\n  Pitch #{pitch_count}:")
                print(f"    Type: {pitch_type}")
                print(f"    Speed: {speed} mph")
                print(f"    Result: {result}")
                print(f"    Count: {balls}-{strikes}")

    # ============================================================
    # STEP 6: Collect ALL Pitches from the Entire Game
    # ============================================================
    print("\n" + "="*60)
    print("--- STEP 6: Collecting ALL Pitches from Game ---")
    print("="*60)

    all_pitches = []

    for play in all_plays:
        inning = play.get('about', {}).get('inning', 0)
        half_inning = play.get('about', {}).get('halfInning', '')
        batter = play.get('matchup', {}).get('batter', {}).get('fullName', 'Unknown')
        pitcher = play.get('matchup', {}).get('pitcher', {}).get('fullName', 'Unknown')

        for pitch_event in play.get('playEvents', []):
            if pitch_event.get('isPitch'):
                pitch_details = pitch_event.get('pitchData', {})

                # Create a dictionary with all the info we care about
                pitch_info = {
                    'inning': inning,
                    'half_inning': half_inning,
                    'batter': batter,
                    'pitcher': pitcher,
                    'pitch_type': pitch_details.get('details', {}).get('type', {}).get('description', 'Unknown'),
                    'speed': pitch_details.get('startSpeed', 0),
                    'result': pitch_event.get('details', {}).get('description', 'Unknown'),
                    'balls': pitch_event.get('count', {}).get('balls', 0),
                    'strikes': pitch_event.get('count', {}).get('strikes', 0)
                }

                all_pitches.append(pitch_info)

    print(f"\nTotal pitches in the game: {len(all_pitches)}")

    # Show first 5 pitches
    print("\nFirst 5 pitches of the game:")
    for i, pitch in enumerate(all_pitches[:5]):
        print(f"\n{i+1}. Inning {pitch['inning']} ({pitch['half_inning']})")
        print(f"   {pitch['pitcher']} → {pitch['batter']}")
        print(f"   {pitch['speed']} mph {pitch['pitch_type']}")
        print(f"   Result: {pitch['result']}")
        print(f"   Count: {pitch['balls']}-{pitch['strikes']}")

print("\n" + "="*60)
print("DONE! Now you understand how the StatsAPI works!")
print("="*60)
print("\nKey Takeaways:")
print("1. statsapi.schedule() gets a list of games")
print("2. Each game has a 'game_id' we need for details")
print("3. statsapi.get('game_playByPlay', ...) gets pitch data")
print("4. We loop through 'allPlays' to find all at-bats")
print("5. We loop through 'playEvents' to find individual pitches")
print("6. We extract the data we care about into a simple dictionary")
