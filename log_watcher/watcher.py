from posixpath import abspath, dirname
import win32file
import win32event
import win32con
from pathlib import Path
import os

# DIR_PATH = dirname(abspath(__file__))
DIR_PATH = Path(__file__).resolve().parent
LINES_TO_READ = 10
BYTE_SIZE_TO_READ = 1024

def get_config_modification_handle():
    '''Returns a Directory change handle on the configuration directory.
    '''
    change_handle = win32file.FindFirstChangeNotification(
        str(DIR_PATH),
        0,
        win32con.FILE_NOTIFY_CHANGE_LAST_WRITE
    )
    return change_handle

def read_last_n_lines(file_path: Path, n: int, chunk_size: int = 1024):
    with open(file_path, "rb") as f:
        f.seek(0, os.SEEK_END)
        buffer = b""
        lines = []

        pos = f.tell()
        #since pointer is at the end tell returns the total size of the file
        #eg pos = 2048
        while pos > 0 and len(lines) <= n:
            read_size = min(chunk_size, pos)
            pos -= read_size
            #pos = 1024
            f.seek(pos)
            chunk = f.read(read_size)
            buffer = chunk + buffer
            lines = buffer.split(b'\n')  

        return [line.decode(errors="ignore") for line in lines[-n:] if line]

def watch_file(change_handle):
    path_to_the_log_file = (DIR_PATH / "./test.log").resolve()
    if not path_to_the_log_file.exists():
        raise ValueError("File test log not found")

    last_modified_at = path_to_the_log_file.stat().st_mtime
    
    try:
        while True:
            result = win32event.WaitForSingleObject(change_handle, 500)
            if result == win32con.WAIT_OBJECT_0:
                updated_last_modified_at = path_to_the_log_file.stat().st_mtime
                if updated_last_modified_at != last_modified_at:
                    lines = read_last_n_lines(path_to_the_log_file, LINES_TO_READ)
                    print("Last 10 lines:")
                    print("\n".join(lines))
                    last_modified_at = updated_last_modified_at

                win32file.FindNextChangeNotification(change_handle)
    except KeyboardInterrupt:
        print("Stopped watching.")
    finally:
        win32file.FindCloseChangeNotification(change_handle)

if __name__ == "__main__":
    print("Hello here...")
    change_handler = get_config_modification_handle()
    watch_file(change_handle=change_handler)
