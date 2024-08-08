from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext

TELEGRAM_BOT_TOKEN = ''

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('שלום! הגיבו על הקובץ עם ההודעה "." כדי להעלות את עץ התיקיות.')

async def handle_message(update: Update, context: CallbackContext):
    if update.message.reply_to_message and update.message.text == '.':
        document = update.message.reply_to_message.document
        if document and document.file_name == 'directory_tree.txt':
            file = await context.bot.get_file(document.file_id)
            await file.download_to_drive('directory_tree.txt')
            context.user_data['directory_tree_file_id'] = document.file_id
            await update.message.reply_text('הקובץ directory_tree.txt התקבל ונשמר. השתמשו בפקודה /show כדי להציג את עץ התיקיות.')
        else:
            await update.message.reply_text('העלו קובץ בשם directory_tree.txt בלבד.')

async def show(update: Update, context: CallbackContext):
    if 'directory_tree_file_id' not in context.user_data:
        await update.message.reply_text('יש להגיב על הקובץ עם ההודעה "." תחילה.')
        return

    tree_structure, file_ids = parse_directory_tree('directory_tree.txt')
    if not tree_structure:
        await update.message.reply_text('הקובץ directory_tree.txt לא תקין או ריק.')
        return

    context.user_data['tree_structure'] = tree_structure
    context.user_data['file_ids'] = file_ids
    context.user_data['current_path'] = []
    await show_directory(update, context, update.message, new_message=True)

def parse_directory_tree(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        return None, None

    tree_structure = {}
    file_ids = {}
    current_path = []

    for line in lines:
        level = line.count(' ' * 4)
        name = line.strip()
        if name.endswith('/'):
            while len(current_path) > level:
                current_path.pop()
            current_path.append(name[:-1])
            add_to_tree(tree_structure, current_path, {})
        else:
            while len(current_path) > level:
                current_path.pop()
            file_name, file_id = parse_file_entry(name)
            add_to_tree(tree_structure, current_path, file_name)
            file_ids['/'.join(current_path + [file_name])] = file_id

    return tree_structure, file_ids

def parse_file_entry(entry):
    if '(ID: ' in entry:
        name, file_id = entry.rsplit(' (ID: ', 1)
        file_id = file_id.rstrip(')')
        return name, file_id
    return entry, None

def add_to_tree(tree, path, item):
    for part in path:
        tree = tree.setdefault(part, {})
    if isinstance(item, str):
        tree[item] = None

async def show_directory(update: Update, context: CallbackContext, message, new_message=False):
    tree_structure = context.user_data['tree_structure']
    current_path = context.user_data['current_path']
    directory = get_directory(tree_structure, current_path)

    buttons = []
    for key, value in directory.items():
        if isinstance(value, dict):
            buttons.append([InlineKeyboardButton(f"{key}/", callback_data=f"enter:{key}")])
        else:
            buttons.append([InlineKeyboardButton(key, callback_data=f"file:{key}")])

    if current_path:
        buttons.append([InlineKeyboardButton("חזור", callback_data="back")])

    if new_message:
        await message.reply_text('בחר קובץ או תיקייה:', reply_markup=InlineKeyboardMarkup(buttons))
    else:
        await message.edit_text('בחר קובץ או תיקייה:', reply_markup=InlineKeyboardMarkup(buttons))

def get_directory(tree, path):
    directory = tree
    for part in path:
        directory = directory[part]
    return directory

async def button(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    data = query.data.split(':')
    action = data[0]

    if action == 'enter':
        directory = data[1]
        context.user_data['current_path'].append(directory)
        await show_directory(update, context, query.message)

    elif action == 'file':
        file_name = data[1]
        current_path = context.user_data['current_path']
        file_path = '/'.join(current_path + [file_name])
        await send_file(update, context, file_path)

    elif action == 'back':
        context.user_data['current_path'].pop()
        await show_directory(update, context, query.message)

async def send_file(update: Update, context: CallbackContext, file_path):
    file_id = context.user_data['file_ids'].get(file_path)
    if file_id:
        # Determine if the file is a photo
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')):
            await update.callback_query.message.reply_photo(photo=file_id)
        else:
            await update.callback_query.message.reply_document(document=file_id)
    else:
        await update.callback_query.message.reply_text(f'לא נמצא ID עבור הקובץ {file_path}.')

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('show', show))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()

if __name__ == '__main__':
    main()
