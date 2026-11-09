import os
import json
import time
from cores.shizuku import ShizukuBridge

class BatteryCog:
    def __init__(self, engine):
        self.engine = engine
        self.design_capacity = 5200  # Change to your phone's design capacity if needed
        self.last_hw_check = 0
        self.cached_hw = None

    def fetch_api_data(self):
        try:
            raw = os.popen("termux-battery-status").read().strip()
            return json.loads(raw) if raw else None
        except:
            return None

    def fetch_hw_data(self):
        curr_time = time.time()
        if curr_time - self.last_hw_check > 2 or self.cached_hw is None:
            raw_dump = ShizukuBridge.execute("dumpsys battery")
            if raw_dump:
                adv = {}
                for line in raw_dump.split('\n'):
                    if ":" in line:
                        k, v = line.split(":", 1)
                        adv[k.strip().lower()] = v.strip()
                self.cached_hw = adv
                self.last_hw_check = curr_time
        return self.cached_hw

    def render(self):
        api = self.fetch_api_data()
        hw = self.fetch_hw_data()
        
        c = self.engine.colors
        if not api:
            return [f"{c['fail']}ERROR: Termux API Unreachable{c['end']}"]

        pct = api.get('percentage', 0)
        temp = api.get('temperature', 0)
        current_ma = api.get('current', 0)

        lines = [
            f"State:  {api.get('status')} ({pct}%)",
            f"{c['core']}[ DEFAULT MONITOR ]{c['end']}",
            f"Temperature:  {temp}°C",
            f"Current:    {current_ma} mA",
        ]

        if hw:
            try:
                f_cap_raw = hw.get('full charge capacity') or hw.get('charge full')
                f_cap = int(f_cap_raw) if f_cap_raw else 0
                if f_cap > 20000: f_cap //= 1000
                
                max_val = f_cap if f_cap > 0 else self.design_capacity
                health_val = (max_val / self.design_capacity) * 100
                
                lines += [
                    f"{c['shizuku']}[ SHIZUKU MONITOR ]{c['end']}",
                    f"Battery Health:      {health_val:.1f}%",
                    f"Listed Capacity:     {max_val} mAh"
                ]
            except:
                lines += [f"{c['fail']}Shizuku: Parsing error...{c['end']}"]
        else:
            lines += [f"\033[2mShizuku: Not Authorized / Offline\033[0m"]

        return lines
