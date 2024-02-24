# Extract-Audio-and-Shots

## Brief

This tool is designed to simplify the process of extracting audio and shots from videos using Python. It provides a user-friendly GUI built with Tkinter and utilizes the MoviePy library for video processing tasks. With this tool, users can easily select source and destination folders, choose extraction modes, set output formats, specify the number of shots to extract per minute, and control the number of parallel threads for faster processing.

## Snapshot

![Tool Snapshot](Snapshot.png)

## Workflow Explanation


1. **Select Source and Destination Folders:** Choose the folder containing your input videos and specify where to save the processed output.
2. **Choose Extraction Modes and Output Formats:** Select the desired extraction modes (audio, shots, or both) and specify the output formats for audio and images (e.g., MP3, WAV, JPEG, PNG).
3. **Set Shot Extraction Parameter:** Specify the number of shots to extract per minute of the video.
4. **Set Number of Workers:** Adjust the number of simultaneous videos being processed. By default, the number of workers is set to the number of available CPU cores.
5. **Run Video Processing:** Click the button to start processing the videos.

## Setup Instructions

### Using Python Virtual Environment

1. Create a Python virtual environment:
   ```bash
   python -m venv local
   ```
2. Install dependencies:
   ```bash
   .\local\Scripts\pip install moviepy==1.0.3
   ```
3. Run the tool:
   ```bash
   .\local\Scripts\python main.py
   ```

### Using Executables

1. Download the pre-built executable from the releases section.
2. Double-click the executable to run the tool.

## Notes

The application features two terminals:
  - An embedded terminal displays processed files along with their status (success or failure).
  - Another terminal provides backend progress updates for each file being processed.
