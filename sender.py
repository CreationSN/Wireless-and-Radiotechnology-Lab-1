import socket
import os
import time

HOST = "127.0.0.1"
PORT = 5001
VIDEO_FOLDER = "videos"
CHECK_INTERVAL = 5  # seconds

os.makedirs(VIDEO_FOLDER, exist_ok=True)

print("Sender started. Watching video folder...")

def send_file(filepath):
    filename = os.path.basename(filepath)

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))

        # Send filename first
        client.sendall(filename.encode())
        response = client.recv(1024)

        if response != b"FILENAME_OK":
            print(f"Receiver did not accept filename for {filename}")
            client.close()
            return False

        # Send file data
        with open(filepath, "rb") as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                client.sendall(data)

        client.sendall(b"EOF")

        # Wait for confirmation
        response = client.recv(1024)
        client.close()

        if response == b"OK":
            print(f"Transfer confirmed: {filename}")
            os.remove(filepath)
            print(f"Deleted local file: {filename}\n")
            return True
        else:
            print(f"No valid confirmation for {filename}")
            return False

    except Exception as e:
        print(f"Error sending {filename}: {e}")
        return False

while True:
    files = [f for f in os.listdir(VIDEO_FOLDER) if f.endswith(".mp4")]
    files.sort()

    for file in files:
        filepath = os.path.join(VIDEO_FOLDER, file)
        send_file(filepath)

    time.sleep(CHECK_INTERVAL)