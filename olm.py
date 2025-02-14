import sys
import os
import argparse

USERNAMES_FILE = 'usernames.txt'
PASSWORDS_FILE = 'passwords.txt'
IPS_FILE = 'ips.txt'
DOMAINS_FILE = 'domains.txt'
ONELINERS_FILE = 'oneliners.txt'

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
        print("No credentials found.")

def remove_by_index(index, file):
    if os.path.exists(file):
        with open(file, 'r') as f:
            lines = f.readlines()
        
        if 0 <= index < len(lines):
            del lines[index]
            with open(file, 'w') as f:
                f.writelines(lines)
            print(f"Removed entry at index {index}.")
        else:
            print("Invalid index.")
    else:
        print("File does not exist.")

def select_by_index(index, file, env_var):
    if os.path.exists(file):
        with open(file, 'r') as f:
            items = f.readlines()
        if 0 <= index < len(items):
            print(f"export {env_var}='{items[index].strip()}'")
        else:
            print("Invalid index.")
    else:
        print(f"No {env_var.lower()}s found.")

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

def execute_oneliner(index):
    if os.path.exists(ONELINERS_FILE):
        with open(ONELINERS_FILE, 'r') as f:
            oneliners = f.readlines()
        if 0 <= index < len(oneliners):
            command = oneliners[index].strip()
            command = command.replace('$username', os.getenv('username', ''))
            command = command.replace('$password', os.getenv('password', ''))
            command = command.replace('$IP', os.getenv('IP', ''))
            os.system(command)
        else:
            print("Invalid index.")
    else:
        print("No one-liners stored.")

def main():
    parser = argparse.ArgumentParser(description="One-Liner Manager (OLM)")
    subparsers = parser.add_subparsers(dest='command')

    add_parser = subparsers.add_parser('add', help="Add username and password")
    add_parser.add_argument('username')
    add_parser.add_argument('password', nargs='?')

    subparsers.add_parser('list', help="List credentials")
    rm_parser = subparsers.add_parser('rm', help="Remove credential by index")
    rm_parser.add_argument('index', type=int)

    sel_parser = subparsers.add_parser('sel', help="Select credentials")
    sel_parser.add_argument('index', type=int)

    ip_parser = subparsers.add_parser('ip', help="Add or list IPs")
    ip_parser.add_argument('ip', nargs='?')
    dn_parser = subparsers.add_parser('dn', help="Add or list domains")
    dn_parser.add_argument('domain', nargs='?')

    sip_parser = subparsers.add_parser('sip', help="Select IP")
    sip_parser.add_argument('index', type=int)
    sdn_parser = subparsers.add_parser('sdn', help="Select domain")
    sdn_parser.add_argument('index', type=int)

    ol_parser = subparsers.add_parser('ol', help="Manage one-liners")
    ol_parser.add_argument('index', nargs='?', type=int, help="Index to overwrite (optional)")
    ol_parser.add_argument('command', nargs='?', help="Command to store (optional)")

    rmol_parser = subparsers.add_parser('rmol', help="Remove one-liner")
    rmol_parser.add_argument('index', type=int)

    ex_parser = subparsers.add_parser('ex', help="Execute one-liner")
    ex_parser.add_argument('index', type=int)

    args = parser.parse_args()

    if args.command == 'add':
        add_username(args.username, args.password)
    elif args.command == 'list':
        list_credentials()
    elif args.command == 'rm':
        remove_by_index(args.index, USERNAMES_FILE)
        remove_by_index(args.index, PASSWORDS_FILE)
    elif args.command == 'sel':
        select_by_index(args.index, USERNAMES_FILE, 'username')
        select_by_index(args.index, PASSWORDS_FILE, 'password')
    elif args.command == 'ip':
        add_entry(IPS_FILE, args.ip) if args.ip else list_entries(IPS_FILE)
    elif args.command == 'dn':
        add_entry(DOMAINS_FILE, args.domain) if args.domain else list_entries(DOMAINS_FILE)
    elif args.command == 'sip':
        select_by_index(args.index, IPS_FILE, 'IP')
    elif args.command == 'sdn':
        select_by_index(args.index, DOMAINS_FILE, 'DOMAIN')
    elif args.command == 'ol':
        if args.index is not None and args.command is not None:
            remove_by_index(args.index, ONELINERS_FILE)
            add_entry(ONELINERS_FILE, args.command)
        elif args.command:
            add_entry(ONELINERS_FILE, args.command)
        else:
            list_entries(ONELINERS_FILE)
    elif args.command == 'rmol':
        remove_by_index(args.index, ONELINERS_FILE)
    elif args.command == 'ex':
        execute_oneliner(args.index)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
