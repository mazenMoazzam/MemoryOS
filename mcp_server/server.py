#!/usr/bin/env python3
"""
MCP Filesystem Server — indexes a codebase into MemoryOS vector memory.

Usage:
    python3 mcp_server/server.py --path /path/to/project [--user my_user]
"""

import argparse
import asyncio
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../backend'))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '../backend/.env'))

from db.postgres import setup_db
from scanner import scan_directory
from indexer import index_file


async def run(path: str, user_id: str):
    print(f"\n🔍 Scanning: {path}")
    files = scan_directory(path)
    print(f"Found {len(files)} files to index\n")

    if not files:
        print("No files found. Check the path and allowed extensions.")
        return

    await setup_db()

    success = 0
    failed = 0

    for i, file in enumerate(files, 1):
        try:
            memory_text = await index_file(file, user_id=user_id)
            print(f"[{i}/{len(files)}] {file['relative_path']}")
            print(f"         → {memory_text[:100]}...")
            success += 1
        except Exception as e:
            print(f"[{i}/{len(files)}] {file['relative_path']} — {e}")
            failed += 1

    print(f"\nDone. {success} indexed, {failed} failed.")


def main():
    parser = argparse.ArgumentParser(description="MemoryOS MCP Filesystem Indexer")
    parser.add_argument("--path", required=True, help="Path to the directory to index")
    parser.add_argument("--user", default="default", help="User ID to associate memories with")
    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: '{args.path}' is not a valid directory.")
        sys.exit(1)

    asyncio.run(run(args.path, args.user))


if __name__ == "__main__":
    main()
