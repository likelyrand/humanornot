print("To use this tool, you need to paste an audio link ending in .mp3, you can paste it with or without the https:// part.")

# I use a function here so when you input an invalid link then it can be called again
def convert():

    i = input("\nAudio Link: ")

    # Check if link is valid
    if i.endswith(".mp3"):

        # If the link does have "https://", remove it because we will need to add 2 slashes to it anyways
        if i.find("https://") != -1:
            i = i[len("https://"):9999]

        # Final string, the 4 slashes are needed to prevent the link from being blocked by Human or Not.
        i = f'&ltaudio controls autoplay&gt &ltsource src&#61"https:////{i}" &lt/audio&gt'

        print(f"\nOutput: {i}")

    else: 
        print("Link does not end with .mp3, please try again with a valid link.")
        convert()

# Call the function, otherwise nothing will happen
convert()
