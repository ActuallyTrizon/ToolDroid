import os
import json
import time
import sys
import subprocess

def run_shizuku_cmd(cmd):
    try:
        result = subprocess.check_output(['rish', '-c', cmd], stderr=subprocess.DEVNULL)
        return result.decode('utf-8')
    except:
        return None

def get_stats():
    battery_raw = os.popen("termux-battery-status").read().strip()
    if not battery_raw:
        return "\033[91mError: Termux:API not detected.\033[0m"
    
    base = json.loads(battery_raw)
    temp = base.get('temperature', 0)
    
    shizuku_active = False
    max_cap, curr_cap, health_pct = "N/A", "N/A", "N/A"
    adv_raw = run_shizuku_cmd("dumpsys battery")
    
    if adv_raw:
        shizuku_active = True
        for line in adv_raw.split('\n'):
            if "Charge counter" in line:
                curr_cap = int(line.split(":")[1].strip()) // 1000 
            if "Full charge capacity" in line:
                max_cap = int(line.split(":")[1].strip()) // 1000
        
        if isinstance(max_cap, int) and max_cap > 0:
            health_pct = f"{(max_cap / 5200) * 100:.1f}%"

    out = [
        "\033[2J\033[H",
        "\033[1;34m--- DroidPulse v1.5.2 by Trizon ---\033[0m",
        f"Charging State:  {base.get('status')} ({base.get('percentage')}%)",
        "-----------------------------------",
        "\033[1;36m[DEFAULT MONITOR]\033[0m",
        f"Health (OS):     {base.get('health').upper()}",
        f"Temperature:     {temp}°C",
        f"Current:         {base.get('current', 0)} mA",
        "-----------------------------------"
    ]

    if shizuku_active:
        out += [
            "\033[1;35m[SHIZUKU FEATURES]\033[0m",
            f"Health (Exact):  {health_pct}",
            f"Max Capacity:    {max_cap} mAh",
            f"Current Charge:  {curr_cap} mAh",
            "-----------------------------------"
        ]
    else:
        out += ["\033[2mShizuku features disabled\033[0m", "-----------------------------------"]

    out.append("Updating every 2s... (Ctrl+C to Exit)")
    return "\n".join(out)

if __name__ == "__main__":
    try:
        while True:
            sys.stdout.write(get_stats())
            sys.stdout.flush()
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n\n\033[1;31mMonitor Offline.\033[0m")
