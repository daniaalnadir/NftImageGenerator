import os

# Rename the files in a code friendly format.
# Replace spaces with underscores and lowercase the file name so it's easier to map the array
def rename_files(name):
    walk_dir = r'C:\nftproject\Traits'
    for root, subdirs, files in os.walk(walk_dir):
        for filename in files:
            file_path = os.path.join(root, filename)
            os.rename(file_path, (file_path.replace(" ", "-").upper()))