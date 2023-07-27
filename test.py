import os

folder_path = os.path.join('Notebook', 'Data')
file_names = os.listdir(folder_path)[0].split('.')[0]

print(f':- {folder_path}----------{file_names}')