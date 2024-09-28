import os
import hashlib
import json
import time
import sys
import threading
import logging
from flask import Flask, render_template, jsonify

# Flask setup
app = Flask(__name__)

# Configuration
HASH_FILE = 'file_hashes.json'      # File to store the original hashes
CHECK_INTERVAL = 60                 # Time interval between checks (in seconds)
LOG_FILE = 'file_changes.log'       # Log file to store file changes
stop_monitoring = False             # Flag to stop monitoring

# Create a logger for file changes (separate from Flask logs)
file_logger = logging.getLogger('file_monitoring')
file_logger.setLevel(logging.INFO)

# Create a file handler for logging file changes
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))

# Add the handler to the logger
file_logger.addHandler(file_handler)

# Disable Flask's logging by disabling the default werkzeug logger
log = logging.getLogger('werkzeug')
log.disabled = True

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
                        # Log the file modification with timestamp (using file_logger)
                        file_logger.info(f"File modified: {file}")
                else:
                    print(f"New file detected: {file}")
                    # Log the new file creation with timestamp (using file_logger)
                    file_logger.info(f"New file detected: {file}")
    
    # Check for deleted files
    for file in saved_hashes:
        if file not in current_hashes:
            print(f"ALERT: {file} has been deleted!")
            # Log the file deletion with timestamp (using file_logger)
            file_logger.info(f"File deleted: {file}")

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
            # Log the stop monitoring event
            file_logger.info("Monitoring stopped by user.")
            break

# Web interface route to display the log file content
@app.route('/')
def dashboard():
    try:
        # Read the file_changes.log file and pass it to the template
        with open(LOG_FILE, 'r') as log_file:
            log_data = log_file.readlines()
        return render_template('dashboard.html', logs=log_data)
    except Exception as e:
        print(f"Error rendering dashboard: {e}")
        return "Error rendering dashboard.", 500

# API route to fetch log data for real-time updates (for AJAX)
@app.route('/logs')
def get_logs():
    try:
        with open(LOG_FILE, 'r') as log_file:
            log_data = log_file.readlines()
        return jsonify(log_data)
    except Exception as e:
        print(f"Error fetching logs: {e}")
        return jsonify([]), 500

# Function to run the file monitoring in a separate thread
def start_monitoring(monitor_dirs):
    global stop_monitoring
    # Main monitoring loop
    while not stop_monitoring:
        monitor_files(monitor_dirs)
        
        # Sleep in smaller intervals to check for the stop flag
        total_sleep_time = 0
        while total_sleep_time < CHECK_INTERVAL and not stop_monitoring:
            time.sleep(1)  # Sleep for 1 second at a time
            total_sleep_time += 1

    print("Monitoring has been stopped.")

# Main function to start both Flask and monitoring
def main():
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
    
    # Log the start of monitoring
    file_logger.info(f"Started monitoring directories: {monitor_dirs}")

    # Start the monitoring in a separate thread
    monitor_thread = threading.Thread(target=start_monitoring, args=(monitor_dirs,))
    monitor_thread.daemon = True
    monitor_thread.start()

    # Start a thread to listen for the 'stop' command
    stop_thread = threading.Thread(target=listen_for_stop)
    stop_thread.daemon = True  # This ensures the thread exits when the main program exits
    stop_thread.start()

    # Start Flask in the main thread
    print("Starting Flask server at http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, threaded=True)

if __name__ == "__main__":
    main()
