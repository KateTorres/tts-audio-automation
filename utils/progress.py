import sys
import time

class ProgressBar:
    def __init__(self, total, prefix='', length=50, fill='█'):
        self.total = total
        self.prefix = prefix
        self.length = length
        self.fill = fill
        self.current = 0
        self.start_time = time.time()

    def update(self, value=None):
        if value is not None:
            self.current = value
        percent = ("{0:.1f}").format(100 * (self.current / float(self.total)))
        filled_length = int(self.length * self.current // self.total)
        bar = self.fill * filled_length + '-' * (self.length - filled_length)
        elapsed = time.time() - self.start_time
        sys.stdout.write(f'\r{self.prefix} |{bar}| {percent}% ({self.current}/{self.total} bytes) Elapsed: {elapsed:.1f}s')
        sys.stdout.flush()
