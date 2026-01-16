import requests

def get_loc():
    data = requests.get("https://ipinfo.io/json").json()
    lat, lon = data['loc'].split(",")
    return (lat, lon)
get_loc()