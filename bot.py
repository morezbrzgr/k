import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, filters
from collections import defaultdict

# تنظیمات اولیه
TOKEN = "7835116613:AAEuZ5mwjpNrozXR75Jjjy4wNhEiwJcprDA"
ADMIN_ID = 651775664  # ایدی ادمین

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# صندوق ورودی برای هر کاربر
user_inboxes = defaultdict(list)  # هر کاربر صندوق ورودی جداگانه دارد

# ذخیره لینک‌های ناشناس
user_links = {}

# دستور /start که دکمه‌ها را ارسال می‌کند
async def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"کاربر جدید وارد ربات شد. شناسه کاربری: {user_id}")
    
    # لینک ناشناس منحصر به فرد برای هر کاربر
    if user_id not in user_links:
        anonymous_link = f"https://t.me/{context.bot.username}?start={user_id}"
        user_links[user_id] = anonymous_link
    
    keyboard = [
        [InlineKeyboardButton("📩 صندوق ورودی", callback_data='inbox')],
        [InlineKeyboardButton("🔗 لینک ناشناس من", callback_data='anonymous_link')],
        [InlineKeyboardButton("⚙️ تنظیمات", callback_data='settings')],
        [InlineKeyboardButton("📚 راهنما", callback_data='help')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text("سلام! لطفاً یکی از گزینه‌ها را انتخاب کنید:", reply_markup=reply_markup)

# ذخیره پیام‌ها در صندوق ورودی هر کاربر
async def save_message_to_inbox(user_id, message, from_user, context: CallbackContext):
    user_inboxes[user_id].append({"message": message, "from_user": from_user})  # ذخیره پیام و اطلاعات فرستنده

    # ارسال پیام جدید به ادمین
    if ADMIN_ID != user_id:  # فقط اگر خود ادمین نیست
        user_name = from_user.username if from_user.username else "بدون یوزرنیم"
        user_full_name = from_user.full_name if from_user.full_name else "نام کاربری"
        user_id = from_user.id

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"پیام جدید از {user_full_name} (@{user_name}, ID: {user_id}):\n{message}"
        )

# نمایش صندوق ورودی برای هر کاربر
async def inbox_handler(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    query = update.callback_query
    await query.answer()

    if user_id not in user_inboxes or not user_inboxes[user_id]:
        await query.edit_message_text(text="صندوق ورودی شما خالی است!")
    else:
        messages_text = "📩 صندوق ورودی شما:\n\n"
        for idx, message_info in enumerate(user_inboxes[user_id]):
            user_full_name = message_info['from_user'].full_name if message_info['from_user'].full_name else "بدون نام"
            user_name = message_info['from_user'].username if message_info['from_user'].username else "بدون یوزرنیم"
            user_id = message_info['from_user'].id

            messages_text += f"{idx+1}. پیام: {message_info['message']}\n"
            messages_text += f"فرستنده: {user_full_name} (@{user_name}, ID: {user_id})\n"

        await query.edit_message_text(text=messages_text)

# نمایش لینک ناشناس
async def anonymous_link_handler(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    anonymous_link = user_links.get(user_id)
    await update.message.reply_text(f"لینک ناشناس شما: {anonymous_link}")

# نمایش پیام‌ها با دکمه‌های پاسخ و بلاک
async def button(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    # بررسی دکمه‌های فشرده‌شده
    if query.data == 'inbox':
        await inbox_handler(update, context)
    elif query.data == 'settings':
        await query.edit_message_text(text="این بخش تنظیمات است.")
    elif query.data == 'help':
        await query.edit_message_text(text="برای استفاده از ربات از دکمه‌ها استفاده کنید.")
    elif query.data == 'anonymous_link':
        await anonymous_link_handler(update, context)

# دستور برای دریافت پیام ناشناس و ذخیره آن
async def receive_anonymous_message(update: Update, context: CallbackContext):
    message = update.message.text
    user_id = update.effective_user.id

    # ذخیره پیام‌ها در صندوق ورودی کاربر
    await save_message_to_inbox(user_id, message, update.effective_user, context)
    await update.message.reply_text("پیام شما با موفقیت ثبت شد و در صندوق ورودی نمایش داده می‌شود!")

# دستور برای مشاهده تنظیمات
async def settings(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id == ADMIN_ID:
        keyboard = [
            [InlineKeyboardButton("🔓 آزادسازی بلاک‌ها", callback_data='unblock_users')],
            [InlineKeyboardButton("🔄 تغییر اسم کاربری", callback_data='change_name')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("تنظیمات:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("شما دسترسی به تنظیمات ندارید.")

# راهنما برای نمایش به کاربر
async def help_handler(update: Update, context: CallbackContext):
    help_text = """
    🔎 **راهنما**
    
    من اینجام که کمکت کنم! 🤓

    🔧 **برای دسترسی به تنظیمات، کافیه دستور /settings رو لمس کنی.** 

    🔹 برای ارسال پیام ناشناس، می‌تونی از لینک ناشناس خودت استفاده کنی. 

    ✨ **برای اینکه بتونی به مخاطب خاصت بطور ناشناس وصل بشی، یکی از راه‌های زیر رو انجام بده:**
    
    1️⃣ **راه اول**: آی‌دی تلگرام شخص (Username@) رو وارد کن تا به اون وصل بشی.
    
    2️⃣ **راه دوم**: یه پیام از شخص مورد نظر رو فوروارد کن تا بررسی کنیم که آیا عضو ربات هست یا نه. (لازمه که طرف دسترسی به فورواردها داشته باشه)
    
    3️⃣ **راه سوم**: شماره تلفن شخص مورد نظر رو ارسال کن تا بررسی کنیم که آیا عضو ربات هست یا نه.
    
    4️⃣ **راه چهارم**: آیدی عددی (ID number) اون شخص رو وارد کن تا بهش وصل بشی.

    📝 **توضیح مهم**: برای روش دوم و سوم، مخاطب باید اجازه بده که ربات‌ها دسترسی به فوروارد پیام‌ها و کانتکت‌هایش داشته باشند.
    
    ⚙️ برای استفاده از این دستورها، کافیه از دکمه‌های شیشه‌ای که در پایین صفحه نشون داده می‌شوند استفاده کنی👇🏻
    """
    await update.message.reply_text(help_text)

# تابع اصلی که اپلیکیشن را راه‌اندازی می‌کند
async def main():
    application = Application.builder().token(TOKEN).build()

    # اضافه کردن هندلرها
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("settings", settings))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_anonymous_message))
    application.add_handler(CommandHandler("help", help_handler))

    # شروع اپلیکیشن
    await application.run_polling()

# فراخوانی تابع اصلی
if __name__ == "__main__":
    import asyncio
    from telegram.ext import Application
    
    async def main():
        application = Application.builder().token(TOKEN).build()

        # اضافه کردن هندلرها
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("settings", settings))
        application.add_handler(CallbackQueryHandler(button))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_anonymous_message))
        application.add_handler(CommandHandler("help", help_handler))

        # شروع اپلیکیشن
        await application.run_polling()

    asyncio.get_event_loop().run_until_complete(main())  # استفاده از event loop موجود
