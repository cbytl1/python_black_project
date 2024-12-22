import numpy as np
import pandas as pd

def generate_ascii_graph(city, days, type):

    df = pd.DataFrame([{
        'time': item['Date'][:10],
        'temperature': item['Temperature']['Maximum']['Value'],
        'wind_speed': item['Day']['Wind']['Speed']['Value'],
        'precipitation_probability': item['Day']['PrecipitationProbability']
    } for item in city['weather']])

    df = df.iloc[:days]
    if type == 'Температура':
        x_values = df['time'].astype(str).tolist()
        y_values = df['temperature'].tolist()
    elif type == 'Скорость ветра':
        x_values = df['time'].astype(str).tolist()
        y_values = df['wind_speed'].tolist()
    elif type == 'Вероятность осадков':
        x_values = df['time'].astype(str).tolist()
        y_values = df['precipitation_probability'].tolist()

    max_y = max(y_values)
    min_y = min(y_values)
    y_range = max_y - min_y
    graph_width = 50  # Ширина графика в символах

    # Генерация уровней для оси Y
    y_levels = np.arange(min_y, max_y + 0.5, max(0.5, max_y//10))[::-1]

    # Построение графика
    graph_lines = []
    for level in y_levels:
        line = f"{round(level, 1):>3} |"
        for y in y_values:
            if level <= y < round(level, 1) + (y_range / len(y_levels)):
                line += "o          "
            else:
                line += "           "
        graph_lines.append(line)

    # Ось X
    x_axis = "     " + "-" * graph_width
    x_labels = "      " + "         ".join(f"{x[-2:]}" for x in x_values[:graph_width // 4])

    # Финальный график
    return f"Прогноз в городе: {city['name']}\nТип прогноза: {type}\n<pre>" +"\n".join(graph_lines + [x_axis, x_labels]) + "</pre>"