import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext

TOKEN = "7835116613:AAEuZ5mwjpNrozXR75Jjjy4wNhEiwJcprDA"
ADMIN_ID = 651775664  # ایدی ادمین

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext):
    if update.effective_user.id != ADMIN_ID:
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"کاربر جدید وارد ربات شد. شناسه کاربری: {update.effective_user.id}")
    
    keyboard = [
        [InlineKeyboardButton("تنظیمات", callback_data='settings')],
        [InlineKeyboardButton("راهنما", callback_data='help')],
        [InlineKeyboardButton("پیام به گروه", callback_data='send_to_group')],
        [InlineKeyboardButton("لینک ناشناس من", callback_data='anonymous_link')],
        [InlineKeyboardButton("به مخاطب خاصم وصلم کن", callback_data='special_contact')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text("سلام! لطفاً یکی از گزینه‌ها را انتخاب کنید:", reply_markup=reply_markup)

async def button(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == 'settings':
        await query.edit_message_text(text="این بخش تنظیمات است.")
    
    elif query.data == 'help':
        await query.edit_message_text(text="برای استفاده از ربات از دکمه‌ها استفاده کنید.")
    
    elif query.data == 'send_to_group':
        await query.edit_message_text(text="پیام به گروه ارسال شد.")
    
    elif query.data == 'anonymous_link':
        user_id = update.effective_user.id
        anonymous_link = f"https://t.me/{context.bot.username}?start={user_id}"
        await query.edit_message_text(text=f"لینک ناشناس شما: {anonymous_link}")
    
    elif query.data == 'special_contact':
        await query.edit_message_text(text="شما به مخاطب خاص وصل شدید.")

async def get_users(update: Update, context: CallbackContext):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("شما دسترسی ندارید!")
        return
    await update.message.reply_text("کاربران جدید از لینک ناشناس وارد شده‌اند.")

async def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("get_users", get_users))
    application.add_handler(CallbackQueryHandler(button))
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# توکن ربات خود را اینجا قرار دهید
TOKEN = 'YOUR_BOT_TOKEN'

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('سلام! به ربات خوش آمدید.')

async def main():
    # ایجاد اپلیکیشن با توکن ربات
    application = Application.builder().token(TOKEN).build()

    # اضافه کردن هندلر برای دستور /start
    application.add_handler(CommandHandler("start", start))

    # شروع به کار ربات با polling
    await application.run_polling()

if __name__ == "__main__":
    # اجرای main با استفاده از async
    import asyncio
    asyncio.run(main())
