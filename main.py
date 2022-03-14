from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# global vars
urban_areas_url = "https://api.teleport.org/api/urban_areas/"
response = requests.get(urban_areas_url)
json_data = response.json()
urban_areas = json_data['_links']['ua:item']


@app.route('/', methods=['POST', 'GET'])
def index():
    uas_list = []
    for area in range(len(urban_areas)):
        uas_list.append(urban_areas[area]['name'])
    
    error = None
    if request.method == 'POST':
        area1 = request.form['area1']
        area2 = request.form['area2'].replace(" ", "-")
        
        data_points = request.form.getlist("ua_data")

        return redirect(url_for('display_uadata', area1=area1, area2=area2,
        data_points=data_points, error=error))
    
    return render_template('index.html', uas_list=uas_list)


@app.route('/uadata', methods=['POST', 'GET'])
def display_uadata():
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        area1 = request.args['area1']
        area2 = request.args['area2']
        data_points = request.args.getlist('data_points')

        area1_url = f"https://api.teleport.org/api/urban_areas/slug:{area1.lower()}/"
        area2_url = f"https://api.teleport.org/api/urban_areas/slug:{area2.lower()}/"

        cities = f"{area1_url}cities/"
        cities2 = f"{area2_url}cities/"
        cities_list = requests.get(cities).json()['_links']['city:items']
        cities2_list = requests.get(cities2).json()['_links']['city:items']
        area1_city_list = []
        for city in cities_list:
            area1_city_list.append(city['name'])
        area2_city_list = []
        for city in cities2_list:
            area2_city_list.append(city['name'])

        details = f"{area1_url}details/"
        details2 = f"{area2_url}details/"
        details_json = requests.get(details).json()['categories']
        details2_json = requests.get(details2).json()['categories']
        
        area1_pop_size = details_json[1]['data'][0]['float_value']
        area1_pop_size_label = details_json[1]['data'][0]['label']
        area2_pop_size = details2_json[1]['data'][0]['float_value']
        area2_pop_size_label = details2_json[1]['data'][0]['label']

        area1_life_exp = details_json[7]['data'][1]['float_value']
        area2_life_exp = details2_json[7]['data'][1]['float_value']

        area1_elevation = details_json[14]['data'][0]['float_value']
        area2_elevation = details2_json[16]['data'][0]['float_value']

        area1_crime_rate = details_json[16]['data'][0]['float_value']
        area2_crime_rate = details2_json[16]['data'][0]['float_value']
    
        
    return render_template('uadata.html', area1=area1, area2=area2,
        area1_city_list=area1_city_list, area2_city_list=area2_city_list,
        area1_pop_size=area1_pop_size, area2_pop_size=area2_pop_size,
        area1_pop_size_label=area1_pop_size_label, area2_pop_size_label=area2_pop_size_label,
        area1_life_exp=area1_life_exp, area2_life_exp=area2_life_exp,
        area1_elevation=area1_elevation, area2_elevation=area2_elevation,
        area1_crime_rate=area1_crime_rate, area2_crime_rate=area2_crime_rate,
        data_points=data_points)


if __name__ == "__main__":
    app.run(debug = True)