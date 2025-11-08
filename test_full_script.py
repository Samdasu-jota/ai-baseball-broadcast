#!/usr/bin/env python3
"""
Generate a full broadcast script without using TTS API
"""

from fetch_game_data import get_recent_games, get_game_pitch_data, get_key_innings_from_scoring
from generate_broadcast import generate_broadcast_script
import statsapi

def generate_game_summary(away_team, home_team, game, pitch_data, game_id):
    """Generate a comprehensive game summary for TTS"""
    summary_lines = []

    away_score = game.get('away_score', 0)
    home_score = game.get('home_score', 0)
    final_inning = game.get('current_inning', 9)

    # Determine winner
    if away_score > home_score:
        winner = away_team
        loser = home_team
        winner_score = away_score
        loser_score = home_score
    else:
        winner = home_team
        loser = away_team
        winner_score = home_score
        loser_score = away_score

    # Natural spoken summary
    if final_inning > 9:
        summary_lines.append(f"That's the game. {winner} wins it in {final_inning} innings, {winner_score} to {loser_score}.")
    else:
        summary_lines.append(f"That's the game. {winner} defeats {loser}, {winner_score} to {loser_score}.")

    # Try to get winning pitcher and save information from API
    try:
        game_data = statsapi.get('game', {'gamePk': game_id})
        decisions = game_data.get('liveData', {}).get('decisions', {})

        winning_pitcher = decisions.get('winner', {}).get('fullName', None)
        losing_pitcher = decisions.get('loser', {}).get('fullName', None)
        save_pitcher = decisions.get('save', {}).get('fullName', None)

        if winning_pitcher:
            summary_lines.append(f"{winning_pitcher} gets the win.")
        if losing_pitcher:
            summary_lines.append(f"{losing_pitcher} takes the loss.")
        if save_pitcher:
            summary_lines.append(f"{save_pitcher} earns the save.")

    except Exception as e:
        # If we can't get pitcher decisions, continue without them
        pass

    return "\n".join(summary_lines)

def main():
    print("=" * 60)
    print("Generating Full Broadcast Script (Text Only)")
    print("=" * 60)

    # Get a recent game
    print("\nFetching recent games...")
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

    print(f"\nGenerating broadcast for:")
    print(f"  {away_team} @ {home_team}")
    print(f"  Final Score: {score}")

    # Get key innings
    print("\nIdentifying key innings...")
    key_innings = get_key_innings_from_scoring(game_id)

    if key_innings:
        print(f"  Scoring innings: {key_innings}")
    else:
        print("  No scoring data, using all pitches")

    # Get pitch data
    print("\nFetching pitch data...")
    pitch_data = get_game_pitch_data(game_id)
    print(f"  Total pitches: {len(pitch_data)}")

    # Generate script
    print("\nGenerating broadcast script...")
    script = generate_broadcast_script(pitch_data, key_innings=key_innings, away_team=away_team, home_team=home_team)

    # Generate game summary
    game_summary = generate_game_summary(away_team, home_team, game, pitch_data, game_id)

    # Save to file
    filename = f"{away_team.replace(' ', '_')}_vs_{home_team.replace(' ', '_')}_script.txt"
    with open(filename, 'w') as f:
        # Metadata (won't be read by TTS)
        f.write(f"# {away_team} @ {home_team}\n")
        f.write(f"# Final Score: {score}\n")
        if key_innings:
            f.write(f"# Scoring Innings: {key_innings}\n")
        f.write("\n" + "=" * 60 + "\n")
        f.write("BROADCAST SCRIPT (for TTS)\n")
        f.write("=" * 60 + "\n\n")

        # Main broadcast content
        f.write(script)

        # Game summary (natural spoken ending)
        f.write("\n\n")
        f.write(game_summary)

    print(f"\n✅ Script saved to: {filename}")
    print(f"   Script length: {len(script)} characters")
    print(f"   Estimated reading time: ~{len(script.split()) // 150} minutes")

    print("\n" + "=" * 60)
    print("PREVIEW (first 1000 characters):")
    print("=" * 60)
    print(script[:1000])
    print("\n... (see full file for complete script)")

if __name__ == "__main__":
    main()
