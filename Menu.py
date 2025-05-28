import customtkinter
import tkinter
import os
from PIL import Image, ImageTk
import time



def run():
    root=customtkinter.CTk()
    #Gjør det full-screen(Ser nok bedre ut på ein mindre skjerm)
    #root.attributes("-fullscreen",True)

    rwidth=800
    rheight=500
    widthAndHeight=f"{rwidth}x{rheight}"

    #Format og farger
    customtkinter.set_appearance_mode("light")
    customtkinter.set_default_color_theme("blue")
    root.geometry(widthAndHeight)


    tab=customtkinter.CTkTabview(master=root,
                                width=rwidth,
                                height=rheight)
    tab.pack(pady=10)

    oversikt=tab.add("Oversikt")
    viktig= tab.add("Må fylles på")
    kalender=tab.add("Kalender")


    scrollFrame=customtkinter.CTkScrollableFrame(oversikt,
                                            width=rwidth,
                                            height=rheight)
    scrollFrame.pack(pady=20)

    ObjList = [
        ["skalpell", 10, os.path.abspath("skalpell.JPEG")],  
        ["Motorsager", 8, os.path.abspath("motorsag.JPEG")],
        ["Sakser", 4, os.path.abspath("sakser.JPEG")],
        ["sprøytenåler", 20, os.path.abspath("sproytenal.JPEG")]
    ]

    #For å oppdatere når elementer legges til
    def update_labels():
        for x, label in enumerate(labels):
            nummerering = f"{x+1}."
            antall = f"{ObjList[x][1]} stk"
            tbp = f"{nummerering.ljust(4)}{str(ObjList[x][0]).ljust(20)}{antall.ljust(15)}"
            label.configure(text=tbp)

    #Legge til funksjon
    def buttFunc(x):
        dialog=customtkinter.CTkInputDialog(text="Kor mange vil du legge til")
        svar=dialog.get_input()
        
        if svar.isdigit():
            ObjList[x][1]+=int(svar)
            update_labels()
            
        else:
            print("jalla")
            return None
            
        
        
    imageWindow=None

    def closeImageWin():
        global imageWindow
        if imageWindow != None:
            imageWindow.destroy()
            imageWindow.update()
            imageWindow=None


    #Bilde funksjon
    def imageFunc(x):
        iwidth=400
        iheight=400
        global imageWindow
        imageWindow=customtkinter.CTkToplevel(oversikt)
        imageWindow.title(f"Bilete av {ObjList[x][0]}:")
        xpos=imageWindow.winfo_screenwidth()-iwidth
        ypos=imageWindow.winfo_screenheight()-iheight

        imageWindow.geometry(f"400x400+{xpos}+{ypos}")
        imageWindow.grab_set()
        imageWindow.overrideredirect(True)


        my_image=customtkinter.CTkImage(light_image=Image.open(ObjList[x][2]), dark_image=Image.open(ObjList[x][2]),size=(400,400))
        bildebox=customtkinter.CTkLabel(imageWindow,text="",image=my_image)
        bildebox.pack(padx=0,pady=0)
        
        imageWindow.after(1000,closeImageWin)

    labels=[]



    for x in range(len(ObjList)):
        #Ny ramme for kvart item
        item_frame = customtkinter.CTkFrame(scrollFrame)
        item_frame.pack(pady=5, padx=5, fill=tkinter.X)  
        
        nummerering = f"{x+1}."
        antall = f"{ObjList[x][1]} stk"
        
        # text label
        tbp = f"{nummerering.ljust(4)}{str(ObjList[x][0]).ljust(20)}{antall.ljust(15)}"
        fontType = ("Courier", 17, "bold")
        label = customtkinter.CTkLabel(item_frame, text=tbp, font=fontType)
        labels.append(label)
        label.grid(row=0, column=0, padx=(0, 10), sticky=tkinter.W)  

        # Bildeknapp
        imageButton = customtkinter.CTkButton(item_frame, text="Sjå bilete", command=lambda idx=x: imageFunc(idx))
        imageButton.grid(row=0, column=1, sticky=tkinter.W)

        #Legg til-knapp
        addButton = customtkinter.CTkButton(item_frame, text="Legg til...", command=lambda idx=x: buttFunc(idx))
        addButton.grid(row=0, column=2, sticky=tkinter.W)  
        
        # For å få knapppene aligned
        addButton.grid_configure(padx=(0, 5))
        imageButton.grid_configure(padx=(0, 5)) 
        
        # Også for alignment
        item_frame.grid_columnconfigure(0, weight=1) 
        item_frame.grid_columnconfigure(1, minsize=100) 
        item_frame.grid_columnconfigure(2, minsize=100) 




    root.mainloop()

if __name__ == "__main__":
    run()