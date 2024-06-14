import customtkinter as CTK
import tkinter as TK
from CUCINA import app as cucina
import tkinter.font as Font
from PIL import Image, ImageTk
import sys
import os

sys.path.insert(0, "../Cucina/Images")

CTK.set_appearance_mode("light")
CTK.set_default_color_theme("bisque-theme.json")

#aWidth, aHeight = "1920", "1080"
class App(CTK.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("CUCINA")
        #self.geometry(f"{aWidth}x{aHeight}")
        self.attributes("-fullscreen", "True")
        self.TtlFont = CTK.CTkFont(family="Arial Black", size=80, weight=Font.BOLD)
        self.LblFont = CTK.CTkFont(family="Arial Bold", size=54, weight=Font.BOLD)
        self.BtnFont = CTK.CTkFont(family="Times Bold", size=32, weight=Font.BOLD)
        self.EtyFont = CTK.CTkFont(family="Helvetica", size=39, weight=Font.NORMAL)  
        self.LoadImages()
    
    def LoadImages(self):
        self.images = []
        items = []
        with os.scandir("../Cucina/Images/") as files:
            for item in files: items.append(item.name)
        for i in range(len(items)):
            img = Image.open(f"../Cucina/Images/{i}.png")
            w, h = img.size
            if i == 4:
                self.images.append(CTK.CTkImage(Image.open(f"../Cucina/Images/{i}.png"), size=(w*0.5,h*0.5)))
            else:
                self.images.append(CTK.CTkImage(Image.open(f"../Cucina/Images/{i}.png"), size=(w*0.2,h*0.2)))
    
    def LoginWindow(self):
        titles = [ "USER LOG-IN","ENTER USERNAME BELOW" ,"USERNAME", "ENTER PASSWORD BELOW", "PASSWORD", "          LOG IN          "]
        # Frames
        self.frA = CTK.CTkFrame(self, bg_color= "transparent")
        self.frA.pack(fill="both", expand=True, side="left")
        self.frB = CTK.CTkFrame(self, bg_color= "transparent")
        self.frB.pack(fill="both", expand=True, side="left")
        self.frC = CTK.CTkFrame(self, bg_color= "transparent")
        self.frC.pack(fill="both", expand=True, side="right")
        # IMAGES
        self.btnA1 = CTK.CTkButton(self.frA, image=self.images[2], text=None, fg_color="transparent", hover_color="grey90")
        self.btnA1.pack(padx=12, pady=32, side="top")
        self.btnA2 = CTK.CTkButton(self.frA, image=self.images[4], text=None, fg_color="transparent", hover_color="grey90")
        self.btnA2.pack(padx=12, pady=160)
        self.btnC3 = CTK.CTkButton(self.frC, text="SECURITY INFORMATION\n\nTERMS OF SERVICE", fg_color="transparent", hover_color="grey90", text_color="grey4",anchor="e")
        self.btnC3.pack(padx=2, pady=32, side="top")
        self.btnC4 = CTK.CTkButton(self.frC, image=self.images[4], text=None, fg_color="transparent", hover_color="grey90")
        self.btnC4.pack(padx=12, pady=198)
        # Title
        self.lblB1 = CTK.CTkLabel(self.frB, text=titles[0], font=self.TtlFont, justify="center", width=780, text_color="#cc5308")
        self.lblB1.pack(padx=12, pady=46)
        # Username Entry Field
        self.lblB2 = CTK.CTkLabel(self.frB, text=titles[1], font=self.LblFont, justify="center", width=780)
        self.lblB2.pack(padx=12, pady=10)
        self.etyB1 = CTK.CTkEntry(self.frB, placeholder_text=titles[2], font=self.EtyFont, width=760, justify="center", height=78, corner_radius=240)
        self.etyB1.pack(padx=12, pady=10)
        # Password Entry Field
        self.lblB3 = CTK.CTkLabel(self.frB, text=titles[3], font=self.LblFont, justify="center", width=780)
        self.lblB3.pack(padx=12, pady=10)
        self.etyB2 = CTK.CTkEntry(self.frB, placeholder_text=titles[4], font=self.EtyFont, show="*", width=760, justify="center", height=78, corner_radius=240)
        self.etyB2.pack(padx=12, pady=10)
        # Log In button
        self.btnB1 = CTK.CTkButton(self.frB, text=titles[5], font=self.BtnFont, command=lambda: self.Login(), corner_radius=30, height=80)
        self.btnB1.pack(padx=12, pady=75)

    def Login(self):
        usrm = self.etyB1.get()
        pwrd = self.etyB2.get()
        if usrm == "" or pwrd == "":
            pass
        else:
            result = cucina.LogIn(usrm, pwrd)
            self.btnB1.configure(True, text=result.upper(), state="disabled", text_color="yellow")
    
if __name__ == "__main__":
    app = App()
    app.after(0, lambda:app.state("zoomed"))
    app.LoginWindow()
    app.mainloop() 