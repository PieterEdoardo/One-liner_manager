#!/bin/bash

echo "[*] Installing OLM..."

# Copy the Python script
sudo cp olm.py /usr/local/bin/olm
sudo chmod +x /usr/local/bin/olm

# Add function to shell profiles
BASHRC="$HOME/.bashrc"
ZSHRC="$HOME/.zshrc"

OLM_FUNCTION=$(cat << 'EOF'

# OLM Shell Function
olm() {
    local cmd output
    output=$(/usr/local/bin/olm "$@")  # Runs Python script
    
    if [[ "$1" == "scr" || "$1" == "sip" || "$1" == "sdn" || "$1" == "sh" ]]; then
        eval "$output"  # Automatically export variables
    else
        echo "$output"
    fi
}

EOF
)

if ! grep -q "olm()" "$BASHRC"; then
    echo "$OLM_FUNCTION" >> "$BASHRC"
    echo "[*] Added OLM function to $BASHRC"
fi

if ! grep -q "olm()" "$ZSHRC"; then
    echo "$OLM_FUNCTION" >> "$ZSHRC"
    echo "[*] Added OLM function to $ZSHRC"
fi

echo "[*] Installation complete. Restart your shell or run 'source ~/.bashrc' (or 'source ~/.zshrc')."
