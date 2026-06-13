[![Created under 'uv' by Astral](https://img.shields.io/badge/created%20under%20uv-Astral-blue)](https://example.com)

# Self Backup Script

This Python script automates the process of backing up specified directories to a designated destination. It checks if any files in the source directories are currently in use before performing the backup to ensure data integrity.

## Features

- Backs up multiple specified directories.
- Checks if files are in use before backing up.
- Allows for testing with a specified test time.
- Creates timestamped backup directories.

## Usage

1. Define the source directories to back up in the `SOURCE_DIRS` dictionary.
2. Set the destination directory for backups in the `DEST_DIR` variable.
3. Specify the time of day to run the backup in the `BACKUP_TIME` variable (24-hour format).
4. Optionally, set a `test_time` for testing purposes.

Run the script:

```sh
python -m backmeup
```
or

```powershell
uv run backmeup.py
```
```powershell
SOURCE_DIRS = {
    "gnupg": r"C:\Users\clldu\.gnupg",
    "sops": r"C:\Users\clldu\.sops",
    "bashrc": r"C:\Users\clldu\.bashrc",
    "gitconfig": r"C:\Users\clldu\.gitconfig",
    "gitconfig_pers": r"C:\Users\clldu\.gitconfig-pers",
    "gitconfig_work": r"C:\Users\clldu\.gitconfig-work",
    "config": r"C:\Users\clldu\.config"
}

DEST_DIR = r"C:\Users\clldu\OneDrive\Documentos\self_backup"
BACKUP_TIME = "13:59"

```
