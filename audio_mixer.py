#!/usr/bin/env python3
"""
Audio mixer for baseball broadcasts
Combines TTS narration with baseball sound effects (glove catches, bat hits, crowd cheers)
"""

from pydub import AudioSegment
from pydub.playback import play
import os

class BaseballAudioMixer:
    """Mixes TTS narration with baseball sound effects"""

    def __init__(self, sound_effects_dir="sound_effects"):
        """Initialize mixer with sound effects directory"""
        self.sound_effects_dir = sound_effects_dir
        self.sounds = {}
        self._load_sound_effects()

    def _load_sound_effects(self):
        """Load all sound effects into memory"""
        if not os.path.exists(self.sound_effects_dir):
            print(f"⚠️  Sound effects directory not found: {self.sound_effects_dir}")
            print(f"   Sound effects will be skipped. To enable:")
            print(f"   1. Create directory: mkdir {self.sound_effects_dir}")
            print(f"   2. Download free baseball sounds from:")
            print(f"      - https://freesound.org")
            print(f"      - https://pixabay.com/sound-effects/search/baseball/")
            print(f"   3. Add files: catch.mp3, hit.mp3, crowd_cheer.mp3, swing_miss.mp3")
            return

        # Expected sound effect files
        effect_files = {
            'catch': 'catch.mp3',          # Glove catching ball (for strikes/balls)
            'hit': 'hit.mp3',              # Bat hitting ball (for balls in play)
            'swing_miss': 'swing_miss.mp3', # Bat swinging and missing
            'crowd_cheer': 'crowd_cheer.mp3', # Crowd cheering (for home runs/big hits)
            'crowd_groan': 'crowd_groan.mp3'  # Crowd groaning (for strikeouts)
        }

        for effect_name, filename in effect_files.items():
            filepath = os.path.join(self.sound_effects_dir, filename)
            if os.path.exists(filepath):
                try:
                    self.sounds[effect_name] = AudioSegment.from_mp3(filepath)
                    print(f"✅ Loaded: {effect_name}")
                except Exception as e:
                    print(f"⚠️  Failed to load {filename}: {e}")
            else:
                print(f"⚠️  Sound effect not found: {filepath}")

    def create_silence(self, duration_ms):
        """Create silent audio segment"""
        return AudioSegment.silent(duration=duration_ms)

    def get_sound_for_result(self, result, at_bat_event=None):
        """
        Get appropriate sound effect for pitch result

        Args:
            result: Pitch result (e.g., "Called Strike", "Ball", "In Play")
            at_bat_event: At-bat outcome (e.g., "Home Run", "Strikeout")

        Returns:
            AudioSegment or None
        """
        result_lower = result.lower()

        # Home run gets special treatment
        if at_bat_event and "home run" in at_bat_event.lower():
            return self.sounds.get('crowd_cheer')

        # Strikeout gets crowd reaction
        if at_bat_event and "strikeout" in at_bat_event.lower():
            return self.sounds.get('crowd_groan')

        # Swinging strike - whoosh sound
        if "swinging" in result_lower or "swing" in result_lower:
            return self.sounds.get('swing_miss')

        # Ball in play - bat hit sound
        if "in play" in result_lower or "hit" in result_lower:
            return self.sounds.get('hit')

        # Strike or ball - glove catch sound
        if "strike" in result_lower or "ball" in result_lower or "foul" in result_lower:
            return self.sounds.get('catch')

        return None

    def mix_broadcast_with_effects(self, narration_audio, pitch_events, output_file):
        """
        Mix narration with sound effects

        Args:
            narration_audio: AudioSegment of TTS narration
            pitch_events: List of dicts with pitch info: [{'result': 'Strike', 'at_bat_event': 'Strikeout', 'timestamp_ms': 1000}, ...]
            output_file: Output filename

        Returns:
            AudioSegment of mixed audio
        """
        if not pitch_events:
            # No events, just return narration as-is
            narration_audio.export(output_file, format="mp3")
            return narration_audio

        # Start with empty audio
        final_audio = AudioSegment.empty()

        prev_timestamp = 0

        for event in pitch_events:
            timestamp_ms = event.get('timestamp_ms', 0)
            result = event.get('result', '')
            at_bat_event = event.get('at_bat_event')

            # Add narration chunk up to this event
            narration_chunk = narration_audio[prev_timestamp:timestamp_ms]
            final_audio += narration_chunk

            # Add anticipation pause (0.8 seconds - time for pitcher windup in listener's mind)
            final_audio += self.create_silence(800)

            # Add appropriate sound effect
            sound_effect = self.get_sound_for_result(result, at_bat_event)
            if sound_effect:
                # Normalize volume of sound effect
                sound_effect = sound_effect - 3  # Slightly quieter than narration
                final_audio += sound_effect

            # Short pause after sound effect
            final_audio += self.create_silence(300)

            prev_timestamp = timestamp_ms

        # Add remaining narration
        final_audio += narration_audio[prev_timestamp:]

        # Export final mix
        final_audio.export(output_file, format="mp3")
        print(f"✅ Mixed audio saved to {output_file}")

        return final_audio


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
