import sys
from cores.engine import ToolDroidEngine

if __name__ == "__main__":
    try:
        app = ToolDroidEngine()
        app.load_cogs()
        app.run()
    except Exception as e:
        print(f"Fatal Error: {e}")
        sys.exit(1)
