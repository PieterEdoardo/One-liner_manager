#!/usr/bin/env python3
import sys
import os

# Define storage paths
DATA_DIR = os.path.expanduser("~")
FILES = {
    "credentials": os.path.join(DATA_DIR, "credentials.txt"),
    "ips": os.path.join(DATA_DIR, "ips.txt"),
    "domains": os.path.join(DATA_DIR, "domains.txt"),
    "oneliners": os.path.join(DATA_DIR, "oneliners.txt"),
    "hashes": os.path.join(DATA_DIR, "hashes.txt")
}

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Helper functions for file operations
def read_file(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return [line.strip() for line in f.readlines()]
    return []

def write_file(filepath, data):
    with open(filepath, "w") as f:
        f.write("\n".join(data) + "\n")

def add_entry(file, entry):
    data = read_file(file)
    data.append(entry)
    write_file(file, data)

def remove_entry(file, index):
    data = read_file(file)
    if 0 <= index < len(data):
        del data[index]
        write_file(file, data)

def list_entries(file):
    entries = read_file(file)
    for i, entry in enumerate(entries):
        print(f"[{i}] {entry}")

def select_entry(file, var_name):
    """Prints an export command for shell integration"""
    data = read_file(file)
    try:
        index = int(sys.argv[2])
        if 0 <= index < len(data):
            print(f"export {var_name}='{data[index]}'")
    except (IndexError, ValueError):
        print("Invalid index")

def execute_one_liner(index, confirm=True):
    """Executes a one-liner, replacing variables with stored values"""
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

def spray_attack():
    """Loops through usernames and tries all passwords before moving to the next username"""
    credentials = read_file(FILES["credentials"])
    
    if not credentials:
        print("No credentials stored.")
        return

    for cred in credentials:
        parts = cred.split(":")
        if len(parts) != 2:
            continue
        user, pwd = parts
        for password in read_file(FILES["credentials"]):
            os.environ["username"], os.environ["password"] = user, pwd
            os.system("olm ex 0 -y")

def main():
    args = sys.argv[1:]

    if len(args) < 1:
        print("Usage: olm <command> [options]")
        return

    command = args[0]

    # Credentials Management
    if command == "cr":
        if len(args) == 3:
            add_entry(FILES["credentials"], f"{args[1]}:{args[2]}")
        else:
            list_entries(FILES["credentials"])
    elif command == "scr":
        select_entry(FILES["credentials"], "username")
        select_entry(FILES["credentials"], "password")
    elif command == "rmcr":
        remove_entry(FILES["credentials"], int(args[1]))

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

    # Spraying Function
    elif command == "spray":
        spray_attack()

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
