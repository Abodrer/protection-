from telebot import TeleBot
from handlers import Handlers
from config import TOKEN

bot = TeleBot(TOKEN)

# إعداد المعالجات
handlers = Handlers(bot)
handlers.setup_handlers()

# تشغيل البوت
if __name__ == "__main__":
    print("🚀 البوت قيد التشغيل...")
    bot.polling(non_stop=True)