import os
import telebot
from telebot.types import ReplyKeyboardMarkup
from flask import Flask
import threading
app = Flask(__name__)
@app.route('/')
def home():
   return "Bot is alive! 🍆" 
TOKEN = os.environ.get("TOKEN")
CHANNEL = "@ashermiz26"
bot = telebot.TeleBot(TOKEN)

PRODUCTS = {
    "🏠 לבית": {
        "🏠 הכל לבית": ["🏠 מוצר לבית\nhttps://temu.to/k/ellwn0to19t", "🏠 מוצר לבית 2\https://temu.to/k/erk5bu0qt22"],
    },
    "⚡ גאדג'טים": {
        "🎧 אוזניות": ["אין מוצרים עדיין - שלח לי קישור"],
        "📱 אביזרי פלאפון": ["אין מוצרים עדיין - שלח לי קישור"],
        "🔌 מטענים": ["אין מוצרים עדיין - שלח לי קישור"],
        "⚡ שאר גאדג'טים": ["⚡ גאדג'ט 1\nhttps://temu.to/k/e7y9tgcqb20", "⚡ גאדג'ט 2\nhttps://share.temu.com/vrHGir5OkFB", "⚡ גאדג'ט 3\nhttps://temu.to/k/e8n6khzwjxc", "⚡ גאדג'ט 4\nhttps://temu.to/k/ehq6vha7qg1", "⚡ גאדג'ט חדש\nhttps://temu.to/k/e108e8m7dwg"],
    },
    "🎮 משחקים": {
        "🧩 פאזלים": ["אין מוצרים עדיין - שלח לי קישור"],
        "🚗 מכוניות": ["🎮 משחק\nhttps://temu.to/k/eg5itx61e06"],
    },
    "👟 נעליים": {
        "👨 נעלי גברים": ["אין מוצרים עדיין - שלח לי קישור"],
        "👩 נעלי נשים": ["אין מוצרים עדיין - שלח לי קישור"],
        "👦 נעלי ילדים": ["אין מוצרים עדיין - שלח לי קישור"],
        "👧 נעלי ילדות": ["אין מוצרים עדיין - שלח לי קישור"],
        "🩴 נעלי בית": {
            "👨 גברים": ["🩴 נעלי בית גברים\nhttps://temu.to/m/pk6b5qvstmr"],
            "👩 נשים": ["אין מוצרים עדיין - שלח לי קישור"],
            "👦 ילדים": ["אין מוצרים עדיין - שלח לי קישור"],
            "👧 ילדות": ["אין מוצרים עדיין - שלח לי קישור"],
        },
    },
    "👕 ביגוד": {
        "👨 גברים": {
            "👔 ביגוד": ["https://temu.to/k/e89xdhq53tg","https://share.temu.com/KXb8s0QeMDB","https://temu.to/k/eif8gvtiuo8"],
            "🩲 הלבשה תחתונה": ["אין מוצרים עדיין - שלח לי קישור"],
            "🌙 פיג'מות": ["אין מוצרים עדיין - שלח לי קישור"],
        },
        "👩 נשים": {
            "👗 ביגוד": ["אין מוצרים עדיין - שלח לי קישור"],
            "🩲 הלבשה תחתונה": ["אין מוצרים עדיין - שלח לי קישור"],
            "🌙 פיג'מות": ["אין מוצרים עדיין - שלח לי קישור"],
        },
        "👦 ילדים": {
            "👕 ביגוד": ["אין מוצרים עדיין - שלח לי קישור"],
            "🩲 הלבשה תחתונה": ["אין מוצרים עדיין - שלח לי קישור"],
            "🌙 פיג'מות": ["אין מוצרים עדיין - שלח לי קישור"],
        },
        "👧 ילדות": {
            "👗 ביגוד": ["אין מוצרים עדיין - שלח לי קישור"],
            "🩲 הלבשה תחתונה": ["אין מוצרים עדיין - שלח לי קישור"],
            "🌙 פיג'מות": ["אין מוצרים עדיין - שלח לי קישור"],
        },
    },
    "🚲 אביזרי אופניים": {
        "🪖 קסדה": ["🪖 קסדה - 59.93₪\nhttps://temu.to/k/ejq000x8a2j"],
        "💡 אורות": ["אין מוצרים עדיין - שלח לי קישור"],
        "🔒 מנעולים": ["אין מוצרים עדיין - שלח לי קישור"],
        "🎒 תיקים": ["אין מוצרים עדיין - שלח לי קישור"],
        "🔧 כלים ותיקון": ["אין מוצרים עדיין - שלח לי קישור"],
        "🚲 שאר אביזרים": ["אין מוצרים עדיין - שלח לי קישור"],
    },
}

user_state = {}
favorites = {}
last_shown = {}

def main_keyboard():
    m = ReplyKeyboardMarkup(resize_keyboard=True)
    m.row("🏠 לבית", "⚡ גאדג'טים")
    m.row("🎮 משחקים", "👟 נעליים")
    m.row("👕 ביגוד", "🚲 אביזרי אופניים")
    m.row("⭐ מועדפים שלי", "🔥 הכל")
    return m

def make_keyboard(items, back_text):
    m = ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(0, len(items), 2):
        if i+1 < len(items):
            m.row(items[i], items[i+1])
        else:
            m.row(items[i])
    m.row(back_text)
    return m

def fav_keyboard():
    m = ReplyKeyboardMarkup(resize_keyboard=True)
    m.row("⭐ שמור למועדפים")
    m.row("⭐ מועדפים שלי")
    m.row("🔙 חזרה לתפריט הראשי")
    return m

@bot.message_handler(commands=['start'])
def welcome(message):
    user_state[message.chat.id] = {"level": "main"}
    bot.send_message(message.chat.id, "🍆 ברוכים הבאים לדיל החצילוני! 🍆\nבחר קטגוריה למטה 👇\n⭐ שמור מוצרים שאהבת במועדפים!", reply_markup=main_keyboard())

@bot.message_handler(func=lambda m: m.text == "🔙 חזרה לתפריט הראשי")
def back_main(message):
    user_state[message.chat.id] = {"level": "main"}
    welcome(message)

@bot.message_handler(func=lambda m: m.text == "🔙 חזרה")
def back_one(message):
    st = user_state.get(message.chat.id, {"level": "main"})
    if st.get("level") == "subsub":
        cat = st.get("cat")
        user_state[message.chat.id] = {"level": "sub", "cat": cat}
        subs = list(PRODUCTS[cat].keys())
        bot.send_message(message.chat.id, f"🍆 בחר ב- {cat} 👇", reply_markup=make_keyboard(subs, "🔙 חזרה לתפריט הראשי"))
        return
    welcome(message)

@bot.message_handler(func=lambda m: m.text == "⭐ מועדפים שלי")
def show_favs(message):
    favs = favorites.get(message.chat.id, [])
    if not favs:
        bot.send_message(message.chat.id, "⭐ אין לך עדיין מועדפים\n\nכנס לקטגוריה, תראה מוצר שאהבת ולחץ על ⭐ שמור למועדפים!", reply_markup=main_keyboard())
        return
    txt = f"⭐ המועדפים שלך ({len(favs)}):\n\n" + "\n\n".join(favs)
    m = ReplyKeyboardMarkup(resize_keyboard=True)
    m.row("🗑️ נקה מועדפים")
    m.row("🔙 חזרה לתפריט הראשי")
    bot.send_message(message.chat.id, txt, reply_markup=m)

@bot.message_handler(func=lambda m: m.text == "🗑️ נקה מועדפים")
def clear_favs(message):
    favorites[message.chat.id] = []
    bot.send_message(message.chat.id, "🗑️ ניקיתי את המועדפים שלך!", reply_markup=main_keyboard())

@bot.message_handler(func=lambda m: m.text == "⭐ שמור למועדפים")
def save_fav(message):
    items = last_shown.get(message.chat.id, [])
    if not items:
        bot.send_message(message.chat.id, "קודם תכנס לקטגוריה ותראה מוצר, ואז תלחץ שמור!", reply_markup=main_keyboard())
        return
    if message.chat.id not in favorites:
        favorites[message.chat.id] = []
    added = 0
    for p in items:
        if p not in favorites[message.chat.id] and "אין מוצרים" not in p:
            favorites[message.chat.id].append(p)
            added += 1
    bot.send_message(message.chat.id, f"⭐ נשמר למועדפים! הוספתי {added} מוצרים\nלחץ על ⭐ מועדפים שלי כדי לראות!", reply_markup=main_keyboard())

@bot.message_handler(func=lambda m: m.text in PRODUCTS)
def show_sub(message):
    cat = message.text
    user_state[message.chat.id] = {"level": "sub", "cat": cat}
    subs = list(PRODUCTS[cat].keys())
    bot.send_message(message.chat.id, f"🍆 בחר תת-קטגוריה ב- {cat} 👇", reply_markup=make_keyboard(subs, "🔙 חזרה לתפריט הראשי"))

@bot.message_handler(func=lambda m: True)
def handle_all(message):
    text = message.text or ""
    chat_id = message.chat.id
    st = user_state.get(chat_id, {"level": "main"})
    if 'temu.to' in text or 'share.temu.com' in text:
        post = f"🍆 דיל חדש בדיל החצילוני! 🍆 טימו\n\n{text}\n\nרוצים עוד? תעקבו!\nhttps://t.me/ashermiz26"
        bot.send_message(CHANNEL, post)
        bot.reply_to(message, "נשלח לערוץ! ✅", reply_markup=main_keyboard())
        return
    if text == "🔥 הכל":
        full = "🍆 כל המבצעים - רק הקישורים שלך:\n\n"
        all_items = []
        def collect(obj):
            nonlocal full
            if isinstance(obj, list):
                for p in obj:
                    if "אין מוצרים" not in p:
                        full += p + "\n\n"
                        all_items.append(p)
            elif isinstance(obj, dict):
                for v in obj.values():
                    collect(v)
        collect(PRODUCTS)
        last_shown[chat_id] = all_items
        bot.send_message(chat_id, full, reply_markup=fav_keyboard())
        return
    if st.get("level") == "sub":
        cat = st.get("cat")
        if cat and text in PRODUCTS.get(cat, {}):
            val = PRODUCTS[cat][text]
            if isinstance(val, dict):
                user_state[chat_id] = {"level": "subsub", "cat": cat, "sub": text}
                subs = list(val.keys())
                bot.send_message(chat_id, f"🍆 בחר ב- {text} 👇", reply_markup=make_keyboard(subs, "🔙 חזרה"))
                return
            else:
                last_shown[chat_id] = val
                txt = f"🍆 מבצעים - {cat} > {text}:\n\n" + "\n\n".join(val)
                bot.send_message(chat_id, txt, reply_markup=fav_keyboard())
                return
    if st.get("level") == "subsub":
        cat = st.get("cat"); sub = st.get("sub")
        if cat and sub and text in PRODUCTS.get(cat, {}).get(sub, {}):
            products = PRODUCTS[cat][sub][text]
            last_shown[chat_id] = products
            txt = f"🍆 מבצעים - {cat} > {sub} > {text}:\n\n" + "\n\n".join(products)
            bot.send_message(chat_id, txt, reply_markup=fav_keyboard())
            return
    bot.send_message(chat_id, "🍆 בחר קטגוריה למטה 👇", reply_markup=main_keyboard())

print("דיל החצילוני רץ - עם מועדפים!")
port = int(os.environ.get("PORT", 10000))
threading.Thread(target=lambda: app.run(host="0.0.0.0", port=port)).start()
bot.polling()
