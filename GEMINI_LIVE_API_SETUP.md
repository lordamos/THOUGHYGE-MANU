# Gemini Live API Setup Guide

This guide will help you set up and run the Gemini Live API script for real-time audio and video interaction.

## Prerequisites

1. **Python Environment**: Make sure you have Python 3.8+ installed
2. **Gemini API Key**: You'll need a Google AI Studio API key
3. **Hardware Requirements**:
   - Microphone for audio input
   - Camera for video input (optional)
   - Speakers or headphones for audio output

## Installation Steps

### 1. Install Required Dependencies

Run the following command to install all necessary packages:

```powershell
pip install google-genai opencv-python pyaudio pillow mss
```

**Note for Windows users**: If you encounter issues with `pyaudio`, you might need to install it separately:

```powershell
pip install pipwin
pipwin install pyaudio
```

### 2. Set up Your Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Set it as an environment variable:

**PowerShell (recommended for this session):**
```powershell
$env:GEMINI_API_KEY="your_api_key_here"
```

**Or permanently set it:**
```powershell
[Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "your_api_key_here", "User")
```

### 3. Test Your Setup

First, check if all dependencies are installed correctly:

```powershell
python -c "import cv2, pyaudio, PIL, mss, google.genai; print('All dependencies installed successfully!')"
```

## Running the Script

The script supports three modes:

### Camera Mode (Default)
Captures video from your webcam:
```powershell
python gemini_live_api.py
# or explicitly
python gemini_live_api.py --mode camera
```

### Screen Share Mode
Captures your screen:
```powershell
python gemini_live_api.py --mode screen
```

### Audio Only Mode
No video capture:
```powershell
python gemini_live_api.py --mode none
```

## How to Use

1. **Start the script** with your preferred mode
2. **Speak** into your microphone - the AI will hear you
3. **Type messages** in the terminal when prompted with `message > `
4. **Listen** to the AI's audio responses
5. **Type 'q'** to quit the application

## Features

- **Real-time audio conversation** with Gemini AI
- **Video input** from camera or screen sharing
- **Text input** via terminal
- **Audio output** with natural speech synthesis
- **Interruption support** - you can interrupt the AI while it's speaking

## Troubleshooting

### Common Issues:

1. **API Key Error**: Make sure your `GEMINI_API_KEY` environment variable is set correctly
2. **Camera Access**: Ensure your camera isn't being used by another application
3. **Audio Issues**: Check your microphone and speaker permissions
4. **Import Errors**: Verify all dependencies are installed correctly

### System Permissions:

On Windows, you might need to allow:
- Camera access for your Python application
- Microphone access
- Speaker/audio output access

## Security Notes

- Your API key grants access to Gemini AI - keep it secure
- Audio and video data is sent to Google's servers for processing
- Consider running in a private environment if handling sensitive information

## Performance Tips

- Close unnecessary applications to ensure smooth audio/video processing
- Use a good quality microphone for better speech recognition
- Ensure stable internet connection for real-time interaction