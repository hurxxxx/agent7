#!/bin/bash

# Script to add conda environment activation to .bashrc
# This will automatically activate the 'langgraph' conda environment when opening a terminal

# Check if .bashrc exists
if [ ! -f ~/.bashrc ]; then
    echo "Error: ~/.bashrc file not found."
    exit 1
fi

# Check if the activation code is already in .bashrc
if grep -q "# Automatically activate langgraph conda environment" ~/.bashrc; then
    echo "The activation code is already in ~/.bashrc."
    exit 0
fi

# Add the activation code to .bashrc
cat << 'EOF' >> ~/.bashrc

# Automatically activate langgraph conda environment
if [ -f "$(conda info --base)/etc/profile.d/conda.sh" ]; then
    . "$(conda info --base)/etc/profile.d/conda.sh"
    if conda env list | grep -q "langgraph"; then
        conda activate langgraph
        echo "Langgraph conda environment activated."
    else
        echo "Warning: langgraph conda environment not found."
        echo "To create it, run:"
        echo "conda create -n langgraph python=3.10"
        echo "conda activate langgraph"
        echo "pip install -r requirements.txt"
    fi
else
    echo "Warning: conda not found or not properly initialized."
fi
EOF

echo "Added langgraph conda environment activation to ~/.bashrc."
echo "The changes will take effect in new terminal sessions."
echo "To activate in the current session, run: source ~/.bashrc"
