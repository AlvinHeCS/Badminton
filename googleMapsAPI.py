import googlemaps

# Replace 'YOUR_API_KEY' with your Google Maps API key
gmaps = googlemaps.Client(key='AIzaSyDHvhgM8GiUP42zy_7qPfmEFMm1xEGqbTA')

# Address to geocode
address = "Lidcombe" + " ,Sydney"

# Geocoding the address
geocode_result = gmaps.geocode(address)

if geocode_result:
    location = geocode_result[0]['geometry']['location']
    print(f"Latitude: {location['lat']}, Longitude: {location['lng']}")
else:
    print("Address not found.")
