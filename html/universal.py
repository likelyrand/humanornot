# No comments, sorry!

APP_TITLE = "Files and links into HoN HTML"

IMGUR_CLIENT_ID = "YOUR_CLIENT_ID"

ICON_B64 = "iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAMAAAC7IEhfAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAtUExURRp4MCe1SDXxYBFQIAAAABFQHyOgPzDdWBVjJw09GCzJUCOhQCOgQB6MNwAAADCXHjcAAAAPdFJOU///////////////////ANTcmKEAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAYdEVYdFNvZnR3YXJlAFBhaW50Lk5FVCA1LjEuNBLfpoMAAAC2ZVhJZklJKgAIAAAABQAaAQUAAQAAAEoAAAAbAQUAAQAAAFIAAAAoAQMAAQAAAAIAAAAxAQIAEAAAAFoAAABphwQAAQAAAGoAAAAAAAAAYAAAAAEAAABgAAAAAQAAAFBhaW50Lk5FVCA1LjEuNAADAACQBwAEAAAAMDIzMAGgAwABAAAAAQAAAAWgBAABAAAAlAAAAAAAAAACAAEAAgAEAAAAUjk4AAIABwAEAAAAMDEwMAAAAADX5rshveZftAAAAMBJREFUOE/VlNkOgzAMBDGYI1D4/8+ts1lzKASVSpXoPGDFHrQkIKrlQ/5MrCRjP2U1pM4Qjoz7IkcZHD9HbFRRDdUGlWOKdoTotnuxRfXDTNcutnqRIQSRsa5HkRAGkT72OyhJnGJjUrWKSDyCrV/oQ7kperRFebSvT6JLZNElfitiM4ltM05hM9vxOIXoa/EQPYcwl6L9owCd6uFGKrga7Bv+6hIcn4lHOH6EGOFshW3wnchf0wrb4CBe8XxxWd550jU2Uc8RoQAAAABJRU5ErkJggg=="

INFO_TEXT = """
    This tool turns files and links into HTML to paste into Human or Not.
    It is split into 2 parts. Left and right. 

    Left side: File Conversion, select some valid files and click "Convert",
    this will upload them to Imgur and turn them into HTML.

    Right side: Link Conversion, paste a link and click "Convert",
    this will turn the link into HTML.

    The 2 middle buttons ("Clear" and "Copy") do exactly what they say,
    "Clear" clears everything back to default,
    and "Copy" copies the output to your clipboard.

    Usage: Either select files and click "Convert",
    or paste a link and click "Convert",
    then click "Copy" in the middle after it has been finished.
    That's all.

"""

image_ext = (".png", ".jpg", ".jpeg", ".gif")
audio_ext = (".mp3", ".ogg")
video_ext = (".mp4", ".mov")

all_ext = image_ext + audio_ext + video_ext

filetypes_str = ""

for filetype in all_ext:
    if filetypes_str == "":
        filetypes_str = filetype
    else:
        filetypes_str = filetypes_str + " " + filetype

filetypes = [("Supported Files", filetypes_str)]

import os
import pyimgur
import pyperclip

import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

import sv_ttk

im = pyimgur.Imgur(IMGUR_CLIENT_ID)

selected_paths = []
path_str = "No files selected."
path_cache = {}
output_copy = ""

root = Tk()
root.iconphoto(True, PhotoImage(data=ICON_B64))

root.title(APP_TITLE)
root.resizable(0, 0)
root.maxsize(500, 500)
root.minsize(500, 500)

info_label = ttk.Label(root, text=INFO_TEXT, justify="center")
info_label.place(relx=0.5, rely=0.34, anchor="center")

path_label = ttk.Label(root, text="0 files selected.", justify="center")
path_label.place(relx=0.08, rely=0.62)

#path_tipbtn = ttk.Button(root, text="?")
#path_tipbtn.place(relx=0.08, rely=0.56)

status_label = ttk.Label(root, text="Start by uploading files or pasting a link.", justify="center")
status_label.place(relx=0.5, rely=0.94, anchor="center")

output_label = ttk.Label(root, text="No output yet.", justify="center")
output_label.place(relx=0.92, rely=0.62, anchor="ne")

entered_link = StringVar(value="Enter Link")
entry = ttk.Entry(root, justify="center", textvariable=entered_link)
entry.place(relx=0.92, rely=0.68, anchor="ne")
entry.bind("<FocusIn>", lambda args: entry.delete('0', 'end'))
def entry_out(e):
    if entered_link.get() == "": entered_link.set("Enter Link")
entry.bind("<FocusOut>", entry_out)

def pick():
    paths = filedialog.askopenfilenames(filetypes=filetypes)
    for path in selected_paths:
        selected_paths.remove(path)

    paths_str = ""

    for path in paths:
        if paths_str == "":
            paths_str = os.path.basename(path)
        else:
            paths_str = paths_str + ", " + os.path.basename(path)
        selected_paths.insert(len(selected_paths), path)

    path_str = paths_str
    #path_tip['text'] = path_str

    if str(len(selected_paths)) == 1:
        path_label['text'] = "1 file selected."
    else:
        path_label['text'] = str(len(selected_paths)) + " files selected."   

def convert_files():

    full_output = []
        
    if len(selected_paths) > 0:

        status_label['text'] = "Uploading files."

        for file in selected_paths:

            # Upload the files to imgur
            url = None

            try:

                path_cache[file]

            except KeyError:

                filename = os.path.basename(file)
                img = im.upload_image(path=file,title=filename)
                url = img.link_medium_thumbnail

                path_cache[file] = img.link_medium_thumbnail

            else:

                url = path_cache[file]
            

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
                full_output.insert(len(full_output), output)
            else:
                # Link is invalid
                status_label['text'] = "Something went wrong, please try again."
    
    output_str = ""

    for output in full_output:
        if output_str == "":
            output_str = output
        else:
            output_str = output_str + "\n" + output
    
    if output_str != "":
        output_copy = output_str
        status_label['text'] = "Files successfully uploaded."
        output_label['text'] = str(len(full_output)) + " converted files to copy."
        if len(full_output) == 1:
            output_label['text'] =  "1 converted file to copy."

def convert_link():
    if entered_link.get() != "":
        i = entered_link.get()

        if i.find("https://") != -1:
            i = i[len("https://"):9999]

        output = ""

        # Check if link ends in one of the valid extensions, and then appropriately convert it into html, i know it may not be the best solution

        # Images
        for ext in image_ext:
            if i.endswith(ext):
                output = f'&ltimg src&#61"//{i}"&gt'

        # Audio
        for ext in audio_ext:
            if i.endswith(ext):
                output = f'&ltaudio controls autoplay&gt &ltsource src&#61"//{i}" &lt/audio&gt'

        #Videos
        for ext in video_ext:
            if i.endswith(ext):
                output = f'&ltvideo autoplay &ltsource src&#61"//{i}"›&lt/video&gt'

        # Check if link was valid
        if output != "":
            output_str = output
    
            if output_str != "":
                output_copy = output_str
                status_label['text'] = "Link successfully converted."
                output_label['text'] = "1 converted link to copy."

def copy():
    status_label['text'] = "Copied to clipboard."
    pyperclip.copy(output_copy)

def clear():
    entered_link.set("Enter Link")
    selected_paths = []
    path_str = "No files selected."
    #path_tip['text'] = path_str
    status_label['text'] = "Start by uploading files or pasting a link."
    path_label['text'] = "0 files selected."


select_button = ttk.Button(root, text="Select Files", default="active", command=pick)
select_button.place(relx=0.08, rely=0.68)

convert_button = ttk.Button(root, text="Convert", default="active", command=convert_files)
convert_button.place(relx=0.08, rely=0.76)



convert_button2 = ttk.Button(root, text="Convert", default="active", command=convert_link)
convert_button2.place(relx=0.92, rely=0.76, anchor="ne")


copy_button = ttk.Button(root, text="Copy", default="active", command=copy)
copy_button.place(relx=0.52, rely=0.84, anchor="nw")

clear_button = ttk.Button(root, text="Clear", default="active", command=clear)
clear_button.place(relx=0.48, rely=0.84, anchor="ne")

# theme
sv_ttk.set_theme("dark")

root.mainloop()
