#!/usr/bin/env python3
"""
Simple microphone test script to verify audio input is working
"""
import pyaudio
import numpy as np
import time

# Audio settings
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  # Same rate as the Gemini script
CHUNK = 1024
RECORD_SECONDS = 5

def test_microphone():
    print("Testing microphone...")
    print(f"Recording for {RECORD_SECONDS} seconds. Please speak into your microphone.")
    
    # Initialize PyAudio
    pya = pyaudio.PyAudio()
    
    try:
        # Get default input device info
        input_info = pya.get_default_input_device_info()
        print(f"Using microphone: {input_info['name']}")
        print(f"Default sample rate: {input_info['defaultSampleRate']} Hz")
        
        # Open stream
        stream = pya.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
            input_device_index=input_info["index"]
        )
        
        print("Recording started...")
        frames = []
        max_amplitude = 0
        
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            try:
                data = stream.read(CHUNK, exception_on_overflow=False)
                frames.append(data)
                
                # Convert to numpy array to check amplitude
                audio_data = np.frombuffer(data, dtype=np.int16)
                current_max = np.max(np.abs(audio_data))
                max_amplitude = max(max_amplitude, current_max)
                
                # Print progress with volume indicator
                progress = (i + 1) / int(RATE / CHUNK * RECORD_SECONDS)
                bars = int(progress * 20)
                volume_bars = min(int(current_max / 1000), 10)  # Scale volume to 0-10
                print(f"\rProgress: [{'='*bars}{' '*(20-bars)}] {progress*100:.0f}% | Volume: [{'#'*volume_bars}{' '*(10-volume_bars)}]", end='')
                
            except Exception as e:
                print(f"\nError reading audio: {e}")
                break
        
        print(f"\nRecording finished!")
        print(f"Maximum amplitude detected: {max_amplitude}")
        
        if max_amplitude > 100:
            print("✅ Microphone is working! Audio input detected.")
        else:
            print("❌ No significant audio detected. Check microphone settings.")
            
    except Exception as e:
        print(f"Error opening audio stream: {e}")
        print("This might be a permission or device access issue.")
        
    finally:
        if 'stream' in locals():
            stream.stop_stream()
            stream.close()
        pya.terminate()

if __name__ == "__main__":
    test_microphone()