from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import logging
import badmintonBooking
import helperFunctions

app = Flask(__name__, static_folder='static')
CORS(app)

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
            #"rating": court[7]
        }
        for court in raw_data
    ]
    return structured_data

# Serve the React app
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and path is not None and app.static_folder:
        # If the file exists in the static folder, serve it
        return send_from_directory(app.static_folder, path)
    # Otherwise, serve index.html
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/search', methods=['POST'])
def search_courts():
    data = request.json
    location = data.get('location', '').lower()
    start_time = data.get('startTime', '')
    end_time = data.get('endTime', '')
    noCourts = data.get('courts', 1)
    month = data.get('month')
    day = data.get('day')
    response_data = convertToDic(
        helperFunctions.aggregateCourts(
            badmintonBooking.sortByDistance(
                helperFunctions.stringToLatLong(location), 
                badmintonBooking.findAllAvaliabilities(day, month, str(start_time), str(end_time), int(noCourts))
            )
        )
    )
    print(response_data)

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
