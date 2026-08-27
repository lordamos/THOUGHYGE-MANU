#!/usr/bin/env python3
import pyaudio

def list_audio_devices():
    pya = pyaudio.PyAudio()
    
    print("Available Audio Input Devices:")
    print("=" * 50)
    
    input_devices = []
    for i in range(pya.get_device_count()):
        device_info = pya.get_device_info_by_index(i)
        if device_info['maxInputChannels'] > 0:
            input_devices.append((i, device_info))
            print(f"Device {i}: {device_info['name']}")
            print(f"  - Max Input Channels: {device_info['maxInputChannels']}")
            print(f"  - Default Sample Rate: {device_info['defaultSampleRate']} Hz")
            print(f"  - Host API: {pya.get_host_api_info_by_index(device_info['hostApi'])['name']}")
            print()
    
    default_input = pya.get_default_input_device_info()
    print(f"Default Input Device: {default_input['name']} (Index: {pya.get_default_input_device_info()['index']})")
    
    pya.terminate()
    return input_devices

if __name__ == "__main__":
    list_audio_devices()