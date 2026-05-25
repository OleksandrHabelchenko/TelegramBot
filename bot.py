import telebot

TOKEN = '8666645591:AAEdw3hlRbJish1BdLNHcHIOlU4kA5sFQJg'

bot = telebot.TeleBot(TOKEN)  

@bot.message_handler(commands=['start']) 
def start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('Weather', 'Joke')
    keyboard.add('Time', 'Help')
    keyboard.add('GitHub authors/write to the author')
    bot.send_message(message.chat.id, "Hi,I'm your bot, choose a command please: ",
                     reply_markup=keyboard)  
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Commands:\n/start' \
    '\n/help\n/time' \
    '\n/joke' \
    '\n/weather\n/about')

@bot.message_handler(commands=['time'])
def time(message):
    import datetime
    now = datetime.datetime.now().strftime('%H:%M:%S')
    bot.send_message(message.chat.id, f'now: {now}')

@bot.message_handler(commands=['joke'])
def joke(message):
    import random
    jokes = ['Why do programmers confuse Halloween and Christmas? Because Oct 31 = Dec 25!',
'How did a programmer explain to his wife why he didn\'t take out the trash? You didn\'t type rm -rf!',
'How many programmers does it take to change a light bulb? None — it\'s a hardware problem!']
    
    bot.send_message(message.chat.id, random.choice(jokes))

@bot.message_handler(commands=['weather'])
def weather(message):
    bot.send_message(message.chat.id, 'Write the name of the city: ')
    bot.register_next_step_handler(message, get_weather)

def get_weather(message):
    city = message.text
    API_KEY = '8ced06cef7271d7ed22b85062e97c6fc'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=en'

    import requests
    response = requests.get(url)
    data = response.json()

    if data['cod'] == 200:       
        temp = data['main']['temp']
        feels = data['main']['feels_like']
        desc = data['weather'][0]['description']
        bot.send_message(message.chat.id, f'Weather in {city}:\n Temp: {temp}°C\n Feels like: {feels}°C\n {desc}')
    else:
        bot.send_message(message.chat.id, 'The city has not been found ')

@bot.message_handler(func=lambda message: message.text == 'Weather')
def weather_button(message):
    weather(message)

@bot.message_handler(func=lambda message: message.text == 'Joke')
def joke_button(message):
    joke(message)

@bot.message_handler(func=lambda message: message.text == 'Time')
def time_button(message):
    time(message)

@bot.message_handler(func=lambda message: message.text == 'Help')
def help_button(message):
    help(message)

@bot.message_handler(func=lambda message: message.text == 'GitHub authors/write to the author')
def about_button(message):
    about(message)

@bot.message_handler(commands=['about'])
def about(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton('GitHub', url='https://github.com/OleksandrHabelchenko'))
    keyboard.add(telebot.types.InlineKeyboardButton('write to the author', url='https://t.me/alexhaby'))
    bot.send_message(message.chat.id, 'The bot was created to study Python', reply_markup=keyboard)

@bot.message_handler(func=lambda message: True)  
def echo(message):
    bot.send_message(message.chat.id, f'You wrote: {message.text}')


bot.polling()


