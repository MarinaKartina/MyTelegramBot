import telebot
from config import TOKEN, keys
from extensions import APIException, Converter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start','help'])
def com_start_help(message):
    text = """Этот бот показывает стоимость валют. \nДля начала работы напишите боту команду в виде:
    \n<имя валюты, цену которой вы хотите узнать> <имя валюты, в которой надо узнать цену первой валюты> 
    <количество первой валюты>
    \nДля получения списка доступных валют введите команду /values"""
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def com_values(message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('Введено неверное количество параметров')

        base, quote, amount = values
        total_base = Converter.get_price(base, quote, amount)

    except APIException as e:
        bot.reply_to(message,f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось выполнить команду\n{e}')
    else:
        text = f'Цена {amount} {base} в валюте {quote} составляет {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)