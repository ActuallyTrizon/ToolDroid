import os
import subprocess

class ShizukuBridge:
    @staticmethod
    def execute(command: str) -> str | None:
        """
        Executes a shell command with root/Shizuku privileges via global 'rish'.
        Passes RISH_APPLICATION_ID and sets working directory to Termux home.
        """
        try:
            env = os.environ.copy()
            env["RISH_APPLICATION_ID"] = "com.termux"
            
            result = subprocess.run(
                ['rish', '-c', command],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=5,
                env=env,
                cwd=os.path.expanduser("~")
            )
            if result.returncode == 0:
                return result.stdout.strip()
            return None
        except Exception:
            return None
