# One-Liner Manager (OLM)

**OLM** is a command-line tool designed for managing credentials, IPs, domains, and executable one-liners in an ethical hacking workflow. It provides an intuitive way to store, retrieve, and execute commands based on stored credentials and targets. This tool shines when there are too many credentials and/or when commands need to be continuesly retyped with slightly different information. Olm can step in, and not just ease, but even semi-automate the process.


## Installation
It's possible to use the installation script. This features automatic installation and ands a wrapper function to your .bashrc. If you don't want that you can do a manual installation, but you'll forgo some of olms automation.

Clone the repository and navigate to the directory:

```bash
git clone https://github.com/PieterEdoardo/One-liner_manager.git
cd One-liner_manager
./install.sh
```

Ensure you have Python 3 installed, then run:

```bash
chmod +x olm.py
```

(Optional: Create a symlink for easier access)

```bash
ln -s $(pwd)/olm.py /usr/local/bin/olm
```

## Usage

Run `olm --help` for an overview of commands.
### Credentials Management

Add/select/remmove Credentials:

    olm cr <username> <password>
    olm scr <index>
    olm rmsc <index>

Stores a new username and optional password.

List Credentials:

    olm cr

Displays stored credentials with indices.

Remove a Credential Set:

    olm rm <index>

Deletes a credential set at the given index.

Select Credentials or any other select command, only relevant incase you didn't use the install.sh and don't have the wrapper function. (Exports to Bash ENV Vars):

    eval $(olm scr <index>)
    eval $(olm sip <index>)
    eval $(olm sdn <index>)
    eval $(olm sha <index>)

Exports $username and $password variables for the selected index.

### IP and Domain Management

Add IPs:

    olm ip <IP_ADDRESS>

Without arguments, lists stored IPs.
With an IP address, adds it to the list.

List all stored ips with

    olm ip

export ip entry to $IP with

    olm sip <index>

Add Domains:

    olm dn <DOMAIN_NAME>

Without arguments, lists stored domains.
With a domain name, adds it to the list.


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

You can use olm to execute spray attacks with commands that traditionally don't allow spraying.

    olm spray <index>
    olm spray <index> --hash
    olm spray <index> --hash --method "password-first"
    olm spray <index> --hash --method "username-first"

Use `--hash` to spray hashes instead in case you spray a tool that uses pass the hash like impacket. The default method is `username-first` and setting it essentially does nothing, but password first can be more efficient spraying hashes.

## Example Usage

```bash
olm add admin hunter2
olm ip 192.168.1.100
olm dn "corp.local"
olm sel 0
olm sip 0
olm sdn 0
olm ol "impacket-secretsdump $DOMAIN/$username:$password@$IP"
olm ex 0 # Executes "impacket-secretsdump corp.local/admin:hunter2@192.168.1.100"
```

## We have to go deeper

You can use olm *recursively* by storing olm commands as one-liners in olm!

```bash
olm ol "olm scr 234; olm sip 4; olm ex 12"
```

## Notes

Use `eval $(olm sel <index>)` for persistent environment variable export in Bash if the install.sh is not used for installation of the tool.
The tool is designed for Linux-based environments; Windows support is not included.
