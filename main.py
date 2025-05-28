import os
import random
import json
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

# === Kitoblar JSON bazasidan o‘qish ===
def get_books(language):
    try:
        with open("kitoblar.json", "r", encoding="utf-8") as f:
            books = json.load(f)

        if language == "uz":
            filtered = [b for b in books if b["til"] == "O'zbek"]
        elif language == "ru":
            filtered = [b for b in books if b["til"] == "Rus"]
        else:
            filtered = books

        if not filtered:
            return "Kitoblar topilmadi."

        return "\n".join([
            f"📘 {b['nomi']} ({b['muallif']}, {b['yil']})" for b in filtered
        ])

    except Exception as e:
        return f"Xatolik yuz berdi: {e}"

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

# === Til tanlash ===
@bot.message_handler(func=lambda message: message.text == "🇺🇿 O‘zbekcha")
def show_menu_uz(message):
    bot.send_message(message.chat.id, "Siz falsafa botidasiz. Quyidagilardan birini tanlang:", reply_markup=main_menu_uz())

@bot.message_handler(func=lambda message: message.text == "🇷🇺 Русский")
def show_menu_ru(message):
    bot.send_message(message.chat.id, "Вы находитесь в философском боте. Выберите действие:", reply_markup=main_menu_ru())

# === O‘zbekcha menyu ===
@bot.message_handler(func=lambda msg: msg.text in [
    "ℹ️ Falsafa haqida", "📚 Adabiyotlar", "🎓 Falsafa ta’lim yo‘nalishlari", "💰 Iqtiboslar", "🌐 Jahon Falsafasi", "📞 Aloqa"
])
def handle_uzbek_menu(msg):
    if msg.text == "ℹ️ Falsafa haqida":
        bot.send_message(msg.chat.id, "Falsafa bu – inson, hayot va borliq haqidagi chuqur tafakkurdir.")
    elif msg.text == "📚 Adabiyotlar":
        bot.send_message(msg.chat.id, get_books("uz"))
    elif msg.text == "🎓 Falsafa ta’lim yo‘nalishlari":
        uz_directions = (
            "🎓 *Falsafa ta’lim yo‘nalishlari:*\n\n"
            "📌 *Metafizika* – Borliqning tabiati, narsalar, voqelik va ularning xususiyatlarini o‘rganadi. Masalan, “Dunyo nima?”, “Xudo bormi?” kabi savollar. Arastu, Platon, Kant.\n\n"
            "📌 *Epistemologiya* – Bilimning mohiyati, manbalari va chegaralari. “Biz nimani bilamiz?”, “Bilim qanchalik ishonchli?” kabi savollar. Dekart, Lokk.\n\n"
            "📌 *Axloq (Etika)* – To‘g‘ri va noto‘g‘ri xatti-harakatlar. Utilitarizm (Bentham, Mill), Deontologiya (Kant).\n\n"
            "📌 *Ekzistensializm* – Inson mavjudligi, erkinlik va ma’no. Sartr, Nitsshe.\n\n"
            "📌 *Analitik falsafa* – Mantiq, til va aniq fikrlash. Vitgenshtayn, Rassel.\n\n"
            "📌 *Kontinental falsafa* – Tajriba, madaniyat va tarix. Husserl, Xaydegger, Fuko, Derrida.\n\n"
            "📌 *Sharq falsafasi* – Konfutsiy, Taoizm, Buddizm, Lao-tszi, Buddha.\n\n"
            "📌 *Siyosiy falsafa* – Jamiyat, hokimiyat, adolat. Lokk, Gobbs, Marks."
        )
        bot.send_message(msg.chat.id, uz_directions, parse_mode="Markdown")
    elif msg.text == "💰 Iqtiboslar":
        bot.send_message(msg.chat.id, f"📖 {random.choice(uz_iqtiboslar)}")
    elif msg.text == "🌐 Jahon Falsafasi":
        bot.send_message(msg.chat.id, "Jahon falsafasi: Sharq, G‘arb, Hind, Xitoy falsafalari va boshqalar.")
    elif msg.text == "📞 Aloqa":
        bot.send_message(msg.chat.id, "Bog‘lanish: @falsafa_admin | Email: falsafa@bot.uz")

# === Ruscha menyu ===
@bot.message_handler(func=lambda msg: msg.text in [
    "ℹ️ О философии", "📚 Литература", "🎓 Направления философии", "💰 Цитаты", "🌐 Мировая философия", "📞 Контакты"
])
def handle_russian_menu(msg):
    if msg.text == "ℹ️ О философии":
        bot.send_message(msg.chat.id, "Философия — это глубокое размышление о жизни, бытии и человеке.")
    elif msg.text == "📚 Литература":
        bot.send_message(msg.chat.id, get_books("ru"))
    elif msg.text == "🎓 Направления философии":
        bot.send_message(msg.chat.id, "Направления: Античная, Исламская, Европейская, Аналитическая философия и этика.")
    elif msg.text == "💰 Цитаты":
        bot.send_message(msg.chat.id, f"📖 {random.choice(ru_iqtiboslar)}")
    elif msg.text == "🌐 Мировая философия":
        bot.send_message(msg.chat.id, "Мировая философия охватывает Восток, Запад, Индию, Китай и другие культуры.")
    elif msg.text == "📞 Контакты":
        bot.send_message(msg.chat.id, "Связь: @falsafa_admin | Email: philosophy@bot.uz")

# === Botni ishga tushirish ===
if __name__ == "__main__":
    print("Falsafa bot ishga tushdi...")
    bot.infinity_polling()
