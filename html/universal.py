# This is a more advanced version of the 3 other files which supports images, audio and videos.

# When more testing is done, i will update the extension list.
image_ext = [".png", ".jpg", ".jpeg"]
audio_ext = [".mp3"]
video_ext = [".mp4"]

valid_ext = ""

for ext in image_ext:
    if valid_ext == "":
        valid_ext = valid_ext + ext
    else:
        valid_ext = valid_ext + ", " + ext

for ext in audio_ext:
    valid_ext = valid_ext + ", " + ext

for ext in video_ext:
    valid_ext = valid_ext + ", " + ext

print("Version 1.0.0")
print("To use this tool, you need to paste a valid link, you can paste it with or without the https:// part.")
print(f"\nValid links end in one of these: {valid_ext}")
print("\nExample: https://i.imgur.com/7x9ejFZ.png")

# I use a function here so when you input an invalid link then it can be called again
def convert():

    i = input("\n\nLink: ")

    # If the link does have "https://", remove it because we will need to add 2 slashes to it anyways
    if i.find("https://") != -1:
        i = i[len("https://"):9999]

    output = ""

    # Check if link ends in one of the valid extensions, and then appropriately convert it into html, i know it may not be the best solution

    # Images
    for ext in image_ext:
        if i.endswith(ext):
            output = f'&ltimg src&#61"https:////{i}"&gt'

    # Audio
    for ext in audio_ext:
        if i.endswith(ext):
            output = f'&ltaudio controls autoplay&gt &ltsource src&#61"https:////{i}" &lt/audio&gt'

    #Videos
    for ext in video_ext:
        if i.endswith(ext):
            output = f'&ltvideo autoplay &ltsource src&#61"https:////{i}"›&lt/video&gt'

    # Check if link was valid
    if output != "":

        # Final string, the 4 slashes are needed to prevent the link from being blocked by Human or Not.
        print(f"\n{output}")
        print("\nThe above text is what you need to paste into Human or Not. You can continue using the tool by pasting a link again.")
        convert()

    else:
        # Link is invalid
        print("Link does not end in one of the valid extensions (like .png or .mp4), please try again with a valid link.")
        convert()

# Call the function, otherwise nothing will happen
convert()
