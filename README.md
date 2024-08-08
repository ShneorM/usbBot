
# Telegram Folder Uploader Bot

A project to upload folders to a Telegram bot using a Tkinter GUI. Handles large files by splitting them and generates a directory tree for navigation.

## Features

- Tkinter GUI for folder selection and upload.
- Splits large files to comply with Telegram's 50MB limit.
- Generates a directory tree file.
- View and download files through the Telegram bot.

## Prerequisites

- Python 3.7+
- `python-telegram-bot` library
- `tkinter` (included with Python)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/telegram-folder-uploader-bot.git
   cd telegram-folder-uploader-bot
   ```

2. Install required libraries:

   ```bash
   pip install python-telegram-bot
   ```

## Usage

1. **Configure the Bot**:

   Edit `upload_to_bot.py` with your bot's token and chat ID.

   ```python
   TELEGRAM_BOT_TOKEN = 'your-telegram-bot-token'
   CHAT_ID = 'your-chat-id'
   ```

2. **Run the GUI**:

   ```bash
   python gui.py
   ```

3. **Upload a Folder**:

   - Select a folder and click "Upload" to start uploading.

4. **Interact with the Bot**:

   - Use `/start` to begin.
   - Reply to any message with `.` to upload the directory tree.
   - Use `/show` to navigate and download files.

## Files Overview

- `gui.py`: GUI code for folder upload.
- `upload_to_bot.py`: Handles file uploads and splitting.
- `bot.py`: Bot commands and interactions.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
