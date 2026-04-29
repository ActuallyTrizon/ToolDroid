import os
import json
import time
import sys

def get_stats():
    try:
        # Fetching data from Termux API
        battery_raw = os.popen("termux-battery-status").read().strip()
        
        if not battery_raw:
            return "\033[91mError: Ensure Termux:API app is installed and battery optimization is off for it.\033[0m"
        
        data = json.loads(battery_raw)
        
        # ANSI escape codes for colors and UI
        # \033[2J\033[H clears screen and moves cursor to top
        output = (
            "\033[2J\033[H" 
            "\033[1;34m--- DroidPulse Hardware Monitor ---\033[0m\n"
            f"Device Status:  \033[1;32mONLINE\033[0m\n"
            f"Battery Level:  {data.get('percentage') or '?'}% \n"
            f"Temperature:    {data.get('temperature') or '?'}°C\n"
            f"Power State:    {data.get('status') or 'Unknown'}\n"
            f"Battery Health: {data.get('health') or 'Unknown'}\n"
            "-----------------------------------\n"
            "Updating every 2s... (Ctrl+C to Stop)"
        )
        return output
    except Exception as e:
        return f"\033[91mCritial Error: {str(e)}\033[0m"

if __name__ == "__main__":
    print("\033[1;33mConnecting to Honor X6b Hardware...\033[0m")
    try:
        while True:
            sys.stdout.write(get_stats())
            sys.stdout.flush()
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n\n\033[1;31mMonitor Disconnected.\033[0m")
