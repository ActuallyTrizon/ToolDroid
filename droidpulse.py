import os
import json
import time

def get_stats():
battery data
    battery = os.popen("termux-battery-status").read()
    data = json.loads(battery)
    
    print("\033[H\033[J")
    print(f"--- DroidPulse Monitor ---")
    print(f"Battery Level: {data['percentage']}%")
    print(f"Temperature:   {data['temperature']}°C")
    print(f"Status:        {data['status']}")
    print(f"Health:        {data['health']}")
    print("--------------------------")

while True:
    get_stats()
    time.sleep(2)
