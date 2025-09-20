#!/usr/bin/env python3
"""
AI Baseball Broadcast Generator
Generate sleep-friendly AI broadcasts of MLB games focusing on pitch-by-pitch action
"""

import os
import sys
import statsapi
from datetime import datetime, timedelta
from openai import OpenAI

# === DATA FETCHING ===

def get_recent_games(team_name=None, days_back=7):
    """Get recent completed games"""
    end_date = datetime.now().strftime('%m/%d/%Y')
    start_date = (datetime.now() - timedelta(days=days_back)).strftime('%m/%d/%Y')
    
    if team_name:
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
                        'pitch_type': pitch_details.get('details', {}).get('type', {}).get('description', 'pitch'),
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

# === SCRIPT GENERATION ===

def format_pitch_type(pitch_type):
    """Clean up pitch type names"""
    if not pitch_type or pitch_type == "Unknown":
        return "pitch"
    return pitch_type.lower()

def generate_pitch_description(pitch):
    """Convert pitch data to broadcast text"""
    pitcher = pitch['pitcher'].split()[-1]
    batter = pitch['batter'].split()[-1]
    
    speed = pitch['speed']
    pitch_type = format_pitch_type(pitch['pitch_type'])
    result = pitch['result'].lower()
    
    if speed > 0:
        speed_text = f"{speed:.1f} mile per hour {pitch_type}"
    else:
        speed_text = pitch_type
    
    if "ball" in result:
        outcome = "ball"
    elif "strike" in result or "foul" in result:
        outcome = "strike"
    elif "hit" in result or "in play" in result:
        outcome = "put in play"
    else:
        outcome = result
    
    return f"{pitcher} delivers a {speed_text} to {batter}, {outcome}."

def generate_inning_intro(inning, half_inning, prev_inning=None, prev_half=None):
    """Generate inning transitions"""
    if prev_inning != inning or prev_half != half_inning:
        if half_inning == "top":
            return f"Top of the {inning}. "
        else:
            return f"Bottom of the {inning}. "
    return ""

def generate_broadcast_script(pitch_data, max_pitches=50):
    """Convert pitch data into a natural broadcast script"""
    if not pitch_data:
        return "No game data available."
    
    script_lines = []
    prev_inning = None
    prev_half = None
    
    # Sample pitches for reasonable broadcast length
    if len(pitch_data) > max_pitches:
        selected_pitches = (
            pitch_data[:15] +
            pitch_data[len(pitch_data)//2:len(pitch_data)//2+10] +
            pitch_data[-25:]
        )
    else:
        selected_pitches = pitch_data
    
    for i, pitch in enumerate(selected_pitches):
        inning_intro = generate_inning_intro(
            pitch['inning'], 
            pitch['half_inning'], 
            prev_inning, 
            prev_half
        )
        
        if inning_intro:
            script_lines.append(inning_intro)
        
        pitch_desc = generate_pitch_description(pitch)
        script_lines.append(pitch_desc)
        
        if i % 5 == 4:
            script_lines.append("")  # Breathing room
        
        prev_inning = pitch['inning']
        prev_half = pitch['half_inning']
    
    return " ".join(script_lines)

# === AUDIO GENERATION ===

def text_to_speech(text, output_file="broadcast_audio.mp3"):
    """Convert text to speech using OpenAI TTS API"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        print("Please set your OpenAI API key:")
        print("export OPENAI_API_KEY='your-api-key-here'")
        return False
    
    try:
        client = OpenAI(api_key=api_key)
        
        print("Generating speech audio...")
        response = client.audio.speech.create(
            model="tts-1",
            voice="onyx",  # Deep, calm voice
            input=text
        )
        
        response.stream_to_file(output_file)
        print(f"Audio saved to {output_file}")
        return True
        
    except Exception as e:
        print(f"Error generating speech: {e}")
        return False

# === MAIN APPLICATION ===

def main():
    print("🎙️  AI Baseball Broadcast Generator")
    print("=" * 50)
    
    # Get recent games
    print("Fetching recent games...")
    recent_games = get_recent_games(days_back=7)
    
    if not recent_games:
        print("No recent games found")
        return
    
    # Show available games
    print(f"Found {len(recent_games)} recent games:")
    for i, game in enumerate(recent_games[:5]):
        away = game.get('away_name', 'Unknown')
        home = game.get('home_name', 'Unknown')
        score = f"{game.get('away_score', 0)}-{game.get('home_score', 0)}"
        print(f"{i+1}. {away} @ {home} ({score})")
    
    # Use first game for now
    selected_game = recent_games[0]
    away_team = selected_game.get('away_name', 'Unknown')
    home_team = selected_game.get('home_name', 'Unknown')
    game_id = selected_game.get('game_id', '')
    
    print(f"\nGenerating broadcast for: {away_team} @ {home_team}")
    
    # Get pitch data
    pitch_data = get_game_pitch_data(game_id)
    
    if not pitch_data:
        print("No pitch data found for this game")
        return
    
    print(f"Processing {len(pitch_data)} pitches...")
    
    # Generate script
    script = generate_broadcast_script(pitch_data, max_pitches=40)
    
    # Save script
    script_file = "broadcast_script.txt"
    with open(script_file, 'w') as f:
        f.write(script)
    print(f"Script saved to {script_file}")
    
    # Preview script
    print("\n" + "="*60)
    print("BROADCAST PREVIEW (first 200 chars):")
    print("="*60)
    print(script[:200] + "...")
    print("="*60)
    
    # Generate audio
    audio_file = f"{away_team.replace(' ', '_')}_vs_{home_team.replace(' ', '_')}_broadcast.mp3"
    print(f"\nGenerating audio broadcast...")
    
    if text_to_speech(script, audio_file):
        print(f"✅ Success! Audio broadcast saved to: {audio_file}")
        print(f"🎧 Play your bedtime baseball broadcast:")
        print(f"   open '{audio_file}'")
    else:
        print("❌ Audio generation failed. Set OPENAI_API_KEY to enable TTS.")
        print(f"📝 Text script available in: {script_file}")

if __name__ == "__main__":
    main()