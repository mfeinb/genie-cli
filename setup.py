#!/usr/bin/env python3
import os
import json
import sys
import shutil

def get_input(prompt, allow_empty=True):
    return input(prompt).strip()

def load_existing_config():
    config_path = os.path.expanduser("~/.genie/config.json")
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Existing config file is invalid. Starting with a fresh configuration.")
        except IOError:
            print("Unable to read existing config file. Starting with a fresh configuration.")
    return {}

def setup():
    print("Welcome to the Genie setup process!")
    
    genie_dir = os.path.expanduser("~/.genie")
    try:
        os.makedirs(genie_dir, exist_ok=True)
    except PermissionError:
        print(f"Error: Unable to create directory {genie_dir}. Please check your permissions.")
        sys.exit(1)

    existing_config = load_existing_config()

    print("\nTo use Genie, you'll need a Google Gemini API key.")
    print("If you don't have one, follow these steps:")
    print("1. Go to https://makersuite.google.com/app/apikey")
    print("2. Create an API key if you haven't already")
    print("3. Copy the API key and paste it here")
    print("(Leave blank to keep the existing API key, if any)")
    
    api_key = get_input("\nEnter your Google Gemini API key: ")
    
    if api_key:
        existing_config['api_key'] = api_key
    elif 'api_key' not in existing_config:
        print("Error: API key is required for first-time setup.")
        sys.exit(1)

    pretty_option = get_input("\nDo you want to use pretty output? (y/n, default: y): ").lower()
    existing_config['pretty_output'] = pretty_option != 'n'

    config_path = os.path.join(genie_dir, "config.json")
    try:
        with open(config_path, 'w') as f:
            json.dump(existing_config, f, indent=2)
    except IOError:
        print(f"Error: Unable to write to {config_path}. Please check your permissions.")
        sys.exit(1)
    
    print(f"\nConfig file updated at {config_path}")

    # Copy genie.py to the .genie directory
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    main_script = os.path.join(script_dir, "genie.py")
    
    if not os.path.exists(main_script):
        print(f"Error: {main_script} not found. Please ensure it's in the same directory as this setup script.")
        sys.exit(1)

    genie_script_path = os.path.join(genie_dir, "genie.py")
    try:
        shutil.copy2(main_script, genie_script_path)
        print(f"Genie script copied to {genie_script_path}")
    except IOError:
        print(f"Error: Unable to copy genie.py to {genie_dir}. Please check your permissions.")
        sys.exit(1)

    print("\nTo complete the installation, add the following line to your shell configuration file")
    print("(.zshrc, .bashrc, .bash_profile, etc.):")
    print(f"\nalias genie='python3 {genie_script_path}'")
    print("\nAfter adding the line, either restart your terminal or run:")
    print("source ~/.zshrc  # if you're using zsh")
    print("source ~/.bashrc  # if you're using bash")
    print("\nThen you can use Genie by typing 'genie' followed by your question in quotes.")

if __name__ == "__main__":
    setup()
