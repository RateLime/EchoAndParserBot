#библиотеки самого бота
import telebot #pip install telebot
from telebot import types
import bs4 #pip install bs4
import requests #pip install requests
import random
import json #это для дикшна
from dicts import dict #сам файл дикшна



#словарь записанных ответов
with open("dicts/dic.json", 'r', encoding='utf-8') as f:
    dice = json.load(f)


#парсируемый сайт
main_url="https://animestyle-shop.ru/products/search?sort=0&balance=&categoryId=&min_cost=&max_cost=&page=1&text=%D0%BC%D0%B8%D0%BA%D1%83"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60'}
miku=[]

#парсер интернет магазина
def get_soup(url):
    res = requests.get(url, headers)
    return bs4.BeautifulSoup(res.text, 'html.parser')
categories_page = get_soup(main_url)
categories = categories_page.findAll('div',class_="catalog__product column")
name = categories_page.findAll('div',class_='product-item__link')
for nameprice in categories:
    name = nameprice.find('div',class_='product-item__link')
    title = name.find('a').text
    pric = str(nameprice.find('div',class_="product-item-price")).replace('<div class="product-item-price product-item-price_with-old">',"").replace("</div>","").replace('<div class="product-item-price">',"")
    imag = str(nameprice.find("img")["src"].replace("//","",1).split()).replace("['","").replace("']","")
    miku.append([pric,title,imag])
miku.sort()
lenmiku = len(miku)
def Bot():
    #ключ телеграм бота
    bot = telebot.TeleBot('6501487948:AAFCXbJHDzH_EFWzFnc66NX_r-KoWznqRN0')
    def button0(message):
        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton('дешевле', callback_data="lowly2")
        item2 = types.InlineKeyboardButton('дороже', callback_data="lowly1")
        markup.add(item1,item2)
        bot.send_message(message.chat.id, "дальше или назад?", reply_markup=markup)
    def button1(message):
        markup = types.InlineKeyboardMarkup(row_width=1)
        item = types.InlineKeyboardButton('Next', callback_data='random')
        markup.add(item)
        bot.send_message(message.chat.id, "Next?", reply_markup=markup)
    @bot.callback_query_handler(func=lambda call: True)
    def callback(call):
        global current_miku
        try:
            current_miku
        except NameError:
            current_miku = 0
        if call.message:
            if call.data == "random":
                randomnum = random.randint(0, lenmiku-1)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                      text=miku[randomnum][2]+"\nИмя: "+miku[randomnum][1]+"\nЦена: "+miku[randomnum][0])
                button1(call.message)
            if call.data == "lowly":
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                      text=miku[current_miku][2]+"\nИмя: "+miku[current_miku][1]+"\nЦена: "+miku[current_miku][0])
                button0(call.message)
            if call.data == "lowly1":
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                      text=miku[current_miku][2]+"\nИмя: "+miku[current_miku][1]+"\nЦена: "+miku[current_miku][0])
                current_miku += 1
                button0(call.message)

            if call.data == "lowly2":
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                      text=miku[current_miku][2] + "\nИмя: " + miku[current_miku][1] + "\nЦена: " + miku[current_miku][
                                          0])
                if current_miku != 0:
                    current_miku -= 1
                    button0(call.message)
                else:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                          text="Дешевле нет.")
                    button0(call.message)



    @bot.message_handler(commands=['miku'])
    def button(message):
        markup = types.InlineKeyboardMarkup(row_width=2)
        item01 = types.InlineKeyboardButton('Рандомная', callback_data='random')
        item02 = types.InlineKeyboardButton("дешевая", callback_data='lowly')
        markup.add(item01,item02)
        bot.send_message(message.chat.id, "какую мику фигурку ты хочешь купить?", reply_markup=markup)



    @bot.message_handler(commands=['start'])
    def start(message):
        bot.send_message(message.chat.id,"Это эхо-бот, с парсером интернет магазина фигурок мику. Если написать что-либо, бот запишет запрос в словарь, и в следующий раз, при запросе, он ответит рандомной записью. Если написать запрос из dic.json, он ответит записаным в нем ответом\n Команды: \n !Команда, Ответ - создание команды \n /miku - парсинг интернет магазина")

    @bot.message_handler(func=lambda message: True)
    def handle_all_messages(message):
        if message.text in dict.dict():
            bot.send_message(message.chat.id, dict.dict()[message.text])
        if message.text[0] == "!":
            if message.text.count(",") != 1:
                bot.send_message(message.chat.id, "Надо написать в стиле: !Команда, Ответ")
            else:
                dict.create(*(message.text[1:].split(",")))
                bot.send_message(message.chat.id, "создана команда "+(message.text[1:].split(","))[0])
        elif message.text not in dict.dict():
            bot.send_message(message.chat.id, dict.rand(message.text))
    bot.polling(none_stop=True)
if __name__ == '__main__':
    Bot()
