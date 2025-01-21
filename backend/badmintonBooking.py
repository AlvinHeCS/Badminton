import requests
from bs4 import BeautifulSoup
import time
import re
from datetime import datetime
from collections import defaultdict
import helperFunctions


# global variables

# NBC
NBCBaseUrl = "https://nbc.yepbooking.com.au/"
NBCUrl = "https://nbc.yepbooking.com.au/ajax/ajax.schema.php" 
NBCName = ["NBC Silverwater", "NBC Seven Hills", "NBC South Granville", "NBC Castle Hill", "NBC Alexandria"]
NBCLocations = ["2b/172 Silverwater Rd, Silverwater NSW 2128", "3/17 Stanton Rd, Seven Hills NSW 2147", "3F/62 Ferndell St, South Granville NSW 2142", "3/16 Anella Ave, Castle Hill NSW 2154", "8/190 Bourke Rd, Alexandria NSW 2015"]
NBCGoogleMaps = ["https://www.google.com/maps/place/NBC+Silverwater/@-33.8297278,151.0463601,17z/data=!3m1!4b1!4m6!3m5!1s0x6b12a4a057af8d55:0x4610331b3c4839a2!8m2!3d-33.8297323!4d151.048935!16s%2Fg%2F1q6cfqnkc?hl=en&entry=ttu&g_ep=EgoyMDI1MDEwNy4wIKXMDSoASAFQAw%3D%3D", "https://www.google.com/maps/place/NBC+Seven+Hills/@-33.7706085,150.9506251,17z/data=!3m2!4b1!5s0x6b12989d2383cd6f:0x32434b9567eb16eb!4m6!3m5!1s0x6b12989d6dc62559:0x4ef989e792603093!8m2!3d-33.770613!4d150.9532!16s%2Fg%2F11c1xjj_v1?hl=en&entry=ttu&g_ep=EgoyMDI1MDEwNy4wIKXMDSoASAFQAw%3D%3D", "https://www.google.com/maps/place/NBC+Granville/@-33.8688954,151.004471,17z/data=!3m1!4b1!4m6!3m5!1s0x6b12bd7942180b8f:0x9ff01957c371c678!8m2!3d-33.8688999!4d151.0070459!16s%2Fg%2F11q24026y9?hl=en&entry=ttu&g_ep=EgoyMDI1MDEwNy4wIKXMDSoASAFQAw%3D%3D", "https://www.google.com/maps/place/NBC+Castle+Hill/@-33.7260253,150.9789682,17z/data=!3m1!4b1!4m6!3m5!1s0x6b12a1b54241fb77:0x8706569ef6ac35b!8m2!3d-33.7260298!4d150.9815431!16s%2Fg%2F11smfhd646?hl=en&entry=ttu&g_ep=EgoyMDI1MDEwNy4wIKXMDSoASAFQAw%3D%3D", "https://www.google.com/maps/place/NBC+Alexandria/@-33.9172217,151.1897761,17z/data=!3m2!4b1!5s0x6b12b1add3036fe5:0x78dd4f4e29552217!4m6!3m5!1s0x6b12b18687e34655:0x5e117607f63d3fa7!8m2!3d-33.9172262!4d151.192351!16s%2Fg%2F11rvcvvqll?hl=en&entry=ttu&g_ep=EgoyMDI1MDEwNy4wIKXMDSoASAFQAw%3D%3D"]
NBCLocationLatLong = ["(-33.829571, 151.048904)", "(-33.770851, 150.952850)", "(-33.863899, 151.010010)", "(-33.726119, 150.981252)", "(-33.905908, 151.201367)"]
NBCLocationImages = ["/NBCSilverwater.jpg", "/NBCSevenHills.jpg", "/NBCGranville.jpg", "/NBCCastleHill.jpg", "/NBCAlexandria.jpg"]
NBCLocationIds = [1,2,4,5,6]

# Alpha
alphaBaseUrl = "https://alphabadminton.yepbooking.com.au/"
alphaUrl = "https://alphabadminton.yepbooking.com.au/ajax/ajax.schema.php"
alphaName = ["Alpha Badminton Centre Slough", "Alpha Badminton Centre Egerton", "Alpha Badminton Centre Auburn"]
alphaLocations = ["47/2 Slough Ave, Silverwater NSW 2128", "46 Egerton St, Silverwater NSW 2128", "Unit 6, Building 2/161 Manchester Rd, Auburn NSW 2144"]
alphaGoogleMaps = ["https://www.google.com/maps/place/Alpha+Badminton+Centre+(Slough)/@-33.8308407,151.0474581,17z/data=!3m2!4b1!5s0x6b12bc8d5d220fb5:0x65d2dad93184697!4m6!3m5!1s0x6b12a4ad006e1723:0x2d069c7e1d2f0156!8m2!3d-33.8308452!4d151.050033!16s%2Fg%2F1q6kk8p46?hl=en&entry=ttu&g_ep=EgoyMDI1MDEwNy4wIKXMDSoASAFQAw%3D%3D","https://www.google.com/maps/place/Alpha+Badminton+Centre+(Egerton)/@-33.8344414,151.0430031,17z/data=!3m1!4b1!4m6!3m5!1s0x6b12a365b5ce9599:0xaf5b3329d6c8ab52!8m2!3d-33.8344459!4d151.045578!16s%2Fg%2F11p_89s47l?hl=en&entry=ttu&g_ep=EgoyMDI1MDEwNy4wIKXMDSoASAFQAw%3D%3D","https://www.google.com/maps/place/Alpha+Badminton+Centre+Auburn/@-33.8454458,151.019012,17z/data=!3m1!4b1!4m6!3m5!1s0x6b12bd9fe93f27f5:0xd6fe1d42d440e244!8m2!3d-33.8454503!4d151.0215869!16s%2Fg%2F11v1973g31?hl=en&entry=ttu&g_ep=EgoyMDI1MDEwNy4wIKXMDSoASAFQAw%3D%3D"]
alphaLocationLatLong = ["(-33.832344, 151.052438)", "(-33.834150, 151.045623)", "(-33.846355, 151.026031)"]
alphaLocationImages = ["/alphaSlough.jpg", "/alphaEgerton.jpg", "/alphaManchester2.png"]
alphaLocationIds = [1,2,3]

# ATC
ATCBaseUrl = "https://australia-badminton-development-centre.yepbooking.com.au/"
ATCUrl = "https://australia-badminton-development-centre.yepbooking.com.au/ajax/ajax.schema.php"
ATCName = ["Australia Badminton Centre Five Dock"]
ATCLocations = ["unit B/131 Parramatta Rd, Five Dock NSW 2046"]
ATCGoogleMaps = ["https://www.google.com/maps/place/ATC+Badminton+Centre/@-33.8700937,151.1170051,17z/data=!3m1!4b1!4m6!3m5!1s0x6b12a5aecefbdd7d:0xc26dc8f71077dc7!8m2!3d-33.8700982!4d151.11958!16s%2Fg%2F11j7k7194_?hl=en&entry=ttu&g_ep=EgoyMDI1MDEwNy4wIKXMDSoASAFQAw%3D%3D"]
ATCLocationImages = ["/ATCFiveDock.jpg"]
ATCLocationLatLong = ["(-33.870441, 151.119598)"]
ATCLocationIds = [3]

# Worx
# Botany
worxBotanyBaseUrl = "https://badmintoncentre-botany.yepbooking.com.au/"
worxBotanyUrl = "https://badmintoncentre-botany.yepbooking.com.au/ajax/ajax.schema.php"
worxBotanyName = ["Badminton Worx Botany"]
worxBotanyLocations = ["Unit 2/30 Sir Joseph Banks St, Botany NSW 2019"]
worxBotanyGoogleMaps = ["https://www.google.com/maps/place/BadmintonWorx+-+Botany/@-33.9495652,151.2003517,17z/data=!3m1!4b1!4m6!3m5!1s0x6b12b13dead7d39d:0x925b3f5725fcc5f0!8m2!3d-33.9495697!4d151.2029266!16s%2Fg%2F11c2kfl3xk?entry=ttu&g_ep=EgoyMDI1MDExNS4wIKXMDSoASAFQAw%3D%3D"]
worxBotanyLocationImages = ["/worxBotany.jpg"]
worxBotanyLocationLatLong = ["(-33.950031, 151.203033)"]
worxBotanyLocationIds = [1]

# Norwest
worxNorwestBaseUrl = "https://badmintonworx-norwest.yepbooking.com.au/"
worxNorwestUrl = "https://badmintonworx-norwest.yepbooking.com.au/ajax/ajax.schema.php"
worxNorwestName = ["Badminton Worx Norwest Building 1", "Badminton Worx Norwest Building 2"]
worxNorwestLocations = ["2/2 Inglewood Pl, Norwest NSW 2153", "2/2 Inglewood Pl, Norwest NSW 2153"]
worxNorwestGoogleMaps = ["https://www.google.com/maps/place/BadmintonWorx+Norwest/@-33.735854,150.9563707,17z/data=!3m2!4b1!5s0x6b12a1fc6334be71:0xcee16ea8bd0a5494!4m6!3m5!1s0x6b12a1b467ba3e39:0x6ec70e335995fc6c!8m2!3d-33.7358585!4d150.9589456!16s%2Fg%2F11fmxj3ck5?entry=ttu&g_ep=EgoyMDI1MDExNS4wIKXMDSoASAFQAw%3D%3D", "https://www.google.com/maps/place/BadmintonWorx+Norwest/@-33.735854,150.9563707,17z/data=!3m2!4b1!5s0x6b12a1fc6334be71:0xcee16ea8bd0a5494!4m6!3m5!1s0x6b12a1b467ba3e39:0x6ec70e335995fc6c!8m2!3d-33.7358585!4d150.9589456!16s%2Fg%2F11fmxj3ck5?entry=ttu&g_ep=EgoyMDI1MDExNS4wIKXMDSoASAFQAw%3D%3D"]
worxNorwestLocationImages = ["/worxNorwest1.jpg", "/worxNorwest2.jpg"]
worxNorwestLocationLatLong = ["(-33.736469, 150.958298)", "(-33.736469, 150.958298)"]
worxNorwestLocationIds = [1, 4]

# Yennora
worxYennoraBaseUrl = "https://badmintoncentre-yennora.yepbooking.com.au/"
worxYennoraUrl = "https://badmintoncentre-yennora.yepbooking.com.au/ajax/ajax.schema.php"
worxYennoraName = ["Badminton Worx Yennora"]
worxYennoraLocations = ["Unit 7 B/26 Nelson Rd, Yennora NSW 2161"]
worxYennoraGoogleMaps = ["https://www.google.com/maps/place/BadmintonWorx+Yennora/@-33.8658291,150.9652316,17z/data=!3m1!4b1!4m6!3m5!1s0x6b12bd973b5439e5:0x9a21c6f43e10c3!8m2!3d-33.8658336!4d150.9678065!16s%2Fg%2F11ryr6mvcv?entry=ttu&g_ep=EgoyMDI1MDExNS4wIKXMDSoASAFQAw%3D%3D"]
worxYennoraLocationImages = ["/worxYennora.jpg"]
worxYennoraLocationLatLong = ["(-33.865341, 150.968246)"]
worxYennoraLocationIds = [1]

# # KBC
KBCBaseUrl = "https://kbcnsw.yepbooking.com.au/"
KBCUrl = "https://kbcnsw.yepbooking.com.au/ajax/ajax.schema.php"
KBCName = ["KBC Rydalmere"]
KBCLocations = ["20 South St, Rydalmere NSW 2116"]
KBCGoogleMaps = ["https://www.google.com/maps/place/KBC+NSW/@-33.8149122,151.0328255,17z/data=!3m1!4b1!4m6!3m5!1s0x6b12a3e5f6791173:0xc50dce1948455b83!8m2!3d-33.8149167!4d151.0354004!16s%2Fg%2F11tfvkplzc?entry=ttu&g_ep=EgoyMDI1MDExNS4wIKXMDSoASAFQAw%3D%3D"]
KBCLocationImages = ["/KBCRydalmere.jpg"]
KBClocationLatLong = ["(-33.814892, 151.035355)"]
KBCLocationIds = [1]


# add badminton company scrappers here
def yepBookingScrapper(baseUrl, url, day, month, locationId):
    # Initialize a session to persist cookies
    session = requests.Session()

    # Simulate a browser visit to establish a session and get initial cookies
    session.get(baseUrl, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    })

    # Set up the URL and parameters for the AJAX request
    params = {
        "day": day,
        "month": month,
        "year": datetime.now().year,
        "id_sport": locationId,
        "event": "pageLoad",
        "tab_type": "normal",
        "timetableWidth": 609,
        "_": int(time.time() * 1000)  # Use dynamic timestamp
    }

    # Headers to simulate a browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Referer": baseUrl,
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest"
    }

    # Perform the AJAX request using the established session
    response = session.get(url, headers=headers, params=params)

    # Check for response status and handle data
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        return(soup.prettify())
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return 1
def rockettoScrapper():
    print("implement this")


# returns location availability for all company locations in a list
def informationForAllLocations(day, month, locationIds, baseUrl, url):
    BookingInfo = []
    for id in locationIds:
        BookingInfo.append(helperFunctions.extract_available_courts(yepBookingScrapper(baseUrl, url, day, month, id)))
    return BookingInfo

# Filter avaliabilites
def yepAvaliabilities(day, month, startTime, endTime, locations, locationLatLong, locationIds, baseUrl, url, noCourts, locationImages, locationNames, locationGoogleMaps):
    # date filter
    if helperFunctions.isDateInPast(day, month):
        print("date is in the past")
        return
    
    # avaliability contains (court No, location, price, location img, name, mapURL, rating) 
    availability = []
    Info = informationForAllLocations(day, month, locationIds, baseUrl, url)
    locationIndex = 0

    for location in Info:
        locationName = locations[locationIndex]
        locationCoord = locationLatLong[locationIndex]
        locationimage = locationImages[locationIndex]
        name = locationNames[locationIndex]
        #rating = helperFunctions.getGoogleStarRating(locationGoogleMaps[locationIndex])
        mapURL = locationGoogleMaps[locationIndex]

        #iterate through courts
        for i in range(len(location) - 1):
            if helperFunctions.isCourtAvailable(helperFunctions.availabilitiesListToDic(location[i]), helperFunctions.timeTo24hr(startTime), helperFunctions.timeTo24hr(endTime)):
                availability.append((i + 1,locationName, locationCoord, str(helperFunctions.getCost(helperFunctions.priceDic(location[len(location) - 1], location[i]), helperFunctions.timeTo24hr(startTime), helperFunctions.timeTo24hr(endTime)) * noCourts), locationimage, name, mapURL))
        locationIndex += 1

    return availability

# Filter by courts
def noCourtsFilter(avaliability, noCourts):
    # Group court counts by location
    location_court_count = defaultdict(set)
    for court_id, location, _, _, _, _, _ in avaliability:
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

# Find avaliabilities for all companies
def findAllAvaliabilities(day, month, startTime, endTime, noCourts):
    
    updated_data = [tup + ("https://nbc.yepbooking.com.au/",) for tup in noCourtsFilter(yepAvaliabilities(day, month, startTime, endTime, NBCLocations, NBCLocationLatLong, NBCLocationIds, NBCBaseUrl, NBCUrl, noCourts, NBCLocationImages, NBCName, NBCGoogleMaps), noCourts)]
    
    updated_data += [tup + ("https://alphabadminton.yepbooking.com.au/",) for tup in noCourtsFilter(yepAvaliabilities(day, month, startTime, endTime, alphaLocations, alphaLocationLatLong, alphaLocationIds, alphaBaseUrl, alphaUrl, noCourts, alphaLocationImages, alphaName, alphaGoogleMaps), noCourts)]

    updated_data += [tup + ("https://australia-badminton-development-centre.yepbooking.com.au/",) for tup in noCourtsFilter(yepAvaliabilities(day, month, startTime, endTime, ATCLocations, ATCLocationLatLong, ATCLocationIds, ATCBaseUrl, ATCUrl, noCourts, ATCLocationImages, ATCName, ATCGoogleMaps), noCourts)]

    updated_data += [tup + ("https://badmintoncentre-botany.yepbooking.com.au/", ) for tup in noCourtsFilter(yepAvaliabilities(day, month, startTime, endTime, worxBotanyLocations, worxBotanyLocationLatLong, worxBotanyLocationIds, worxBotanyBaseUrl, worxBotanyUrl, noCourts, worxBotanyLocationImages, worxBotanyName, worxBotanyGoogleMaps), noCourts)]

    updated_data += [tup + ("https://badmintonworx-norwest.yepbooking.com.au/", ) for tup in noCourtsFilter(yepAvaliabilities(day, month, startTime, endTime, worxNorwestLocations, worxNorwestLocationLatLong, worxNorwestLocationIds, worxNorwestBaseUrl, worxNorwestUrl, noCourts, worxNorwestLocationImages, worxNorwestName, worxNorwestGoogleMaps), noCourts)]

    updated_data += [tup + ("https://badmintoncentre-yennora.yepbooking.com.au/", ) for tup in noCourtsFilter(yepAvaliabilities(day, month, startTime, endTime, worxYennoraLocations, worxYennoraLocationLatLong, worxBotanyLocationIds, worxYennoraBaseUrl, worxYennoraUrl, noCourts, worxYennoraLocationImages, worxYennoraName, worxYennoraGoogleMaps), noCourts)]

    updated_data += [tup + ("https://kbcnsw.yepbooking.com.au/", ) for tup in noCourtsFilter(yepAvaliabilities(day, month, startTime, endTime, KBCLocations, KBClocationLatLong, KBCLocationIds, KBCBaseUrl, KBCUrl, noCourts, KBCLocationImages, KBCName, KBCGoogleMaps), noCourts)]
    return updated_data

def sortByDistance(destination, avaliabilities):
    destination_lat, destination_lng = destination['lat'], destination['lng']
    
    # Create a new list with distances calculated
    augmented_list = []
    for tup in avaliabilities:
        # Convert address to latitude and longitude
        latLong = helperFunctions.stringToLatLong(tup[2])
        # Calculate the distance
        distance = helperFunctions.haversine_distance(destination_lat, destination_lng, latLong['lat'], latLong['lng'])
        augmented_list.append((tup, distance))
    
    # Sort the list based on distance
    sorted_list = sorted(augmented_list, key=lambda x: x[1])
    
    # Return only the original tuples, now sorted by distance
    return [tup[0] for tup in sorted_list]

# you cannot book 362 days in advanced otherwise u get an error from the websites

#print(helperFunctions.aggregateCourts(sortByDistance(helperFunctions.stringToLatLong("(-33.849602, 151.032745)"), findAllAvaliabilities(23, 1, "10:00pm", "11:00pm", 2))))

#print(yepAvaliabilities(23, 1, "10:00pm",  "11:00pm", worxBotanyLocations, worxBotanyLocationLatLong, worxBotanyLocationIds, worxBotanyBaseURL, worxBotanyURL, 1, worxBotanyLocationImages, worxBotanyName, worxBotanyGoogleMaps))
#yepAvaliabilities(day, month, startTime, endTime, alphaLocations, alphaLocationLatLong, alphaLocationIds, alphaBaseUrl, alphaUrl, noCourts, alphaLocationImages, alphaName, alphaGoogleMaps)
#print(helperFunctions.extract_available_courts(yepBookingScrapper(worxNorwestBaseUrl, worxNorwestUrl, 22, 1, 1)))
# helperFunctions.aggregateCourts
print(helperFunctions.aggregateCourts(sortByDistance(helperFunctions.stringToLatLong("(-33.849602, 151.032745)"), findAllAvaliabilities(22, 1, "2:00pm", "3:00pm", 2))))
#print(yepAvaliabilities(22, 1, "2:00pm",  "3:00pm", worxNorwestLocations, worxNorwestLocationLatLong, worxNorwestLocationIds, worxNorwestBaseUrl, worxNorwestUrl, 1, worxNorwestLocationImages, worxNorwestName, worxNorwestGoogleMaps))