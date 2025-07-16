from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext import CallbackContext

# 7835116613:AAEuZ5mwjpNrozXR75Jjjy4wNhEiwJcprDA
TOKEN = "YOUR_BOT_TOKEN"

# فقط شما می‌توانید آیدی طرف مقابل رو ببینید
YOUR_ID = 123456789  # این رو با آیدی خودتون جایگزین کنید

# ذخیره اطلاعات چت‌ها
chats = {}

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "سلام! این ربات برای چت ناشناس است. با ارسال پیام، شروع به چت کنید."
    )

def forward_message(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat.id
    text = update.message.text

    # اگر پیام از طرف خود شما نیست، آن رو به کاربر دیگه ارسال کن
    if chat_id != YOUR_ID:
        # پیدا کردن چت ناشناس بعدی
        other_chat_id = None
        for user_id, chat in chats.items():
            if user_id != chat_id and chat["active"] == False:
                other_chat_id = user_id
                break
        
        # اگر چت ناشناس پیدا شد، پیام رو ارسال کن
        if other_chat_id:
            chats[other_chat_id]["active"] = True
            chats[chat_id]["active"] = True
            context.bot.send_message(other_chat_id, f"پیام از {chat_id}: {text}")
        
        # ذخیره چت‌های ناشناس
        if chat_id not in chats:
            chats[chat_id] = {"active": False}

        # ارسال پاسخ که چت به طور ناشناس شروع شده
        update.message.reply_text("پیام شما به طرف دیگر ارسال شد.")
    else:
        update.message.reply_text("شما نمی‌توانید پیام خودتان را ارسال کنید.")

def show_user_id(update: Update, context: CallbackContext) -> None:
    if update.message.chat.id == YOUR_ID:
        for user_id, chat in chats.items():
            if chat["active"]:
                update.message.reply_text(f"آیدی طرف مقابل: {user_id}")
    else:
        update.message.reply_text("شما نمی‌توانید آیدی طرف مقابل را ببینید.")

def main() -> None:
    # به روزرسانی ربات
    updater = Updater(TOKEN)

    # دستورات ربات
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("myid", show_user_id))  # فقط خودتون می‌تونید اینو استفاده کنید
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, forward_message))

    # شروع ربات
    updater.start_polling()

    # ربات رو در حالت دائمی راه‌اندازی می‌کنیم
    updater.idle()

if __name__ == '__main__':
    main()
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext import filters

def start(update: Update, context):
    update.message.reply_text("سلام! من ربات چت ناشناس هستم.")

def handle_message(update: Update, context):
    # اینجا کد خودت رو برای ارسال پیام یا پردازش پیام‌ها بنویس
    update.message.reply_text("پیامی دریافت شد!")

def main():
    updater = Updater("YOUR_API_KEY", use_context=True)
    dp = updater.dispatcher

    # اضافه کردن CommandHandler
    dp.add_handler(CommandHandler("start", start))
    
    # اضافه کردن MessageHandler
    dp.add_handler(MessageHandler(filters.TEXT, handle_message))  # تغییرات جدید فیلترها

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
