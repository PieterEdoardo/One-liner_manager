import sys
import os
import argparse

USERNAMES_FILE = 'usernames.txt'
PASSWORDS_FILE = 'passwords.txt'
IPS_FILE = 'ips.txt'
DOMAINS_FILE = 'domains.txt'


def add_username(username, password=None):
    with open(USERNAMES_FILE, 'a') as user_file:
        user_file.write(username + '\n')
    with open(PASSWORDS_FILE, 'a') as pass_file:
        pass_file.write((password or '') + '\n')


def list_credentials():
    if os.path.exists(USERNAMES_FILE) and os.path.exists(PASSWORDS_FILE):
        with open(USERNAMES_FILE, 'r') as user_file, open(PASSWORDS_FILE, 'r') as pass_file:
            usernames = user_file.readlines()
            passwords = pass_file.readlines()

        for i in range(max(len(usernames), len(passwords))):
            username = usernames[i].strip() if i < len(usernames) else ''
            password = passwords[i].strip() if i < len(passwords) else ''
            print(f'{i}: {username} - {password}')
    else:
        print("No credentials found. Files don't exist or are empty.")


def remove_by_index(index):
    if os.path.exists(USERNAMES_FILE) and os.path.exists(PASSWORDS_FILE):
        with open(USERNAMES_FILE, 'r') as user_file, open(PASSWORDS_FILE, 'r') as pass_file:
            usernames = user_file.readlines()
            passwords = pass_file.readlines()

        if 0 <= index < len(usernames) and 0 <= index < len(passwords):
            usernames.pop(index)
            passwords.pop(index)
            with open(USERNAMES_FILE, 'w') as user_file, open(PASSWORDS_FILE, 'w') as pass_file:
                user_file.writelines(usernames)
                pass_file.writelines(passwords)
            print(f"Removed credential set at index {index}")
        else:
            print("Invalid index. No entry removed.")
    else:
        print("No credentials found. Files don't exist or are empty.")


def select_by_index(index, file, env_var):
    if os.path.exists(file):
        with open(file, 'r') as f:
            items = f.readlines()

        if 0 <= index < len(items):
            item = items[index].strip()
            print(f"export {env_var}='{item}'")
        else:
            print("Invalid index. No entry selected.")
    else:
        print(f"No {env_var.lower()}s found. File doesn't exist or is empty.")


def add_entry(file, entry):
    with open(file, 'a') as f:
        f.write(entry + '\n')


def list_entries(file):
    if os.path.exists(file):
        with open(file, 'r') as f:
            for i, line in enumerate(f):
                print(f'{i}: {line.strip()}')
    else:
        print("No entries found.")


def main():
    parser = argparse.ArgumentParser(description="Credential management tool for usernames, IPs, and domains.")
    subparsers = parser.add_subparsers(dest='command')

    # Add username and password
    add_parser = subparsers.add_parser('add', help="Add a new username and password.")
    add_parser.add_argument('username', help="The username to add.")
    add_parser.add_argument('password', nargs='?', help="The password to add (optional).")

    # List credentials
    subparsers.add_parser('list', help="List all saved credentials with indices.")

    # Remove credentials
    rm_parser = subparsers.add_parser('rm', help="Remove a credential by index.")
    rm_parser.add_argument('index', type=int, help="The index of the credential to remove.")

    # Select credentials
    sel_parser = subparsers.add_parser('sel', help="Select a credential by index and export as environment variables.")
    sel_parser.add_argument('index', type=int, help="The index of the credential to select.")

    # Add or list IPs
    ip_parser = subparsers.add_parser('ip', help="Add or list IP addresses.")
    ip_parser.add_argument('ip', nargs='?', help="The IP address to add (optional).")

    # Add or list domain names
    dn_parser = subparsers.add_parser('dn', help="Add or list domain names.")
    dn_parser.add_argument('domain', nargs='?', help="The domain name to add (optional).")

    # Select IP
    sip_parser = subparsers.add_parser('sip', help="Select an IP by index and export as $IP.")
    sip_parser.add_argument('index', type=int, help="The index of the IP to select.")

    # Select domain name
    sdn_parser = subparsers.add_parser('sdn', help="Select a domain by index and export as $DOMAIN.")
    sdn_parser.add_argument('index', type=int, help="The index of the domain to select.")

    args = parser.parse_args()

    if args.command == 'add':
        add_username(args.username, args.password)
    elif args.command == 'list':
        list_credentials()
    elif args.command == 'rm':
        remove_by_index(args.index)
    elif args.command == 'sel':
        select_by_index(args.index, USERNAMES_FILE, 'username')
        select_by_index(args.index, PASSWORDS_FILE, 'password')
    elif args.command == 'ip':
        if args.ip:
            add_entry(IPS_FILE, args.ip)
        else:
            list_entries(IPS_FILE)
    elif args.command == 'dn':
        if args.domain:
            add_entry(DOMAINS_FILE, args.domain)
        else:
            list_entries(DOMAINS_FILE)
    elif args.command == 'sip':
        select_by_index(args.index, IPS_FILE, 'IP')
    elif args.command == 'sdn':
        select_by_index(args.index, DOMAINS_FILE, 'DOMAIN')
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
