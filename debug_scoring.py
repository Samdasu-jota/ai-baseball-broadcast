#!/usr/bin/env python3
"""
Debug script to see what scoring plays API returns
"""

import statsapi
from fetch_game_data import get_recent_games

# Get a recent game
recent_games = get_recent_games(days_back=7)
if recent_games:
    game = recent_games[0]
    game_id = game['game_id']

    print(f"Game: {game['away_name']} @ {game['home_name']}")
    print(f"Score: {game['away_score']}-{game['home_score']}")
    print(f"Game ID: {game_id}")
    print("\n" + "="*60)
    print("Scoring Plays Output:")
    print("="*60)

    try:
        scoring = statsapi.game_scoring_plays(game_id)
        print(repr(scoring))
        print("\n" + "="*60)
        print("Human Readable:")
        print("="*60)
        print(scoring)
    except Exception as e:
        print(f"Error: {e}")
