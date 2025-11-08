#!/usr/bin/env python3
"""
Debug script to see all available pitch data fields
"""

import statsapi
import json
from fetch_game_data import get_recent_games

# Get a recent game
recent_games = get_recent_games(days_back=7)
if recent_games:
    game = recent_games[0]
    game_id = game['game_id']

    print(f"Game ID: {game_id}")
    print("="*60)

    playbyplay = statsapi.get('game_playByPlay', {'gamePk': game_id})

    # Get first few plays to see at-bat results
    for play in playbyplay.get('allPlays', [])[:5]:
        print("\n" + "="*60)
        print("PLAY RESULT (At-bat outcome):")
        print("="*60)
        print(json.dumps(play.get('result', {}), indent=2))
        print("\nPlay description:", play.get('result', {}).get('description', 'N/A'))
        print("Event:", play.get('result', {}).get('event', 'N/A'))
        print("Event type:", play.get('result', {}).get('eventType', 'N/A'))
