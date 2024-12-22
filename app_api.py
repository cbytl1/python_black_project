# from app import *

# @server.route('/get_data', methods=['GET'])
# def get_data():
#     city_names = request.args.get('cities')
#     if not city_names:
#         return jsonify({'error': 'Parameter "cities" is required'}), 400

#     city_names = city_names.split(',')
#     global cities
#     cities = []
#     for city in city_names:
#         loc = fetch_location_key(city.strip())
#         if loc:
#             weather = fetch_daily_forecast(loc[0])
#             if weather:
#                 cities.append({
#                     "name": city,
#                     "loc_key": loc[0],
#                     "lat": loc[1],
#                     "lon": loc[2],
#                     "weather": weather
#                 })
#             else:
#                 return jsonify({'error': f"Weather data not found for city: {city}"}), 404
#         else:
#             return jsonify({'error': f"City not found: {city}"}), 404

#     return jsonify(cities), 200

# @server.route('/open_graph', methods=['GET'])
# def get_data():
#     city_names = request.args.get('cities')
#     if not city_names:
#         return jsonify({'error': 'Parameter "cities" is required'}), 400

#     city_names = city_names.split(',')
#     graph(cities_input=city_names)

# open_graph_app = dash.Dash(name="weather", server=server, url_base_pathname="/open_graph/")
# open_graph_app.layout = html.Div(children=[
#     html.Div(id='container-button-basic',children=[]),
# ])

# def graph(cities_input):
#     data = []
#     global cities
#     cities = []
#     cities_name = [x['props']['value'] for x in cities_input if x['props']['value'] != None]
#     last_city = cities_name[1]
#     cities_name.remove(last_city)
#     cities_name.append(last_city)
#     if len(cities_name) >= 2:
#         for city in cities_name:
#             loc = fetch_location_key(city)
#             if loc:
#                 weather = fetch_daily_forecast(loc[0])
#                 if weather:
#                     graph = get_graph(weather, "Температура")
#                     cities.append({"name": city, "loc_key": loc[0], "lat": loc[1], "lon": loc[2], "weather": weather })

#                     data.append(html.H2(children=f'График города {city}'))
#                     data.append(dcc.RadioItems(id={'type': 'graph-type', 'index':len(cities) },options=[{'label': i, 'value': i} for i in ['Температура', 'Скорость ветра', 'Вероятность осадков']],value='Температура', style={"display": "inline-block"}))
#                     data.append(dcc.Slider(id={'type':'day-slider', 'index': len(cities)},min=1,max=5,marks={1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, value=5,step=None))
#                     data.append(dcc.Graph(id={'type': 'graph', 'index': len(cities)}, figure=graph))
#                     data.append(html.Div(id={'type': 'graph-index', 'index':len(cities)},children= f'{len(cities)}'))

#                 else:
#                     return f"Не удалось получить погоду {city}"
#             else:
#                 return f"Не удалось найти город {city}"
#         data.append(dcc.Graph(id='map', figure=get_map()))
#     else:
#         return "Заполните пустые поля"
#     container = open_graph_app.layout.children
#     for child in container:
#         if child.id == 'container-button-basic':
#             child.children.append(data)
#             break