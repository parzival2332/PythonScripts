import os
import sys
import time
import logging
import shutil
from os.path import splitext, exists, join
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler

source_directory = r"C:\Users\Monty\Downloads"
destination_directory_pdf = r"C:\Users\Monty\Downloads\PDFs"
destination_directory_exe = r"C:\Users\Monty\Downloads\EXEs"
destination_directory_zip = r"C:\Users\Monty\Downloads\ZIPs"
destination_directory_doc = r"C:\Users\Monty\Downloads\DOCs"
destination_directory_img = r"C:\Users\Monty\Downloads\IMGs"
destination_directory_other = r"C:\Users\Monty\Downloads\OTHERs"
destination_directory_vedio = r"C:\Users\Monty\Downloads\VEDIOs"


def make_unique(destination, name):
    filename, extension = splitext(name)
    counter = 1
    # * IF FILE EXISTS, ADDS NUMBER TO THE END OF THE FILENAME
    while exists(f"{destination}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name


def move(destination, file, name):
    full_destination_path = os.path.join(destination, name)
    
    # Check if the file still exists in the source directory
    if os.path.isfile(file):
        if os.path.isfile(full_destination_path):
            unique_name = make_unique(destination, name)
            full_unique_path = os.path.join(destination, unique_name)
            os.rename(file, full_unique_path)
        else:
            shutil.move(file, full_destination_path)
    else:
        print(f"File '{name}' no longer exists in the source directory.")



class MoverHandler(FileSystemEventHandler): #inherits from the FileSystemEventHandler class
    def on_modified(self, event): 
        with os.scandir(source_directory) as files:
            for file in files:
                name = file.name
                destination = source_directory
                if name.endswith(".pdf") or name.endswith(".PDF"):
                    destination = destination_directory_pdf
                    move(destination, file, name)
                if name.endswith(".zip"):
                    destination = destination_directory_zip
                    move(destination, file, name)
                if name.endswith(".mp4"):
                    destination = destination_directory_vedio
                    move(destination, file, name)
                if name.endswith(".jpg"):
                    destination = destination_directory_img
                    move(destination, file, name)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_directory #whenevr a file is added to this directory(the downloads folder), the event handler will be called
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()              