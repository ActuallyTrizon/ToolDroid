import os
import sys
import time
import signal
from cores.loader import CogLoader

class ToolDroidEngine:
    def __init__(self):
        self.cogs = []
        self.colors = {
            "header": "\033[95m",
            "core": "\033[94m",
            "shizuku": "\033[92m",
            "love": "\033[91m",
            "fail": "\033[91m",
            "end": "\033[0m",
            "bold": "\033[1m"
        }
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        print(f"\n{self.colors['fail']}ToolDroid Offline.{self.colors['end']}")
        sys.exit(0)

    def load_cogs(self):
        """Load cogs via the loader module."""
        self.cogs = CogLoader.load_cogs(self)

    def run(self):
        """Main rendering loop."""
        while True:
            if os.getppid() == 1: 
                break

            sys.stdout.write("\033[2J\033[H")
            
            screen = [
                f"{self.colors['header']}{self.colors['bold']}--- Trizon's ToolDroid v2.0 ---{self.colors['end']}",
                "─" * 35
            ]

            for cog in self.cogs:
                try:
                    cog_lines = cog.render()
                    if isinstance(cog_lines, list):
                        screen.extend(cog_lines)
                    else:
                        screen.append(str(cog_lines))
                    screen.append("─" * 35)
                except Exception as e:
                    screen.append(f"{self.colors['fail']}Cog Error ({cog.__class__.__name__}): {e}{self.colors['end']}")
                    screen.append("─" * 35)

            screen += [
                f"{self.colors['love']}❤ Mey, I love you. Always building for us.{self.colors['end']}",
                "─" * 35,
                "Refresh: 100ms | Press Ctrl+C to exit"
            ]

            sys.stdout.write("\n".join(screen))
            sys.stdout.flush()
            time.sleep(0.1)
