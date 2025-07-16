from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext

# دستور /start که دکمه‌ها را ارسال می‌کند
async def start(update: Update, context: CallbackContext):
    if update.effective_user.id != ADMIN_ID:
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"کاربر جدید وارد ربات شد. شناسه کاربری: {update.effective_user.id}")

    # ایجاد کیبورد برای نمایش در چت
    keyboard = [
        [KeyboardButton("تنظیمات")],
        [KeyboardButton("راهنما")],
        [KeyboardButton("پیام به گروه")],
        [KeyboardButton("لینک ناشناس من")],
        [KeyboardButton("به مخاطب خاصم وصلم کن")]
    ]
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text("سلام! لطفاً یکی از گزینه‌ها را انتخاب کنید:", reply_markup=reply_markup)

# هندلر برای دکمه‌ها
async def button(update: Update, context: CallbackContext):
    text = update.message.text

    if text == 'تنظیمات':
        await update.message.reply_text("این بخش تنظیمات است.")
    
    elif text == 'راهنما':
        await update.message.reply_text("برای استفاده از ربات از دکمه‌ها استفاده کنید.")
    
    elif text == 'پیام به گروه':
        await update.message.reply_text("پیام به گروه ارسال شد.")
    
    elif text == 'لینک ناشناس من':
        user_id = update.effective_user.id
        anonymous_link = f"https://t.me/{context.bot.username}?start={user_id}"
        await update.message.reply_text(f"لینک ناشناس شما: {anonymous_link}")
    
    elif text == 'به مخاطب خاصم وصلم کن':
        await update.message.reply_text("شما به مخاطب خاص وصل شدید.")
