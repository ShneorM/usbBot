import os
import asyncio
from telegram import Bot
from telegram.error import NetworkError, TelegramError, BadRequest

# החלף את הטוקן של הבוט שלך כאן
TELEGRAM_BOT_TOKEN = ''
# החלף את מזהה הצ'אט שלך כאן
CHAT_ID = ''

# מגבלת גודל הקובץ של Telegram (בבתים)
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

# מבנה נתונים לשמירת ה-ID של הקבצים
file_ids = {}

async def send_file(bot, chat_id, document_path):
    try:
        file_size = os.path.getsize(document_path)
        if file_size > 0:
            if file_size > MAX_FILE_SIZE:
                await split_and_send_file(bot, chat_id, document_path)
            else:
                with open(document_path, 'rb') as file:
                    if document_path.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
                        message = await bot.send_video(chat_id=chat_id, video=file)
                        file_id = message.video.file_id
                    elif document_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')):
                        message = await bot.send_photo(chat_id=chat_id, photo=file)
                        file_id = message.photo[-1].file_id  # largest size
                    else:
                        message = await bot.send_document(chat_id=chat_id, document=file)
                        file_id = message.document.file_id
                    file_ids[document_path] = file_id
                    print(f"Successfully sent: {document_path} with file ID: {file_id}")
        else:
            print(f"File is empty, skipping: {document_path}")
    except NetworkError as e:
        print(f"Network error: {e}")
    except BadRequest as e:
        print(f"Bad request: {e}")
    except TelegramError as e:
        print(f"Telegram error: {e}")
    except Exception as e:
        print(f"Error: {e}")

async def split_and_send_file(bot, chat_id, file_path):
    file_size = os.path.getsize(file_path)
    part_num = 1

    with open(file_path, 'rb') as file:
        while chunk := file.read(MAX_FILE_SIZE):
            part_file_path = f"{file_path}.part{part_num}"
            with open(part_file_path, 'wb') as part_file:
                part_file.write(chunk)

            await send_file(bot, chat_id, part_file_path)
            os.remove(part_file_path)
            part_num += 1

    await bot.send_message(chat_id,
                           text=f"File {os.path.basename(file_path)} was split into {part_num - 1} parts and sent. Please recombine them using a suitable tool.")

def get_files_in_directory(directory):
    file_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file != 'directory_tree.txt':  # דילוג על הקובץ directory_tree.txt
                file_paths.append(os.path.join(root, file))
    return file_paths

def generate_directory_tree(directory, output_file, file_ids):
    with open(output_file, 'w', encoding='utf-8') as file:
        for root, dirs, files in os.walk(directory):
            level = root.replace(directory, '').count(os.sep)
            indent = ' ' * 4 * level
            file.write(f"{indent}{os.path.basename(root)}/\n")
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                if f != 'directory_tree.txt':  # דילוג על הקובץ directory_tree.txt
                    file_id = file_ids.get(os.path.join(root, f), 'No ID')
                    file.write(f"{subindent}{f} (ID: {file_id})\n")

async def upload_files(directory, progress_var, progress_label, root):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    files = get_files_in_directory(directory)
    total_files = len(files)
    for i, file_path in enumerate(files, start=1):
        await send_file(bot, CHAT_ID, file_path)
        progress = (i / total_files) * 100
        progress_var.set(progress)
        progress_label.config(text=f"Progress: {progress:.2f}%")
        root.update_idletasks()

    tree_file = os.path.join(directory, 'directory_tree.txt')
    generate_directory_tree(directory, tree_file, file_ids)
    await send_file(bot, CHAT_ID, tree_file)

    # מחיקת קובץ עץ התיקיות לאחר השליחה
    os.remove(tree_file)
    print(f"Deleted the directory tree file: {tree_file}")
    progress_label.config(text="Upload complete!")
