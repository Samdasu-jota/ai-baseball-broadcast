#!/usr/bin/env python3

def format_pitch_type(pitch_type):
    """Clean up pitch type names"""
    if not pitch_type or pitch_type == "Unknown":
        return "pitch"
    return pitch_type.lower()

def format_count(balls, strikes):
    """Format the count in a natural way"""
    if balls == 0 and strikes == 0:
        return ""
    return f"The count is {balls} and {strikes}. "

def generate_pitch_description(pitch):
    """Convert pitch data to broadcast text"""
    pitcher = pitch['pitcher'].split()[-1]  # Use last name only
    batter = pitch['batter'].split()[-1]    # Use last name only
    
    speed = pitch['speed']
    pitch_type = format_pitch_type(pitch['pitch_type'])
    result = pitch['result'].lower()
    
    # Create natural descriptions
    if speed > 0:
        speed_text = f"{speed:.1f} mile per hour {pitch_type}"
    else:
        speed_text = pitch_type
    
    # Different result descriptions
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
    
    # Take a sample of pitches to keep broadcast reasonable length
    if len(pitch_data) > max_pitches:
        # Take key moments: first few innings, middle, and end
        selected_pitches = (
            pitch_data[:15] +  # First 15 pitches
            pitch_data[len(pitch_data)//2:len(pitch_data)//2+10] +  # 10 from middle
            pitch_data[-25:]   # Last 25 pitches
        )
    else:
        selected_pitches = pitch_data
    
    for i, pitch in enumerate(selected_pitches):
        # Add inning introduction if needed
        inning_intro = generate_inning_intro(
            pitch['inning'], 
            pitch['half_inning'], 
            prev_inning, 
            prev_half
        )
        
        if inning_intro:
            script_lines.append(inning_intro)
        
        # Add pitch description
        pitch_desc = generate_pitch_description(pitch)
        script_lines.append(pitch_desc)
        
        # Add some breathing room every few pitches
        if i % 5 == 4:
            script_lines.append("")  # Pause
        
        prev_inning = pitch['inning']
        prev_half = pitch['half_inning']
    
    return " ".join(script_lines)

def main():
    # Test with sample pitch data
    sample_pitches = [
        {
            'inning': 1,
            'half_inning': 'top',
            'batter': 'Mike Trout',
            'pitcher': 'Jacob deGrom',
            'pitch_type': 'Fastball',
            'speed': 98.5,
            'result': 'Ball',
            'balls': 1,
            'strikes': 0
        },
        {
            'inning': 1,
            'half_inning': 'top',
            'batter': 'Mike Trout',
            'pitcher': 'Jacob deGrom',
            'pitch_type': 'Slider',
            'speed': 84.2,
            'result': 'Called Strike',
            'balls': 1,
            'strikes': 1
        },
        {
            'inning': 1,
            'half_inning': 'bottom',
            'batter': 'Ronald Acuña Jr.',
            'pitcher': 'Shohei Ohtani',
            'pitch_type': 'Curveball',
            'speed': 78.9,
            'result': 'Foul',
            'balls': 0,
            'strikes': 1
        }
    ]
    
    script = generate_broadcast_script(sample_pitches)
    print("Sample broadcast script:")
    print("=" * 50)
    print(script)

if __name__ == "__main__":
    main()