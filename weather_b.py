import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import requests

TOKEN = ''
API_KEY = ''
Weather_API = 'https://api.openweathermap.org/data/2.5/weather'
cataas_api = 'https://cataas.com/cat'

def get_emoji(code):
    if 200 <= code <= 232:
        return '⛈️'
    elif 300 <= code <= 321:
        return '🌦️'
    elif 500 <= code <= 531:
        return '🌧️'
    elif code == 611:
        return '🌨️'
    elif 600 <= code <= 622:
        return '❄️'
    elif 700 <= code <= 781:
        return '🌫️'
    elif code == 800:
        return '☀️'
    elif 801 <= code <= 804:
        return ['🌤️', '⛅', '☁️', '☁️'][code - 801]
    else:
        return '🌡️'

bot = telebot.TeleBot(TOKEN)
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton('📍 Погода сейчас', request_location=True))
keyboard.add(KeyboardButton('ℹ️ О проекте'))

def get_weather(lat, lon):
    params = {'lat': lat,'lon': lon,'lang': 'ru','units': 'metric','appid': API_KEY}
    try:
        response = requests.get(url=Weather_API, params=params)
        data = response.json()

        city_name = data['name']
        description = data['weather'][0]['description']
        code = data['weather'][0]['id']
        temp = round(data['main']['temp'])
        temp_feels_like = round(data['main']['feels_like'])
        humidity = data['main']['humidity']
        emoji = get_emoji(code)

        message = f"🏙️ Погода в: {city_name}\n"
        message += f"{emoji} {description.capitalize()}\n"
        message += f"🌡️ Температура: {temp}°C\n"
        message += f"🤔 Ощущается как: {temp_feels_like}°C\n"
        message += f"💧 Влажность: {humidity}%\n"

        if temp < -20:
            message += "🥶 Очень холодно!\n"
        elif temp < 0:
            message += "🧣 Не забудьте надеть шапку!\n"
        elif temp > 20:
            message += "😎 Отличная погода для прогулки!\n"
        elif temp > 30:
            message += "🥵 Очень жарко!\n"

        return message

    except Exception as e:
        print(f"Ошибка при запросе погоды: {e}")
        return "❌ Произошла ошибка при получении данных о погоде."

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "🌤️Добро пожаловать в Бот Погоды!🌤️\n\n""Нажмите кнопку \"📍 Погода сейчас\" и разрешите доступ к геолокации,чтобы узнать погоду в вашем местоположении.", reply_markup=keyboard)

def rnd_cat():
    cat = requests.get(cataas_api)
    return cat.content

@bot.message_handler(commands=['secret_cat'])# команда /secret_cat
def secret_cat(message):
    cat_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    cat_keyboard.add(KeyboardButton('😺 Котик!'))
    cat_keyboard.add(KeyboardButton('☀ Вернуться к погоде'))
    bot.send_message(message.chat.id,"🤫 Секретная команда 🤫\n\n""📱 При нажатии на кнопку \"😺 Котик!\", вы получите случайного котика.", reply_markup = cat_keyboard)

@bot.message_handler(func=lambda message: message.text == '😺 Котик!')
def send_cat(message):
    wait_mess = bot.send_message(message.chat.id, "🔍 Ищу котика... Подождите секунду.")
    cat=rnd_cat()
    bot.send_photo(message.chat.id, cat, caption="😸 Котик!")
    bot.delete_message(message.chat.id, wait_mess.message_id)

@bot.message_handler(func=lambda message: message.text=="☀ Вернуться к погоде")
def back_to_project(message):
    bot.send_message(message.chat.id, "🌤️Вы вернулись в 'погодный бот'!",reply_markup=keyboard)

@bot.message_handler(func= lambda message: message.text == "ℹ️ О проекте")
def send_about_project(message):
    bot.send_message(message.chat.id, "📋 О Проекте:\n\n""✏Название бота: Погода сейчас.\n""⛅Данный бот поможет определить температуру и погоду в вашем или заданом вами местоположении.\n\n""🗃Истоники, используемые для получения информации о погоде: openweathermap.org\n\n""🙍‍♂️Автор: Сарафанов Андрей.", reply_markup=keyboard)

@bot.message_handler(content_types=['location'])
def send_weather(message):
    wait_mess = bot.send_message(message.chat.id, "🔍 Получаю данные о погоде... Подождите секунду.")
    lon = message.location.longitude
    lat = message.location.latitude
    weather_text = get_weather(lat, lon)
    bot.edit_message_text(weather_text, message.chat.id, wait_mess.message_id)

@bot.message_handler(func=lambda message: True)
def other(message):
    bot.send_message(message.chat.id,"❗Нажмите кнопку \"📍 Погода сейчас\" и отправьте свою геолокацию!",reply_markup=keyboard)

print("Бот запущен и готов к работе!!")
bot.infinity_polling()