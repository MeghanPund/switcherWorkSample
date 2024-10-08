from flask import Flask, render_template, request, redirect, url_for
import json
import requests

app = Flask(__name__)
database = "mappedNames.json"
data = json.loads(open(database).read())


@app.route('/', methods=['POST', 'GET'])
def index():
    urban_areas_url = "https://api.teleport.org/api/urban_areas/"
    response = requests.get(urban_areas_url)
    json_data = response.json()
    urban_areas = json_data['_links']['ua:item']
    uas_list = []
    for area in range(len(urban_areas)):
        uas_list.append(urban_areas[area]['name'])
    
    if request.method == 'POST':
        area1 = request.form['area1']
        print(area1)
        area2 = request.form['area2']
        print(area2)
        
        data_points = request.form.getlist("ua_data")

        return redirect(url_for('display_uadata', area1=area1, area2=area2,
        data_points=data_points))
    
    return render_template('index.html', uas_list=uas_list)


@app.route('/uadata', methods=['POST', 'GET'])
def display_uadata():
    if request.method == 'GET':
        area1name = request.args['area1']
        area1 = data[area1name]
        area2name = request.args['area2']
        area2 = data[area2name]
        data_points = request.args.getlist('data_points')
        print(data_points)

        area1_url = f"https://api.teleport.org/api/urban_areas/slug:{area1}/"
        area2_url = f"https://api.teleport.org/api/urban_areas/slug:{area2}/"

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

        area1_pix_url = f"{area1_url}images/"
        area2_pix_url = f"{area2_url}images/"
        area1_pix_web = requests.get(area1_pix_url).json()['photos'][0]['image']['web']
        area2_pix_web = requests.get(area2_pix_url).json()['photos'][0]['image']['web']
        area1_pix_mobile = requests.get(area1_pix_url).json()['photos'][0]['image']['mobile']
        area2_pix_mobile = requests.get(area2_pix_url).json()['photos'][0]['image']['mobile']

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
        area2_elevation = details2_json[14]['data'][0]['float_value']

        area1_crime_rate = details_json[16]['data'][0]['float_value']
        area2_crime_rate = details2_json[16]['data'][0]['float_value']
    elif request.method == 'GET':
        pass    
        
    return render_template('uadata.html', area1name= area1name, area2name=area2name,
        area1=area1, area2=area2,
        area1_city_list=area1_city_list, area2_city_list=area2_city_list,
        area1_pix_web=area1_pix_web, area2_pix_web=area2_pix_web,
        area1_pix_mobile=area1_pix_mobile, area2_pix_mobile=area2_pix_mobile,
        area1_pop_size=area1_pop_size, area2_pop_size=area2_pop_size,
        area1_pop_size_label=area1_pop_size_label, area2_pop_size_label=area2_pop_size_label,
        area1_life_exp=area1_life_exp, area2_life_exp=area2_life_exp,
        area1_elevation=area1_elevation, area2_elevation=area2_elevation,
        area1_crime_rate=area1_crime_rate, area2_crime_rate=area2_crime_rate,
        data_points=data_points)


if __name__ == "__main__":
    app.run(debug = True)