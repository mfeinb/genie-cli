#!/usr/bin/env python3
import os
import sys
import subprocess
import json
import requests
import textwrap

# ANSI color codes
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

def load_config():
    config_path = os.path.expanduser("~/.genie/config.json")
    if not os.path.exists(config_path):
        print(f"{RED}Config file not found. Please run the setup script first.{RESET}")
        sys.exit(1)
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"{RED}Error: The config file at {config_path} is not valid JSON. Please check its contents.{RESET}")
        sys.exit(1)
    except IOError:
        print(f"{RED}Error: Unable to read {config_path}. Please check your permissions.{RESET}")
        sys.exit(1)

def get_command_suggestion(api_key, question):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key
    }
    data = {
        "contents": [{
            "parts": [{
                "text": f"""You are a CLI expert. Given the following question, suggest an appropriate command-line command.
                Only provide the command itself, without any explanations or additional text.
                
                Question: {question}"""
            }]
        }]
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text'].strip()
    else:
        print(f"{RED}Error: API request failed with status code {response.status_code}{RESET}")
        print(response.text)
        sys.exit(1)

def print_boxed(text, color=BLUE):
    width = min(os.get_terminal_size().columns - 4, 100)
    lines = textwrap.wrap(text, width=width)
    
    print(f"{color}┌{'─' * (width + 2)}┐{RESET}")
    for line in lines:
        print(f"{color}│ {line:<{width}} │{RESET}")
    print(f"{color}└{'─' * (width + 2)}┘{RESET}")

def main():
    if len(sys.argv) < 2:
        print(f"{YELLOW}Usage: genie 'Your question here'{RESET}")
        sys.exit(1)

    config = load_config()
    api_key = config.get('api_key')

    if not api_key:
        print(f"{RED}Error: API key is missing from the config. Please run the setup script again.{RESET}")
        sys.exit(1)

    question = " ".join(sys.argv[1:])
    
    try:
        print(f"\n{BOLD}🧞 Genie is thinking...{RESET}\n")
        command = get_command_suggestion(api_key, question)
        
        print(f"{BOLD}Your question:{RESET}")
        print_boxed(question, BLUE)
        
        print(f"\n{BOLD}Suggested command:{RESET}")
        print_boxed(command, GREEN)
        
        user_input = input(f"\n{YELLOW}Do you want to run this command? (Y/N): {RESET}").strip().lower()
        
        if user_input == 'y':
            print(f"\n{BOLD}Executing command...{RESET}\n")
            try:
                result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
                print(f"{BOLD}Output:{RESET}")
                print_boxed(result.stdout.strip() or "No output", BLUE)
                if result.stderr:
                    print(f"\n{BOLD}Errors:{RESET}")
                    print_boxed(result.stderr.strip(), RED)
            except subprocess.TimeoutExpired:
                print(f"{RED}Error: The command took too long to execute and was terminated.{RESET}")
            except subprocess.CalledProcessError as e:
                print(f"{RED}Error: The command failed with return code {e.returncode}{RESET}")
                if e.output:
                    print(f"\n{BOLD}Output:{RESET}")
                    print_boxed(e.output.strip(), BLUE)
                if e.stderr:
                    print(f"\n{BOLD}Errors:{RESET}")
                    print_boxed(e.stderr.strip(), RED)
        else:
            print(f"\n{YELLOW}Command not executed.{RESET}")
    
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}Operation cancelled by user.{RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{RED}An unexpected error occurred: {str(e)}{RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()
