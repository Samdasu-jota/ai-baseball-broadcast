#!/usr/bin/env python3

from fetch_game_data import get_recent_games, get_game_pitch_data
from generate_broadcast import generate_broadcast_script

def main():
    print("Getting recent game data...")
    recent_games = get_recent_games(days_back=7)
    
    if not recent_games:
        print("No recent games found")
        return
    
    test_game = recent_games[0]
    away_team = test_game.get('away_name', 'Unknown')
    home_team = test_game.get('home_name', 'Unknown')
    game_id = test_game.get('game_id', '')
    
    print(f"Generating broadcast for: {away_team} @ {home_team}")
    
    # Get pitch data
    pitch_data = get_game_pitch_data(game_id)
    
    if pitch_data:
        print(f"Processing {len(pitch_data)} pitches...")
        
        # Generate broadcast script
        script = generate_broadcast_script(pitch_data, max_pitches=40)
        
        print("\n" + "="*60)
        print("AI BASEBALL BROADCAST")
        print("="*60)
        print(script)
        print("="*60)
        
        # Save to file for TTS testing
        with open('broadcast_script.txt', 'w') as f:
            f.write(script)
        print("\nScript saved to broadcast_script.txt")
        
    else:
        print("No pitch data found")

if __name__ == "__main__":
    main()