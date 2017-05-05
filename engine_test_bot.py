import telebot
import engine
import os
from random import randint

bot = telebot.TeleBot("TOKEN")

ACTIVE_USERS = {}
PHOTO_URL = "http://url.com/"

def draw_buttons():
    keyboard = telebot.types.InlineKeyboardMarkup()
    left = telebot.types.InlineKeyboardButton("<-", callback_data='/left')
    up = telebot.types.InlineKeyboardButton("/\\", callback_data='/up')
    down = telebot.types.InlineKeyboardButton("\\/", callback_data='/down')
    right = telebot.types.InlineKeyboardButton("->", callback_data='/right')
    keyboard.row(left, up, down, right)
    return keyboard


@bot.message_handler(commands=['start', 'help'])
def help(message):
    bot.send_message(message.chat.id, "OpenRPG engine preview. Use /spawn to start")

@bot.message_handler(commands=['spawn'])
def spawn(message):
    map_spawn_pos = [randint(200, 2800), randint(200, 1500)]
    usr = engine.character('hero.jpg', map_pos=map_spawn_pos)
    move = engine.mover(usr)
    fname = engine.save_background(move.spawn(), "serv/{0}{1}.jpg".format(message.chat.id, usr.getpos()))
    m = bot.send_message(message.chat.id, '''<a href="{0}{1}">.</a>'''.format(PHOTO_URL, fname.split("/")[1]), reply_markup=draw_buttons(), parse_mode='html')
    ACTIVE_USERS[message.chat.id] = [move, m.message_id]

@bot.callback_query_handler(lambda query: query.data=='/left')
def left(query):
    if query.message.chat.id not in ACTIVE_USERS.keys():
        bot.send_message(query.message.chat.id, "Spawn yourself first")
    else:
        os.remove('serv/{0}{1}.jpg'.format(query.message.chat.id,
                                                  ACTIVE_USERS[query.message.chat.id][0].user.getpos()))
        fname = engine.save_background(ACTIVE_USERS[query.message.chat.id][0].left(),
                                       "serv/{0}{1}.jpg".format(query.message.chat.id,
                                                                ACTIVE_USERS[query.message.chat.id][0].user.getpos()))
        fname_handle = open(fname, 'rb')
        bot.edit_message_text(
            '''<a href="{0}{1}">.</a>'''.format(PHOTO_URL, fname.split('/')[1]),
            chat_id=query.message.chat.id, message_id=ACTIVE_USERS[query.message.chat.id][1], parse_mode='html', reply_markup=draw_buttons())
        fname_handle.close()

@bot.callback_query_handler(lambda query: query.data=='/right')
def right(query):
    if query.message.chat.id not in ACTIVE_USERS.keys():
        bot.send_message(query.message.chat.id, "Spawn yourself first")
    else:
        os.remove('serv/{0}{1}.jpg'.format(query.message.chat.id,
                                                  ACTIVE_USERS[query.message.chat.id][0].user.getpos()))
        fname = engine.save_background(ACTIVE_USERS[query.message.chat.id][0].right(),
                                       "serv/{0}{1}.jpg".format(query.message.chat.id,
                                                           ACTIVE_USERS[query.message.chat.id][0].user.getpos()))
        fname_handle = open(fname, 'rb')
        bot.edit_message_text(
            '''<a href="{0}{1}">.</a>'''.format(PHOTO_URL, fname.split('/')[1]),
            chat_id=query.message.chat.id, message_id=ACTIVE_USERS[query.message.chat.id][1], parse_mode='html',
            reply_markup=draw_buttons())
        fname_handle.close()

@bot.callback_query_handler(lambda query: query.data=='/up')
def up(query):
    if query.message.chat.id not in ACTIVE_USERS.keys():
        bot.send_message(query.message.chat.id, "Spawn yourself first")
    else:
        os.remove('serv/{0}{1}.jpg'.format(query.message.chat.id,
                                                  ACTIVE_USERS[query.message.chat.id][0].user.getpos()))
        fname = engine.save_background(ACTIVE_USERS[query.message.chat.id][0].up(),
                                       "serv/{0}{1}.jpg".format(query.message.chat.id,
                                                           ACTIVE_USERS[query.message.chat.id][0].user.getpos()))
        fname_handle = open(fname, 'rb')
        bot.edit_message_text(
            '''<a href="{0}{1}">.</a>'''.format(PHOTO_URL, fname.split('/')[1]),
            chat_id=query.message.chat.id, message_id=ACTIVE_USERS[query.message.chat.id][1], parse_mode='html',
            reply_markup=draw_buttons())
        fname_handle.close()

@bot.callback_query_handler(lambda query: query.data=='/down')
def down(query):
    if query.message.chat.id not in ACTIVE_USERS.keys():
        bot.send_message(query.message.chat.id, "Spawn yourself first")
    else:
        os.remove('serv/{0}{1}.jpg'.format(query.message.chat.id,
                                                  ACTIVE_USERS[query.message.chat.id][0].user.getpos()))
        fname = engine.save_background(ACTIVE_USERS[query.message.chat.id][0].down(),
                                       "serv/{0}{1}.jpg".format(query.message.chat.id,
                                                           ACTIVE_USERS[query.message.chat.id][0].user.getpos()))
        fname_handle = open(fname, 'rb')
        bot.edit_message_text(
            '''<a href="{0}{1}">.</a>'''.format(PHOTO_URL, fname.split('/')[1]),
            chat_id=query.message.chat.id, message_id=ACTIVE_USERS[query.message.chat.id][1], parse_mode='html',
            reply_markup=draw_buttons())
        fname_handle.close()

@bot.message_handler(commands=['end_game'])
def end_game(message):
    os.remove('serv/{0}{1}.jpg'.format(message.chat.id,
                                              ACTIVE_USERS[message.chat.id][0].user.getpos()))
    del ACTIVE_USERS[message.chat.id]
    bot.send_message(message.chat.id, "Game stopped")

bot.polling(none_stop=True)