# File Integrity Monitoring Tool

## Overview
The **File Integrity Monitoring Tool** is a Python-based program designed to monitor files and directories for unauthorized changes. It calculates and stores file hashes (SHA-256) to detect modifications, deletions, or new files being added. The tool raises alerts if any changes are detected and allows the user to stop monitoring gracefully.

## Features
- **Monitor Multiple Directories**: Specify one or more directories to monitor for file changes.
- **File Hashing**: Uses SHA-256 to compute the hash of files to detect changes.
- **Change Detection**: Detects file modifications, deletions, and the addition of new files.
- **Real-Time Monitoring**: Continuously monitors the specified directories at regular intervals.
- **Dynamic Interval Update**: Allows the user to change the file check interval via a web interface.
- **Dashboard Interface**: Provides a web-based dashboard for viewing logs and managing the file check interval.
- **Graceful Exit**: Allows the user to stop monitoring by typing `stop` in the terminal.

## Prerequisites
- Python 3.x

## Setup and Installation

1. **Clone the Repository** (or download the script):
   ```bash
   git clone https://github.com/muxueya/FileIntegrityMonitor.git
   cd file-integrity-monitoring
   ```

2. **Install Dependencies**: 
   The script uses only Python's built-in libraries, so no additional dependencies are required.

## Usage 

You can run the monitoring tool either by specifying directories via command-line arguments or by entering them interactively when prompted.

### 1. Command-Line Argument Usage 

To run the tool and monitor specific directories:


```bash
python script.py /path/to/directory1 /path/to/directory2
```

Example:


```bash
python script.py /path/to/directory
```

### 2. Interactive Mode 

If no directories are provided as command-line arguments, the tool will prompt you to input directories one by one:


```bash
Enter a directory to monitor (or press Enter to finish): /path/to/directory
Enter a directory to monitor (or press Enter to finish): /path/to/another_directory
Enter a directory to monitor (or press Enter to finish):  [Press Enter to finish]
```

### Stopping Monitoring 
While the program is running, you can stop monitoring by typing `stop` in the terminal:

```bash
stop
Stopping monitoring...
Monitoring has been stopped.
```

### Alerts 

The tool will output messages to the terminal when:
 
- A file has been modified:

```bash
ALERT: /path/to/file.txt has been modified!
```
 
- A new file has been added:

```bash
New file detected: /path/to/newfile.txt
```
 
- A file has been deleted:

```bash
ALERT: /path/to/deletedfile.txt has been deleted!
```

## Dynamic Interval Update and Dashboard (New Features) 

The monitoring interval can now be updated dynamically from the web interface.
 
1. **Run the Flask server** :
The Flask web server will start automatically with the file monitoring. You can access the web interface via:

```bash
http://localhost:5000
```
 
2. **Update the Check Interval** :
From the web interface, enter the new interval (in seconds) and click "Update Interval". This change will immediately take effect for subsequent checks.
 
3. **View Logs in Real-Time** :
The dashboard will display the file changes as logs in real time. You can also search through the logs using the provided search bar.

## Configuration 
 
- **`CHECK_INTERVAL`** : The time interval between each check, in seconds (default: 60 seconds).
 
- **`HASH_FILE`** : The name of the JSON file used to store the file hashes (default: `file_hashes.json`).

You can modify these values in the script's configuration section to suit your needs:


```python
HASH_FILE = 'file_hashes.json'
CHECK_INTERVAL = 60  # Time interval between checks in seconds
```

## Example Run 


```bash
python script.py /path/to/directory
Monitoring directories: ['/path/to/directory']
Next check in 60 seconds...
New file detected: /path/to/directory/example.txt
Next check in 60 seconds...
stop
Stopping monitoring...
Monitoring has been stopped.
```
