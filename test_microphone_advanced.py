#!/usr/bin/env python3
"""
Advanced microphone test script to try different devices and sample rates
"""
import pyaudio
import numpy as np
import time

# Test different sample rates
RATES_TO_TEST = [16000, 44100, 48000]
FORMAT = pyaudio.paInt16
CHANNELS = 1
CHUNK = 1024
RECORD_SECONDS = 3

def test_device(device_index, device_name, sample_rate):
    """Test a specific device at a specific sample rate"""
    print(f"\n--- Testing Device {device_index}: {device_name} at {sample_rate} Hz ---")
    
    pya = pyaudio.PyAudio()
    
    try:
        # Try to open the stream
        stream = pya.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=sample_rate,
            input=True,
            frames_per_buffer=CHUNK,
            input_device_index=device_index
        )
        
        print(f"Stream opened successfully. Recording for {RECORD_SECONDS} seconds...")
        max_amplitude = 0
        
        for i in range(0, int(sample_rate / CHUNK * RECORD_SECONDS)):
            try:
                data = stream.read(CHUNK, exception_on_overflow=False)
                
                # Convert to numpy array to check amplitude
                audio_data = np.frombuffer(data, dtype=np.int16)
                current_max = np.max(np.abs(audio_data))
                max_amplitude = max(max_amplitude, current_max)
                
                # Show simple progress
                if i % 10 == 0:
                    progress = (i + 1) / int(sample_rate / CHUNK * RECORD_SECONDS)
                    print(f"Progress: {progress*100:.0f}% | Current volume: {current_max}")
                
            except Exception as e:
                print(f"Error reading audio: {e}")
                break
        
        print(f"Recording finished! Maximum amplitude: {max_amplitude}")
        
        if max_amplitude > 100:
            print("✅ SUCCESS: Audio detected!")
            return True
        else:
            print("❌ No audio detected")
            return False
            
    except Exception as e:
        print(f"❌ Failed to open stream: {e}")
        return False
        
    finally:
        if 'stream' in locals():
            stream.stop_stream()
            stream.close()
        pya.terminate()

def test_promising_devices():
    """Test the most promising microphone devices"""
    
    # Devices to test (based on your list)
    devices_to_test = [
        (1, "Microphone (USBAudio1.0)"),           # Your current default
        (17, "Headset (Galaxy Buds FE)"),          # Bluetooth headset with 16kHz
        (22, "Microphone Array 2"),                # Intel SST with 16kHz 
        (23, "Microphone Array 3"),                # Intel SST with 16kHz
        (31, "Microphone (Realtek HD Audio)")      # Built-in mic
    ]
    
    print("Testing promising microphone devices...")
    print("PLEASE SPEAK INTO YOUR MICROPHONE during each test!")
    print("=" * 60)
    
    successful_configs = []
    
    for device_index, device_name in devices_to_test:
        # Test different sample rates for each device
        for rate in RATES_TO_TEST:
            success = test_device(device_index, device_name, rate)
            if success:
                successful_configs.append((device_index, device_name, rate))
                break  # Found working config for this device, move to next
    
    print("\n" + "=" * 60)
    print("RESULTS:")
    
    if successful_configs:
        print("✅ Working microphone configurations found:")
        for device_index, device_name, rate in successful_configs:
            print(f"  - Device {device_index}: {device_name} at {rate} Hz")
        
        # Recommend the best option
        print(f"\n🎯 RECOMMENDED: Use Device {successful_configs[0][0]} ({successful_configs[0][1]}) at {successful_configs[0][2]} Hz")
        
    else:
        print("❌ No working microphone configurations found.")
        print("This suggests a Windows permissions issue or hardware problem.")
        print("\nTroubleshooting steps:")
        print("1. Check Windows Privacy Settings → Microphone")
        print("2. Make sure your microphone is not muted")
        print("3. Try a different microphone/headset")
        print("4. Restart your audio drivers")

if __name__ == "__main__":
    test_promising_devices()