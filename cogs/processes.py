import time
from cores.shizuku import ShizukuBridge

class ProcessesCog:
    def __init__(self, engine):
        self.engine = engine
        self.last_check = 0
        self.cached_data = []

    def render(self):
        c = self.engine.colors
        curr_time = time.time()
        
        if curr_time - self.last_check > 5 or not self.cached_data:
            raw_ps = ShizukuBridge.execute("ps -A -o NAME,%CPU --sort=-%CPU 2>/dev/null | head -n 4")
            lines = [f"{c['core']}[ TOP PROCESSES ]{c['end']}"]
            
            if raw_ps:
                procs = raw_ps.split('\n')
                for p in procs[1:]:
                    if p.strip():
                        lines.append(f"  {p.strip()[:33]}")
            else:
                lines.append("  Process list restricted or unavailable.")
                
            self.cached_data = lines
            self.last_check = curr_time
            
        return self.cached_data
