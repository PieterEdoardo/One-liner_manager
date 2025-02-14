import sys
import os
import argparse

USERNAMES_FILE = 'usernames.txt'
PASSWORDS_FILE = 'passwords.txt'
IPS_FILE = 'ips.txt'
DOMAINS_FILE = 'domains.txt'
ONELINERS_FILE = 'oneliners.txt'


def modify_file(file, action, entry=None, index=None):
    """Handles adding, removing, and listing entries in a file."""
    if action == "add" and entry:
        with open(file, "a") as f:
            f.write(entry + "\n")

    elif action == "list":
        if os.path.exists(file):
            with open(file, "r") as f:
                lines = f.readlines()
                for i, line in enumerate(lines):
                    print(f"{i}: {line.strip()}")
        else:
            print(f"No entries found in {file}.")

    elif action == "remove" and index is not None:
        if os.path.exists(file):
            with open(file, "r") as f:
                lines = f.readlines()

            if 0 <= index < len(lines):
                del lines[index]
                with open(file, "w") as f:
                    f.writelines(lines)
                print(f"Removed entry at index {index} from {file}.")
            else:
                print("Invalid index.")
        else:
            print(f"{file} does not exist or is empty.")


def add_credential(username, password=None):
    """Adds a username-password pair while maintaining line alignment."""
    with open(USERNAMES_FILE, "a") as user_file, open(PASSWORDS_FILE, "a") as pass_file:
        user_file.write(username + "\n")
        pass_file.write((password or '') + "\n")


def list_credentials():
    """Lists all stored credentials with indices."""
    if os.path.exists(USERNAMES_FILE) and os.path.exists(PASSWORDS_FILE):
        with open(USERNAMES_FILE, "r") as user_file, open(PASSWORDS_FILE, "r") as pass_file:
            usernames = user_file.readlines()
            passwords = pass_file.readlines()

        for i in range(max(len(usernames), len(passwords))):
            username = usernames[i].strip() if i < len(usernames) else ''
            password = passwords[i].strip() if i < len(passwords) else ''
            print(f"{i}: {username} - {password}")
    else:
        print("No credentials found.")


def remove_credential(index):
    """Removes a credential pair at a given index."""
    if os.path.exists(USERNAMES_FILE) and os.path.exists(PASSWORDS_FILE):
        with open(USERNAMES_FILE, "r") as user_file, open(PASSWORDS_FILE, "r") as pass_file:
            usernames = user_file.readlines()
            passwords = pass_file.readlines()

        if 0 <= index < len(usernames) and 0 <= index < len(passwords):
            del usernames[index]
            del passwords[index]

            with open(USERNAMES_FILE, "w") as user_file, open(PASSWORDS_FILE, "w") as pass_file:
                user_file.writelines(usernames)
                pass_file.writelines(passwords)

            print(f"Removed credential set at index {index}")
        else:
            print("Invalid index.")
    else:
        print("No credentials found.")


def select_entry(file, index, env_var):
    """Exports an entry as an environment variable for Bash."""
    if os.path.exists(file):
        with open(file, "r") as f:
            lines = f.readlines()

        if 0 <= index < len(lines):
            item = lines[index].strip()
            print(f"export {env_var}='{item}'")
        else:
            print("Invalid index.")
    else:
        print(f"No {env_var.lower()}s found in {file}.")


def execute_oneliner(index, auto_confirm=False):
    """Executes a one-liner from the list with an optional confirmation."""
    if os.path.exists(ONELINERS_FILE):
        with open(ONELINERS_FILE, 'r') as f:
            oneliners = f.readlines()

        if 0 <= index < len(oneliners):
            command = oneliners[index].strip()

            if auto_confirm:
                os.system(command)
            else:
                confirm = input(f"Execute: {command}? (y/n): ")
                if confirm.lower() == 'y':
                    os.system(command)
                else:
                    print("Execution canceled.")
        else:
            print("Invalid index.")
    else:
        print("No one-liners found.")


def main():
    parser = argparse.ArgumentParser(description="One-Liner Manager (OLM) - Credential, IP, and One-Liner Management Tool")
    subparsers = parser.add_subparsers(dest="command")

    # Credential commands
    cr_parser = subparsers.add_parser("cr", help="Add a new credential.")
    cr_parser.add_argument("username", nargs="?", help="The username to add.")
    cr_parser.add_argument("password", nargs="?", help="The password to add (optional).")

    scr_parser = subparsers.add_parser("scr", help="Select a credential set by index and export.")
    scr_parser.add_argument("index", type=int, help="The index of the credential to select.")

    rmcr_parser = subparsers.add_parser("rmcr", help="Remove a credential set by index.")
    rmcr_parser.add_argument("index", type=int, help="The index of the credential to remove.")

    # IP commands
    ip_parser = subparsers.add_parser("ip", help="Add or list IP addresses.")
    ip_parser.add_argument("ip", nargs="?", help="The IP address to add (optional).")

    sip_parser = subparsers.add_parser("sip", help="Select an IP by index and export as $IP.")
    sip_parser.add_argument("index", type=int, help="The index of the IP to select.")

    rmip_parser = subparsers.add_parser("rmip", help="Remove an IP by index.")
    rmip_parser.add_argument("index", type=int, help="The index of the IP to remove.")

    # Domain commands
    dn_parser = subparsers.add_parser("dn", help="Add or list domain names.")
    dn_parser.add_argument("domain", nargs="?", help="The domain name to add (optional).")

    sdn_parser = subparsers.add_parser("sdn", help="Select a domain by index and export as $DOMAIN.")
    sdn_parser.add_argument("index", type=int, help="The index of the domain to select.")

    rmdn_parser = subparsers.add_parser("rmdn", help="Remove a domain by index.")
    rmdn_parser.add_argument("index", type=int, help="The index of the domain to remove.")

    # One-Liner commands
    ol_parser = subparsers.add_parser("ol", help="Add or list one-liners.")
    ol_parser.add_argument("oneliner", nargs="?", help="The one-liner to add (optional).")

    rmol_parser = subparsers.add_parser("rmol", help="Remove a one-liner by index.")
    rmol_parser.add_argument("index", type=int, help="The index of the one-liner to remove.")

    ex_parser = subparsers.add_parser("ex", help="Execute a one-liner by index.")
    ex_parser.add_argument("index", type=int, help="The index of the one-liner to execute.")
    ex_parser.add_argument("-y", action="store_true", help="Execute immediately without confirmation.")

    args = parser.parse_args()

    if args.command == "cr":
        if args.username:
            add_credential(args.username, args.password)
        else:
            list_credentials()
    elif args.command == "scr":
        select_entry(USERNAMES_FILE, args.index, "username")
        select_entry(PASSWORDS_FILE, args.index, "password")
    elif args.command == "rmcr":
        remove_credential(args.index)
    elif args.command == "ex":
        execute_oneliner(args.index, args.y)
    else:
        modify_file(**vars(args))

if __name__ == "__main__":
    main()
