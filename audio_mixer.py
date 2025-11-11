#!/usr/bin/env python3
"""
Audio mixer for baseball broadcasts
Combines TTS narration with baseball sound effects (glove catches, bat hits, crowd reactions)
Uses user's custom sound effect organization with pitch speed-based selection
"""

from pydub import AudioSegment
from pydub.playback import play
import os
import random

class BaseballAudioMixer:
    """Mixes TTS narration with baseball sound effects"""

    def __init__(self, sound_effects_dir="sound_effects", enable_background_crowd=True):
        """
        Initialize mixer with sound effects directory

        Args:
            sound_effects_dir: Directory containing sound effect folders
            enable_background_crowd: Whether to mix in continuous crowd ambiance
        """
        self.sound_effects_dir = sound_effects_dir
        self.enable_background_crowd = enable_background_crowd
        self.sounds = {}
        self._load_sound_effects()

    def _load_sound_effects(self):
        """Load all sound effects from user's folder structure"""
        if not os.path.exists(self.sound_effects_dir):
            print(f"⚠️  Sound effects directory not found: {self.sound_effects_dir}")
            print(f"   Sound effects will be skipped.")
            return

        # User's directory structure:
        # sound_effects/
        #   catching ball/
        #     fastball.mp3
        #     slowball.mp3
        #   hitting ball/
        #     bat1.mp3
        #     bat2.mp3
        #     bat3.mp3
        #     bunt.mp3
        #   reaction/
        #     any hit or homerun.mp3
        #     normal croud sound.mp3

        print("🔊 Loading sound effects...")

        # Catching ball sounds
        catching_dir = os.path.join(self.sound_effects_dir, "catching ball")
        self._load_file(catching_dir, "fastball.mp3", "catch_fastball")
        self._load_file(catching_dir, "slowball.mp3", "catch_slowball")

        # Hitting ball sounds
        hitting_dir = os.path.join(self.sound_effects_dir, "hitting ball")
        self._load_file(hitting_dir, "bat1.mp3", "bat1")
        self._load_file(hitting_dir, "bat2.mp3", "bat2")
        self._load_file(hitting_dir, "bat3.mp3", "bat3")
        self._load_file(hitting_dir, "bunt.mp3", "bunt")

        # Reaction sounds
        reaction_dir = os.path.join(self.sound_effects_dir, "reaction")
        self._load_file(reaction_dir, "any hit or homerun.mp3", "hit_reaction")
        self._load_file(reaction_dir, "normal croud sound.mp3", "crowd_ambient")

        print(f"\n✅ Loaded {len(self.sounds)} sound effects")

    def _load_file(self, directory, filename, key):
        """Helper to load a single sound file"""
        filepath = os.path.join(directory, filename)
        if os.path.exists(filepath):
            try:
                self.sounds[key] = AudioSegment.from_mp3(filepath)
                print(f"   ✅ {key}: {filename}")
            except Exception as e:
                print(f"   ⚠️  Failed to load {filename}: {e}")
        else:
            print(f"   ⚠️  Not found: {filepath}")

    def create_silence(self, duration_ms):
        """Create silent audio segment"""
        return AudioSegment.silent(duration=duration_ms)

    def get_catching_sound(self, pitch_type, speed):
        """
        Get appropriate catching sound based on pitch type and speed

        Rules:
        - fastball.mp3: four-seam fastball, sinker (>93 mph), cutter (>94 mph), any pitch >95 mph
        - slowball.mp3: all other pitches

        Args:
            pitch_type: Type of pitch (e.g., "fastball", "curveball", "slider")
            speed: Pitch speed in MPH

        Returns:
            AudioSegment or None
        """
        pitch_lower = pitch_type.lower() if pitch_type else ""

        # Rule 1: Four-seam fastball always uses fastball sound
        if "fastball" in pitch_lower and "seam" not in pitch_lower:
            return self.sounds.get('catch_fastball')

        # Rule 2: Sinker > 93 mph uses fastball sound
        if "sinker" in pitch_lower and speed > 93:
            return self.sounds.get('catch_fastball')

        # Rule 3: Cutter > 94 mph uses fastball sound
        if "cutter" in pitch_lower and speed > 94:
            return self.sounds.get('catch_fastball')

        # Rule 4: Any pitch > 95 mph uses fastball sound
        if speed > 95:
            return self.sounds.get('catch_fastball')

        # All other pitches use slowball sound
        return self.sounds.get('catch_slowball')

    def get_hitting_sound(self, at_bat_event):
        """
        Get appropriate hitting sound based on at-bat outcome

        Rules:
        - Home run: bat1.mp3
        - Bunt: bunt.mp3
        - Any other hit: random (bat1, bat2, or bat3)

        Args:
            at_bat_event: At-bat outcome (e.g., "Home Run", "Single", "Bunt")

        Returns:
            AudioSegment or None
        """
        if not at_bat_event:
            # Random bat sound for generic hits
            bat_sounds = [self.sounds.get('bat1'), self.sounds.get('bat2'), self.sounds.get('bat3')]
            bat_sounds = [s for s in bat_sounds if s is not None]
            return random.choice(bat_sounds) if bat_sounds else None

        event_lower = at_bat_event.lower()

        # Home run always uses bat1
        if "home run" in event_lower or "homerun" in event_lower:
            return self.sounds.get('bat1')

        # Bunt uses bunt sound
        if "bunt" in event_lower:
            return self.sounds.get('bunt')

        # Any other hit: random bat sound
        bat_sounds = [self.sounds.get('bat1'), self.sounds.get('bat2'), self.sounds.get('bat3')]
        bat_sounds = [s for s in bat_sounds if s is not None]
        return random.choice(bat_sounds) if bat_sounds else None

    def get_reaction_sound(self, at_bat_event):
        """
        Get crowd reaction sound

        Rules:
        - Any hit or home run: "any hit or homerun.mp3"
        - Default: none (background crowd is continuous)

        Args:
            at_bat_event: At-bat outcome

        Returns:
            AudioSegment or None
        """
        if not at_bat_event:
            return None

        event_lower = at_bat_event.lower()

        # Any hit or home run gets crowd reaction
        if any(word in event_lower for word in ["home run", "homerun", "single", "double", "triple", "hit"]):
            return self.sounds.get('hit_reaction')

        return None

    def get_sound_for_result(self, pitch_type, speed, result, at_bat_event=None):
        """
        Get appropriate sound effect(s) for pitch result

        Args:
            pitch_type: Type of pitch (e.g., "fastball", "curveball")
            speed: Pitch speed in MPH
            result: Pitch result (e.g., "Called Strike", "Ball", "In Play")
            at_bat_event: At-bat outcome (e.g., "Home Run", "Strikeout")

        Returns:
            dict with 'catch' and 'reaction' sounds, or None
        """
        result_lower = result.lower()
        sounds = {}

        # Ball in play - use hitting sound + reaction
        if "in play" in result_lower or "hit" in result_lower:
            sounds['hit'] = self.get_hitting_sound(at_bat_event)
            sounds['reaction'] = self.get_reaction_sound(at_bat_event)
        else:
            # Strike, ball, or foul - use catching sound
            sounds['catch'] = self.get_catching_sound(pitch_type, speed)

        return sounds

    def mix_broadcast_with_effects(self, narration_audio, pitch_events, output_file, enable_background_crowd=None):
        """
        Mix narration with sound effects

        User's sounds already include pitch/windup, so NO anticipation pause needed

        Args:
            narration_audio: AudioSegment of TTS narration
            pitch_events: List of dicts with pitch info:
                [{'pitch_type': 'fastball', 'speed': 95, 'result': 'Strike',
                  'at_bat_event': 'Strikeout', 'timestamp_ms': 1000}, ...]
            output_file: Output filename
            enable_background_crowd: Override instance setting for background crowd

        Returns:
            AudioSegment of mixed audio
        """
        if enable_background_crowd is None:
            enable_background_crowd = self.enable_background_crowd

        if not pitch_events:
            # No events, just add background crowd if enabled
            final_audio = self._add_background_crowd(narration_audio) if enable_background_crowd else narration_audio
            final_audio.export(output_file, format="mp3")
            return final_audio

        # Start with empty audio
        final_audio = AudioSegment.empty()
        prev_timestamp = 0

        for event in pitch_events:
            timestamp_ms = event.get('timestamp_ms', 0)
            pitch_type = event.get('pitch_type', '')
            speed = event.get('speed', 0)
            result = event.get('result', '')
            at_bat_event = event.get('at_bat_event')

            # Add narration chunk up to this event
            narration_chunk = narration_audio[prev_timestamp:timestamp_ms]
            final_audio += narration_chunk

            # Get appropriate sound effect(s)
            sounds = self.get_sound_for_result(pitch_type, speed, result, at_bat_event)

            # Add sound effects
            if sounds.get('catch'):
                # Catching sound (already has pitch windup built-in)
                final_audio += sounds['catch']

            if sounds.get('hit'):
                # Hitting sound (already has pitch windup built-in)
                final_audio += sounds['hit']

            if sounds.get('reaction'):
                # Crowd reaction (comes right after hit)
                final_audio += sounds['reaction']

            # Brief pause after sound effects before next narration
            final_audio += self.create_silence(200)

            prev_timestamp = timestamp_ms

        # Add remaining narration
        final_audio += narration_audio[prev_timestamp:]

        # Add background crowd ambiance if enabled
        if enable_background_crowd:
            final_audio = self._add_background_crowd(final_audio)

        # Export final mix
        final_audio.export(output_file, format="mp3")
        print(f"✅ Mixed audio saved to {output_file}")

        return final_audio

    def _add_background_crowd(self, audio):
        """
        Add continuous background crowd ambiance throughout the broadcast

        Args:
            audio: Main audio (narration + effects)

        Returns:
            AudioSegment with crowd ambiance mixed in
        """
        crowd = self.sounds.get('crowd_ambient')
        if not crowd:
            return audio

        # Loop crowd sound to match broadcast length
        crowd_length = len(crowd)
        audio_length = len(audio)
        loops_needed = (audio_length // crowd_length) + 1

        looped_crowd = crowd * loops_needed
        looped_crowd = looped_crowd[:audio_length]  # Trim to exact length

        # Mix at lower volume (-15 dB so it doesn't overpower narration)
        looped_crowd = looped_crowd - 15

        # Overlay crowd behind main audio
        mixed = audio.overlay(looped_crowd)

        return mixed


def main():
    """Test the audio mixer"""
    print("🎙️  Baseball Audio Mixer Test")
    print("=" * 60)

    mixer = BaseballAudioMixer()

    print("\n📁 Sound Effects Status:")
    print(f"   Loaded {len(mixer.sounds)} sound effects")

    if mixer.sounds:
        print("\n🎵 Available sounds:")
        for name in mixer.sounds.keys():
            print(f"   - {name}")
    else:
        print("\n⚠️  No sound effects loaded")
        print("   The mixer will work without sound effects,")
        print("   but download some for the full experience!")


if __name__ == "__main__":
    main()
