# File Integrity Monitoring Tool

## Overview
The **File Integrity Monitoring Tool** is a Python-based program designed to monitor files and directories for unauthorized changes. It calculates and stores file hashes (SHA-256) to detect modifications, deletions, or new files being added. The tool raises alerts if any changes are detected and allows the user to stop monitoring gracefully.

## Features
- **Monitor Multiple Directories**: Specify one or more directories to monitor for file changes.
- **File Hashing**: Uses SHA-256 to compute the hash of files to detect changes.
- **Change Detection**: Detects file modifications, deletions, and the addition of new files.
- **Real-Time Monitoring**: Continuously monitors the specified directories at regular intervals.
- **Graceful Exit**: Allows the user to stop monitoring by typing `stop` in the terminal.

## Prerequisites
- Python 3.x

## Setup and Installation

1. **Clone the Repository** (or download the script):
   ```bash
   git clone https://github.com/yourusername/file-integrity-monitoring.git
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
python script.py C:\Apple\test
```

### 2. Interactive Mode

If no directories are provided as command-line arguments, the tool will prompt you to input directories one by one:
```bash
Enter a directory to monitor (or press Enter to finish): C:\Apple\test
Enter a directory to monitor (or press Enter to finish): C:\Work\project
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
  ```
  ALERT: /path/to/file.txt has been modified!
  ```
- A new file has been added:
  ```
  New file detected: /path/to/newfile.txt
  ```
- A file has been deleted:
  ```
  ALERT: /path/to/deletedfile.txt has been deleted!
  ```

## Configuration

- **`CHECK_INTERVAL`**: The time interval between each check, in seconds (default: 60 seconds).
- **`HASH_FILE`**: The name of the JSON file used to store the file hashes (default: `file_hashes.json`).

You can modify these values in the script's configuration section to suit your needs:
```python
HASH_FILE = 'file_hashes.json'
CHECK_INTERVAL = 60  # Time interval between checks in seconds
```

## Example Run

```bash
python script.py C:\Apple\test
Monitoring directories: ['C:\Apple\test']
Next check in 60 seconds...
New file detected: C:\Apple\test\example.txt
Next check in 60 seconds...
stop
Stopping monitoring...
Monitoring has been stopped.
```