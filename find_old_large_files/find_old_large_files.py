import os
import time
from pathlib import Path
import argparse
import logging
import concurrent.futures
from tqdm import tqdm

class FileScanner:
    def __init__(self, dir_path, size_limit, days_limit, excluded_extensions, trash_dir):
        self.dir_path = Path(dir_path)
        self.size_limit = size_limit
        self.days_limit = days_limit
        self.excluded_extensions = set(excluded_extensions)
        self.trash_dir = Path(trash_dir)
        self.files_to_move = []

        logging.basicConfig(filename=self.trash_dir / 'file_scanner.log', 
                            level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info('Initialized FileScanner with dir_path: %s, size_limit: %s, days_limit: %s, excluded_extensions: %s, trash_dir: %s',
                     dir_path, size_limit, days_limit, excluded_extensions, trash_dir)

    def file_age_in_days(self, file_path):
        return (time.time() - file_path.stat().st_mtime) / (60*60*24)

    def scan_files(self):
        print("Starting the file scanning process... This may take a while, please hang tight.")
        for entry in os.scandir(self.dir_path):
            if entry.is_file():
                yield entry.path

    def process_file(self, file_path):
        try:
            if (file_path.stat().st_size > self.size_limit and
                self.file_age_in_days(file_path) > self.days_limit and
                file_path.suffix not in self.excluded_extensions):
                self.files_to_move.append(file_path)
                logging.info('Added file to move: %s', file_path)
                return file_path
        except FileNotFoundError:
            logging.error('File not found: %s', file_path)

    def total_size_in_gb(self):
        total_size = sum(file_path.stat().st_size for file_path in self.files_to_move)
        return total_size / (1024 * 1024 * 1024)

    def move_files_to_trash(self):
        self.trash_dir.mkdir(parents=True, exist_ok=True)
        for file_path in tqdm(self.files_to_move, desc='Moving files', ncols=70):
            try:
                file_path.rename(self.trash_dir / file_path.name)
                logging.info('Moved file to trash: %s', file_path)
            except OSError as e:
                logging.error('Error moving file: %s', e)

def main():
    home = str(Path.home())

    parser = argparse.ArgumentParser(description="Find and remove large, old files.")
    parser.add_argument("--size", type=int, default=100, help="File size limit in MB")
    parser.add_argument("--days", type=int, default=365, help="File age limit in days")
    parser.add_argument("--dir", type=str, default=home, help="Directory to scan")
    parser.add_argument("--exclude", type=str, nargs='*', default=['.docx', '.xlsx'], help="File extensions to exclude")
    parser.add_argument("--trash", type=str, default=os.path.join(home, 'trash'), help="Directory to move files to")

    args = parser.parse_args()
    size_limit = args.size * 1024 * 1024

    scanner = FileScanner(args.dir, size_limit, args.days, args.exclude, args.trash)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(scanner.process_file, Path(file)) for file in scanner.scan_files()]
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc='Scanning files', ncols=70):
            file_path = future.result()
            if file_path is not None:
                print(f"Old, large file: {file_path} Size: {file_path.stat().st_size/1024/1024:.2f} MB")

    print("Total size to be moved to trash: {:.2f} GB".format(scanner.total_size_in_gb()))
    input("Press enter to move these files to trash...")
    scanner.move_files_to_trash()

if __name__ == "__main__":
    main()
