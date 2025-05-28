import os
import random
import telebot
from telebot.types import ReplyKeyboardMarkup
from dotenv import load_dotenv

# .env fayldan tokenni yuklash
load_dotenv()
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))

# === Iqtiboslar ===
uz_iqtiboslar = [
    "Tekshirilmagan hayot yashashga arzimaydi. – Sokrat",
    "Men o‘ylayman, demak men boraman. – Reni Dekart",
    "Bo‘lish – bu sezilishdir. – Jorj Berkli",
    "Baxt – aql emas, tasavvur idealidir. – Immanuil Kant"
]

ru_iqtiboslar = [
    "Неисследованная жизнь не стоит того, чтобы её жить. – Сократ",
    "Я мыслю, следовательно, я существую. – Рене Декарт",
    "Быть — значит быть воспринимаемым. – Джордж Беркли",
    "Счастье — это идеал воображения, а не разума. – Иммануил Кант"
]

# === Menyular ===

def language_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🇺🇿 O‘zbekcha", "🇷🇺 Русский")
    return markup

def main_menu_uz():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("ℹ️ Falsafa haqida", "📚 Adabiyotlar")
    markup.row("🎓 Falsafa ta’lim yo‘nalishlari", "💰 Iqtiboslar")
    markup.row("🌐 Jahon Falsafasi", "📞 Aloqa")
    return markup

def main_menu_ru():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("ℹ️ О философии", "📚 Литература")
    markup.row("🎓 Направления философии", "💰 Цитаты")
    markup.row("🌐 Мировая философия", "📞 Контакты")
    return markup

# === /start komandasi ===

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Здравствуйте / Assalomu alaykum! Пожалуйста, выберите язык / Tilni tanlang:",
        reply_markup=language_menu()
    )

# === Til tanlanganda ===

@bot.message_handler(func=lambda message: message.text == "🇺🇿 O‘zbekcha")
def show_menu_uz(message):
    bot.send_message(message.chat.id, "Siz falsafa botidasiz. Quyidagilardan birini tanlang:", reply_markup=main_menu_uz())

@bot.message_handler(func=lambda message: message.text == "🇷🇺 Русский")
def show_menu_ru(message):
    bot.send_message(message.chat.id, "Вы находитесь в философском боте. Выберите действие:", reply_markup=main_menu_ru())

# === O‘zbekcha menyu tugmalari ===

@bot.message_handler(func=lambda msg: msg.text in [
    "ℹ️ Falsafa haqida", "📚 Adabiyotlar", "🎓 Falsafa ta’lim yo‘nalishlari", "💰 Iqtiboslar", "🌐 Jahon Falsafasi", "📞 Aloqa"
])
def handle_uzbek_menu(msg):
    if msg.text == "ℹ️ Falsafa haqida":
        bot.send_message(msg.chat.id, "Falsafa bu – inson, hayot va borliq haqidagi chuqur tafakkurdir.")
    elif msg.text == "📚 Adabiyotlar":
        bot.send_message(msg.chat.id, "Falsafa uchun tavsiya etilgan asarlar:\n- Aristotel: Metafizika\n- Ibn Sino: Shifo\n- Kant: Sof aql tanqidi")
    elif msg.text == "🎓 Falsafa ta’lim yo‘nalishlari":
        bot.send_message(msg.chat.id, "Yo‘nalishlar: Antik, Islom, Yevropa, Analitik, Etika va boshqalar.")
    elif msg.text == "💰 Iqtiboslar":
        bot.send_message(msg.chat.id, f"📖 {random.choice(uz_iqtiboslar)}")
    elif msg.text == "🌐 Jahon Falsafasi":
        bot.send_message(msg.chat.id, "Jahon falsafasi: Sharq, G‘arb, Hind, Xitoy falsafalari va boshqalar.")
    elif msg.text == "📞 Aloqa":
        bot.send_message(msg.chat.id, "Bog‘lanish: @falsafa_admin | Email: falsafa@bot.uz")

# === Русский язык кнопки ===

@bot.message_handler(func=lambda msg: msg.text in [
    "ℹ️ О философии", "📚 Литература", "🎓 Направления философии", "💰 Цитаты", "🌐 Мировая философия", "📞 Контакты"
])
def handle_russian_menu(msg):
    if msg.text == "ℹ️ О философии":
        bot.send_message(msg.chat.id, "Философия — это глубокое размышление о жизни, бытии и человеке.")
    elif msg.text == "📚 Литература":
        bot.send_message(msg.chat.id, "Рекомендуемые книги:\n- Аристотель: Метафизика\n- Авиценна: Шифо\n- Кант: Критика чистого разума")
    elif msg.text == "🎓 Направления философии":
        bot.send_message(msg.chat.id, "Направления: Античная, Исламская, Европейская, Аналитическая философия и этика.")
    elif msg.text == "💰 Цитаты":
        bot.send_message(msg.chat.id, f"📖 {random.choice(ru_iqtiboslar)}")
    elif msg.text == "🌐 Мировая философия":
        bot.send_message(msg.chat.id, "Мировая философия охватывает Восток, Запад, Индию, Китай и другие культуры.")
    elif msg.text == "📞 Контакты":
        bot.send_message(msg.chat.id, "Связь: @falsafa_admin | Email: philosophy@bot.uz")

# === Ishga tushurish ===

if __name__ == "__main__":
    print("Falsafa bot ishga tushdi...")
    bot.infinity_polling()
