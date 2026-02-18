from flask import Flask, render_template, jsonify, request
import random
import math

app = Flask(__name__)

# Collection of interesting locations around the world (lat, lng)
# All locations verified to have Street View coverage
LOCATIONS = [
    {"lat": 48.8584, "lng": 2.2945, "name": "Eiffel Tower, Paris"},
    {"lat": 40.7580, "lng": -73.9855, "name": "Times Square, New York"},
    {"lat": 35.6586, "lng": 139.7454, "name": "Tokyo Shibuya Crossing, Japan"},
    {"lat": 51.5007, "lng": -0.1246, "name": "Big Ben, London"},
    {"lat": -33.8568, "lng": 151.2153, "name": "Sydney Opera House"},
    {"lat": 55.7539, "lng": 37.6208, "name": "Red Square, Moscow"},
    {"lat": 41.8902, "lng": 12.4922, "name": "Colosseum, Rome"},
    {"lat": 25.1972, "lng": 55.2744, "name": "Burj Khalifa, Dubai"},
    {"lat": 37.9715, "lng": 23.7267, "name": "Acropolis, Athens"},
    {"lat": -22.9519, "lng": -43.2105, "name": "Christ the Redeemer, Rio"},
    {"lat": 43.7230, "lng": 10.3966, "name": "Leaning Tower of Pisa"},
    {"lat": 1.2868, "lng": 103.8545, "name": "Marina Bay, Singapore"},
    {"lat": 52.5162, "lng": 13.3777, "name": "Brandenburg Gate, Berlin"},
    {"lat": 37.8199, "lng": -122.4783, "name": "Golden Gate Bridge, SF"},
    {"lat": -34.6037, "lng": -58.3816, "name": "Buenos Aires Obelisk"},
    {"lat": 41.4036, "lng": 2.1744, "name": "Sagrada Familia, Barcelona"},
    {"lat": 48.8606, "lng": 2.3376, "name": "Notre-Dame, Paris"},
    {"lat": 40.4319, "lng": -3.6928, "name": "Puerta del Sol, Madrid"},
    {"lat": 45.4408, "lng": 12.3155, "name": "St Mark's Square, Venice"},
    {"lat": 34.1016, "lng": -118.3416, "name": "Hollywood Sign, LA"},
    {"lat": 51.1789, "lng": -1.8262, "name": "Stonehenge, UK"},
    {"lat": 29.9792, "lng": 31.1342, "name": "Great Pyramid of Giza"},
    {"lat": 40.6892, "lng": -74.0445, "name": "Statue of Liberty, NYC"},
    {"lat": 38.8977, "lng": -77.0365, "name": "Washington Monument"},
    {"lat": 43.0731, "lng": -89.4012, "name": "Wisconsin State Capitol"},
]

current_location = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/new-location')
def new_location():
    global current_location
    current_location = random.choice(LOCATIONS)
    # Return location without revealing too much, but include name for display after guess
    return jsonify({
        "lat": current_location["lat"],
        "lng": current_location["lng"],
        "name": current_location.get("name", "Unknown Location")
    })

@app.route('/api/check-guess', methods=['POST'])
def check_guess():
    data = request.json
    guess_lat = data['lat']
    guess_lng = data['lng']
    
    if current_location is None:
        return jsonify({"error": "No active location"}), 400
    
    # Calculate distance using Haversine formula
    distance = calculate_distance(
        current_location['lat'], current_location['lng'],
        guess_lat, guess_lng
    )
    
    # Calculate score (max 5000 points)
    # Score decreases exponentially with distance
    # Perfect score if within 1km, 0 if over 2000km
    if distance < 1:
        score = 5000
    elif distance > 2000:
        score = 0
    else:
        # Exponential decay
        score = int(5000 * math.exp(-distance / 500))
    
    return jsonify({
        "distance": round(distance, 2),
        "score": score,
        "actual_location": {
            "lat": current_location['lat'],
            "lng": current_location['lng'],
            "name": current_location['name']
        }
    })

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two points on Earth using Haversine formula.
    Returns distance in kilometers.
    """
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = (math.sin(delta_lat / 2) ** 2 +
         math.cos(lat1_rad) * math.cos(lat2_rad) *
         math.sin(delta_lon / 2) ** 2)
    c = 2 * math.asin(math.sqrt(a))
    
    distance = R * c
    return distance

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
