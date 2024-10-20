#!/usr/bin/env python3
"""Copy items named exactly level<digits> from a source folder to a destination.

Usage:
  python copy_levels.py --src "D:\\SteamLibrary\\steamapps\\common\\Neon White\\Neon White_Data" \
                        --dst "D:\\Downloads\\Code\\NeonWhiteCustomLevels\\custom_levels" [--execute]

By default the script performs a dry-run. Pass `--execute` to actually copy and overwrite.
"""
import os
import re
import shutil
import argparse
import sys


def norm(p: str) -> str:
    return os.path.normpath(os.path.expanduser(os.path.expandvars(p)))


def find_matches(src: str):
    pattern = re.compile(r'^level\d+$')
    matches = []
    try:
        with os.scandir(src) as it:
            for entry in it:
                if pattern.match(entry.name):
                    matches.append((entry.name, entry.path, entry.is_dir()))
    except FileNotFoundError:
        print(f"Source folder not found: {src}")
        return []
    return matches


def copy_item(src_path: str, dst_path: str, is_dir: bool):
    if is_dir:
        if os.path.exists(dst_path):
            shutil.rmtree(dst_path)
        shutil.copytree(src_path, dst_path)
    else:
        # file
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        if os.path.exists(dst_path):
            os.remove(dst_path)
        shutil.copy2(src_path, dst_path)


def main():
    p = argparse.ArgumentParser(description='Copy levelN items from source to destination (dry-run default)')
    p.add_argument('--src', required=False,
                   default=r'D:\\SteamLibrary\\steamapps\\common\\Neon White\\Neon White_Data')
    p.add_argument('--dst', required=False,
                   default=r'D:\\Downloads\\Code\\NeonWhiteCustomLevels\\custom_levels')
    p.add_argument('--execute', action='store_true', help='Perform actual copy. Without this the script only does a dry-run')
    args = p.parse_args()

    src = norm(args.src)
    dst = norm(args.dst)

    matches = find_matches(src)
    if not matches:
        print('No matching items found.')
        return 0

    print(f"Found {len(matches)} matching item(s) in: {src}")
    for name, path, is_dir in matches:
        dst_path = os.path.join(dst, name)
        if args.execute:
            try:
                print(f"Copying: {path} -> {dst_path}")
                os.makedirs(dst, exist_ok=True)
                copy_item(path, dst_path, is_dir)
            except Exception as e:
                print(f"ERROR copying {path}: {e}")
        else:
            print(f"Would copy: {path} -> {dst_path}")

    if args.execute:
        print('Copy complete.')
    else:
        print('Dry-run complete. Rerun with --execute to perform the copy.')

    return 0


if __name__ == '__main__':
    sys.exit(main())
