import requests
from bs4 import BeautifulSoup
import time
import re
from datetime import datetime, timedelta
from collections import defaultdict
import googlemaps
import math


# fixes table row structure in html
def fix_tr_structure(html):
    tr_matches = re.findall(r'(<tr.*?>.*?)(?=<tr|$)', html, re.DOTALL)
    
    fixed_rows = [f"{match}</tr>\n" if not match.endswith("</tr>") else match for match in tr_matches]
    
    fixed_html = ''.join(fixed_rows)
    
    lines = fixed_html.split('\n')  
    trimmed_lines = lines[:-6]  
    return '\n'.join(trimmed_lines)  

def extract_available_courts(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract all rows
    tables = soup.find_all('table')
    courtsId = tables[0]
    bookings = tables[1]
    courtAvailability = bookings.find_all('tr')
    tmp = fix_tr_structure(courtAvailability[2].prettify())
    new_soup = BeautifulSoup(tmp, 'html.parser')
    
    data = []
    rows = new_soup.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        titles = []
        for cell in cells:
            title = cell.get('title')  
            if not title:
                title = cell.get_text(strip=True)
            if title == "": 
                aTag = cell.find('a')
                title = aTag.get('title')
            titles.append(title)
        data.append(titles)
    for i, court in enumerate(data):
        data[i] = formatClosed(court)

    return data

def split_closed_slot(slot):
    start, end = slot.split('–')[0], slot.split(' ')[0].split('–')[1]
    start_time = datetime.strptime(start, "%I:%M%p")
    end_time = datetime.strptime(end, "%I:%M%p")
    
    closed_slots = []
    while start_time < end_time:
        next_time = start_time + timedelta(hours=1)
        if next_time > end_time:
            next_time = end_time
        closed_slots.append(f"{start_time.strftime('%I:%M%p').lstrip('0').lower()}–{next_time.strftime('%I:%M%p').lstrip('0').lower()} - Closed")
        start_time = next_time
    
    return closed_slots

def formatClosed(timeSlots):
    result = []
    for slot in timeSlots:
        if "Closed" in slot:
            result.extend(split_closed_slot(slot))
        else:
            result.append(slot)
    return result

# returns {startTime:Avaliability}
def availabilitiesListToDic(locationAvailabilities):
    availabilityDic = {}
    for slot in locationAvailabilities:
        time_range, status = slot.split(" - ")
        start, _ = time_range.split("–")       
        availabilityDic[timeTo24hr(start)] = status.strip()
    return availabilityDic

# returns {startTime:Price}
def priceDic(price, locationAvailabability):
    prices = {}
    priceIndex = 0
    for slot in locationAvailabability:
        time_range, _ = slot.split(" - ")
        start, _ = time_range.split("–")
        prices[timeTo24hr(start)] = int(price[priceIndex].strip("$"))
        priceIndex += 1
    return prices



def timeTo24hr(time):
    time_24_hour = datetime.strptime(time, "%I:%M%p").strftime("%H:%M")
    return time_24_hour

# returns if a court is available at the location that fits time range
def isCourtAvailable(courtInfo, startTime, endTime):
    # Create the range of times for the requested reservation
    currentTime = startTime
    while currentTime != endTime:
        
        if courtInfo.get(currentTime.upper(), None) != "Available":
            return False
        currentTime = increment_time(currentTime)

    return True

# returns cost of time range played
def getCost(price, startTime, endTime):
    total = 0
    currentTime = startTime
    while currentTime != endTime:
        total += price[currentTime]
        currentTime = increment_time(currentTime)
    return total

# increments string time by 1 hr
def increment_time(time_str):
    time_obj = datetime.strptime(time_str, "%H:%M")
    new_time = time_obj + timedelta(hours=1)
    return new_time.strftime("%H:%M")

def isDateInPast(day, month):
    day = int(day)
    month = int(month)
    today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    givenDate = datetime(today.year, month, day)
    return givenDate < today

def noCourtsFilter(avaliability, noCourts):
    # Group court counts by location
    location_court_count = defaultdict(set)
    for court_id, location, _ in avaliability:
        location_court_count[location].add(court_id)
    
    # Find locations that meet the required number of courts
    valid_locations = {
        location for location, courts in location_court_count.items()
        if len(courts) >= noCourts
    }
    
    # Filter the court list to include only valid locations
    filtered_court_list = [
        court for court in avaliability if court[1] in valid_locations
    ]
    
    return filtered_court_list


# # convert address to latitude and longitude
# def addressToLatLong(address):
#     gmaps = googlemaps.Client(key='AIzaSyDHvhgM8GiUP42zy_7qPfmEFMm1xEGqbTA')

#     # Geocoding the address
#     geocode_result = gmaps.geocode(address)

#     if geocode_result:
#         location = geocode_result[0]['geometry']['location']
#         return location
    
#     else:
#         print("Address not found.")
#         return


def stringToLatLong(coord_string):
    # Remove the parentheses and split the string by comma
    coord_string = coord_string.strip("()")
    lat, lng = map(float, coord_string.split(", "))

    # Return the dictionary with 'lat' and 'lng' keys
    return {'lat': lat, 'lng': lng}

def haversine_distance(lat1, lng1, lat2, lng2):
    """
    Calculate the great-circle distance between two points on the Earth.
    """
    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert degrees to radians
    lat1, lng1, lat2, lng2 = map(math.radians, [lat1, lng1, lat2, lng2])

    # Differences
    dlat = lat2 - lat1
    dlng = lng2 - lng1

    # Haversine formula
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c  # Distance in kilometers


def aggregateCourts(data):
    combined = defaultdict(lambda: {'court_ids': '', 'latlong': '', 'price': 0, 'url': ''})

    for court_id, address, latlong, price, url, image, name, mapsURL in data:
        if combined[address]['court_ids']:
            combined[address]['court_ids'] += f", {court_id}"
        else:
            combined[address]['court_ids'] = str(court_id)
        combined[address]['latlong'] = latlong
        combined[address]['price'] = price
        combined[address]['url'] = url
        combined[address]['image'] = image
        combined[address]['name'] = name
        combined[address]['mapsURL'] = mapsURL
        #combined[address]['rating'] = rating

    return [(value['court_ids'], address, value['latlong'], value['price'], value['url'], value['image'], value['name'], value['mapsURL']) for address, value in combined.items()]

def getGoogleStarRating(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers, stream=True)
    for line in response.iter_lines(decode_unicode=True):
        if "★★★★★" in line:
            return 5
        if "★★★★☆" in line:
            return 4
        if "★★★☆☆" in line:
            return 3
        if "★★☆☆☆" in line:
            return 2
        if "★☆☆☆☆" in line:
            return 1
        if "☆☆☆☆☆" in line:
            return 0

print(getGoogleStarRating("https://www.google.com/maps/place/NBC+Castle+Hill/@-33.7260253,150.9789682,17z/data=!3m1!4b1!4m6!3m5!1s0x6b12a1b54241fb77:0x8706569ef6ac35b!8m2!3d-33.7260298!4d150.9815431!16s%2Fg%2F11smfhd646?hl=en&entry=ttu&g_ep=EgoyMDI1MDEwNy4wIKXMDSoASAFQAw%3D%3D"))