from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
import logging
import badmintonBooking
import helperFunctions
import os

app = Flask(__name__, static_folder='../frontend/build', template_folder='../frontend/build')
CORS(app)

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set to INFO to capture general logs
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Suppress Flask's built-in static file logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.WARNING)


def convertToDic(raw_data):
    # Convert tuples to list of dictionaries
    structured_data = [
        {
            "courtNos": court[0],
            "address": court[1],
            "price": court[4],
            "URL": court[5],
            "image": court[6],
            "name": court[2],
            "mapsURL": court[7],
            # "rating": court[7]
        }
        for court in raw_data
    ]
    return structured_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory(os.path.join(app.static_folder, 'static'), path)

@app.route('/<path:path>')
def serve_build_files(path):
    try:
        # Try to serve the requested file
        return send_from_directory(app.static_folder, path)
    except:
        # If file is not found, serve the React app (SPA fallback)
        return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search_courts():
    # Extract and log search parameters
    data = request.json
    location = data.get('location', '').lower()
    start_time = data.get('startTime', '')
    end_time = data.get('endTime', '')
    noCourts = data.get('courts', 1)
    month = data.get('month')
    day = data.get('day')

    logging.info("Search parameters received: location=%s, start_time=%s, end_time=%s, noCourts=%d, month=%s, day=%s",
                 location, start_time, end_time, noCourts, month, day)

    # Call helper functions to process the request
    response_data = convertToDic(
        helperFunctions.aggregateCourts(
            badmintonBooking.sortByDistance(
                helperFunctions.stringToLatLong(location),
                badmintonBooking.findAllAvaliabilities(day, month, str(start_time), str(end_time), int(noCourts))
            )
        )
    )

    # Log the search results
    logging.info("Search results: %s", response_data)

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
