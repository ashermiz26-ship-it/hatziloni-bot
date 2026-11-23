import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = os.environ.get("BOT_TOKEN", "")
bot = telebot.TeleBot(TOKEN)

PRODUCTS = {
    "🏠 לבית": {
        "🏠 הכל לבית": [
            "🏠 מוצר לבית\nhttps://temu.to/k/e11wn0to19t",
            "🏠 מוצר לבית 2\nhttps://temu.to/k/erk5bu0qt22",
        ],
    },
    "⚡ גאדג'טים": {
        "⚡ הכל גאדג'טים": [
            "⚡ מוצר גאדג'ט\nhttps://temu.to/k/e11wn0to19t",
        ],
    },
    "🎮 משחקים": {
        "🎮 הכל משחקים": [
            "🎮 מוצר משחק\nhttps://temu.to/k/e11wn0to19t",
        ],
    },
    "👟 נעליים": {
        "👨 גברים": {
            "👟 נעלי גברים": [
                "👟 מוצר נעליים\nhttps://temu.to/k/e11wn0to19t",
            ],
        },
        "👩 נשים": {
            "👟 נעלי נשים": [
                "👟 מוצר נעליים\nhttps://temu.to/k/e11wn0to19t",
            ],
        },
    },
    "👨 גברים": {
        "👔 חולצה": [
            "👔 חולצה 1\nhttps://temu.to/k/egb5hatagrm",
            "👔 חולצה אחורה\nhttps://temu.to/k/e89xdhq53tg",
            "👔 חולצה 3\nhttps://share.temu.com/KXb8s0QeMDB",
            "👔 חולצה 4\nhttps://temu.to/k/eif8gvtiuo8",
        ],
        "🩲 הלבשה תחתונה": [
            "🩲 מוצר הלבשה\nhttps://temu.to/k/e11wn0to19t",
        ],
        "🌙 פיג'מות": [
            "🌙 פיג'מה\nhttps://temu.to/k/e11wn0to19t",
        ],
    },
    "👩 נשים": {
        "👔 חולצה": [
            "👔 חולצת נשים\nhttps://temu.to/k/e11wn0to19t",
        ],
    },
    "👦 ילדים": {
        "👔 חולצה": [
            "👔 חולצת ילדים\nhttps://temu.to/k/e11wn0to19t",
        ],
    },
    "👧 ילדות": {
        "👔 חולצה": [
            "👔 חולצת ילדות\nhttps://temu.to/k/e11wn0to19t",
        ],
    },
    "🚲 אביזרי אופניים": {
        "🚲 הכל אופניים": [
            "🚲 מוצר אופניים\nhttps://temu.to/k/e11wn0to19t",
        ],
    },
}

user_state = {}
favorites = {}

def make_kb(buttons):
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for b in buttons:
        kb.add(KeyboardButton(b))
    return kb

def main_buttons():
    return list(PRODUCTS.keys()) + ["⭐ מועדפים שלי", "🔥 הכל", "⬅️ חזרה"]

def find_node(text):
    if text in PRODUCTS:
        return PRODUCTS[text]
    for cat, subs in PRODUCTS.items():
        if isinstance(subs, dict):
            if text in subs:
                return subs[text]
            for sub, subs2 in subs.items():
                if isinstance(subs2, dict) and text in subs2:
                    return subs2[text]
    return None

@bot.message_handler(commands=["start"])
def start(m):
    bot.send_message(m.chat.id, "🍆 ברוכים הבאים לדיל החצילוני!\nבחר קטגוריה 👇", reply_markup=make_kb(main_buttons()))

@bot.message_handler(func=lambda m: True)
def handle_all(m):
    text = (m.text or "").strip()
    if text == "⬅️ חזרה" or text == "חזרה לתפריט הראשי":
        bot.send_message(m.chat.id, "🍆 תפריט ראשי 👇", reply_markup=make_kb(main_buttons()))
        return
    if text == "⭐ מועדפים שלי":
        favs = favorites.get(m.chat.id, [])
        if not favs:
            bot.send_message(m.chat.id, "אין לך עדיין מועדפים ❤️", reply_markup=make_kb(main_buttons()))
        else:
            bot.send_message(m.chat.id, "\n\n".join(favs), reply_markup=make_kb(main_buttons()))
        return
    if text == "🔥 הכל":
        all_items = []
        for cat, subs in PRODUCTS.items():
            for sub, subs2 in subs.items():
                if isinstance(subs2, dict):
                    for prod, items in subs2.items():
                        all_items.extend(items)
                elif isinstance(subs2, list):
                    all_items.extend(subs2)
        bot.send_message(m.chat.id, "\n\n".join(all_items[:20]), reply_markup=make_kb(main_buttons()))
        return
    node = find_node(text)
    if isinstance(node, dict):
        btns = list(node.keys()) + ["⬅️ חזרה"]
        bot.send_message(m.chat.id, f"🍆 {text} - בחר 👇", reply_markup=make_kb(btns))
        return
    if isinstance(node, list):
        msg = f"🍆 {text} - מבצעים 👇\n\n" + "\n\n".join(node)
        bot.send_message(m.chat.id, msg, reply_markup=make_kb(main_buttons()))
        return
    bot.send_message(m.chat.id, "🍆 תפריט ראשי 👇", reply_markup=make_kb(main_buttons()))

if __name__ == "__main__":
    print("Bot running...")
    bot.infinity_polling()
