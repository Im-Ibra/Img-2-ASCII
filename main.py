from tkinter.filedialog import askopenfilename
from tkinter import ttk
import tkinter as tk
from PIL import Image
import os


def Convert2Ascii():
#Opens the file selection window
  file = askopenfilename()
#If the user doens't select any file then the program closes
  if not file:
      print("No file selected.")
      exit()
#Creates the directory where the ASCII will be stored and sets the ASCII path
  os.makedirs("output", exist_ok=True)
  ascii_path = f"output/{os.path.basename(file)}.txt"
#Checks which mode the user selects, swapping the characters accordingly
  if darkMode.get() == True:
    ASCII_CHARS = " .:-=+*#%@"
  else:
    ASCII_CHARS = "@%#*+=-:. "
#Constant for the new image width, sets the number of characters per row to 100
  NEW_WIDTH = 100
#Opens the file selected as "im" with the Image function from the PIL library
  with Image.open(file) as im:
#Converts the file/"im" from RGBA to RGB
      im = im.convert("RGB")
#Gets the width and height from file/"im"
      width, height = im.size
#Aspect ratio formula
      aspectRatio = height / width
#Formula to get the new image height, sets it to 55%
      newHeight = int(NEW_WIDTH * aspectRatio * 0.55)
#Resizes the file/"im" with the new dimensions
      im = im.resize((NEW_WIDTH, newHeight))
#Gets the pixels data
      pixels = im.getdata()
#Function that gets the corresponding character according to the pixel
      def pixel_to_char(brightness):
#Calculates the index by dividing the brightness by 256 (the max number on the RGB) then multiplying it by the length of the ASCII_CHARS (10)
          index = int(brightness / 256 * len(ASCII_CHARS))
#Returns the exact character
          return ASCII_CHARS[min(index, len(ASCII_CHARS) - 1)]
#Empty string that will hold every single character
      asciiStr = ""
#Loops through the pixels takes the index and colors
      for i, (r, g, b) in enumerate(pixels):
#Brightness formula, 0.21 = 21%, .72 = 72%, .07 = 7%, these indicate how much color the human eye sees
          brightness = int(0.21*r + 0.72*g + 0.07*b)
#Adds the character to the empty string by calling the previous function and passing brightness as a parameter
          asciiStr += pixel_to_char(brightness)
#Checks if the line is full (100 characters) if so then goes to then next line
          if (i + 1) % NEW_WIDTH == 0:
              ascii_str += "\n"
#Opens the end result as "f" and writes in the string containing the ASCII text
  with open(ascii_path, "w") as f:
      f.write(asciiStr)

#Dictionary containing the Dark and Light mode
modeValues = {
   "Dark Mode" : True,
   "Light Mode" : False
}

#Tkinter window setup
root = tk.Tk()
root.geometry("600x150")
root.title("Img2ASCII")
darkMode = tk.BooleanVar(value=True)

col = 3
for (text, value) in modeValues.items():
   ttk.Radiobutton(root, text = text, variable = darkMode,
                   value = value).grid(column=col, row=0, sticky = "w", padx = 20, pady = 20)
   col += 1

button = ttk.Button(root, text="Choose file", command=Convert2Ascii)
button.grid(column=6, row=0, padx = 20)

root.mainloop()

