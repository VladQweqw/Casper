from datetime import datetime
import os
from pathlib import Path

LOGS_DIR = 'attacker/logs'
LOGS_FILE = 'attacker.log'
COMPLETE_LOG_PATH = os.path.join(LOGS_DIR, LOGS_FILE)

# make sure file xists
os.makedirs(LOGS_DIR, exist_ok=True)
open(COMPLETE_LOG_PATH, 'a').close()

def write_log_on_file(log_message, log_file_path=COMPLETE_LOG_PATH):
    """
        log_message: String, message to be saved
        log_file_path String, path of the log file
    """

    log_file = Path(log_file_path)

    # check if the file exists
    if not log_file.exists():
        return False, f"Log file {log_file_path} does not exists"
    
    # check if te size is under 10MB, otherwise erase te log file
    size_bytes = log_file.stat().st_size
    size_kbytes = size_bytes / 1024
    size_mbs = size_kbytes / (1024 * 1024)

    if size_mbs > 10:
        log_file.write("")
    
    # write log
    with log_file.open('a') as f:
        f.write(log_message + '\n')
        
    return True, "Log written"

def log(severity='INFO', message='', write_on_ram=True, verbose=False, log_path = COMPLETE_LOG_PATH):
    """
        severity: INFO/WARNING/ERROR, severity of the log 
        message: String, log string
        write_to_ram: Boolean, if the log should be written on the log file
        verbose: Boolean, if the log should be printed in the console
        log_path: String, specify a log path, path must contain the file
    """

    now = datetime.now()
    year = now.year
    time_format = f"{now.day}/{now.month}/{now.year} {now.hour}:{now.minute}:{now.second}"
     
    log_format = f"{time_format} [{severity.upper()}] {message}"

    if not verbose:
        print(log_format)

    if write_on_ram:
        write_log_on_file(log_format)
