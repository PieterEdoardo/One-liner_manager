# One-Liner Manager (OLM)

**OLM** is a command-line tool designed for managing credentials, IPs, domains, and executable one-liners in an ethical hacking workflow. It provides an intuitive way to store, retrieve, and execute commands based on stored credentials and targets. This tool shines when there are too many credentials and/or when commands need to be continuesly retyped with slightly different information. Olm can step in, and not just ease, but even semi-automate the process.https://github.com/PieterEdoardo/One-liner_manager/blob/main/README.md


## Installation

Clone the repository and navigate to the directory:

    git clone <your-repo-url>
    cd olm

Ensure you have Python 3 installed, then run:

    chmod +x olm.py

(Optional: Create a symlink for easier access)

    ln -s $(pwd)/olm.py /usr/local/bin/olm

## Usage

Run olm --help for an overview of commands.
### Credentials Management

Add Credentials:

    olm add <username> [password]

Stores a new username and optional password.

List Credentials:

    olm list

Displays stored credentials with indices.

Remove a Credential Set:

    olm rm <index>

Deletes a credential set at the given index.

Select Credentials (Exports to Bash ENV Vars):

    eval $(olm sel <index>)

Exports $username and $password variables for the selected index.

### IP and Domain Management

Add/List IPs:

    olm ip [IP_ADDRESS]

Without arguments, lists stored IPs.
With an IP address, adds it to the list.

Add/List Domains:

    olm dn [DOMAIN_NAME]

Without arguments, lists stored domains.
With a domain name, adds it to the list.

Select IP (Exports to Bash ENV Var):

    eval $(olm sip <index>)

Sets $IP to the selected IP.

Select Domain (Exports to Bash ENV Var):

    eval $(olm sdn <index>)

Sets $DOMAIN to the selected domain.

### One-Liner Management

Store a One-Liner:

    olm ol "<command>"

Saves a command template. Example:

    olm ol "ssh $username@$IP"

List One-Liners:

    olm ol

Displays stored one-liners with indices.

Overwrite a One-Liner:

    olm ol <index> "<new command>"

Example:

    olm ol 2 "scp file.txt $username@$IP:/tmp/"

Remove a One-Liner:

    olm rmol <index>

Deletes a one-liner at the given index.

Execute a One-Liner (With Substitutions):

    olm ex <index>

Runs the stored command, replacing $username, $password, and $IP with the selected credentials and target.

## Example Usage

```bash
olm add admin hunter2
olm ip 192.168.1.100
olm sel 0
olm sip 0
olm ol "ssh $username@$IP"
```
olm ex 0  # Executes "ssh admin@192.168.1.100"

## Notes

Use `eval $(olm sel <index>)` for persistent environment variable export in Bash.
The tool is designed for Linux-based environments; Windows support is not included.
