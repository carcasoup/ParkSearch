import telebot
from geopy.distance import geodesic as GD
from telebot import types
import config

# Список координат парковочных мест и ссылок на Яндекс.Карты
coords = [
    (56.543893, 38.168832, 'https://yandex.ru/maps/-/CDGZj8Ke'),
    (56.543665, 38.170533, 'https://yandex.ru/maps/-/CDGZjPLJ'),
    (56.543992, 38.171264, 'https://yandex.ru/maps/-/CDGZj-3i'),
    (56.545015, 38.173749, 'https://yandex.ru/maps/-/CDGZnY9O'),
    (56.545068, 38.172837, 'https://yandex.ru/maps/-/CDGZnF-o'),
    (56.544997, 38.172221, 'https://yandex.ru/maps/-/CDGZnVn2'),
    (56.544982, 38.171727, 'https://yandex.ru/maps/-/CDGZnC1O'),
    (56.545525, 38.170489, 'https://yandex.ru/maps/-/CDGZnOZo'),
    (56.545951, 38.170551, 'https://yandex.ru/maps/-/CDGZn0IR'),
    (56.546299, 38.171940, 'https://yandex.ru/maps/-/CDGZnH1y'),
    (56.545946, 38.173458, 'https://yandex.ru/maps/-/CDGZnToh'),
    (56.546067, 38.174295, 'https://yandex.ru/maps/-/CDGZn-6m'),
    (56.545382, 38.174169, 'https://yandex.ru/maps/-/CDGZrMOZ')
]

# Инициализация бота
bot = telebot.TeleBot(config.TOKEN)

# Команда /start
@bot.message_handler(commands=['start'])
def welcome(message):
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton(text='Запрос геолокации', request_location=True)
    buttons.add(btn1)
    bot.send_message(message.chat.id,
                     'Привет!\nЯ — ParkSearch, чат-бот для поиска парковочных мест поблизости. '
                     'Чтобы я мог отправить подходящие парковки — нажми "Запрос геолокации".',
                     reply_markup=buttons)

# Обработка полученной геолокации
@bot.message_handler(content_types=['location'])
def check_location(message):
    user_coords = (message.location.latitude, message.location.longitude)

    # Запись координат пользователя в файл
    with open('coords.txt', 'a') as file:
        file.write(f'@{message.from_user.username} — {user_coords[0]}, {user_coords[1]}\n')

    # Вычисляем расстояния до всех парковок
    distances = [GD(place[:-1], user_coords).km for place in coords]
    sorted_distances = sorted(distances)

    # Определяем 3 ближайших парковки
    nearest_indices = [distances.index(d) for d in sorted_distances[:3]]

    for i, idx in enumerate(nearest_indices, 1):
        lat, lon, link = coords[idx]
        distance = distances[idx]
        bot.send_message(message.chat.id,
                         f"{i}-е ближайшее парковочное место: {link}\n"
                         f"Находится в {round(distance, 3)} км от вас.")
        bot.send_location(message.chat.id, latitude=lat, longitude=lon)

# Запуск бота
bot.polling(none_stop=True)
