import os
import time
import argparse
import logging
from pathlib import Path
import concurrent.futures
from tqdm import tqdm

class FileScanner:
    def __init__(self, dir_path, size_limit, days_limit, excluded_extensions, trash_dir):
        self.dir_path = dir_path
        self.size_limit = size_limit
        self.days_limit = days_limit
        self.excluded_extensions = set(excluded_extensions)  # Changed from list to set
        self.trash_dir = trash_dir
        self.files_to_move = []

        logging.basicConfig(filename=os.path.join(self.trash_dir, 'file_scanner.log'), 
                            level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info('Initialized FileScanner with dir_path: %s, size_limit: %s, days_limit: %s, excluded_extensions: %s, trash_dir: %s',
                     dir_path, size_limit, days_limit, excluded_extensions, trash_dir)

    @staticmethod
    def file_age_in_days(file_path):
        return (time.time() - os.path.getmtime(file_path)) / (60*60*24)

    def count_files(self):
        for _, _, filenames in os.scandir(self.dir_path):
            yield len(filenames)

    def scan_files(self, file_handler=None):
        print("Starting the file scanning process... This may take a while, please hang tight.")
        num_files = sum(self.count_files())
        with tqdm(total=num_files, desc='Scanning files', ncols=70) as pbar:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = []
                for entry in os.scandir(self.dir_path):
                    if entry.is_file():
                        futures.append(executor.submit(self.process_file, entry.path, file_handler, pbar))
                concurrent.futures.wait(futures)

    def process_file(self, file_path, file_handler, pbar):
        try:
            if (os.path.getsize(file_path) > self.size_limit and
                self.file_age_in_days(file_path) > self.days_limit and
                Path(file_path).suffix not in self.excluded_extensions):
                self.files_to_move.append(file_path)
                logging.info('Added file to move: %s', file_path)
                if file_handler is not None:
                    file_handler(file_path)
        except FileNotFoundError:
            logging.error('File not found: %s', file_path)
        pbar.update()

    def total_size_in_gb(self):
        total_size = sum(os.path.getsize(file_path) for file_path in self.files_to_move)
        return total_size / (1024 * 1024 * 1024)

    def move_files_to_trash(self):
        os.makedirs(self.trash_dir, exist_ok=True)
        with tqdm(total=len(self.files_to_move), desc='Moving files', ncols=70) as pbar:
            for file_path in self.files_to_move:
                try:
                    os.rename(file_path, os.path.join(self.trash_dir, os.path.basename(file_path)))
                    logging.info('Moved file to trash: %s', file_path)
                except OSError as e:  # Specific Exception Handling
                    logging.error('Error moving file: %s', e)
                pbar.update()
        logging.info('Completed moving files to trash')

    def print_file(self, file_path):
        size_in_mb = os.path.getsize(file_path) / (1024 * 1024)
        if size_in_mb < 1024:
            print(f"Old, large file: {file_path} Size: {size_in_mb:.2f} MB")
            logging.info('Old, large file: %s Size: %.2f MB', file_path, size_in_mb)
        else:
            size_in_gb = size_in_mb / 1024
            print(f"Old, large file: {file_path} Size: {size_in_gb:.2f} GB")
            logging.info('Old, large file: %s Size: %.2f GB', file_path, size_in_gb)

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
    # ...
    print("Total size to be moved to trash: {:.2f} GB".format(scanner.total_size_in_gb()))
    user_input = input("Do you want to move these files to trash? (Y/N): ")
    if user_input.lower() == 'y':
        scanner.move_files_to_trash()
    else:
        print("Files were not moved to trash.")
# ...

if __name__ == "__main__":
    main()
