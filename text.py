from graph import generate_ascii_graph

def start_msg (username):
    return f"Привет, {username}!👋\n Я бот, который поможет узнать погоду в разных городах🤖\n\nИспользуй команду /weather для запроса прогноза погоды."

def help_msg():
    return "Доступные команды:\n\n/start - Приветствие\n/help - Справка по командам\n/weather - Прогноз погоды"

def city_first_msg():
    return "Введите название начального города🏙️:"

def city_last_msg():
    return "Введите название конечного города🌆:"

def city_other_msg():
    return "Введите название промежуточного города🏠:"

def cities_setting_msg(cities):
    return f"Почти все готово, но давай удостоверимся, что все выбрано правильно😎\n\nВыбранные города: {', '.join(cities)}"

def cities_clear_msg():
    return "Названия городов очищены✅"

def get_graph_msg(city, days=5, type="Температура"):
    ascii_graph = generate_ascii_graph(city, days, type)
    return ascii_graph

def last_graph_msg(cities):
    return f"Для настройки графика используй кнопки ниже🤗\n\nТакже можете посмотреть более подробные графики на веб-сервисе по ссылке 👇\n\nhttp://127.0.0.1:8050?cities={','.join(cities).replace(' ', '_')}"

def new_type_msg():
    return "Введите название города, параметры которого нужно поменять:"

def city_not_found_msg():
    return "Город, который вы ввели не найден, попробуйте ещё раз:"

def choice_new_type_msg():
    return "Выбери на какой тип графика поменять📈:"

def new_day_msg():
    return "Введите название города, параметры которого нужно поменять:"

def choice_new_day_msg():
    return "На сколько дней хочешь прогноз?"