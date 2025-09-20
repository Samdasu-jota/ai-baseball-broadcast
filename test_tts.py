#!/usr/bin/env python3

import os
from openai import OpenAI

def text_to_speech(text, output_file="broadcast_audio.mp3"):
    """Convert text to speech using OpenAI TTS API"""
    
    # Check for API key
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
            voice="onyx",  # Deep, calm voice good for bedtime
            input=text
        )
        
        # Save audio file
        response.stream_to_file(output_file)
        print(f"Audio saved to {output_file}")
        return True
        
    except Exception as e:
        print(f"Error generating speech: {e}")
        return False

def main():
    # Test with sample text first
    sample_text = """
    Top of the 1st inning. deGrom delivers a 98.5 mile per hour fastball to Trout, ball. 
    deGrom delivers a 84.2 mile per hour slider to Trout, strike. 
    Bottom of the 1st. Ohtani delivers a 78.9 mile per hour curveball to Acuña, strike.
    """
    
    print("Testing OpenAI TTS with sample text...")
    success = text_to_speech(sample_text, "test_broadcast.mp3")
    
    if success:
        print("Success! Test audio generated.")
        print("Try playing it: open test_broadcast.mp3")
    else:
        print("TTS test failed. Check your OpenAI API key.")

if __name__ == "__main__":
    main()