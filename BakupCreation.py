import os
import glob
import re
import datetime
import shutil


def delete_oldest_backup_if_more_than_four(directory_path):
    try:
        # Get a list of all files in the directory
        files = glob.glob(os.path.join(directory_path, 'Backup_*'))

        # Filter out directories and get the modification time for each file
        file_times = [(file, os.path.getmtime(file)) for file in files if os.path.isfile(file)]

        if len(file_times) <= 4:
            print("There are 4 or fewer backup files in the directory. No file will be deleted.")
            return

        # Sort files based on modification time in ascending order (oldest first)
        oldest_file = min(file_times, key=lambda x: x[1])[0]

        # Delete the oldest backup file
        os.remove(oldest_file)

        print(f"The oldest backup file '{oldest_file}' has been deleted.")

    except Exception as e:
        print(f"Error: {e}")

# Example usage

def copy_file(source_path, destination_path):
    try:
        # Copy the file from source to destination
        shutil.copy2(source_path, destination_path)
        print(f"File copied successfully from {source_path} to {destination_path}")

    except FileNotFoundError:
        print(f"Source file '{source_path}' not found.")

    except PermissionError:
        print(f"Permission error. Unable to copy the file.")

def get_current_timestamp():
    # Get the current date and time
    current_datetime = datetime.datetime.now()

    # Format the date and time to create a timestamp
    timestamp = current_datetime.strftime("%Y_%m_%d (%H %M %S)")

    return timestamp


def CreateBackup(filepath):
    BakupAddress=os.path.dirname(filepath)
    basename=str(os.path.basename(filepath)).replace(".xlsx","")
    FolderName="Backup_Folder" +basename

    timestamp = get_current_timestamp()
    backupfilename = f"Backup_{timestamp}.xlsx"

 
    BackupAddress= os.path.join(BakupAddress,FolderName)
    if not os.path.exists(BackupAddress):
        os.mkdir(BackupAddress)

    copy_file(filepath, destination_path=os.path.join(BackupAddress,backupfilename))
    delete_oldest_backup_if_more_than_four(BackupAddress)



# delete_oldest_backup_if_more_than_four()