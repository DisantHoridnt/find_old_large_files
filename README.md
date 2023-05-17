# Find Old Large Files

Find Old Large Files is a free, open-source utility that helps you keep your computer clean by finding and removing large, old files. It offers similar functionality to CleanMyMac X, but is completely free to use.

## Features

- **Find Large, Old Files:** Find Old Large Files scans your specified directory for files that are larger than a specified size and older than a specified number of days.
- **Safe Deletion:** Instead of deleting files immediately, Find Old Large Files moves them to a specified "trash" directory, giving you the chance to recover them if needed.
- **Exclusion List:** You can specify file extensions to exclude from the scan to prevent important file types from being moved to the trash.

## Usage

You can use Find Old Large Files from the command line as follows:

```bash
python find_old_large_files.py --size 200 --days 180 --dir /Users/username/Documents --exclude .pdf .docx --trash /Users/username/trash
```
## The parameters are as follows:

--size: The file size limit in MB. Files larger than this size will be moved to the trash.
--days: The file age limit in days. Files older than this number of days will be moved to the trash.
--dir: The directory to scan for large, old files.
--exclude: A list of file extensions to exclude from the scan.
--trash: The directory to move the large, old files to.
Installation

You can install Find Old Large Files using pip:

```bash
pip install find_old_large_files
```

## Safety

Find Old Large Files is designed to be safe to use. It will not delete any files without your confirmation, and it allows you to review the files it has identified for deletion before it moves them to the trash. However, as with any utility that modifies your file system, you should use it with caution. Always make sure your important files are backed up before running Find Old Large Files.

## Contributions

Contributions are welcome! Please feel free to submit a pull request.

## License

This project is licensed under the terms of the MIT license.