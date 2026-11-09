import subprocess

class ShizukuBridge:
    @staticmethod
    def execute(command: str) -> str | None:
        """
        Executes a shell command with root/Shizuku privileges via global 'rish'.
        Returns stdout as a string, or None if it fails.
        """
        try:
            result = subprocess.run(
                ['rish', '-c', command],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return result.stdout.strip()
            return None
        except Exception:
            return None
