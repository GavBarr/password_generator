from PIL import Image
import random
import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD



image_path=""
def image_to_ascii(image_path, chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ", new_width=80):
    """Converts an image to ASCII art."""

    image = Image.open(image_path)
    width, height = image.size
    aspect_ratio = height/width
    new_height = int(aspect_ratio * new_width)
    image = image.resize((new_width, new_height))
    image = image.convert('L')  # Convert to grayscale

    pixels = image.getdata()
    ascii_image = ""

    for pixel in pixels:
        index = int(pixel * (len(chars) - 1) / 256)
        ascii_image += chars[index]

    ascii_image = "\n".join(ascii_image[i:(i+new_width)] for i in range(0, len(ascii_image), new_width))
    return ascii_image

#function to take the ascii string, convert it to a password
#500 minimum character length for "ascii_art" arg0
#return -1 if failure occurs
#there is a 25 character limit of how long the password can be, this is to oblige to most websites login password restrictions etc.
def password_algorithm(ascii_art):

    if len(ascii_art)<500:
        return -1


    start_pos = 117
    end_pos = len(ascii_art)-250
    i=0
    j=0

    sliced_ascii = ascii_art[start_pos:end_pos]
    sliced_char=""
    converted_password=""
    final_pass=""
    
    for i in range(len(sliced_ascii)):
        sliced_char = sliced_ascii[i:i+2]
        try:
            int(sliced_char)
            sliced_char=hex(sliced_char)
        except:
            try:
                sliced_char=str(ord(sliced_char))
            except:
                sliced_char=str(ord(sliced_char[0:1]))

        converted_password=sliced_char+converted_password


        i+=1
    
    for j in range(len(converted_password)):
        sliced_char=converted_password[j:j+4]
        if int(sliced_char[0:2]) in range(0, 32) or int(sliced_char[0:2]) == 127:
            continue
        else:
            if int(sliced_char) % 2 == 1:
                final_pass+=hex(int(sliced_char))
            else:
                final_pass+=str(chr(int(sliced_char[0:2])))


        j+=1

    length = len(final_pass)
    middle = int(length/4)
    end = int(length/3)
    final_pass=final_pass[0:7]+final_pass[middle:middle+7]+final_pass[middle+8:middle+11]+final_pass[end:end+8]
    final_pass=final_pass.replace(" ","")

    return final_pass


# Create a Tkinter window with DnD support
class FileDropApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Password Generator")
        self.geometry("400x300")
        self.config(bg="#0d1014")

        # Create a Text widget styled to look like a Label
        
        self.text_widget = tk.Text(self, font=("Arial", 14), wrap=tk.WORD, bg="#22272e", relief=tk.FLAT, bd=0, height=5)
        self.text_widget.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

        # Make the Text widget read-only but still selectable
        self.text_widget.tag_configure("center", justify="center",foreground="white")
        self.text_widget.insert(tk.END, "Drag and drop a file here", "center")
        self.text_widget.config(state=tk.DISABLED)




        # Bind drop event to the Text widget
        self.text_widget.drop_target_register(DND_FILES)
        self.text_widget.dnd_bind('<<Drop>>', self.on_file_drop)

    def on_file_drop(self, event):
        # Display the dropped file path
        file_path = event.data
        image_path = file_path #assign the image_path global so then it can be passed in main easily
        print(image_path)
        ascii_art = image_to_ascii(image_path)
        final_password=password_algorithm(ascii_art)

        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(tk.END, f"{final_password}","center")
        self.text_widget.config(state=tk.DISABLED)

        
        #self.label.config(text=f"File Dropped:\n{file_path}")
        

    

if __name__ == "__main__":

    app = FileDropApp()
    app.mainloop()

        



