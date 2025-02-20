#!/usr/bin/env python3
import sys
import os
import argparse
from typing import List

# Define storage paths
DATA_DIR = os.path.expanduser("~")
FILES = {
    "usernames": os.path.join(DATA_DIR, "usernames.txt"),  # Separate file for usernames
    "passwords": os.path.join(DATA_DIR, "passwords.txt"),  # Separate file for passwords
    "ips": os.path.join(DATA_DIR, "ips.txt"),
    "domains": os.path.join(DATA_DIR, "domains.txt"),
    "oneliners": os.path.join(DATA_DIR, "oneliners.txt"),
    "hashes": os.path.join(DATA_DIR, "hashes.txt")
}

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Helper functions for file operations
def read_file(filepath: str) -> List[str]:
    """Reads a file and returns its lines as a list of strings."""
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return [line.strip() for line in f.readlines()]
    return []

def write_file(filepath: str, data: List[str]) -> None:
    """Writes a list of strings to a file."""
    with open(filepath, "w") as f:
        f.write("\n".join(data) + "\n")

def add_entry(file: str, entry: str) -> None:
    """Adds an entry to a file."""
    data = read_file(file)
    data.append(entry)
    write_file(file, data)

def remove_entry(file: str, index: int) -> None:
    """Removes an entry from a file by index."""
    data = read_file(file)
    if 0 <= index < len(data):
        del data[index]
        write_file(file, data)

def list_entries(file: str) -> None:
    """Lists all entries in a file."""
    entries = read_file(file)
    for i, entry in enumerate(entries):
        print(f"[{i}] {entry}")

def select_entry(file: str, var_name: str) -> None:
    """Prints an export command for shell integration."""
    data = read_file(file)
    try:
        index = int(sys.argv[2])
        if 0 <= index < len(data):
            print(f"export {var_name}='{data[index]}'")
    except (IndexError, ValueError):
        print("Invalid index")

def execute_one_liner(index: int, confirm: bool = True) -> None:
    """Executes a one-liner, replacing variables with stored values."""
    one_liners = read_file(FILES["oneliners"])
    if 0 <= index < len(one_liners):
        command = one_liners[index]
        for var in ["username", "password", "IP", "DOMAIN", "hash"]:
            command = command.replace(f"${var}", os.getenv(var, f"<{var}>"))
        if confirm:
            confirm_exec = input(f"Execute: {command}? (y/n): ").strip().lower()
            if confirm_exec != "y":
                print("Execution cancelled.")
                return
        os.system(command)

def spray_attack(one_liner_index: int, use_hash: bool = False) -> None:
    """
    Performs a spray attack using either passwords or hashes.
    Args:
        one_liner_index (int): Index of the one-liner to execute.
        use_hash (bool): If True, uses hashes instead of passwords.
    """
    usernames = read_file(FILES["usernames"])
    passwords = read_file(FILES["passwords"])
    hashes = read_file(FILES["hashes"]) if use_hash else None
    
    if not usernames:
        print("No usernames stored.")
        return

    if use_hash:
        if not hashes:
            print("No hashes stored.")
            return
        # Spray attack with hashes
        for hash_value in hashes:
            for username in usernames:
                os.environ["username"], os.environ["hash"] = username, hash_value
                print(f"Trying username: {username}, hash: {hash_value}")
                execute_one_liner(one_liner_index, confirm=False)  # Execute specified one-liner
    else:
        if not passwords:
            print("No passwords stored.")
            return
        # Spray attack with passwords
        for password in passwords:
            for username in usernames:
                os.environ["username"], os.environ["password"] = username, password
                print(f"Trying username: {username}, password: {password}")
                execute_one_liner(one_liner_index, confirm=False)  # Execute specified one-liner

def main() -> None:
    args = sys.argv[1:]

    if len(args) < 1:
        print("Usage: olm <command> [options]")
        return

    command = args[0]

    # Credentials Management
    if command == "cr":
        if len(args) == 3:
            add_entry(FILES["usernames"], args[1])  # Add username
            add_entry(FILES["passwords"], args[2])  # Add password
        else:
            print("Usernames:")
            list_entries(FILES["usernames"])
            print("\nPasswords:")
            list_entries(FILES["passwords"])
    elif command == "scr":
        select_entry(FILES["usernames"], "username")
        select_entry(FILES["passwords"], "password")
    elif command == "rmcr":
        remove_entry(FILES["usernames"], int(args[1]))
        remove_entry(FILES["passwords"], int(args[1]))

    # IP Management
    elif command == "ip":
        if len(args) == 2:
            add_entry(FILES["ips"], args[1])
        else:
            list_entries(FILES["ips"])
    elif command == "sip":
        select_entry(FILES["ips"], "IP")
    elif command == "rmip":
        remove_entry(FILES["ips"], int(args[1]))

    # Domain Management
    elif command == "dn":
        if len(args) == 2:
            add_entry(FILES["domains"], args[1])
        else:
            list_entries(FILES["domains"])
    elif command == "sdn":
        select_entry(FILES["domains"], "DOMAIN")
    elif command == "rmdn":
        remove_entry(FILES["domains"], int(args[1]))

    # One-Liner Management
    elif command == "ol":
        if len(args) == 2:
            add_entry(FILES["oneliners"], args[1])
        else:
            list_entries(FILES["oneliners"])
    elif command == "rmol":
        remove_entry(FILES["oneliners"], int(args[1]))
    elif command == "ex":
        execute_one_liner(int(args[1]), confirm="-y" not in args)

    # Spray Attack
    elif command == "spray":
        if len(args) < 2:
            print("Usage: olm spray <one-liner-index> [--hash]")
            return
        one_liner_index = int(args[1])
        use_hash = "--hash" in args
        spray_attack(one_liner_index, use_hash=use_hash)

    # Hash Management
    elif command == "ha":
        if len(args) == 2:
            add_entry(FILES["hashes"], args[1])
        else:
            list_entries(FILES["hashes"])
    elif command == "sha":
        select_entry(FILES["hashes"], "hash")
    elif command == "rmha":
        remove_entry(FILES["hashes"], int(args[1]))

if __name__ == "__main__":
    main()
