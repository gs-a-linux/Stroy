#!/bin/bash

# --- Aether OS: Stroy Installer ---
echo "--- Starting Stroy Terminal Installation ---"

# 1. Check for Python
if ! command -v python3 &> /dev/null; then
    echo "!!!! Error: Python3 is not installed. Please install it first."
    exit 1
fi

# 2. Install dependencies
echo "*#@ Installing Python dependencies..."
python3 -m pip install -r requirements.txt

# 3. Make the python script executable
chmod +x stroy.py

# 4. Create the global command
# We use /usr/local/bin so it works for all users
echo "*#@ Creating global 'stroy' command..."
sudo ln -sf "$(pwd)/stroy.py" /usr/local/bin/stroy

# 5. Success Marker
echo "*()( INSTALLATION SUCCESSFUL"
echo "You can now start the terminal by typing: stroy"