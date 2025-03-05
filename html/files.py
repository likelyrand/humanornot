# This file takes a path, which can be either a folder or file, and uploads all the valid files to imgur, then does the thingy so u can paste it into Human or Not.
# I will merge this with the universal.py soon

import os
import pyimgur

CLIENT_ID = "YOUR_CLIENT_ID"

# We will need this to upload the files
im = pyimgur.Imgur(CLIENT_ID)

# All the valid extensions, the for loops are a bit of mess
# When more testing is done, i will update the extension list.
image_ext = [".png", ".jpg", ".jpeg", ".gif"]
audio_ext = [".mp3"]
video_ext = [".mp4"]

all_ext = []

for ext in image_ext:
    all_ext.insert(len(all_ext), ext)
for ext in audio_ext:
    all_ext.insert(len(all_ext), ext)
for ext in video_ext:
    all_ext.insert(len(all_ext), ext)

valid_ext = ""

for ext in all_ext:
    if valid_ext == "":
        valid_ext = valid_ext + ext
    else:
        valid_ext = valid_ext + ", " + ext

# Information
print("Version 1.0.0")
print("To use this tool, you need to paste the full path to your file (or folder of it).")
print(f"\nValid files end in one of these: {valid_ext}")
print("\nExample: C:\\path\\to\\file.png")

# I use a function here so when you input an invalid link then it can be called again
def convert():

    error = False
    no_files = False

    path = input("\n\nFull path to fiie: ")
    print(" ")

    path.replace("/", "\\")

    # Windows "Copy Path" adds quotes by default, so we should remove them
    path.replace('"', "")
    path.replace("'", "")

    # List of files to upload, the below if statements will fill this list
    to_upload = []

    # If the path even exists
    if path != "" and os.path.exists(path):

        # If path is a folder, loop through all the files there and add them to the list
        if os.path.isdir(path):

            any = False

            for file in os.listdir(path):

                filename = os.fsdecode(file)
                valid = False

                for ext in all_ext:

                    if filename.endswith(ext):

                        valid = True
                        any = True
                
                if valid:
                    to_upload.insert(len(to_upload), path+"\\\\"+file)
            
            if not any:
                no_files = True
        
        # Else if path is a file, add it to the list
        elif os.path.isfile(path):

            for ext in all_ext:
                if path.endswith(ext):
                    valid = True
                
            if valid:
                to_upload.insert(len(to_upload), path)
            else:
                no_files = True

        else:
            error = True
    
    # If no files to upload
    if len(to_upload) == 0:
        error = True
    
    for file in to_upload:

        # Upload the files to imgur
        filename = os.path.basename(file)
        img = im.upload_image(path=file,title=filename)

        url = img.link_medium_thumbnail

        # If the link does have "https://", remove it because we will need to add 2 slashes to it anyways
        if url.find("https://") != -1:
            url = url[len("https://"):9999]

        output = ""

        # Check if url ends in one of the valid extensions, and then appropriately convert it into html, i know it may not be the best solution

        # Images
        for ext in image_ext:
            if url.endswith(ext):
                output = f'&ltimg src&#61"//{url}"&gt'

        # Audio
        for ext in audio_ext:
            if url.endswith(ext):
                output = f'&ltaudio controls autoplay&gt &ltsource src&#61"//{url}" &lt/audio&gt'

        #Videos
        for ext in video_ext:
            if url.endswith(ext):
                output = f'&ltvideo autoplay &ltsource src&#61"//{url}"›&lt/video&gt'

        # Check if link was valid
        if output != "":

            # Final string, the 4 slashes are needed to prevent the link from being blocked by Human or Not.
            print(f"\n{output}")
            print("\nThe above text is what you need to paste into Human or Not. You can continue using the tool by pasting a path again.")
            convert()

        else:
            # Link is invalid
            print("Link does not end in one of the valid extensions (like .png or .mp4), please try again with a valid link.")
            convert()

    if error:
        if no_files:
            print("Path is either not a valid file or there are no valid files in path!")
        else:
            print("Invalid path!")
        convert()

# Call the function, otherwise nothing will happen
convert()

# The calls of the function inside of the function are so you don't have to run the file every time you want to upload something more than once
