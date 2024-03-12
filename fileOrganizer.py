import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Specify file types and their target destinations
file_types = {
    ".jpg": "C:/Users/lak91/OneDrive/Desktop",  
    ".jpeg": "C:/Users/lak91/OneDrive/Desktop",  
    ".svg": "C:/Users/lak91/OneDrive/Desktop",  
    ".png": "C:/Users/lak91/OneDrive/Desktop",  
    ".avif": "C:/Users/lak91/OneDrive/Desktop",  

    ".pdf": "C:/Users/lak91/OneDrive/Documents/StudyMaterial",
    ".ppt": "C:/Users/lak91/OneDrive/Documents/StudyMaterial",
    ".pptx": "C:/Users/lak91/OneDrive/Documents/StudyMaterial",
    ".doc": "C:/Users/lak91/OneDrive/Documents/StudyMaterial",
    ".docx": "C:/Users/lak91/OneDrive/Documents/StudyMaterial",

    ".exe": "C:/Users/lak91/Downloads/SETUPS",  
    # add more file types and destinations as per ur need
}


def organize_files(event):

    if event.is_directory:
        return None

    file_path = event.src_path
    
    # Check if the file exists
    if not os.path.exists(file_path):
        return None

    file_name, extension = os.path.splitext(file_path)

    # check if downloaded file's extension exists in our file types dictionary
    if extension in file_types:
        destination = file_types[extension]
        os.makedirs(destination, exist_ok=True)  # create destination folder if it doesnt exist
        
        # wait for browser to process the downloaded file
        time.sleep(5)
        # move the downloaded file to the destination 
        shutil.move(file_path, os.path.join(destination, os.path.basename(file_path)))
    

# event handler - monitors the downloads folder
class DownloadsHandler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        organize_files(event)

# set your downloads folder path (this should be same as where the browser downlaods the files)
downloads_path = os.path.expanduser("C:/Users/lak91/Downloads/")

# create event handler and observer objects
event_handler = DownloadsHandler()
observer = Observer()

# start the observer
observer.schedule(event_handler, downloads_path, recursive=True)
observer.start()

# observer constantly monitors every second, and checks for keyboard interrupt
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()

