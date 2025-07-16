from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.ext import CallbackContext

# توکن ربات تلگرام شما
TOKEN = "YOUR_BOT_TOKEN"

# فقط شما می‌توانید آیدی طرف مقابل رو ببینید
YOUR_ID = 123456789  # این رو با آیدی خودتون جایگزین کنید

# ذخیره اطلاعات چت‌ها
chats = {}

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "سلام! این ربات برای چت ناشناس است. با ارسال پیام، شروع به چت کنید."
    )

async def forward_message(update: Update, context: CallbackContext) -> None:
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
            await context.bot.send_message(other_chat_id, f"پیام از {chat_id}: {text}")
        
        # ذخیره چت‌های ناشناس
        if chat_id not in chats:
            chats[chat_id] = {"active": False}

        # ارسال پاسخ که چت به طور ناشناس شروع شده
        await update.message.reply_text("پیام شما به طرف دیگر ارسال شد.")
    else:
        await update.message.reply_text("شما نمی‌توانید پیام خودتان را ارسال کنید.")

async def show_user_id(update: Update, context: CallbackContext) -> None:
    if update.message.chat.id == YOUR_ID:
        for user_id, chat in chats.items():
            if chat["active"]:
                await update.message.reply_text(f"آیدی طرف مقابل: {user_id}")
    else:
        await update.message.reply_text("شما نمی‌توانید آیدی طرف مقابل را ببینید.")

async def main() -> None:
    # به روزرسانی ربات
    application = Application.builder().token(TOKEN).build()

    # دستورات ربات
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("myid", show_user_id))  # فقط خودتون می‌تونید اینو استفاده کنید
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_message))

    # شروع ربات
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())

