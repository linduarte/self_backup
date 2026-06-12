import os
import shutil
import time
from datetime import datetime

import psutil

USER = os.getlogin()
HOME = os.path.join("C:\\Users", USER)

SOURCE_DIRS = {
    "gnupg": os.path.join(HOME, ".gnupg"),
    "sops": os.path.join(HOME, ".sops"),
    "bashrc": os.path.join(HOME, ".bashrc"),
    "gitconfig": os.path.join(HOME, ".gitconfig"),
    "gitconfig_pers": os.path.join(HOME, ".gitconfig-pers"),
    "gitconfig_work": os.path.join(HOME, ".gitconfig-work"),
    "config": os.path.join(HOME, ".config"),
}

DEST_DIR = os.path.join(HOME, "OneDrive", "Documentos", "self_backup")
BACKUP_TIME = "14:01"


def is_in_use(directory: str) -> bool:
    """Check if any file in the directory is currently open or in use."""
    for proc in psutil.process_iter(["pid", "name", "open_files"]):
        for file in proc.info.get("open_files") or []:
            if file.path.startswith(directory):
                return True
    return False


def backup_item(name: str, path: str, dest_root: str) -> None:
    """Back up a single file or directory."""
    backup_subdir = os.path.join(dest_root, name)

    # Case 1: It's a file
    if os.path.isfile(path):
        os.makedirs(backup_subdir, exist_ok=True)
        dest_file = os.path.join(backup_subdir, os.path.basename(path))
        shutil.copy2(path, dest_file)
        return

    # Case 2: It's a directory
    if os.path.isdir(path):
        for root, _dirs, files in os.walk(path):
            for file in files:
                source_file = os.path.join(root, file)
                relative_path = os.path.relpath(source_file, path)
                dest_file = os.path.join(backup_subdir, relative_path)

                os.makedirs(os.path.dirname(dest_file), exist_ok=True)
                shutil.copy2(source_file, dest_file)


def backup_files() -> None:
    """Back up all configured items."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    os.makedirs(DEST_DIR, exist_ok=True)

    for name, path in SOURCE_DIRS.items():
        backup_item(name, path, DEST_DIR)

    print(f"Backup completed successfully at {timestamp}.")


def run_backup_at_time(test_time: str | None = None) -> None:
    """Run the backup when the system time matches BACKUP_TIME."""
    while True:
        current_time = time.strftime("%H:%M")
        print(f"Current time: {current_time}")

        if test_time:
            current_time = test_time
            print(f"Test time override: {test_time}")

        if current_time == BACKUP_TIME:
            print("It's time for a backup!")

            if any(is_in_use(path) for path in SOURCE_DIRS.values()):
                print("One of the source directories is in use. Waiting...")
                while any(is_in_use(path) for path in SOURCE_DIRS.values()):
                    time.sleep(60)
            else:
                backup_files()

            if test_time:
                print("Test completed, exiting loop.")
                break

        time.sleep(10)


if __name__ == "__main__":
    test_time = "14:01"
    run_backup_at_time(test_time)
