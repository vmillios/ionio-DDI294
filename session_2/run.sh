#!/bin/bash

# This script installs dependencies and runs the Streamlit app.

# echo "--- Installing Python dependencies ---"
# pip install streamlit plyer

echo ""
echo "--- NOTE: System dependencies may be required ---"
echo "On Debian/Ubuntu, you might need: sudo apt-get install libnotify-bin"
echo "On Fedora, you might need: sudo dnf install libnotify"
echo "-------------------------------------------------"
echo ""

echo "--- Starting Streamlit App ---"
streamlit run app.py
