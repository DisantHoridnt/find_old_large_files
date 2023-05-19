import os
import time
import argparse
import logging
import concurrent.futures
from pathlib import Path
from tqdm import tqdm

class FileScanner:
    def __init__(self, dir_path, size_limit, days_limit, excluded_extensions, trash_dir):
        self.dir_path = dir_path
        self.size_limit = size_limit
        self.days_limit = days_limit
        self.excluded_extensions = set(excluded_extensions)
        self.trash_dir = trash_dir
        self.files_to_move = []

        # Make sure trash_dir exists before initializing logging
        os.makedirs(self.trash_dir, exist_ok=True)
        
        logging.basicConfig(filename=os.path.join(self.trash_dir, 'file_scanner.log'), 
                            level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info('Initialized FileScanner')

    @staticmethod
    def file_age_in_days(file_path):
        return (time.time() - os.path.getmtime(file_path)) / (60*60*24)

    def gen_files(self, path=None):
        if path is None:
            path = self.dir_path

        for entry in os.scandir(path):
            if entry.is_dir(follow_symlinks=False):
                yield from self.gen_files(entry.path)
            else:
                yield entry

    def scan_files(self, file_handler=None):
        print("Starting the file scanning process... This may take a while, please hang tight.")
        with tqdm(total=sum(1 for _ in self.gen_files()), desc='Scanning files', ncols=70) as pbar:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(self.process_file, entry.path, file_handler, pbar) for entry in self.gen_files()]
            concurrent.futures.wait(futures)

    def process_file(self, file_path, file_handler, pbar):
        try:
            if (os.path.getsize(file_path) > self.size_limit and
                self.file_age_in_days(file_path) > self.days_limit and
                not Path(file_path).suffix in self.excluded_extensions):
                self.files_to_move.append(file_path)  # Add to files to be moved
                logging.info('Added file to move: %s', file_path)
                if file_handler is not None:
                    file_handler(file_path)
        except FileNotFoundError:
            logging.error('File not found: %s', file_path)
        pbar.update()

    def total_size_in_gb(self):
        total_size = sum(os.path.getsize(file_path) for file_path in self.files_to_move)
        return total_size / (1024 * 1024 * 1024)  # Convert bytes to gigabytes

    def move_files_to_trash(self):
        os.makedirs(self.trash_dir, exist_ok=True)
        with tqdm(total=len(self.files_to_move), desc='Moving files', ncols=70) as pbar:
            for file_path in self.files_to_move:
                try:
                    os.rename(file_path, os.path.join(self.trash_dir, os.path.basename(file_path)))
                    logging.info('Moved file to trash: %s', file_path)
                except OSError as e:  # Catch specifically the OSError
                    logging.error('Error moving file: %s', e)
                pbar.update()
        logging.info('Finished moving files')

def main():
    home = str(Path.home())

    parser = argparse.ArgumentParser(description="Find and remove large, old files.")
    parser.add_argument("--size", type=int, default=100, help="File size limit in MB, it will be converted to bytes")
    parser.add_argument("--days", type=int, default=365, help="File age limit in days")
    parser.add_argument("--dir", type=str, default=home, help="Directory to scan")
    parser.add_argument("--exclude", type=str, nargs='*', default=['.docx', '.xlsx'], help="File extensions to exclude")
    parser.add_argument("--trash", type=str, default=os.path.join(home, 'trash'), help="Directory to move files to")

    args = parser.parse_args()

    # Ensure provided directories exist
    if not os.path.isdir(args.dir):
        print(f"The provided directory '{args.dir}' does not exist.")
        return
    if not os.path.exists(args.trash):
        os.makedirs(args.trash, exist_ok=True)

    size_limit = args.size * 1024 * 1024  # Convert size from MB to bytes

    scanner = FileScanner(args.dir, size_limit, args.days, args.exclude, args.trash)

    scanner.scan_files()
    print(f"Total size to be moved to trash: {scanner.total_size_in_gb():.2f} GB")

    while True:
        choice = input("Do you want to move these files to trash? (yes/no): ")
        if choice.lower() == 'yes':
            scanner.move_files_to_trash()
            break
        elif choice.lower() == 'no':
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

if __name__ == "__main__":
    main()
