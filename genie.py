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
        print("Config file not found. Please run the setup script first.")
        sys.exit(1)
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Error: The config file at {config_path} is not valid JSON. Please check its contents.")
        sys.exit(1)
    except IOError:
        print(f"Error: Unable to read {config_path}. Please check your permissions.")
        sys.exit(1)

def get_ai_response(api_key, prompt):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key
    }
    data = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text'].strip()
    else:
        print(f"Error: API request failed with status code {response.status_code}")
        print(response.text)
        sys.exit(1)

def get_command_suggestion(api_key, question):
    prompt = f"""You are a CLI expert. Given the following question, suggest an appropriate command-line command.
    Only provide the command itself, without any explanations or additional text.
    
    Question: {question}"""
    return get_ai_response(api_key, prompt)

def get_command_explanation(api_key, command):
    prompt = f"""Explain the following command in simple terms. Break down each part of the command and describe what it does, but keep it as short as possible:

    Command: {command}"""
    return get_ai_response(api_key, prompt)

def print_boxed(text, color=BLUE, use_pretty=True):
    if not use_pretty:
        print(text)
        return

    width = min(os.get_terminal_size().columns - 4, 100)
    
    # Split the text into lines, respecting original newlines
    lines = text.split('\n')
    
    # Wrap each line individually
    wrapped_lines = []
    for line in lines:
        if line.strip() == '':
            wrapped_lines.append('')
        else:
            wrapped_lines.extend(textwrap.wrap(line, width=width))
    
    print(f"{color}┌{'─' * (width + 2)}┐{RESET}")
    for line in wrapped_lines:
        print(f"{color}│ {line:<{width}} │{RESET}")
    print(f"{color}└{'─' * (width + 2)}┘{RESET}")


def print_formatted(text, color=RESET, use_pretty=True):
    if use_pretty:
        print(f"{color}{text}{RESET}")
    else:
        print(text)

def main():
    if len(sys.argv) < 2:
        print("Usage: genie 'Your question here'")
        sys.exit(1)

    config = load_config()
    api_key = config.get('api_key')
    use_pretty = config.get('pretty_output', True)

    if not api_key:
        print("Error: API key is missing from the config. Please run the setup script again.")
        sys.exit(1)

    question = " ".join(sys.argv[1:])
    
    try:
        print_formatted("🧞 Genie is thinking...", BOLD, use_pretty)
        command = get_command_suggestion(api_key, question)
        
        print_formatted("\nYour question:", BOLD, use_pretty)
        print_boxed(question, BLUE, use_pretty)
        
        print_formatted("\nSuggested command:", BOLD, use_pretty)
        print_boxed(command, GREEN, use_pretty)
        
        while True:
            user_input = input("\nDo you want to (R)un, (E)xplain, or (C)ancel this command? [R/E/C]: ").strip().lower()
            
            if user_input == 'r':
                print_formatted("\nExecuting command...", BOLD, use_pretty)
                try:
                    result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
                    print_formatted("Output:", BOLD, use_pretty)
                    print_boxed(result.stdout.strip() or "No output", BLUE, use_pretty)
                    if result.stderr:
                        print_formatted("\nErrors:", BOLD, use_pretty)
                        print_boxed(result.stderr.strip(), RED, use_pretty)
                except subprocess.TimeoutExpired:
                    print_formatted("Error: The command took too long to execute and was terminated.", RED, use_pretty)
                except subprocess.CalledProcessError as e:
                    print_formatted(f"Error: The command failed with return code {e.returncode}", RED, use_pretty)
                    if e.output:
                        print_formatted("\nOutput:", BOLD, use_pretty)
                        print_boxed(e.output.strip(), BLUE, use_pretty)
                    if e.stderr:
                        print_formatted("\nErrors:", BOLD, use_pretty)
                        print_boxed(e.stderr.strip(), RED, use_pretty)
                break
            elif user_input == 'e':
                print_formatted("\nExplaining the command...", BOLD, use_pretty)
                explanation = get_command_explanation(api_key, command)
                print_formatted("\nExplanation:", BOLD, use_pretty)
                print_boxed(explanation, YELLOW, use_pretty)
            elif user_input == 'c':
                print_formatted("\nCommand cancelled.", YELLOW, use_pretty)
                break
            else:
                print_formatted("Invalid input. Please enter 'R' to run, 'E' to explain, or 'C' to cancel.", RED, use_pretty)
    
    except KeyboardInterrupt:
        print_formatted("\nOperation cancelled by user.", YELLOW, use_pretty)
        sys.exit(0)
    except Exception as e:
        print_formatted(f"\nAn unexpected error occurred: {str(e)}", RED, use_pretty)
        sys.exit(1)

if __name__ == "__main__":
    main()
