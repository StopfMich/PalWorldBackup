import shutil
import os
import sys
import threading
from datetime import datetime
import schedule
import time
from plyer import notification

stop_thread = False

target_dir = ""
source_dir = ""

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def make_backup(bu_source_dir, bu_target_dir, backup_time):
    global target_dir
    global source_dir
    target_dir = bu_target_dir
    source_dir = bu_source_dir
    job()
    if backup_time != 0:
        schedule.every(backup_time).hours.do(job)
        threading.Thread(target=run_schedule).start()

def run_schedule():
    global stop_thread
    while True:
        if stop_thread:
            break
        schedule.run_pending()
        time.sleep(1)

def stop():
    global stop_thread
    stop_thread = True

def job():
    # Get the current date and format it into a string
    current_day = datetime.now().strftime('%d.%m.%Y')
    current_time = datetime.now().strftime('%H-%M-%S')
    print(f'Backing up saves to {current_day}/{current_time}')

    # Define the source and target directories
    target_dir_time = os.path.expanduser(f'{target_dir}/{current_day}/{current_time}')

    # Check if the target directory exists, if not, create it
    if not os.path.exists(target_dir_time):
        os.makedirs(target_dir_time)

    # Get a list of all folders in the source directory
    folders = os.listdir(source_dir)

    # Loop through the list of folders and copy each one to the target directory
    for folder in folders:
        shutil.copytree(os.path.join(source_dir, folder), os.path.join(target_dir_time, folder))

    notification.notify(
        title='Palworld Backup successful',
        message=f'Backuped created at {current_time} on {current_day}'.replace('-', ':'),
        app_name='Palworld Backup',
        app_icon=resource_path('img/PalWorldBackup.ico'),
        timeout=10
    )

