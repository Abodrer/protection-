from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


class BotUtils:
    def __init__(self, bot):
        self.bot = bot

    def safe_reply(self, message, text, markup=None):
        try:
            self.bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="HTML")
        except Exception as e:
            print(f"Error in sending message: {e}")

    def is_admin(self, message):
        try:
            admins = self.bot.get_chat_administrators(message.chat.id)
            admin_ids = [admin.user.id for admin in admins]
            return message.from_user.id in admin_ids
        except Exception as e:
            print(f"Error checking admin: {e}")
            return False

    def get_welcome_markup(self):
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("🔔 قناة التحديثات", url="https://t.me/hakomi4"),
            InlineKeyboardButton("👨‍💻 المطور الأساسي", url="https://t.me/oliceer"),
            InlineKeyboardButton("👨‍💻 المطور الثانوي", url="https://t.me/sx_foxr")
        )
        return markup