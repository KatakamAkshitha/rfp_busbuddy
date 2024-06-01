from flask import Flask, jsonify, request, render_template,url_for
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/searchRoutes')
def search_routes_page():
    return render_template('searchRoutes.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/routes/<string:time_slot>.json')
def get_routes(time_slot):
    try:
        with open(f'routes_{time_slot}.json', 'r') as file:
            routes = json.load(file)
        return jsonify(routes)
    except Exception as e:
        print(f'Error loading routes for {time_slot}:', e)
        return jsonify([])

def filter_routes(routes, current_location):
    if not current_location:
        return routes
    lower_case_location = current_location.lower()
    filtered_routes = [route for route in routes if any(lower_case_location in stop.lower() for stop in route['stops'])]
    return filtered_routes

@app.route('/search_routes', methods=['POST'])
def search_routes():
    data = request.get_json()
    current_location = data.get('current_location')
    time_slot = data.get('time_slot')

    try:
        with open(f'routes_{time_slot}.json', 'r') as file:
            routes = json.load(file)
        filtered_routes = filter_routes(routes, current_location)
        return jsonify(filtered_routes)
    except Exception as e:
        print(f'Error loading routes for {time_slot}:', e)
        return jsonify([])
    



# Function to load routes data from JSON file
def load_routes_data(filename):
    try:
        with open(filename, 'r') as file:
            routes = json.load(file)
        return routes
    except Exception as e:
        print(f'Error loading routes from {filename}:', e)
        return []

# Function to find a route by route number
def find_route(route_no, time_slot):
    if time_slot not in routes_data:
        return None
    routes = routes_data[time_slot]
    for route in routes:
        if route['route_no'] == route_no:
            return route
    return None

routes_mrng = load_routes_data('routes_mrng.json')
routes_af = load_routes_data('routes_af.json')
routes_sb = load_routes_data('routes_sb.json')

routes_data = {
    'mrng': routes_mrng,
    'af': routes_af,
    'sb': routes_sb
}


# Route to display the page for displaying routes
@app.route('/displayRoutes')
def display_routes_page():
    return render_template('displayRoutes.html')

# Route to handle the POST request for displaying routes
@app.route('/display_routes', methods=['POST'])
def display_routes():
    data = request.get_json()
    route_no = data.get('route_no')
    time_slot = data.get('time_slot')

    route = find_route(route_no, time_slot)
    if route:
        return jsonify([route])  # Returning an array containing the route object
    else:
        return jsonify([])

if __name__ == '__main__':
    app.run()
