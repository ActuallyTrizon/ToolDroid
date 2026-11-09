import time
from cores.shizuku import ShizukuBridge

class CpuCog:
    def __init__(self, engine):
        self.engine = engine
        self.last_check = 0
        self.cached_data = None

    def render(self):
        c = self.engine.colors
        curr_time = time.time()
        
        if curr_time - self.last_check > 3 or self.cached_data is None:
            thermal_raw = ShizukuBridge.execute("cat /sys/class/thermal/thermal_zone*/temp 2>/dev/null | head -n 3")
            cpu_info = ShizukuBridge.execute("dumpsys cpuinfo | head -n 3")
            
            lines = [f"{c['core']}[ CPU & THERMAL MONITOR ]{c['end']}"]
            
            if thermal_raw:
                temps = []
                for t in thermal_raw.split('\n'):
                    if t.strip().isdigit():
                        val = int(t.strip())
                        if val > 1000: val //= 1000
                        temps.append(f"{val}°C")
                if temps:
                    lines.append(f"Thermal Zones: {' | '.join(temps)}")
                else:
                    lines.append("Thermal Zones: Reading...")
            else:
                lines.append("Thermal Zones: Unavailable")
                
            if cpu_info:
                first_line = cpu_info.split('\n')[0] if cpu_info else "Active"
                lines.append(f"CPU Load: {first_line[:32]}")
            else:
                lines.append("CPU Load: Unavailable")
                
            self.cached_data = lines
            self.last_check = curr_time
            
        return self.cached_data
