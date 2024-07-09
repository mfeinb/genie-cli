# 🧞 Genie: Your AI-Powered CLI Assistant

Genie is a magical command-line tool that harnesses the power of Google's Gemini AI to suggest and execute shell commands based on your natural language queries. Say goodbye to forgetting command syntax or endlessly searching for the right commands online!

![Genie Demo](images/logo.webp)

## ✨ Features

- 🤖 Powered by Google's Gemini AI for accurate command suggestions
- 💬 Use natural language to get command-line suggestions
- 🚀 Execute suggested commands directly from the tool
- 🎨 Optional pretty output for enhanced readability
- 🔒 Secure storage of your API key
- 🔧 Easy setup and configuration

## 🛠 Installation

1. Clone this repository:
   ```
   git clone https://github.com/mfeinb/genie-cli.git
   cd genie-cli
   ```

2. Run the setup script:
   ```
   python3 setup.py
   ```

3. Follow the prompts to enter your Google Gemini API key and choose your output preferences.

4. Add the suggested alias to your shell configuration file (e.g., `.zshrc` or `.bashrc`):
   ```
   alias genie='python3 ~/.genie/genie.py'
   ```

5. Reload your shell configuration:
   ```
   source ~/.zshrc  # or ~/.bashrc, depending on your shell
   ```

## 🎩 Usage

Once installed, using Genie is as simple as:

```
genie "your question here"
```

For example:
```
genie "show me the largest files in the current directory"
```

Genie will suggest a command, and you can choose to execute it or not.

## 📋 Requirements

- Python 3.6+
- `requests` library (installed automatically during setup)
- Google Gemini API key (obtainable from [Google AI Studio](https://makersuite.google.com/app/apikey))

## 🔐 Security

Your API key is stored locally in `~/.genie/config.json`. Always keep this file secure and never share it publicly.

## 🎭 Customization

You can re-run the setup script at any time to change your API key or toggle pretty output:

```
python3 setup.py
```

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/mfeinb/genie-cli/issues).

## 📜 License

This project is [MIT](https://choosealicense.com/licenses/mit/) licensed.

## 🙏 Acknowledgements

- Google Gemini AI for powering the command suggestions
- All the CLI wizards who inspired this project
- Claude for actually writing this code

---

Made with ❤️ and a bit of magic ✨
