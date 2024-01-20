import datetime
import telebot
import random
from telebot import types
import sqlite3
import time

NUM = 1
d = datetime.datetime.now()
DT = d.strftime('%H:%M:%S')
print(DT)
token = "6574968034:AAEoxdxZe6zBm7_kvmOsLdNKkwIushzecqs"
bot = telebot.TeleBot(token)
chated = [1, 2,3,4,5]


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Используйте команду /search чтобы найти собеседника')


globalTable = []


@bot.message_handler(commands=['search'])
def search(message):
    bot.send_message(message.chat.id, "Поиск собеседника")
    connect = sqlite3.connect('usersDATA.sql')
    cursor = connect.cursor()
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS users 
                   (id int auto_increment primary key,
                   chat_id int,
                   status varchar(10),
                    rank int
                    time VARCHAR(10)
                    )''')
    connect.commit()
    print('aloha')
    search = 'search'
    afk = 'afk'
    busy = 'busy'
    chatID = message.chat.id
    print(chatID)
    #    cursor.execute("INSERT INTO users (id) VALUES ('%s')" % (chatID))
    # bot.send_message(message.chat.id, )
    people_id = message.chat.id
    users = cursor.fetchall()
    print(users, 'd')
    if users == []:
        print(users, 's')
        cursor.execute("INSERT INTO users (chat_id) VALUES ('%s')" % (chatID))
        connect.commit()
    else:
        print('s')
    cursor.execute("UPDATE users SET status == ? WHERE chat_id == ?", (search, chatID))
    connect.commit()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    print(chated)
    bot.send_message(message.chat.id, "Cобеседник найден")
    r = random.randint(1, 5)

    for i in users:
        r = random.randint(1, 5)
        if i[2] == 'search':
            if chated[0] == 1:
                chated[0] = i[1]
            elif chated[2] == 3:
                chated[2] = i[1]
            elif chated[3] == 4:
                chated[3] = i[1]
            elif chated[4] == 5:
                chated[4] = i[1]
            else:
                chated[1] = i[1]

    cursor.close()
    connect.close()


@bot.message_handler(content_types=['photo'])
def sendMsg1(message):
    chat_id = message.chat.id
    photo = message.photo
    if chated[1] == chat_id:
        bot.send_photo(chated[0], str(len(photo)))
    elif chated[0] == chat_id:
        bot.send_photo(chated[1], photo)


@bot.message_handler(content_types=['text'])
def sendMsg(message):
    global NUM
    NUM += 1

    chat_id = message.chat.id
    text = message.text
    connect = sqlite3.connect('dialog.sql')
    cursor = connect.cursor()
    cursor.execute('''
       CREATE TABLE IF NOT EXISTS dialog(
       dialog_id int , 
       message VARCHAR(1000),
       author int ,
       ts VARCHAR(10));
       ''')
    connect.commit()
    cursor.execute(
        "INSERT INTO dialog (dialog_id,message,author,ts) VALUES ('%s','%s','%s','%s')" % (NUM, text, chat_id, f'{DT}'))
    connect.commit()
    cursor.execute('SELECT * FROM dialog')
    users = cursor.fetchall()
    print(users)
    if chated[1] == chat_id:
        bot.send_message(chated[0], text)
    r = random.randint(1, 5)
    r1 = random.randint(1, 5)
    r2 = random.randint(1, 5)
    r3 = random.randint(1, 5)


    bot.send_message(chated[r1], text)


@bot.message_handler(commands=['bup'])
def start(message):
    kb = types.InlineKeyboardMarkup(row_width=1)
    da = types.InlineKeyboardButton(text='кнопка 1', callback_data='btn1')
    btn1 = types.InlineKeyboardButton(text='кнопка 2', callback_data='btn2')
    kb.add(btn1)
    bot.send_message(message.chat.id, 'hey! look at this!', reply_markup=kb)


@bot.message_handler(func=lambda callback: callback.data)
def check_callback_data(callback):
    if callback.data == 'btn1':
        bot.send_message(callback.message.chat.id, 'вы нажали на первую кнопку')


bot.polling(none_stop=True)