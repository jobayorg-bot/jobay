import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os

# لاگ برای بررسی
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# متغیرهای محیطی
BOT_TOKEN = os.getenv("7691709850:AAHBKDMIegmEg8ybA0jVFvbGzCxZnHDmA3M")
ADMIN_ID = int(os.getenv("5134131639"))  # آیدی عددی خودت

# دیکشنری ذخیره پیام‌ها
user_messages = {}

# شروع
def start(update: Update, context: CallbackContext):
    update.message.reply_text("سلام! پیامت چیه  :)")

# هندل پیام‌ها
def handle_message(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    text = update.message.text
    user_info = update.message.from_user

    # ذخیره پیام
    user_messages[user_id] = {
        "username": user_info.username,
        "first_name": user_info.first_name,
    }

    # ارسال به ادمین
    message_to_admin = (
        f"📩 پیام جدید:\n"
        f"👤 نام: {user_info.first_name}\n"
        f"🆔 آیدی عددی: {user_id}\n"
        f"🔗 یوزرنیم: @{user_info.username or 'ندارد'}\n"
        f"📝 پیام: {text}\n\n"
        f"برای پاسخ بنویس:\n/reply {user_id} پیام_شما"
    )
    context.bot.send_message(chat_id=ADMIN_ID, text=message_to_admin)

# پاسخ دادن به کاربر
def reply_command(update: Update, context: CallbackContext):
    args = context.args
    if len(args) < 2:
        update.message.reply_text("فرمت درست: /reply آیدی پیام")
        return

    try:
        user_id = int(args[0])
        reply_text = " ".join(args[1:])
        context.bot.send_message(chat_id=user_id, text=f"👤 پاسخ ادمین:\n{reply_text}")
        update.message.reply_text("✅ ارسال شد.")
    except Exception as e:
        update.message.reply_text(f"خطا در ارسال: {e}")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("reply", reply_command))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if name == "__main__":
    main()