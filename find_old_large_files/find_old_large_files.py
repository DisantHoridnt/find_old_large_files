import os
import time
import argparse
from pathlib import Path


class FileScanner:
    def __init__(self, dir_path, size_limit, days_limit, excluded_extensions, trash_dir):
        self.dir_path = dir_path
        self.size_limit = size_limit
        self.days_limit = days_limit
        self.excluded_extensions = excluded_extensions
        self.trash_dir = trash_dir

    @staticmethod
    def file_age_in_days(file_path):
        return (time.time() - os.path.getmtime(file_path)) / (60*60*24)

    def scan_files(self, file_handler):
        result = []
        for foldername, subfolders, filenames in os.walk(self.dir_path):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                try:
                    if (os.path.getsize(file_path) > self.size_limit and
                        self.file_age_in_days(file_path) > self.days_limit and
                        not Path(file_path).suffix in self.excluded_extensions):
                        result.append(file_handler(file_path))
                except FileNotFoundError:
                    print(f"File not found: {file_path}, skipping.")
        return result

    def print_file(self, file_path):
        print(f"Old, large file: {file_path} Size: {os.path.getsize(file_path)} bytes")

    def move_file_to_trash(self, file_path):
        os.makedirs(self.trash_dir, exist_ok=True)
        os.rename(file_path, os.path.join(self.trash_dir, os.path.basename(file_path)))
        print(f"Moved old, large file to trash: {file_path} Size: {os.path.getsize(file_path)} bytes")


def main():
    home = str(Path.home())

    parser = argparse.ArgumentParser(description="Find and remove large, old files.")
    parser.add_argument("--size", type=int, default=100, help="File size limit in MB")
    parser.add_argument("--days", type=int, default=365, help="File age limit in days")
    parser.add_argument("--dir", type=str, default=home, help="Directory to scan")
    parser.add_argument("--exclude", type=str, nargs='*', default=['.docx', '.xlsx'], help="File extensions to exclude")
    parser.add_argument("--trash", type=str, default=os.path.join(home, 'trash'), help="Directory to move files to")

    args = parser.parse_args()
    size_limit = args.size * 1024 * 1024  # Convert size from MB to bytes

    scanner = FileScanner(args.dir, size_limit, args.days, args.exclude, args.trash)
    scanner.scan_files(scanner.print_file)
    input("Press enter to move these files to trash...")
    scanner.scan_files(scanner.move_file_to_trash)


if __name__ == "__main__":
    main()
