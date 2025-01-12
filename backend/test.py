import requests

url = "https://roketto.sportlogic.net.au/secure/customer/booking/v1/public/fetch-booking-details"
cookies = {
    "JSESSIONID": "8B5121C950F7CA8AE21C51C3AB9726DC",
    "_gid": "GA1.3.1744344730.1736581732",
    "_ga": "GA1.1.594019486.1734870988",
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}

response = requests.get(url, headers=headers, cookies=cookies)

if response.status_code == 200:
    try:
        # Attempt to parse JSON
        data = response.json()
        print("Booking Details:", data)
    except requests.exceptions.JSONDecodeError:
        # Handle non-JSON response
        print("Non-JSON Response:")
        print(response.text)
else:
    print(f"Request failed with status code {response.status_code}")
    print("Response Content:", response.text)
