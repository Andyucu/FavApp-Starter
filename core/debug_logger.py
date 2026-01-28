"""Debug logging utility for FavApp Starter."""

import os
import sys
from datetime import datetime
from typing import Optional


class DebugLogger:
    """Logger that writes debug messages to a file."""

    _instance: Optional['DebugLogger'] = None
    _log_file_path: Optional[str] = None
    _log_file = None

    @classmethod
    def get_instance(cls) -> 'DebugLogger':
        """Get or create the singleton logger instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        """Initialize the logger."""
        if DebugLogger._instance is not None:
            raise RuntimeError("Use get_instance() to get the logger")

        # Determine log file location
        if getattr(sys, 'frozen', False):
            # Running from .exe - log next to executable
            base_dir = os.path.dirname(sys.executable)
        else:
            # Running from source - log in project root
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        self._log_file_path = os.path.join(base_dir, "debug.log")

        # Open log file in append mode - DISABLED (uncomment to enable debug logging)
        # try:
        #     self._log_file = open(self._log_file_path, 'a', encoding='utf-8')
        #     self.log("=" * 80)
        #     self.log(f"FavApp Starter Debug Log - Session started")
        #     self.log(f"Log file: {self._log_file_path}")
        #     self.log("=" * 80)
        # except Exception as e:
        #     print(f"Failed to open log file: {e}")
        #     self._log_file = None
        self._log_file = None  # Debug logging disabled

    def log(self, message: str):
        """Write a message to the log file and console."""
        # Debug logging disabled - uncomment to enable
        pass
        # timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        # log_line = f"[{timestamp}] {message}"

        # # Write to console
        # print(log_line)

        # # Write to file
        # if self._log_file:
        #     try:
        #         self._log_file.write(log_line + "\n")
        #         self._log_file.flush()  # Ensure immediate write
        #     except Exception as e:
        #         print(f"Failed to write to log file: {e}")

    def close(self):
        """Close the log file."""
        # Debug logging disabled - uncomment to enable
        pass
        # if self._log_file:
        #     try:
        #         self.log("=" * 80)
        #         self.log("Session ended")
        #         self.log("=" * 80 + "\n")
        #         self._log_file.close()
        #         self._log_file = None
        #     except Exception:
        #         pass

    def __del__(self):
        """Cleanup when logger is destroyed."""
        self.close()


# Convenience function
def log(message: str):
    """Log a debug message."""
    logger = DebugLogger.get_instance()
    logger.log(message)
