import requests

def get_loc():
    data = requests.get("https://ipinfo.io/json").json()
    lat, lon = data['loc'].split(",")
    print(lat, lon)
    return 22,77
get_loc()