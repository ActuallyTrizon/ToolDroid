import time
from cores.shizuku import ShizukuBridge

class NetworkCog:
    def __init__(self, engine):
        self.engine = engine
        self.last_check = 0
        self.cached_data = []

    def render(self):
        c = self.engine.colors
        curr_time = time.time()
        
        if curr_time - self.last_check > 4 or not self.cached_data:
            net_raw = ShizukuBridge.execute("ip route show 2>/dev/null | head -n 2")
            lines = [f"{c['core']}[ NETWORK MONITOR ]{c['end']}"]
            
            if net_raw:
                for line in net_raw.split('\n'):
                    if line.strip():
                        lines.append(f"  {line.strip()[:33]}")
            else:
                lines.append("  Network status: Connected")
                
            self.cached_data = lines
            self.last_check = curr_time
            
        return self.cached_data
