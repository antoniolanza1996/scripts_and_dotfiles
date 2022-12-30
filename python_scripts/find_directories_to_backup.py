"""Helper Python script useful to quickly find the directories with some changes done after --last_backup_date.
In this way, we can simply backup only these directories printed by this script.

Usage examples:
    1. python3 find_directories_to_backup.py --last_backup_date 2022-09-09 --base_dir PATH_TO_BASE_DIR --verbose
"""

import argparse
from datetime import datetime
import os
import logging
from typing import List, Tuple


logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        datefmt='%d-%b-%y %H:%M:%S',
        handlers=[logging.StreamHandler()]
    )

logger = logging.getLogger(__name__)


def run_fast_scandir(dir: str) -> Tuple[List[str], List[str]]:
    """Source: https://stackoverflow.com/a/59803793"""
    logger.debug(f"run_fast_scandir executed on {dir}")
    subfolders, files = [], []
    try:
        for f in os.scandir(dir):
            if f.is_dir():
                subfolders.append(f.path)
            if f.is_file():
                files.append(f.path)

        for dir in list(subfolders):
            sf, f_ = run_fast_scandir(dir)
            subfolders.extend(sf)
            files.extend(f_)
    except PermissionError:
        logger.error(f"Captured PermissionError exception... skipping {dir}")
    return subfolders, files


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--last_backup_date',
        type=lambda s: datetime.strptime(s, '%Y-%m-%d'),
        help="Last backup date in YYYY-MM-DD format",
        required=True
    )

    parser.add_argument(
        '--base_dir',
        help='Base directory to be recursively scanned',
        required=False,
        default='.',
        type=str
    )
    parser.add_argument(
        '-v', '--verbose',
        help='Verbose logging',
        action='store_true'
    )
    args = parser.parse_args()
    logger.info(args)
    logger.info(f"Start recursively scanning {args.base_dir}...")
    subfolders, files = run_fast_scandir(args.base_dir)
    logger.info(f"Scanning completed... Found {len(subfolders)} sub-folders and {len(files)} files...")

    logger.info(f"Start searching files modified after {args.last_backup_date}...")
    files_recently_changed = []
    for file_name in files:
        try:
            mtime = os.path.getmtime(file_name)
        except OSError:
            mtime = 0
            logger.error(f"Captured OSError exception... setting mtime=0 for {file_name}")
        last_modified_date = datetime.fromtimestamp(mtime)
        if last_modified_date > args.last_backup_date:
            files_recently_changed.append(file_name)
            if args.verbose:
                logger.info(f"{file_name} has been modified on {last_modified_date}")

    dirs_recently_changed = sorted(set([os.path.dirname(f) for f in files_recently_changed]))
    logger.info(
        f"Search completed... Found {len(files_recently_changed)} files changed after {args.last_backup_date}..." +
        f"These {len(files_recently_changed)} files are related to {len(dirs_recently_changed)} directories..."
    )
    if args.verbose:
        for ix, dir in enumerate(dirs_recently_changed):
            logger.info(f"\t\t{ix+1}) {dir}")
    logger.info("Start searching common parent directories (e.g. if there are A/B and A/B/C, A/B/C will be removed)...")
    relevant_dirs_recently_changed = []
    for ix1, dir1 in enumerate(dirs_recently_changed):
        relevant_dir = True
        for ix2, dir2 in enumerate(dirs_recently_changed):
            if dir1.startswith(dir2) and len(dir1) > len(dir2):
                relevant_dir = False
                break
        if relevant_dir:
            relevant_dirs_recently_changed.append(dir1)
    logger.info(f"Search completed... Found {len(relevant_dirs_recently_changed)} directories...")
    logger.info(f"You need to backup these {len(relevant_dirs_recently_changed)} directories:")
    relevant_dirs_recently_changed = sorted(relevant_dirs_recently_changed)
    for ix, dir in enumerate(relevant_dirs_recently_changed):
        logger.info(f"\t\t{ix+1}) {dir}")
