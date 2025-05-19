import random

import telebot
import json

Token = "7653262395:AAGEtbhvkXeLLS1xoGPjO_eEMuVwFAd6BnM"

bot = telebot.TeleBot(Token)

user = {"id": {"watermelon": "арбуз"}}
with open("data.json", "r", encoding="utf - 8") as data:
    user = json.load(data)


@bot.message_handler(commands=["start"])
def handler_start(message):
    bot.send_message(message.chat.id,
                     " я помогу тебе разнаобразить словарный запас с помощью тренеровок пиши сюда новые слова  заходи в меню и тренеруйся ")


@bot.message_handler(commands=["learn"])
def handler_learn(message):
    bot.send_message(message.chat.id, "давай скорее начнём обучение")
    user_dict = user.get(str(message.chat.id), {})

    ask_translation(message.chat.id, user[str(message.chat.id)], int(message.text.split()[1]))



@bot.message_handler(commands=["help"])
def handler_help(message):
    bot.send_message(message.chat.id, "для укрепления словарного запаса")
    bot.send_message(message.chat.id, "learn,help,start")
    bot.send_message(message.chat.id, "Настя")


@bot.message_handler(commands=["add_word"])
def handler_add_word(message):
    global user
    id = message.chat.id
    dict = message.text.split()
    dict = dict[1:]
    user_dict = user.get(id, {})
    if len(dict) == 2:
        word, translate = dict[0].lower(), dict[1].lower()
        user_dict[word] = translate
        user[id] = user_dict
        with open("data.json", "w", encoding="utf - 8") as data:
            json.dump(user, data, ensure_ascii=False)

        bot.send_message(message.chat.id, "слово добавлено")
    else:
        bot.send_message(message.chat.id, "произошла ошибка проверьте написание")


@bot.message_handler(func=lambda message: True)
def handler_all(message):
    # bot.send_message(message.chat.id, message.text)
    if message.text.lower() == "как тебя зовут":
        bot.send_message(message.chat.id, "привет меня зовут лягух")
    elif message.text.lower() == "расcкажи о себе":
        bot.send_message(message.chat.id,
                         "мой любимый цвет зелёный а ещё я люблю смотреть и читать гарри поттера а моё любимое животное гусь")
    elif message.text.lower() == "расcкажи шутку":
        bot.send_message(message.chat.id,
                         "Только один процент современных школьников, которых заставляют учить наизусть стихи Пушкина, начинают понимать Пушкина. Остальные 99% начинают понимать Дантеса!"
                         )

    elif message.text.lower() == "как дела":
        bot.send_message(message.chat.id,
                         "хорошо")


def ask_translation(chat_id, words, left):
    if left > 0:
        learn = random.choice(list(words.keys()))
        bot.send_message(chat_id, f"введите перевод слова {learn} ")
        translation = words[learn]

        bot.register_next_step_handler_by_chat_id(chat_id,check_translation, left-1, translation)
    else:
        bot.send_message(chat_id,"спасибо за урок ")


def check_translation(message, left, exspected_translation):
    user_translation = message.text.strip().lower()
    if user_translation == exspected_translation.lower():
        bot.send_message(message.chat.id,"правильно молодец")
    else:
        bot.send_message(message.chat.id, f"неправильно:правильный перевод:{exspected_translation}")
    ask_translation(message.chat.id,user[str(message.chat.id)],left)




if __name__ == "__main__":
    bot.polling(none_stop=True)
