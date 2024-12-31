from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils import BotUtils
import random


class Handlers:
    def __init__(self, bot):
        self.bot = bot
        self.games = {}
        self.utils = BotUtils(bot)

    def setup_handlers(self):
        @self.bot.message_handler(commands=["start"])
        def private_chat(message):
            if message.chat.type == "private":
                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton("➕ أضف للبوت للمجموعه", url=f"http://t.me/{self.bot.get_me().username}?startgroup=true"))
                self.utils.safe_reply(message, "اهلا بيك ببوت الأحكام! فكرته بسيطه وما اعتقد تحتاج شرح، استمتع! 🙃", markup)

        @self.bot.message_handler(content_types=["new_chat_members"])
        def on_user_added(message):
            if self.bot.get_me().id in [member.id for member in message.new_chat_members]:
                markup = self.utils.get_welcome_markup()
                self.utils.safe_reply(message, "تم التفعيل التلقائيّ للمجموعةِ بنجاح!", markup)

        @self.bot.message_handler(func=lambda msg: msg.text.lower() == "أحكام")
        def start_game_command(message):
            if not self.utils.is_admin(message):
                self.utils.safe_reply(message, "⚠️ هذا الأمر فقط للأدمنز!")
                return
            user = message.from_user.first_name
            self.start_game(message, user)

        @self.bot.message_handler(func=lambda msg: msg.text.lower() == "أنا")
        def join_game_command(message):
            user = message.from_user.first_name
            self.join_game(message, user)

        @self.bot.message_handler(func=lambda msg: msg.text.lower() == "تم")
        def finish_game_command(message):
            user = message.from_user.first_name
            self.finish_game(message, user)

        @self.bot.message_handler(func=lambda msg: msg.text.lower() == "أنهاء")
        def stop_game_command(message):
            user = message.from_user.first_name
            self.stop_game(message, user)

        @self.bot.message_handler(commands=["help"])
        def help_command(message):
            markup = self.utils.get_welcome_markup()
            self.utils.safe_reply(
                message,
                "🤖 <b>تعليمات اللعبة:</b>\n\n"
                "1️⃣ اكتب <b>'أحكام'</b> لبدء اللعبة.\n"
                "2️⃣ إذا تريد تشارك، اكتب <b>'أنا'</b>.\n"
                "3️⃣ من تخلصون التسجيل، اكتب <b>'تم'</b> لاختيار الحاكم والمحكوم.\n"
                "4️⃣ استمتعوا باللعبة! 🎉",
                markup
            )

        @self.bot.message_handler(content_types=["left_chat_member"])
        def user_left_group(message):
            if message.left_chat_member.id == self.bot.get_me().id:
                if message.chat.id in self.games:
                    del self.games[message.chat.id]
                    print(f"تم حذف بيانات المجموعة {message.chat.id} بعد مغادرة البوت.")

    def start_game(self, message, user):
        if message.chat.id in self.games:
            self.utils.safe_reply(message, "⚠️ اكو لعبة شغالة بالفعل! انتظر لتكمل.")
        else:
            self.games[message.chat.id] = {"owner": user, "players": []}
            self.utils.safe_reply(
                message,
                f"🎮 <b>{user}</b> بدأ لعبة جديدة! \n"
                "📌 إذا تريد تشارك، اكتب كلمة <b>'أنا'</b>.\n"
                "✏️ من تخلصون التسجيل، اكتب كلمة <b>'تم'</b> للبدء."
            )

    def join_game(self, message, user):
        if message.chat.id in self.games:
            if user not in self.games[message.chat.id]["players"]:
                self.games[message.chat.id]["players"].append(user)
                self.utils.safe_reply(message, f"🎉 <b>{user}</b> شارك باللعبة!")
            else:
                self.utils.safe_reply(message, "✅ انت مسجل من قبل!")
        else:
            self.utils.safe_reply(message, "⚠️ ماكو لعبة شغالة هسه!")

    def finish_game(self, message, user):
        if message.chat.id in self.games and self.games[message.chat.id]["owner"] == user:
            players = self.games[message.chat.id]["players"]
            if len(players) < 2:
                self.utils.safe_reply(message, "⚠️ لازم اكو على الأقل لاعبين اثنين!")
            else:
                roles = random.sample(players, 2)
                self.utils.safe_reply(
                    message,
                    f"🎉 تم اختيار اللاعبين:\n"
                    f"👑 <b>الحاكم:</b> {roles[0]}\n"
                    f"🤔 <b>المحكوم:</b> {roles[1]}"
                )
                del self.games[message.chat.id]
        else:
            self.utils.safe_reply(message, "⚠️ بس مالك اللعبة يقدر يكتب 'تم'.")

    def stop_game(self, message, user):
        if message.chat.id in self.games:
            del self.games[message.chat.id]
            self.utils.safe_reply(message, "❌ تم إيقاف اللعبة الحالية!")