#!/usr/bin/env python3
import os
import argparse
from typing import List

# Define storage paths
DATA_DIR = os.path.expanduser("~")
FILES = {
    "usernames": os.path.join(DATA_DIR, "usernames.txt"),
    "passwords": os.path.join(DATA_DIR, "passwords.txt"),
    "ips": os.path.join(DATA_DIR, "ips.txt"),
    "domains": os.path.join(DATA_DIR, "domains.txt"),
    "oneliners": os.path.join(DATA_DIR, "oneliners.txt"),
    "hashes": os.path.join(DATA_DIR, "hashes.txt"),
}

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)


# Helper functions for file operations
def read_file(filepath: str) -> List[str]:
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return [line.strip() for line in f.readlines()]
    return []


def write_file(filepath: str, data: List[str]) -> None:
    with open(filepath, "w") as f:
        f.write("\n".join(data) + "\n")


def add_entry(file: str, entry: str) -> None:
    data = read_file(file)
    data.append(entry)
    write_file(file, data)


def remove_entry(file: str, index: int) -> None:
    data = read_file(file)
    if 0 <= index < len(data):
        del data[index]
        write_file(file, data)


def list_entries(file: str) -> None:
    entries = read_file(file)
    for i, entry in enumerate(entries):
        print(f"[{i}] {entry}")


def select_entry(file: str, var_name: str) -> None:
    entries = read_file(file)
    if args.index is not None and 0 <= args.index < len(entries):
        print(f"export {var_name}='{entries[args.index]}'")
    else:
        print("Invalid index or missing argument")


def execute_one_liner(index: int, confirm: bool = True) -> None:
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


def spray_attack(one_liner_index: int, method: str, use_hash: bool = False) -> None:
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
        creds = hashes
        env_var = "hash"
    else:
        if not passwords:
            print("No passwords stored.")
            return
        creds = passwords
        env_var = "password"

    if method == "username-first":
        for username in usernames:
            for cred in creds:
                os.environ["username"], os.environ[env_var] = username, cred
                print(f"Trying username: {username}, {env_var}: {cred}")
                execute_one_liner(one_liner_index, confirm=False)
    else:  # password-first
        for cred in creds:
            for username in usernames:
                os.environ["username"], os.environ[env_var] = username, cred
                print(f"Trying username: {username}, {env_var}: {cred}")
                execute_one_liner(one_liner_index, confirm=False)


def main():
    parser = argparse.ArgumentParser(description="One-Liner Manager (OLM)")
    subparsers = parser.add_subparsers(dest="command")

    # Credentials
    parser_cr = subparsers.add_parser("cr")
    parser_cr.add_argument("username", nargs="?")
    parser_cr.add_argument("password", nargs="?")

    parser_scr = subparsers.add_parser("scr")
    parser_scr.add_argument("index", type=int, nargs="?")

    parser_rmcr = subparsers.add_parser("rmcr")
    parser_rmcr.add_argument("index", type=int)

    # Spray attack
    parser_spray = subparsers.add_parser("spray")
    parser_spray.add_argument("one_liner_index", type=int)
    parser_spray.add_argument("--hash", action="store_true")
    parser_spray.add_argument("--method", choices=["username-first", "password-first"], default="username-first")

    # Hash management
    parser_ha = subparsers.add_parser("ha")
    parser_ha.add_argument("hash", nargs="?")

    parser_sha = subparsers.add_parser("sha")
    parser_sha.add_argument("index", type=int, nargs="?")

    parser_rmha = subparsers.add_parser("rmha")
    parser_rmha.add_argument("index", type=int)

    # IP Management
    parser_ip = subparsers.add_parser("ip")
    parser_ip.add_argument("ip", nargs="?")

    parser_sip = subparsers.add_parser("sip")
    parser_sip.add_argument("index", type=int, nargs="?")

    parser_rmip = subparsers.add_parser("rmip")
    parser_rmip.add_argument("index", type=int)

    # Domain Management
    parser_dn = subparsers.add_parser("dn")
    parser_dn.add_argument("domain", nargs="?")

    parser_sdn = subparsers.add_parser("sdn")
    parser_sdn.add_argument("index", type=int, nargs="?")

    parser_rmdn = subparsers.add_parser("rmdn")
    parser_rmdn.add_argument("index", type=int)

    # One-Liner Management
    parser_ol = subparsers.add_parser("ol")
    parser_ol.add_argument("one_liner", nargs="?")

    parser_rmol = subparsers.add_parser("rmol")
    parser_rmol.add_argument("index", type=int)

    # One-Liner Execution
    parser_ex = subparsers.add_parser("ex")
    parser_ex.add_argument("index", type=int)
    parser_ex.add_argument("-y", action="store_true", help="Bypass confirmation")

    args = parser.parse_args()

    # Command Execution
    if args.command == "cr":
        if args.username and args.password:
            add_entry(FILES["usernames"], args.username)
            add_entry(FILES["passwords"], args.password)
        else:
            print("Usernames:")
            list_entries(FILES["usernames"])
            print("\nPasswords:")
            list_entries(FILES["passwords"])

    elif args.command == "scr":
        select_entry(FILES["usernames"], "username")
        select_entry(FILES["passwords"], "password")

    elif args.command == "rmcr":
        remove_entry(FILES["usernames"], args.index)
        remove_entry(FILES["passwords"], args.index)

    elif args.command == "spray":
        spray_attack(args.one_liner_index, args.method, args.hash)

    elif args.command == "ha":
        if args.hash:
            add_entry(FILES["hashes"], args.hash)
        else:
            list_entries(FILES["hashes"])

    elif args.command == "sha":
        select_entry(FILES["hashes"], "hash")

    elif args.command == "rmha":
        remove_entry(FILES["hashes"], args.index)

    elif args.command == "ip":
        if args.ip:
            add_entry(FILES["ips"], args.ip)
        else:
            list_entries(FILES["ips"])

    elif args.command == "sip":
        select_entry(FILES["ips"], "IP")

    elif args.command == "rmip":
        remove_entry(FILES["ips"], args.index)

    elif args.command == "dn":
        if args.domain:
            add_entry(FILES["domains"], args.domain)
        else:
            list_entries(FILES["domains"])

    elif args.command == "sdn":
        select_entry(FILES["domains"], "DOMAIN")

    elif args.command == "rmdn":
        remove_entry(FILES["domains"], args.index)

    elif args.command == "ol":
        if args.one_liner:
            add_entry(FILES["oneliners"], args.one_liner)
        else:
            list_entries(FILES["oneliners"])

    elif args.command == "rmol":
        remove_entry(FILES["oneliners"], args.index)

    elif args.command == "ex":
        execute_one_liner(args.index, not args.y)

if __name__ == "__main__":
    main()
