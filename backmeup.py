import psutil
from datetime import datetime
import os
import shutil
import time

# Define the source directories to back up
SOURCE_DIRS = {
    "gnupg": r"C:\Users\clldu\.gnupg",
    "sops": r"C:\Users\clldu\.sops",
    "bashrc": r"C:\Users\clldu\.bashrc",
    "gitconfig": r"C:\Users\clldu\.gitconfig",
    "gitconfig_pers": r"C:\Users\clldu\.gitconfig-pers",
    "gitconfig_work": r"C:\Users\clldu\.gitconfig-work",
    "config": r"C:\Users\clldu\.config"
}

# Define the destination directory for backups
DEST_DIR = r"C:\Users\clldu\OneDrive\Documentos\self_backup"

# Time of day to run the backup (24-hour format)
BACKUP_TIME = "14:01"

def is_in_use(directory):
    # Check if any file in the directory is currently open or in use
    for proc in psutil.process_iter(['pid', 'name', 'open_files']):
        for file in proc.info['open_files'] or []:
            if file.path.startswith(directory):
                return True
    return False

def backup_files():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for label, source_dir in SOURCE_DIRS.items():
        backup_subdir = os.path.join(DEST_DIR, f"{label}_{timestamp}")

        if not os.path.exists(backup_subdir):
            os.makedirs(backup_subdir)

        for root, dirs, files in os.walk(source_dir):
            for file in files:
                source_file = os.path.join(root, file)
                relative_path = os.path.relpath(source_file, source_dir)
                dest_file = os.path.join(backup_subdir, relative_path)

                # Create destination directory if it doesn't exist
                os.makedirs(os.path.dirname(dest_file), exist_ok=True)
                shutil.copy2(source_file, dest_file)

    print(f"Backup completed successfully at {timestamp}.")

def run_backup_at_time(test_time=None):
    while True:
        current_time = time.strftime("%H:%M")
        print(f"Current time: {current_time}")  # Debug print
        if test_time:
            current_time = test_time
            print(f"Test time: {test_time}")  # Debug print

        if current_time == BACKUP_TIME:
            print("It's time for a backup!")

            if any(is_in_use(dir) for dir in SOURCE_DIRS.values()):
                print("One of the source directories is in use. Waiting...")
                while any(is_in_use(dir) for dir in SOURCE_DIRS.values()):
                    time.sleep(60)  # Wait for a minute before checking again
            else:
                backup_files()

            if test_time:
                print("Test completed, exiting loop.")
                break  # Exit after one iteration if running a test

        time.sleep(10)  # Check every 10 seconds for testing purposes

if __name__ == "__main__":
    # Set a test time for testing purposes
    test_time = "14:01"
    run_backup_at_time(test_time)
