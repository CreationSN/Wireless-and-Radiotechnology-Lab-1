# Wireless and Radiotechnology Lab 1 - Video Recording & Transfer System

A Python-based system for recording, transmitting, and receiving video files over a network. This project demonstrates socket programming and real-time video handling using OpenCV.

## Overview

This system consists of three main components that work together to:
1. **Record** video from a webcam
2. **Send** recorded videos over a network
3. **Receive** and save transmitted videos

## Components

### 1. **recorder.py** - Video Recorder
Continuously records video from the system's webcam and saves it locally.

**Features:**
- Records 10-second video clips
- Captures every 2 minutes (120-second interval)
- Resolution: 640x480 at 20 FPS
- Saves files with timestamp: `video_YYYYMMDD_HHMMSS.mp4`
- Saves to local `videos/` folder

**Usage:**
```bash
python recorder.py
```

**Configuration:**
- `RECORD_SECONDS = 10` - Duration of each recording
- `INTERVAL_SECONDS = 120` - Wait time between recordings
- `FPS = 20.0` - Frames per second
- `FRAME_WIDTH = 640` - Video width in pixels
- `FRAME_HEIGHT = 480` - Video height in pixels

### 2. **sender.py** - Video Sender
Monitors the local `videos/` folder and sends any MP4 files to the receiver.

**Features:**
- Watches `videos/` folder for new MP4 files
- Automatically sends files to receiver on `localhost:5001`
- Deletes local file after successful transfer
- Checks folder every 5 seconds
- Sends filename first for server acknowledgment
- Sends data in 4KB chunks

**Usage:**
```bash
python sender.py
```

**Configuration:**
- `HOST = "127.0.0.1"` - Receiver IP address
- `PORT = 5001` - Receiver port
- `CHECK_INTERVAL = 5` - Folder check interval in seconds

### 3. **receiver.py** - Video Receiver
A server that listens for incoming video files and saves them to disk.

**Features:**
- Listens on port 5001
- Accepts connections from senders
- Receives filename and validates it
- Saves received video to `received_videos/` folder
- Sends confirmation after successful receipt
- Handles multiple connections

**Usage:**
```bash
python receiver.py
```

**Configuration:**
- `HOST = "0.0.0.0"` - Bind to all interfaces
- `PORT = 5001` - Listening port
- `SAVE_FOLDER = "received_videos"` - Download directory

## System Architecture

```
Webcam → [recorder.py] → videos/ 
                           ↓
                      [sender.py] → Network (localhost:5001)
                                        ↓
                                   [receiver.py] → received_videos/
```

## Installation & Setup

### Prerequisites
- Python 3.6+
- OpenCV: `pip install opencv-python`
- Socket library (built-in)

### Installation
```bash
pip install opencv-python
```

### Directory Structure
```
lab 1/
├── recorder.py
├── sender.py
├── receiver.py
├── videos/              (created automatically)
├── received_videos/     (created automatically)
└── README.md
```

## Running the System

### Option 1: All Processes on Same Machine

**Terminal 1 - Start the receiver:**
```bash
python receiver.py
```
Output: `Receiver is waiting for files...`

**Terminal 2 - Start the sender:**
```bash
python sender.py
```
Output: `Sender started. Watching video folder...`

**Terminal 3 - Start the recorder:**
```bash
python recorder.py
```
Output: `Recorder started. Press Ctrl+C to stop.`

### Workflow
1. Recorder captures 10-second video clips in the `videos/` folder
2. Sender detects new videos and transmits them to receiver
3. Receiver saves videos to `received_videos/` folder
4. Sender deletes local copies after successful transfer

### Stopping the System
Press `Ctrl+C` in any terminal to stop the process.

## Key Features

✅ **Automatic Recording** - Captures video at regular intervals  
✅ **Network Transfer** - Sends files over TCP/IP sockets  
✅ **File Management** - Automatic cleanup of sent files  
✅ **Error Handling** - Graceful error messages and recovery  
✅ **Real-time Processing** - Watches folders and sends files automatically  

## Protocol Details

### File Transfer Protocol
1. **Sender** opens TCP connection to Receiver
2. **Sender** transmits filename (as string)
3. **Receiver** responds with `FILENAME_OK` acknowledgment
4. **Sender** transmits file data in 4KB chunks
5. **Sender** transmits `EOF` marker to signal end
6. **Receiver** confirms with `OK` message
7. Connection closes, local file deleted

## Troubleshooting

### Receiver not found
- Ensure receiver.py is running first
- Check that port 5001 is not in use: `netstat -ano | findstr :5001`
- Verify HOST/PORT settings match between sender and receiver

### Webcam not working
- Check if webcam is connected
- Verify no other application is using the webcam
- Try: `python -c "import cv2; cap = cv2.VideoCapture(0); print(cap.isOpened())"`

### Files not transferring
- Ensure `videos/` folder exists and is writable
- Check network connectivity between components
- Review console output for error messages

## Notes

- The system deletes local videos after successful transmission to save disk space
- All processes should be run in separate terminals for proper monitoring
- File transfers are synchronous; sender waits for confirmation before deletion
- Generated video files are named with timestamps for easy identification

## Lab Assignment
This project demonstrates practical implementation of:
- Socket programming for client-server communication
- Real-time video capture and encoding
- File I/O operations
- Process synchronization and monitoring
- Error handling and protocol design
