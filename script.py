import os
import hashlib
import json
import time
import sys
import threading

# Configuration
HASH_FILE = 'file_hashes.json'      # File to store the original hashes
CHECK_INTERVAL = 60                 # Time interval between checks (in seconds)
stop_monitoring = False             # Flag to stop monitoring


# Function to calculate the SHA-256 hash of a file
def calculate_hash(file_path):
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except (FileNotFoundError, PermissionError):
        print(f"Error: Could not access {file_path}.")
        return None

# Function to get all files in a directory recursively
def get_all_files(directory):
    file_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_paths.append(os.path.join(root, file))
    return file_paths

# Function to load saved file hashes from a JSON file
def load_hashes():
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, 'r') as f:
            return json.load(f)
    return {}

# Function to save file hashes to a JSON file
def save_hashes(hashes):
    with open(HASH_FILE, 'w') as f:
        json.dump(hashes, f, indent=4)

# Function to monitor directories and check for file changes
def monitor_files(monitor_dirs):
    # Load previous file hashes
    saved_hashes = load_hashes()

    # Dictionary to store current file hashes
    current_hashes = {}

    # Check all files in the monitored directories
    for directory in monitor_dirs:
        files = get_all_files(directory)
        for file in files:
            file_hash = calculate_hash(file)
            if file_hash:
                current_hashes[file] = file_hash

                # Compare with the saved hash
                if file in saved_hashes:
                    if saved_hashes[file] != file_hash:
                        print(f"ALERT: {file} has been modified!")
                else:
                    print(f"New file detected: {file}")
    
    # Check for deleted files
    for file in saved_hashes:
        if file not in current_hashes:
            print(f"ALERT: {file} has been deleted!")

    # Save current hashes for the next monitoring cycle
    save_hashes(current_hashes)

# Function to stop monitoring via user input
def listen_for_stop():
    global stop_monitoring
    while True:
        user_input = input()
        if user_input.lower() == 'stop':
            stop_monitoring = True
            print("Stopping monitoring...")
            break

# Main loop to monitor files at regular intervals
def main():
    global stop_monitoring

    # Get the directory to monitor from command line or prompt
    if len(sys.argv) > 1:
        monitor_dirs = sys.argv[1:]
    else:
        monitor_dirs = []
        while True:
            directory = input("Enter a directory to monitor (or press Enter to finish): ").strip()
            if directory:
                if os.path.isdir(directory):
                    monitor_dirs.append(directory)
                else:
                    print(f"Error: {directory} is not a valid directory.")
            else:
                break

    if not monitor_dirs:
        print("No directories provided for monitoring. Exiting...")
        return

    # Ensure no duplicate directories are added
    monitor_dirs = list(set(monitor_dirs))

    print(f"Monitoring directories: {monitor_dirs}")
    
    # Start a thread to listen for the 'stop' command
    stop_thread = threading.Thread(target=listen_for_stop)
    stop_thread.daemon = True  # This ensures the thread exits when the main program exits
    stop_thread.start()

    # Main monitoring loop
    while not stop_monitoring:
        monitor_files(monitor_dirs)
        
        # Sleep in smaller intervals to check for the stop flag
        total_sleep_time = 0
        while total_sleep_time < CHECK_INTERVAL and not stop_monitoring:
            time.sleep(1)  # Sleep for 1 second at a time
            total_sleep_time += 1

    print("Monitoring has been stopped.")

if __name__ == "__main__":
    main()
