import os
import json
import time
import sys
import subprocess

def run_shizuku_cmd(cmd):
    """Executes a command via Shizuku's rish shell."""
    try:
        # We use rish -c to run a single command via Shizuku
        result = subprocess.check_output(['rish', '-c', cmd], stderr=subprocess.DEVNULL)
        return result.decode('utf-8')
    except:
        return None

def get_stats():
    # 1. Get Basic Stats from Termux API
    battery_raw = os.popen("termux-battery-status").read().strip()
    if not battery_raw:
        return "\033[91mError: Install/Open Termux:API app\033[0m"
    
    base_data = json.loads(battery_raw)
    
    # 2. Try to get Advanced Stats via Shizuku
    shizuku_active = False
    max_cap = "N/A"
    curr_cap = "N/A"
    health_pct = "N/A"
    
    # dumpsys battery contains the raw hardware registers
    adv_raw = run_shizuku_cmd("dumpsys battery")
    
    if adv_raw:
        shizuku_active = True
        for line in adv_raw.split('\n'):
            if "Charge counter" in line:
                # current mAh
                curr_cap = int(line.split(":")[1].strip()) // 1000 
            if "Full charge capacity" in line:
                # max mAh
                max_cap = int(line.split(":")[1].strip()) // 1000
        
        if isinstance(max_cap, int) and max_cap > 0:
            # Simple health calc: (Current Max / Design Capacity)
            # Note: 5000 is typical for Honor X6b, adjust if needed
            health_pct = f"{(max_cap / 5200) * 100:.1f}%" 

    # UI Output
    output = [
        "\033[2J\033[H",
        "\033[1;34m--- DroidPulse Hardware Monitor ---\033[0m",
        f"Shizuku Status:  {'✅ Authorized' if shizuku_active else '❌ Not Detected'}",
        f"Battery Level:   {base_data.get('percentage')}%",
        f"Temperature:     {base_data.get('temperature')}°C",
        f"Power Current:   {base_data.get('current', 'N/A')} mA",
        "-----------------------------------",
        f"Health (Actual): {health_pct}",
        f"Max Capacity:    {max_cap} mAh",
        f"Current Charge:  {curr_cap} mAh",
        "-----------------------------------",
        "Updating every 2s... (Ctrl+C to Stop)"
    ]
    return "\n".join(output)

if __name__ == "__main__":
    # Check for rish installation first
    if not os.path.exists("/data/data/com.termux/files/usr/bin/rish"):
        print("\033[1;33mHint: To see Max Capacity, install 'shizuku' and 'rish' in Termux.\033[0m")
    
    try:
        while True:
            sys.stdout.write(get_stats())
            sys.stdout.flush()
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n\n\033[1;31mMonitor Disconnected.\033[0m")
