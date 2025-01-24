from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
import logging
import badmintonBooking
import helperFunctions
import os

app = Flask(__name__, static_folder='../frontend/build/static', template_folder='../frontend/build')
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

@app.route('/')
def index():
    return render_template('index.html')


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
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
