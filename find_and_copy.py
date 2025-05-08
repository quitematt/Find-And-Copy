import argparse
import logging
import shutil
from pathlib import Path
from tqdm import tqdm
import datetime
import argparse

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

log_dir = Path('logs')
log_dir.mkdir(exist_ok=True)

log_filename = log_dir / f"find_and_copy_{timestamp}.log"

# Set up logging
logging.basicConfig(
    filename=log_filename,
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def read_file_list(file_list_path):
    try:
        with open(file_list_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except Exception as e:
        logging.error(f"Error reading {file_list_path}: {e}")
        raise

def find_and_copy_files(file_names, search_root, destination):
    files_not_found = []
    for file_name in tqdm(file_names, desc="Searching for files", unit="file"):
        logging.info(f"Searching for: {file_name}")
        found = False
        for file_path in Path(search_root).rglob(f"*{file_name}*.*"):
            if file_path.is_file():
                logging.info(f"Matched: {file_path.name}")
                dest_path = destination / f"{file_name}{file_path.suffix}"
                try:
                    shutil.copy2(file_path, dest_path)
                    logging.info(f"Copied: {file_path} -> {dest_path}")
                    found = True
                    break  # Stop after first match
                except Exception as e:
                    logging.error(f"Failed to copy {file_path}: {e}")
        if not found:
            logging.warning(f"File not found: {file_name}")
            files_not_found.append(file_name)

    if files_not_found:
        logging.info(f"Total files not found: {len(files_not_found)}")
        logging.info("Missing files:")
        for nf in files_not_found:
            logging.info(f"{nf}")
    else:
        logging.info("All files were found and copied successfully.")

def main():
    parser = argparse.ArgumentParser(description='Find and copy files from a list.')
    parser.add_argument('file_list', help='Path to files.txt')
    parser.add_argument('search_root', help='Root directory to search (e.g., /parent)')
    args = parser.parse_args()

    destination_dir = Path.cwd() / 'copied_files'
    destination_dir.mkdir(exist_ok=True)

    file_names = read_file_list(args.file_list)
    find_and_copy_files(file_names, Path(args.search_root), destination_dir)

if __name__ == "__main__":
    main()
