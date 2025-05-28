import customtkinter
import tkinter
import os
from PIL import Image, ImageTk

class InventoryApp:
    def __init__(self, master):
        self.master = master
        self.master.geometry("800x500")
        self.master.title("Inventory App")

        self.tab = customtkinter.CTkTabview(master=self.master, width=800, height=500)
        self.tab.pack(pady=10)

        self.oversikt = self.tab.add("Oversikt")
        self.viktig = self.tab.add("Må fylles på")
        self.kalender = self.tab.add("Kalender")

        self.scrollFrame = customtkinter.CTkScrollableFrame(self.oversikt, width=800, height=500)
        self.scrollFrame.pack(pady=20)

        self.ObjList = [
            ["skalpell", 10, os.path.abspath("skalpell.JPEG")],
            ["Motorsager", 8, os.path.abspath("motorsag.JPEG")],
            ["Sakser", 4, os.path.abspath("sakser.JPEG")],
            ["sprøytenåler", 20, os.path.abspath("sproytenal.JPEG")]
        ]

        self.labels = []
        for x in range(len(self.ObjList)):
            self.create_item_frame(x)

    def create_item_frame(self, x):
        item_frame = customtkinter.CTkFrame(self.scrollFrame)
        item_frame.pack(pady=5, padx=5, fill=tkinter.X)

        nummerering = f"{x + 1}."
        antall = f"{self.ObjList[x][1]} stk"

        tbp = f"{nummerering.ljust(4)}{str(self.ObjList[x][0]).ljust(20)}{antall.ljust(15)}"
        fontType = ("Courier", 17, "bold")
        label = customtkinter.CTkLabel(item_frame, text=tbp, font=fontType)
        self.labels.append(label)
        label.grid(row=0, column=0, padx=(0, 10), sticky=tkinter.W)

        imageButton = customtkinter.CTkButton(item_frame, text="Sjå bilete", command=lambda idx=x: self.image_func(idx))
        imageButton.grid(row=0, column=1, sticky=tkinter.W)

        addButton = customtkinter.CTkButton(item_frame, text="Legg til...", command=lambda idx=x: self.butt_func(idx))
        addButton.grid(row=0, column=2, sticky=tkinter.W)

        addButton.grid_configure(padx=(0, 5))
        imageButton.grid_configure(padx=(0, 5))
        
        item_frame.grid_columnconfigure(0, weight=1)
        item_frame.grid_columnconfigure(1, minsize=100)
        item_frame.grid_columnconfigure(2, minsize=100)

    def image_func(self, x):
        iwidth = 400
        iheight = 400
        image_window = customtkinter.CTkToplevel(self.oversikt)
        image_window.title(f"Bilete av {self.ObjList[x][0]}:")
        xpos = image_window.winfo_screenwidth() - iwidth
        ypos = image_window.winfo_screenheight() - iheight
        image_window.geometry(f"400x400+{xpos}+{ypos}")
        image_window.grab_set()
        image_window.overrideredirect(True)

        my_image = customtkinter.CTkImage(light_image=Image.open(self.ObjList[x][2]), 
                                          dark_image=Image.open(self.ObjList[x][2]), size=(400, 400))
        bildebox = customtkinter.CTkLabel(image_window, text="", image=my_image)
        bildebox.pack(padx=0, pady=0)

        image_window.after(2000, image_window.destroy)

    def butt_func(self, x):
        dialog = customtkinter.CTkInputDialog(text="Kor mange vil du legge til")
        svar = dialog.get_input()
        if svar.isdigit():
            self.ObjList[x][1] += int(svar)
            self.update_labels()
        else:
            print("jalla")

    def update_labels(self):
        for x, label in enumerate(self.labels):
            nummerering = f"{x + 1}."
            antall = f"{self.ObjList[x][1]} stk"
            tbp = f"{nummerering.ljust(4)}{str(self.ObjList[x][0]).ljust(20)}{antall.ljust(15)}"
            label.configure(text=tbp)

def main():
    root = customtkinter.CTk()
    app = InventoryApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
