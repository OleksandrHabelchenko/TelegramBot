import telebot

TOKEN = '8666645591:AAEdw3hlRbJish1BdLNHcHIOlU4kA5sFQJg'

bot = telebot.TeleBot(TOKEN)  # create bot object with token

@bot.message_handler(commands=['start'])  # triggers when user sends /start
def start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)  # create keyboard
    keyboard.add('Weather', 'Joke')        # add buttons row 1
    keyboard.add('Time', 'Help')           # add buttons row 2
    keyboard.add('GitHub authors/write to the author')  # add buttons row 3
    bot.send_message(message.chat.id, "Hi,I'm your bot, choose a command please: ",
                     reply_markup=keyboard)  # send message with keyboard

@bot.message_handler(commands=['help'])   # triggers when user sends /help
def help(message):
    bot.send_message(message.chat.id, 'Commands:\n/start' \
    '\n/help\n/time' \
    '\n/joke' \
    '\n/weather\n/about')

@bot.message_handler(commands=['time'])   # triggers when user sends /time
def time(message):
    import datetime
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=3)  # get current time
    bot.send_message(message.chat.id, f'now: {now.strftime("%H:%M:%S")}')

@bot.message_handler(commands=['joke'])   # triggers when user sends /joke
def joke(message):
    import random
    jokes = ['Why do programmers confuse Halloween and Christmas? Because Oct 31 = Dec 25!',
'How did a programmer explain to his wife why he didn\'t take out the trash? You didn\'t type rm -rf!',
'How many programmers does it take to change a light bulb? None — it\'s a hardware problem!']
    bot.send_message(message.chat.id, random.choice(jokes))  # send random joke

@bot.message_handler(commands=['weather'])  # triggers when user sends /weather
def weather(message):
    bot.send_message(message.chat.id, 'Write the name of the city: ')
    bot.register_next_step_handler(message, get_weather)  # wait for city name

def get_weather(message):                  # called after user sends city name
    city = message.text
    API_KEY = '8ced06cef7271d7ed22b85062e97c6fc'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=en'
    import requests
    response = requests.get(url)           # send request to weather API
    data = response.json()                 # convert response to dictionary

    if data['cod'] == 200:                 # 200 means request was successful
        temp = data['main']['temp']        # get temperature
        feels = data['main']['feels_like'] # get feels like temperature
        desc = data['weather'][0]['description']  # get weather description
        bot.send_message(message.chat.id, f'Weather in {city}:\n Temp: {temp}°C\n Feels like: {feels}°C\n {desc}')
    else:
        bot.send_message(message.chat.id, 'The city has not been found ')

@bot.message_handler(func=lambda message: message.text == 'Weather')  # keyboard button Weather
def weather_button(message):
    weather(message)

@bot.message_handler(func=lambda message: message.text == 'Joke')     # keyboard button Joke
def joke_button(message):
    joke(message)

@bot.message_handler(func=lambda message: message.text == 'Time')     # keyboard button Time
def time_button(message):
    time(message)

@bot.message_handler(func=lambda message: message.text == 'Help')     # keyboard button Help
def help_button(message):
    help(message)

@bot.message_handler(func=lambda message: message.text == 'GitHub authors/write to the author')  # keyboard button GitHub
def about_button(message):
    about(message)

@bot.message_handler(commands=['about'])  # triggers when user sends /about
def about(message):
    keyboard = telebot.types.InlineKeyboardMarkup()  # create inline keyboard
    keyboard.add(telebot.types.InlineKeyboardButton('GitHub', url='https://github.com/OleksandrHabelchenko'))
    keyboard.add(telebot.types.InlineKeyboardButton('write to the author', url='https://t.me/alexhaby'))
    bot.send_message(message.chat.id, 'The bot was created to study Python', reply_markup=keyboard)

@bot.message_handler(func=lambda message: True)  # responds to any message
def echo(message):
    bot.send_message(message.chat.id, f'You wrote: {message.text}')

bot.polling()  # start bot, listen for new messages

# Декораторы @bot.message_handler — это способ сказать боту "когда получишь такое сообщение — вызови вот эту функцию".
# Команда /start — создаёт клавиатуру с кнопками и отправляет приветствие.
# Команда /help — отправляет список всех команд.
# Команда /time — берёт текущее время с сервера и отправляет пользователю.
# Команда /joke — выбирает случайную шутку из списка и отправляет.
# Команда /weather — спрашивает город, ждёт ответа через register_next_step_handler, потом вызывает get_weather.
# Функция get_weather — отправляет запрос на openweathermap.org, получает данные в виде словаря JSON, берёт температуру и описание и отправляет пользователю.
# Обработчики кнопок — когда пользователь нажимает кнопку на клавиатуре — это просто текстовое сообщение. Мы проверяем текст и вызываем нужную функцию.
# Команда /about — создаёт inline кнопки со ссылками на GitHub и телеграм автора.
# Функция echo — срабатывает на любое сообщение которое не является командой, повторяет его обратно.
# bot.polling() — запускает бота, он постоянно проверяет есть ли новые сообщения и обрабатывает их.