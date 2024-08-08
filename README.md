
# Telegram Folder Uploader Bot

A project to upload folders to a Telegram bot.
generates a directory tree for navigation.

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


Install required libraries:

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


## Cloud Deployment

To keep the bot running continuously, it is recommended to deploy the bot to a cloud service. Here are general steps to do this:

1. **Choose a Cloud Provider**: You can use providers like AWS, Heroku, Google Cloud, or any other cloud service that supports running Python applications.

2. **Deploy the Bot**:

   - Upload your project files to the cloud service.
   - Make sure to configure the environment variables for `TELEGRAM_BOT_TOKEN` and `CHAT_ID`.

3. **Run the Bot**:

   - Start the bot script (`bot.py`) on your cloud service.
   - Ensure the bot script runs as a background service or using a process manager to keep it alive.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
