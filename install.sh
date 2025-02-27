#!/bin/bash

# Install OLM
chmod +x olm.py
sudo mv olm.py /usr/local/bin/olm

# Define shell function with automatic exporting
OLM_FUNCTION=$(cat << 'EOF'

# OLM Shell Function
olm() {
    local cmd output
    output=$(/usr/local/bin/olm "$@")  # Runs Python script
    
    if [[ "$1" == "scr" || "$1" == "sip" || "$1" == "sdn" || "$1" == "sha" ]]; then
        eval "$output"  # Automatically export variables
    else
        echo "$output"
    fi
}

EOF
)

# Add function to .bashrc if not present
if ! grep -Fxq "$OLM_FUNCTION" "$HOME/.bashrc"; then
    echo "$OLM_FUNCTION" >> "$HOME/.bashrc"
fi

# Add function to .zshrc if not present
if ! grep -Fxq "$OLM_FUNCTION" "$HOME/.zshrc"; then
    echo "$OLM_FUNCTION" >> "$HOME/.zshrc"
fi

echo "OLM installed. Restart your shell or run 'source ~/.bashrc' (or 'source ~/.zshrc' for Zsh) to enable persistent exports."
