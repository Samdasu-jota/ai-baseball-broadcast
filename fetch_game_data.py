#!/usr/bin/env python3

import statsapi
import json
from datetime import datetime, timedelta

def get_recent_games(team_name=None, days_back=3):
    """Get recent completed games"""
    end_date = datetime.now().strftime('%m/%d/%Y')
    start_date = (datetime.now() - timedelta(days=days_back)).strftime('%m/%d/%Y')
    
    if team_name:
        # Get team ID first
        teams = statsapi.get('teams', {'sportId': 1})['teams']
        team_id = None
        for team in teams:
            if team_name.lower() in team['name'].lower():
                team_id = team['id']
                break
        
        if team_id:
            schedule = statsapi.schedule(start_date=start_date, end_date=end_date, team=team_id)
        else:
            print(f"Team '{team_name}' not found")
            return []
    else:
        schedule = statsapi.schedule(start_date=start_date, end_date=end_date)
    
    return [game for game in schedule if game['status'] == 'Final']

def get_game_pitch_data(game_id):
    """Get detailed pitch-by-pitch data for a specific game"""
    try:
        # Get play-by-play data
        playbyplay = statsapi.get('game_playByPlay', {'gamePk': game_id})
        
        pitch_data = []
        
        for play in playbyplay.get('allPlays', []):
            inning = play.get('about', {}).get('inning', 0)
            half_inning = play.get('about', {}).get('halfInning', '')
            batter = play.get('matchup', {}).get('batter', {}).get('fullName', 'Unknown')
            pitcher = play.get('matchup', {}).get('pitcher', {}).get('fullName', 'Unknown')
            
            for pitch_event in play.get('playEvents', []):
                if pitch_event.get('isPitch'):
                    pitch_details = pitch_event.get('pitchData', {})
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
                    pitch_data.append(pitch_info)
        
        return pitch_data
        
    except Exception as e:
        print(f"Error fetching game data: {e}")
        return []

def main():
    # Test with a recent game
    print("Fetching recent games...")
    recent_games = get_recent_games(days_back=7)
    
    if not recent_games:
        print("No recent games found")
        return
    
    # Debug: print the structure of the first game
    test_game = recent_games[0]
    print("Game data structure:")
    print(json.dumps(test_game, indent=2)[:500] + "...")
    
    # Try to get basic game info
    away_team = test_game.get('away_name', 'Unknown')
    home_team = test_game.get('home_name', 'Unknown')
    game_id = test_game.get('game_id', '')
    
    print(f"Testing with game: {away_team} @ {home_team}")
    print(f"Game ID: {game_id}")
    
    # Fetch pitch data
    pitch_data = get_game_pitch_data(game_id)
    
    if pitch_data:
        print(f"Found {len(pitch_data)} pitches")
        print("\nFirst few pitches:")
        for i, pitch in enumerate(pitch_data[:5]):
            print(f"{i+1}. Inning {pitch['inning']} {pitch['half_inning']}: {pitch['pitcher']} to {pitch['batter']}")
            print(f"   {pitch['speed']} mph {pitch['pitch_type']}, {pitch['result']} (Count: {pitch['balls']}-{pitch['strikes']})")
    else:
        print("No pitch data found")

if __name__ == "__main__":
    main()