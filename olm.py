import sys
import os
import argparse

USERNAMES_FILE = 'usernames.txt'
PASSWORDS_FILE = 'passwords.txt'
IPS_FILE = 'ips.txt'
DOMAINS_FILE = 'domains.txt'
ONELINERS_FILE = 'oneliners.txt'


def read_file(file):
    """Reads a file and returns a list of stripped lines."""
    return open(file).read().splitlines() if os.path.exists(file) else []


def write_file(file, lines):
    """Writes a list of lines to a file."""
    with open(file, 'w') as f:
        f.write('\n'.join(lines) + '\n')


def add_entry(file, entry):
    """Adds an entry to a file."""
    with open(file, 'a') as f:
        f.write(entry + '\n')


def list_entries(file, label):
    """Lists entries from a file with an index."""
    entries = read_file(file)
    if entries:
        for i, entry in enumerate(entries):
            print(f'{i}: {entry}')
    else:
        print(f"No {label} found.")


def remove_by_index(file, index, label):
    """Removes an entry from a file by index."""
    entries = read_file(file)
    if 0 <= index < len(entries):
        del entries[index]
        write_file(file, entries)
        print(f"Removed {label} at index {index}.")
    else:
        print(f"Invalid index. No {label} removed.")


def select_by_index(file, index, env_var):
    """Selects an entry by index and prints an export command."""
    entries = read_file(file)
    if 0 <= index < len(entries):
        print(f"export {env_var}='{entries[index]}'")
    else:
        print(f"Invalid index. No {env_var.lower()} selected.")


def execute_one_liner(index, confirm):
    """Executes a stored one-liner, replacing variables with selected values."""
    one_liners = read_file(ONELINERS_FILE)
    usernames = read_file(USERNAMES_FILE)
    passwords = read_file(PASSWORDS_FILE)
    ips = read_file(IPS_FILE)
    domains = read_file(DOMAINS_FILE)

    if 0 <= index < len(one_liners):
        cmd = one_liners[index]
        env_vars = {
            "$username": os.getenv("username", usernames[0] if usernames else ""),
            "$password": os.getenv("password", passwords[0] if passwords else ""),
            "$IP": os.getenv("IP", ips[0] if ips else ""),
            "$DOMAIN": os.getenv("DOMAIN", domains[0] if domains else "")
        }

        for var, value in env_vars.items():
            cmd = cmd.replace(var, value)

        if confirm:
            os.system(cmd)
        else:
            print(f"Executing: {cmd}")
            if input("Proceed? (y/n): ").lower() == 'y':
                os.system(cmd)
    else:
        print("Invalid one-liner index.")


def spray_attack(confirm):
    """Loops through all usernames and tries each username with all passwords before moving to the next username."""
    usernames = read_file(USERNAMES_FILE)
    passwords = read_file(PASSWORDS_FILE)
    ips = read_file(IPS_FILE)
    domains = read_file(DOMAINS_FILE)

    one_liners = read_file(ONELINERS_FILE)
    
    if not usernames or not passwords or not one_liners:
        print("Missing usernames, passwords, or one-liners.")
        return

    for username in usernames:
        for password in passwords:
            for cmd in one_liners:
                env_vars = {
                    "$username": username,
                    "$password": password,
                    "$IP": os.getenv("IP", ips[0] if ips else ""),
                    "$DOMAIN": os.getenv("DOMAIN", domains[0] if domains else "")
                }

                for var, value in env_vars.items():
                    cmd = cmd.replace(var, value)

                if confirm:
                    os.system(cmd)
                else:
                    print(f"Executing: {cmd}")
                    if input("Proceed? (y/n): ").lower() == 'y':
                        os.system(cmd)


def main():
    parser = argparse.ArgumentParser(description="One-Liner Manager (OLM)")
    subparsers = parser.add_subparsers(dest='command')

    # Credentials Management
    cr_parser = subparsers.add_parser('cr', help="Add or list credentials.")
    cr_parser.add_argument('username', nargs='?', help="The username to add.")
    cr_parser.add_argument('password', nargs='?', help="The password to add.")

    scr_parser = subparsers.add_parser('scr', help="Select a credential by index.")
    scr_parser.add_argument('index', type=int, help="The index of the credential to select.")

    rmcr_parser = subparsers.add_parser('rmcr', help="Remove a credential by index.")
    rmcr_parser.add_argument('index', type=int, help="The index of the credential to remove.")

    # IP Management
    ip_parser = subparsers.add_parser('ip', help="Add or list IP addresses.")
    ip_parser.add_argument('ip', nargs='?', help="The IP address to add.")

    sip_parser = subparsers.add_parser('sip', help="Select an IP by index.")
    sip_parser.add_argument('index', type=int, help="The index of the IP to select.")

    rmip_parser = subparsers.add_parser('rmip', help="Remove an IP by index.")
    rmip_parser.add_argument('index', type=int, help="The index of the IP to remove.")

    # Domain Management
    dn_parser = subparsers.add_parser('dn', help="Add or list domains.")
    dn_parser.add_argument('domain', nargs='?', help="The domain to add.")

    sdn_parser = subparsers.add_parser('sdn', help="Select a domain by index.")
    sdn_parser.add_argument('index', type=int, help="The index of the domain to select.")

    rmdn_parser = subparsers.add_parser('rmdn', help="Remove a domain by index.")
    rmdn_parser.add_argument('index', type=int, help="The index of the domain to remove.")

    # One-Liner Management
    ol_parser = subparsers.add_parser('ol', help="Store, list, or overwrite one-liners.")
    ol_parser.add_argument('index_or_command', nargs='?', help="Index to overwrite or command to store.")
    ol_parser.add_argument('new_command', nargs='?', help="New command to overwrite an existing one.")

    rmol_parser = subparsers.add_parser('rmol', help="Remove a one-liner by index.")
    rmol_parser.add_argument('index', type=int, help="The index of the one-liner to remove.")

    ex_parser = subparsers.add_parser('ex', help="Execute a stored one-liner.")
    ex_parser.add_argument('index', type=int, help="The index of the one-liner to execute.")
    ex_parser.add_argument('-y', action='store_true', help="Skip confirmation and execute immediately.")

    spray_parser = subparsers.add_parser('spray', help="Perform a spraying attack (loop usernames through all passwords).")
    spray_parser.add_argument('-y', action='store_true', help="Skip confirmation and execute immediately.")

    args = parser.parse_args()

    if args.command == 'cr':
        if args.username:
            add_entry(USERNAMES_FILE, args.username)
            add_entry(PASSWORDS_FILE, args.password or "")
        else:
            list_entries(USERNAMES_FILE, "credentials")
    elif args.command == 'scr':
        select_by_index(USERNAMES_FILE, args.index, 'username')
        select_by_index(PASSWORDS_FILE, args.index, 'password')
    elif args.command == 'rmcr':
        remove_by_index(USERNAMES_FILE, args.index, "credential")
        remove_by_index(PASSWORDS_FILE, args.index, "password")
    elif args.command == 'ex':
        execute_one_liner(args.index, args.y)
    elif args.command == 'spray':
        spray_attack(args.y)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
