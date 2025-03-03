print("To use this tool, you need to paste an image link ending in .png or .jpeg (like https://i.imgur.com/7x9ejFZ.png), you can paste it with or without the https:// part.\nImgur is most recommended here.")

# I use a function here so when you input an invalid link then it can be called again
def convert():

    i = input("\nImage Link: ")

    # Check if link is valid
    if i.endswith(".png") or i.endswith(".jpeg") or i.endswith(".jpg"):

        # If the link does have "https://", remove it because we will need to add 2 slashes to it anyways
        if i.find("https://") != -1:
            i = i[len("https://"):9999]

        # Final string, the 4 slashes are needed to prevent the link from being blocked by Human or Not.
        i = f'&ltimg src&#61"https:////{i}"&gt'

        print(f"\nOutput: {i}")

    else: 
        print("Link does not end with .png or .jpeg, please try again with a valid link.")
        convert()

# Call the function, otherwise nothing will happen
convert()
