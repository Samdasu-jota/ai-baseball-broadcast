#!/usr/bin/env python3
"""
Broadcast script generation module
Converts pitch data into natural language broadcast commentary
"""
import random

def format_pitch_type(pitch_type):
    """Clean up pitch type names"""
    if not pitch_type or pitch_type == "Unknown":
        return "pitch"

    # User-specified simplifications for clarity
    pitch_lower = pitch_type.lower()
    if "four-seam" in pitch_lower or "4-seam" in pitch_lower:
        return "fastball"
    elif "two-seam" in pitch_lower or "2-seam" in pitch_lower:
        return "sinker"

    # All other pitch types stay as-is
    return pitch_lower

def format_pitch_location(pX, pZ, zone):
    """Describe the pitch location in broadcast terms"""
    if pX is None or pZ is None:
        return ""

    # Horizontal location (from catcher's perspective)
    if pX < -0.7:
        horizontal = "inside"
    elif pX > 0.7:
        horizontal = "outside"
    else:
        horizontal = "middle"

    # Vertical location
    if pZ > 3.5:
        vertical = "high"
    elif pZ < 1.5:
        vertical = "low"
    else:
        vertical = ""

    # Combine to make natural description
    if vertical and horizontal != "middle":
        location = f"{vertical} and {horizontal}"
    elif vertical:
        location = vertical
    elif horizontal != "middle":
        location = horizontal
    else:
        location = "down the middle"

    return location

def format_count(balls, strikes):
    """Format the count in a natural way"""
    if balls == 0 and strikes == 0:
        return ""
    return f"The count is {balls} and {strikes}. "

def format_at_bat_outcome(at_bat_event):
    """Format the at-bat outcome for broadcast with dramatic pauses"""
    if not at_bat_event:
        return ""

    # Map event types to broadcast descriptions
    # Add ellipses for dramatic moments
    event_lower = at_bat_event.lower()

    if "strikeout" in event_lower or "strike out" in event_lower:
        return "And... struck him out!"
    elif "walk" in event_lower:
        return "Ball four... that's a walk."
    elif "home run" in event_lower or "homerun" in event_lower:
        return "And it's gone... home run!"
    elif "double" in event_lower:
        return "That's a double!"
    elif "triple" in event_lower:
        return "And... he's got a triple!"
    elif "single" in event_lower:
        return "Base hit."
    elif "groundout" in event_lower or "ground out" in event_lower:
        return "Ground out."
    elif "flyout" in event_lower or "fly out" in event_lower:
        return "Fly out."
    elif "lineout" in event_lower or "line out" in event_lower:
        return "Line out."
    elif "pop out" in event_lower or "popout" in event_lower:
        return "Pop out."
    elif "sac fly" in event_lower or "sacrifice" in event_lower:
        return "Sacrifice fly."
    elif "double play" in event_lower:
        return "Double play!"
    elif "error" in event_lower:
        return "Error on the play."
    else:
        # Default: just use the event name
        return f"{at_bat_event}."

def generate_pitch_description(pitch, mention_batter=True, mention_pitcher=True):
    """Convert pitch data to broadcast text with varied, natural broadcaster style

    Args:
        pitch: Pitch data dictionary
        mention_batter: Whether to mention the batter's name (False for continuation pitches)
        mention_pitcher: Whether to mention the pitcher's name (False after introduction)
    """
    pitcher = pitch['pitcher'].split()[-1]  # Use last name only
    batter = pitch['batter'].split()[-1]    # Use last name only

    speed = pitch['speed']
    pitch_type = format_pitch_type(pitch['pitch_type'])
    result = pitch['result'].lower()
    location = format_pitch_location(pitch.get('pX'), pitch.get('pZ'), pitch.get('zone'))

    # Get count for context
    balls = pitch.get('balls', 0)
    strikes = pitch.get('strikes', 0)

    # Action verbs for variety (instead of always "delivers")
    pitch_verbs = ["fires", "deals", "throws", "comes with"]
    verb = random.choice(pitch_verbs)

    # Build pitch speed and type description
    speed_int = int(round(speed)) if speed > 0 else None

    # Different result descriptions - more vivid
    if "ball" in result:
        if "high" in location:
            outcome = "high, ball"
        elif "low" in location:
            outcome = "low, ball"
        else:
            outcome = "ball"
    elif "called" in result and "strike" in result:
        outcome = "got him looking, strike"
    elif "swinging" in result or ("strike" in result and "foul" not in result):
        outcome = "swings and misses, strike"
    elif "foul" in result:
        outcome = "foul ball"
    elif "hit" in result or "in play" in result:
        outcome = "in play"
    else:
        outcome = result

    # Add count context for dramatic moments
    count_context = ""
    if balls == 3 and strikes == 2:
        count_context = "Full count, 3 and 2... "
    elif balls == 0 and strikes == 2:
        count_context = "Now 0 and 2... "
    elif balls == 3 and strikes == 0:
        count_context = "3-0 count... "

    # Choose sentence pattern randomly for variety
    pattern = random.randint(1, 4)

    # Pattern 1: Direct with action verb
    if pattern == 1:
        if mention_pitcher and mention_batter:
            if speed_int and location:
                pitch_text = f"{count_context}{pitcher} {verb} a {speed_int} mile per hour {pitch_type}, {location}, to {batter}. {outcome.capitalize()}."
            elif speed_int:
                pitch_text = f"{count_context}{pitcher} {verb} a {speed_int} mile per hour {pitch_type} to {batter}. {outcome.capitalize()}."
            else:
                pitch_text = f"{count_context}{pitcher} {verb} the {pitch_type} to {batter}. {outcome.capitalize()}."
        elif mention_pitcher:
            if speed_int and location:
                pitch_text = f"{count_context}{pitcher} {verb} a {speed_int} mile per hour {pitch_type}, {location}. {outcome.capitalize()}."
            elif speed_int:
                pitch_text = f"{count_context}{pitcher} {verb} a {speed_int} mile per hour {pitch_type}. {outcome.capitalize()}."
            else:
                pitch_text = f"{count_context}{pitcher} {verb} the {pitch_type}. {outcome.capitalize()}."
        else:
            if speed_int and location:
                pitch_text = f"{count_context}The {pitch_type}, {speed_int}, {location}. {outcome.capitalize()}."
            elif speed_int:
                pitch_text = f"{count_context}The {pitch_type}, {speed_int}. {outcome.capitalize()}."
            else:
                pitch_text = f"{count_context}The {pitch_type}. {outcome.capitalize()}."

    # Pattern 2: "Here's the pitch..." announcer style
    elif pattern == 2:
        if mention_batter:
            if speed_int and location:
                pitch_text = f"{count_context}Here's the pitch to {batter}... {pitch_type}, {speed_int} miles per hour, {location}. {outcome.capitalize()}."
            elif speed_int:
                pitch_text = f"{count_context}Here's the pitch to {batter}... {pitch_type}, {speed_int}. {outcome.capitalize()}."
            else:
                pitch_text = f"{count_context}Here's the pitch to {batter}... {pitch_type}. {outcome.capitalize()}."
        else:
            if speed_int and location:
                pitch_text = f"{count_context}Here's the pitch... {pitch_type}, {speed_int}, {location}. {outcome.capitalize()}."
            elif speed_int:
                pitch_text = f"{count_context}Here's the pitch... {pitch_type}, {speed_int}. {outcome.capitalize()}."
            else:
                pitch_text = f"{count_context}Here's the pitch... {pitch_type}. {outcome.capitalize()}."

    # Pattern 3: Speed first "95 on the gun..."
    elif pattern == 3 and speed_int:
        if location:
            pitch_text = f"{count_context}{speed_int} on the gun... {pitch_type}, {location}. {outcome.capitalize()}."
        else:
            pitch_text = f"{count_context}{speed_int} miles per hour, {pitch_type}. {outcome.capitalize()}."

    # Pattern 4: Minimal / fallback
    else:
        if speed_int and location:
            pitch_text = f"{count_context}The {pitch_type}, {speed_int}, {location}. {outcome.capitalize()}."
        elif speed_int:
            pitch_text = f"{count_context}The {pitch_type}, {speed_int}. {outcome.capitalize()}."
        else:
            pitch_text = f"{count_context}The {pitch_type}. {outcome.capitalize()}."

    # Add at-bat outcome if this is the last pitch
    at_bat_event = pitch.get('at_bat_event')
    if at_bat_event:
        at_bat_outcome = format_at_bat_outcome(at_bat_event)
        if at_bat_outcome:
            pitch_text += f" {at_bat_outcome}"

        # Add RBI and score if runs were scored
        rbi = pitch.get('rbi', 0)
        if rbi > 0:
            if rbi == 1:
                pitch_text += f" That brings in a run."
            else:
                pitch_text += f" That brings in {rbi} runs."

    return pitch_text

def generate_inning_intro(inning, half_inning, prev_inning=None, prev_half=None):
    """Generate inning transitions"""
    if prev_inning != inning or prev_half != half_inning:
        if half_inning == "top":
            return f"Top of the {inning}."
        else:
            return f"Bottom of the {inning}."
    return ""

def generate_inning_summary(away_score, home_score, away_team=None, home_team=None):
    """Generate score summary at end of inning half"""
    if away_team and home_team:
        if away_score > home_score:
            return f"After that half inning, {away_team} leads {away_score} to {home_score}."
        elif home_score > away_score:
            return f"After that half inning, {home_team} leads {home_score} to {away_score}."
        else:
            return f"After that half inning, we're tied at {away_score}."
    else:
        # Without team names, just mention who's leading
        if away_score > home_score:
            return f"The visitors lead {away_score} to {home_score}."
        elif home_score > away_score:
            return f"The home team leads {home_score} to {away_score}."
        else:
            return f"We're tied at {away_score}."

def select_pitches_from_key_innings(pitch_data, key_innings):
    """Select all pitches from specific innings (e.g., scoring innings)"""
    if not key_innings:
        # Fallback: if no key innings, return all pitches
        return pitch_data

    selected_pitches = []
    for pitch in pitch_data:
        if pitch['inning'] in key_innings:
            selected_pitches.append(pitch)

    return selected_pitches

def generate_broadcast_script(pitch_data, max_pitches=50, key_innings=None, away_team=None, home_team=None):
    """Convert pitch data into a natural broadcast script

    Args:
        pitch_data: List of pitch dictionaries
        max_pitches: Maximum number of pitches to include (ignored if key_innings provided)
        key_innings: List of specific innings to include (e.g., [1, 3, 7, 9])
        away_team: Away team name (for score summaries)
        home_team: Home team name (for score summaries)
    """
    if not pitch_data:
        return "No game data available."

    script_lines = []
    prev_inning = None
    prev_half = None

    # Select pitches based on key innings if provided
    if key_innings:
        selected_pitches = select_pitches_from_key_innings(pitch_data, key_innings)
        print(f"Selected {len(selected_pitches)} pitches from innings: {key_innings}")
    elif len(pitch_data) > max_pitches:
        # Fallback: Take key moments: first few innings, middle, and end
        selected_pitches = (
            pitch_data[:15] +  # First 15 pitches
            pitch_data[len(pitch_data)//2:len(pitch_data)//2+10] +  # 10 from middle
            pitch_data[-25:]   # Last 25 pitches
        )
    else:
        selected_pitches = pitch_data
    
    prev_batter = None
    prev_pitcher = None
    prev_pitcher_in_inning = None
    prev_away_score = 0
    prev_home_score = 0

    for i, pitch in enumerate(selected_pitches):
        current_inning = pitch['inning']
        current_half = pitch['half_inning']

        # Check if inning half ended (before starting new half)
        if prev_inning is not None and (prev_inning != current_inning or prev_half != current_half):
            # Add score summary at end of previous half inning
            script_lines.append("\n")
            score_summary = generate_inning_summary(prev_away_score, prev_home_score, away_team, home_team)
            script_lines.append(score_summary)
            script_lines.append("\n")

        # Add inning introduction if needed
        inning_intro = generate_inning_intro(
            current_inning,
            current_half,
            prev_inning,
            prev_half
        )

        if inning_intro:
            # Add extra line break before new inning
            if script_lines:
                script_lines.append("\n")
            script_lines.append(inning_intro)
            script_lines.append("\n")
            # Reset tracking for new inning
            prev_batter = None
            prev_pitcher_in_inning = None

        # Check if pitcher changed or new inning (need to introduce pitcher)
        current_pitcher = pitch['pitcher']
        current_inning_key = (pitch['inning'], pitch['half_inning'])

        # Mention pitcher if:
        # 1. First pitch of the inning (remind listeners who's pitching)
        # 2. Pitcher changed mid-inning
        if prev_pitcher_in_inning != current_pitcher:
            mention_pitcher = True
            prev_pitcher_in_inning = current_pitcher
        else:
            mention_pitcher = False

        # Check if batter changed (new at-bat)
        current_batter = pitch['batter']
        mention_batter = (current_batter != prev_batter)

        # Add pitch description
        pitch_desc = generate_pitch_description(pitch, mention_batter=mention_batter, mention_pitcher=mention_pitcher)
        script_lines.append(pitch_desc)
        script_lines.append(" ")

        # Check if at-bat ended (ball in play means batter's turn is likely over)
        result = pitch['result'].lower()
        at_bat_ended = False
        if "in play" in result or "hit" in result:
            prev_batter = None  # Reset so next batter gets introduced
            at_bat_ended = True
        else:
            prev_batter = current_batter

        prev_pitcher = current_pitcher

        # Track scores for summary
        prev_away_score = pitch['away_score']
        prev_home_score = pitch['home_score']

        # Add paragraph break after at-bat ends for natural breathing room
        if at_bat_ended:
            script_lines.append("\n\n")

        prev_inning = pitch['inning']
        prev_half = pitch['half_inning']

    # Add final score summary at end of game
    if selected_pitches:
        final_pitch = selected_pitches[-1]
        script_lines.append("\n\n")
        final_score_summary = generate_inning_summary(final_pitch['away_score'], final_pitch['home_score'], away_team, home_team)
        script_lines.append(final_score_summary)
        script_lines.append("\n")

    return "".join(script_lines)

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