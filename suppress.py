import sys
import os
import re
from threading import Thread

def suppress_jack_errors():
    """Redirect low-level stderr to filter JACK errors."""
    # Patterns to suppress
    patterns = [
        r'Cannot connect to server socket',
        r'Cannot connect to server request channel',
        r'jack server is not running',
        r'JackShmReadWritePtr',
        r'RuntimeWarning: invalid value encountered in sqrt rms = np.max(np.sqrt(np.mean(audio_data**2, axis=0) + 1e-7))'
    ]
    
    # Save original stderr file descriptor
    original_stderr_fd = sys.stderr.fileno()
    saved_stderr_fd = os.dup(original_stderr_fd)
    
    # Create a pipe
    read_fd, write_fd = os.pipe()
    
    # Redirect stderr to the pipe's write end
    os.dup2(write_fd, original_stderr_fd)
    
    # Close unnecessary file descriptors
    os.close(write_fd)
    
    def filter_errors():
        """Read from pipe and filter lines."""
        while True:
            data = os.read(read_fd, 1024).decode()
            if not data:
                break
            for line in data.split('\n'):
                if not any(re.search(p, line) for p in patterns):
                    # Write non-JACK errors to original stderr
                    os.write(saved_stderr_fd, (line + '').encode())
    
    # Start the filtering thread
    thread = Thread(target=filter_errors, daemon=True)
    thread.start()