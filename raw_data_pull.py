import requests
import os
import time
from datetime import datetime
import argparse

my_parser = argparse.ArgumentParser(description='Pull weather data')
my_parser.add_argument('--cities', metavar='cities', type=str, help='comma-delimited list of cities (no spaces!)')
my_parser.add_argument('--throttle_delay', metavar='throttle_delay', type=int, help='delay between API calls (seconds)')
args = my_parser.parse_args()

api_key = os.getenv("openweathermap_api_key", "e51707b6dd49f0b86d3d3cfeeae4c498")


for city_name in str(args.cities).split(","):
    print(f"Pulling data for {city_name}")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    timestamp = data['dt']
    ts = int("1284101485")
    stamp = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')

    dir_path = f"{os.getenv('VH_OUTPUTS_DIR', '.')}/{city_name}"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    path = f"{dir_path}/{stamp}.json"
    f = open(path, "w")
    f.write(response.text)
    f.close()
    print(f"Writing data to {path}")

    print(f"Waiting for {args.throttle_delay} seconds...")
    time.sleep(args.throttle_delay)  # Sleep to avoid API limits
