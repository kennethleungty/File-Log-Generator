# ==================================
#        File Activity Tracker
# ==================================

# Make necessary imports
import os
import time
from datetime import datetime
import numpy as np
import pandas as pd

# Set base directory
basepath = os.getcwd()
os.chdir(basepath)
print('Current working directory = '+os.getcwd())

# Set name of Excel sheet to collate the file activity log
activity_log_filename = 'File Activity Log.xlsx' # Can rename based on preference

# Create function to obtain list of subdirectories
def get_all_subdir(path):
    subdir_list = []
    for dirpath, dirnames, filenames in os.walk(path):
        subdir_list.append(dirpath)
    return subdir_list

# Collate all folders and subfolders (aka subdirectories)
subdirectory_list = get_all_subdir(basepath)
subdirectory_list

# List of column headers
column_list = ['Modified Time', 'Folder Path', 'File Name', 'File Extension','Change Time',
               'Access Time', 'Person who Modified', 'Details']

if os.path.isfile(f'./{activity_log_filename}'):
    df_existing_log = pd.read_excel(f'./{activity_log_filename}')
    # Convert NaN in columns to empty string (so that drop_duplicates can work)
    df_existing_log = df_existing_log.replace(np.nan, '', regex=True)
    print('Successfully imported existing file activity log')
else:
    df_existing_log = pd.DataFrame(columns=column_list)
    print('No file activity log exists. Creating new file')

# Create temporary dataframe for the file log
df_temp_log = pd.DataFrame(columns=column_list)

# Create function for datetime conversion into readable date format
def convert_datetime(time):
    updated_time = datetime.strptime(time, "%a %b %d %H:%M:%S %Y")
    final_time = updated_time.strftime('%Y-%b-%d %H:%M')
    return final_time

# Generate rows for each file (that ends with pdf, xlsx, or docx)
for subdir in subdirectory_list:
        for file in os.listdir(subdir):
            if file.lower().endswith(('.pdf', '.xlsx', '.docx')):
                filepath = subdir+'\\'+file
                _, file_ext = os.path.splitext(filepath)
                shortened_subdir = subdir.replace(basepath, '')
                if shortened_subdir == '':
                    shortened_subdir = '\\'
                modified_time = time.ctime(os.path.getmtime(filepath))
                modified_time = convert_datetime(modified_time)
                access_time = time.ctime(os.path.getatime(filepath))
                access_time = convert_datetime(access_time)
                change_time = time.ctime(os.path.getctime(filepath))
                change_time = convert_datetime(change_time)
                df_temp_log = df_temp_log.append({'Modified Time': modified_time,
                                                  'Folder Path': shortened_subdir,
                                                  'File Name': file,
                                                  'File Extension': file_ext,
                                                  'Change Time': change_time,
                                                  'Access Time': access_time,
                                                  'Person who Modified': '',
                                                  'Details': ''},
                                                  ignore_index=True)
                df_temp_log.sort_values(by = ['Modified Time'], inplace=True, ascending = False)
                df_temp_log.drop_duplicates(subset=None, keep="first", inplace=True)

# Match with existing log, and remove any duplicates
df_final_log = pd.concat([df_existing_log, df_temp_log])
df_final_log.sort_values(by = ['Modified Time'], inplace=True, ascending = False)
df_final_log.drop_duplicates(subset=None, keep="first", inplace=True)

# Delete rows that reflect the changes in the File Activity Log file creation
df_final_log = df_final_log[df_final_log['File Name'] != activity_log_filename]

# Export final dataframe
df_final_log.to_excel(activity_log_filename,index=False)
print('File activity log generation complete')

# Future Work: Pull further specific details from Office documents
# e.g. who created file, when last saved etc
