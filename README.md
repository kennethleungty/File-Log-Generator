# File Tracker
Automatic Excel file generator for tracking of file changes in a folder
___

## Motivation
- Multiple collaborators contributing to a single shared folder (e.g. Dropbox, Google Drive) can make multiple changes over time, with files added constantly
- File tracking service is a paid feature for certain platforms (e.g. Dropbox)


## Solution
- In order to better track the file additions into Shared folders, and to quickly generate a full list of files in a shared folder, this Python script was written such that the file tracking process can be simplified

## How to use
- Place the file_activity_tracker.py in the parent directory you wish to track. The script will automatically crawl through all sub-directories to collate the list of files. 
- In Command Prompt, change the directory to the parent directory (e.g. cd C:/Desktop/Shared_Folder), and run the .py file (i.e. python file_activity_tracker.py) 
- Run the above step whenever you want to have an updated list of the files (together with indication of recent changes)
- Once the script has been run, an Excel file will automatically be generated in your parent directory
