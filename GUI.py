import customtkinter as CTK
import tkinter as TK
from CUCINA import app as cucina
import tkinter.font as Font
from PIL import Image, ImageTk
import sys
import os
import keyboard
from DataStoreModel import run as dataBase


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
        self.LoadImages()
        self.lgnFailCount = 0
        self.key = ""
        self.frA = CTK.CTkFrame(self, bg_color= "transparent")
        self.frB = CTK.CTkFrame(self, bg_color= "transparent")
        self.frC = CTK.CTkFrame(self, bg_color= "transparent")
        self.frBA = CTK.CTkFrame(self.frB, bg_color= "transparent")
        self.frBB = CTK.CTkFrame(self.frB, bg_color= "transparent")
    
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
    
    def WindowHandler(self, next):
        self.UnmapFrames()
        if next == 0:
            self.after(0, self.AdminPage())
        elif next == 1:
            self.after(0, self.LoginWindow())
            #self.after(0, self.bind('<Return>', self.Login))
        elif next == 2:
            #self.after(0, self.bind('<Return>', self.Register))
            self.after(0, self.RegistrationWindow())
        elif next == 3:
            self.after(0, self.HomePage())

    def UnmapFrames(self):
        if self.frA.winfo_ismapped():
            for widget in self.frA.winfo_children():
                widget.pack_forget()
        if self.frB.winfo_ismapped():
            for widget in self.frB.winfo_children():
                widget.pack_forget()
        if self.frC.winfo_ismapped():
            for widget in self.frC.winfo_children():
                widget.pack_forget()
    
    def LoginWindow(self):
        TtlFont = CTK.CTkFont(family="Arial Black", size=80, weight=Font.BOLD)
        LblFont = CTK.CTkFont(family="Arial Bold", size=54, weight=Font.BOLD)
        BtnFont = CTK.CTkFont(family="Times Bold", size=32, weight=Font.BOLD)
        EtyFont = CTK.CTkFont(family="Helvetica", size=39, weight=Font.NORMAL) 
        titles = ["USER LOG-IN","ENTER USERNAME BELOW" ,"USERNAME", "ENTER PASSWORD BELOW", "PASSWORD", "          LOG IN          ", "      REGISTER      "]
        # Frames
        self.frA.pack(fill="both", expand=True, side="left")
        self.frB.pack(fill="both", expand=True, side="left")
        self.frC.pack(fill="both", expand=True, side="right")
        # IMAGES
        self.btnA1 = CTK.CTkButton(self.frA, image=self.images[2], text=None, fg_color="transparent", hover_color="grey90")
        self.btnA1.pack(padx=12, pady=32, side="top")
        self.btnA2 = CTK.CTkButton(self.frA, image=self.images[4], text=None, fg_color="transparent", hover_color="grey90")
        self.btnA2.pack(padx=12, pady=160)
        self.btnC3 = CTK.CTkButton(self.frC, text="SECURITY INFORMATION\n\nTERMS OF SERVICE", fg_color="transparent", hover_color="grey90", text_color="grey4",anchor="e")
        self.btnC3.pack(padx=12, pady=12, side="top", anchor="ne")
        self.btnC4 = CTK.CTkButton(self.frC, image=self.images[4], text=None, fg_color="transparent", hover_color="grey90")
        self.btnC4.pack(padx=12, pady=198)
        # Title
        self.lblB1 = CTK.CTkLabel(self.frB, text=titles[0], font=TtlFont, justify="center", width=780, text_color="#cc5308")
        self.lblB1.pack(padx=12, pady=46)
        # Username Entry Field
        self.lblB2 = CTK.CTkLabel(self.frB, text=titles[1], font=LblFont, justify="center", width=780)
        self.lblB2.pack(padx=12, pady=10)
        self.etyB1 = CTK.CTkEntry(self.frB, placeholder_text=titles[2], font=EtyFont, width=760, justify="center", height=78, corner_radius=240)
        self.etyB1.pack(padx=12, pady=10)
        # Password Entry Field
        self.lblB3 = CTK.CTkLabel(self.frB, text=titles[3], font=LblFont, justify="center", width=780)
        self.lblB3.pack(padx=12, pady=10)
        self.etyB2 = CTK.CTkEntry(self.frB, placeholder_text=titles[4], font=EtyFont, show="*", width=760, justify="center", height=78, corner_radius=240)
        self.etyB2.pack(padx=12, pady=10)
        # Log In button
        self.btnB1 = CTK.CTkButton(self.frB, text=titles[5], font=BtnFont, command=lambda: self.Login(), corner_radius=30, height=80)
        self.btnB1.pack(padx=12, pady=30)
        # Regist button
        self.btnB2 = CTK.CTkButton(self.frB, text=titles[6], font=BtnFont, command=lambda: self.WindowHandler(2), corner_radius=30, height=80)
        self.btnB2.pack(padx=12, pady=10, anchor="n")
    
    def GridCell(self, win, entry, row, column, font):
        cell = CTK.CTkEntry(win, font=font, width=156, corner_radius=2)
        cell.grid(row=row, column=column, padx=1, pady=2, sticky="N")
        cell.insert("end", entry)
        cell.configure(state="disable")
    
    def ListAccounts(self, win, font, accList):
        arr = []
        fields = []
        for field in accList[0][1]:
                    fields.append(field)
        for acc in accList:
            if acc[1]["username"] == "Lindt":
                pass
            else:
                arr.append([acc[1][x] for x in acc[1]])
        for k in range(len(fields)):
            self.GridCell(win, fields[k], 0, k, font)
        for r in range(len(arr)):
            for c in range(4):
                self.GridCell(win, arr[r][c], r+1, c, font)
    
    def AdminPage(self):
        self.WindowHandler(3)
        self.newCtk = CTK.CTk()
        #newCtk.geometry("1600x600")
        self.newCtk.title("Admin Access")
        txt = ["ACCOUNT SEARCH", "ENTER USERNAME", "SEARCH"]
        self.frD = CTK.CTkScrollableFrame(self.newCtk, bg_color= "transparent", width=630, height=570)
        self.frD.grid(row=0, column=0, columnspan=4, rowspan=50)
        TtlFont = CTK.CTkFont(family="Arial Black", size=80, weight=Font.BOLD)
        LblFont = CTK.CTkFont(family="Arial Bold", size=48, weight=Font.BOLD)
        BtnFont = CTK.CTkFont(family="Times Bold", size=32, weight=Font.BOLD)
        EtyFont = CTK.CTkFont(family="Helvetica", size=12, weight=Font.NORMAL)
        EtyFont1 = CTK.CTkFont(family="Helvetica", size=32, weight=Font.NORMAL)
        self.ListAccounts(self.frD, EtyFont, cucina.dtList)
        lbl1 = CTK.CTkLabel(self.newCtk, text=txt[0], font=LblFont)
        lbl1.grid(row=0, column=5, sticky="n", columnspan=2)
        self.ety1 = CTK.CTkEntry(self.newCtk, placeholder_text=txt[1], font=EtyFont1, width=320)
        self.ety1.grid(row=1, column=5, sticky="n", padx=5)
        self.ety1.bind("<Key>", self.Click)
        self.ety1.bind("<BackSpace>", self.Click)
        btn1 = CTK.CTkButton(self.newCtk, text=txt[2], font=BtnFont, command=lambda: self.AccountSearch(self.ety1.get()))
        btn1.grid(row=1, column=6, sticky="n", padx=5)
        self.newCtk.mainloop()
    
    def Click(self, event):
        EtyFont = CTK.CTkFont(family="Helvetica", size=12, weight=Font.NORMAL)
        entry = self.ety1.get()
        if len(entry) > 0:
            self.AccountSearch(entry)
        elif len(entry) == 0:
            for child in self.frD.winfo_children():
                child.grid_forget()
            self.ListAccounts(self.frD, EtyFont, cucina.dtList)

    def AccountSearch(self, entry):
        accounts, pos, posRange = dataBase.BulkSearch(entry)
        EtyFont = CTK.CTkFont(family="Helvetica", size=12, weight=Font.NORMAL)
        for child in self.frD.winfo_children():
            child.grid_forget()
        self.ListAccounts(self.frD, EtyFont, accounts)

    def HomePage(self):
        TtlFont = CTK.CTkFont(family="Arial Black", size=80, weight=Font.BOLD)
        LblFont = CTK.CTkFont(family="Arial Bold", size=54, weight=Font.BOLD)
        BtnFont = CTK.CTkFont(family="Times Bold", size=32, weight=Font.BOLD)
        EtyFont = CTK.CTkFont(family="Helvetica", size=39, weight=Font.NORMAL) 
        try:
            name = self.account[1]["name"]
            titles = [name + "'s Kitchen", "DISCOVER RECIPES", "SEARCH YOUR PANTRY", "LOGOUT"]
            self.btnA0 = CTK.CTkButton(self.frA, text=titles[3], font=BtnFont, corner_radius=30, height=80, text_color_disabled="#f3e8c6", fg_color="#f3e8c6", hover="#f3e8c6",text_color="#f3e8c6", command=None)
        except KeyError:
            titles = ["Admin Access", "DISCOVER RECIPES", "SEARCH YOUR PANTRY", "LOGOUT"]
            self.btnA0 = CTK.CTkButton(self.frA, text=" ADMIN ", font=BtnFont, corner_radius=30, height=80, command=lambda: self.WindowHandler(0))
        # Frames
        self.frA.pack(fill="both", expand=True, side="top")
        self.frB.pack(fill="both", expand=True, side="left")
        self.frC.pack(fill="both", expand=True, side="right")
        #self.frBA.pack(fill="both", expand=True, side="left")
        #self.frBB.pack(fill="both", expand=True, side="right")
        # IMAGES
        self.btnB1 = CTK.CTkButton(self.frB, image=self.images[4], text=None, fg_color="transparent", hover_color="grey90")
        self.btnB1.pack(padx=12, pady=10, side="top", fill="y")
        self.btnC2 = CTK.CTkButton(self.frC, image=self.images[4], text=None, fg_color="transparent", hover_color="grey90")
        self.btnC2.pack(padx=12, pady=10, side="top", fill="y")
        # Alignment button
        self.btnA0.pack(padx=12, pady=20, side="left", anchor="ne")
        # Title
        self.lblA1 = CTK.CTkLabel(self.frA, text=titles[0], font=TtlFont, justify="center", text_color="#cc5308")
        self.lblA1.pack(padx=12, pady=20, side="left", anchor="n", fill="x", expand=True)
        # Log Out button
        self.btnA1 = CTK.CTkButton(self.frA, text=titles[3], font=BtnFont, command=lambda: self.WindowHandler(1), corner_radius=30, height=80)
        self.btnA1.pack(padx=12, pady=12, side="right", anchor="ne")
        # Navigation buttons
        self.btnB2 = CTK.CTkButton(self.frB, text=titles[1], font=BtnFont, command=lambda: None, corner_radius=30, height=80)
        self.btnB2.pack(padx=12, pady=120)
        self.btnC2 = CTK.CTkButton(self.frC, text=titles[2], font=BtnFont, command=lambda: None, corner_radius=30, height=80)
        self.btnC2.pack(padx=12, pady=120)
    
    def RegistrationWindow(self):
        TtlFont = CTK.CTkFont(family="Arial Black", size=54, weight=Font.BOLD)
        LblFont = CTK.CTkFont(family="Arial Bold", size=36, weight=Font.BOLD)
        BtnFont = CTK.CTkFont(family="Times Bold", size=24, weight=Font.BOLD)
        EtyFont = CTK.CTkFont(family="Helvetica", size=28, weight=Font.NORMAL) 
        titles = [ "ACCOUNT REGISTRATION","ENTER YOUR OWN NAME BELOW" ,"NAME", "ENTER A UNIQUE USERNAME BELOW", "USERNAME", "ENTER A SECURE PASSWORD BELOW", "PASSWORD", "          REGISTER          ", "          LOGIN          "]
        # Frames
        self.frA.pack(fill="both", expand=True, side="left")
        self.frB.pack(fill="both", expand=True, side="left")
        self.frC.pack(fill="both", expand=True, side="right")
        # IMAGES
        self.btnA1 = CTK.CTkButton(self.frA, image=self.images[2], text=None, fg_color="transparent", hover_color="grey90")
        self.btnA1.pack(padx=12, pady=32, side="top")
        self.btnA2 = CTK.CTkButton(self.frA, image=self.images[4], text=None, fg_color="transparent", hover_color="grey90")
        self.btnA2.pack(padx=12, pady=160)
        self.btnC3 = CTK.CTkButton(self.frC, text="SECURITY INFORMATION\n\nTERMS OF SERVICE", fg_color="transparent", hover_color="grey90", text_color="grey4",anchor="e")
        self.btnC3.pack(padx=30, pady=32, side="top", anchor="ne")
        self.btnC4 = CTK.CTkButton(self.frC, image=self.images[4], text=None, fg_color="transparent", hover_color="grey90")
        self.btnC4.pack(padx=12, pady=198)
        # Title
        self.lblB1 = CTK.CTkLabel(self.frB, text=titles[0], font=TtlFont, justify="center", width=780, text_color="#cc5308")
        self.lblB1.pack(padx=12, pady=40)
        # Name Entry Field
        self.lblB2 = CTK.CTkLabel(self.frB, text=titles[1], font=LblFont, justify="center", width=780)
        self.lblB2.pack(padx=12, pady=8)
        self.etyB1 = CTK.CTkEntry(self.frB, placeholder_text=titles[2], font=EtyFont, width=620, justify="center", height=68, corner_radius=240)
        self.etyB1.pack(padx=12, pady=8)
        # Username Entry Field
        self.lblB3 = CTK.CTkLabel(self.frB, text=titles[3], font=LblFont, justify="center", width=780)
        self.lblB3.pack(padx=12, pady=8)
        self.etyB2 = CTK.CTkEntry(self.frB, placeholder_text=titles[4], font=EtyFont, width=620, justify="center", height=68, corner_radius=240)
        self.etyB2.pack(padx=12, pady=8)
        # Password Entry Field
        self.lblB4 = CTK.CTkLabel(self.frB, text=titles[5], font=LblFont, justify="center", width=780)
        self.lblB4.pack(padx=12, pady=8)
        self.etyB3 = CTK.CTkEntry(self.frB, placeholder_text=titles[6], font=EtyFont, show="*", width=620, justify="center", height=68, corner_radius=240)
        self.etyB3.pack(padx=12, pady=8)
        # Register button
        self.btnB1 = CTK.CTkButton(self.frB, text=titles[7], font=BtnFont, command=lambda: self.Register(), corner_radius=30, height=58)
        self.btnB1.pack(padx=12, pady=60)
        # Log in button
        #self.btnB2 = CTK.CTkButton(self.frB, text=titles[8], font=BtnFont, command=lambda: self.WindowHandler(1), corner_radius=30, height=32)
    
    def Register(self):
        name = self.etyB1.get()
        usrm = self.etyB2.get()
        pwrd = self.etyB3.get()
        self.etyB1.delete(0, CTK.END)
        self.etyB2.delete(0, CTK.END)
        self.etyB3.delete(0, CTK.END)
        if name == "" or usrm == "" or pwrd == "":
            pass
        else:
            result = cucina.RegisterAccount(usrm, pwrd, name)
            if result == "Success":
                self.btnB1.configure(True, text=result.upper(), state="disabled", text_color_disabled="cornflower blue")
                self.after(640, lambda: self.btnB1.configure(True, text="LOG IN TO YOUR NEW ACCOUNT", state="normal", text_color="#fbf4ed", command=lambda: self.WindowHandler(1)))
                #self.btnB2.pack(padx=12, pady=10)
            else:
                self.btnB1.configure(True, text=result.upper(), state="disabled", text_color_disabled="cornflower blue")
                self.after(640, lambda: self.btnB1.configure(True, text="REGISTER", state="normal", text_color="#fbf4ed"))

    def Login(self):
        usrm = self.etyB1.get()
        pwrd = self.etyB2.get()
        self.etyB1.delete(0, CTK.END)
        self.etyB2.delete(0, CTK.END)
        if usrm == "" or pwrd == "":
            pass
        else:
            result = cucina.LogIn(usrm, pwrd)
            if result == "Logged in as Admin" or result == "Login successful":
                self.btnB1.configure(True, text=result.upper(), state="disabled", text_color_disabled="cornflower blue")
                self.account = cucina.Search(usrm)
                self.WindowHandler(3)
            elif self.lgnFailCount > 0:
                self.btnB1.configure(True, text=result.upper(), state="disabled", text_color_disabled="cornflower blue")
                self.after(640, lambda: self.btnB1.configure(True, text="          LOG IN          ", state="normal", text_color="#fbf4ed"))
                #self.btnB2.pack(padx=12, pady=10)
            else:
                self.lgnFailCount += 1
                self.btnB1.configure(True, text=result.upper(), state="disabled", text_color_disabled="cornflower blue")
                self.after(640, lambda: self.btnB1.configure(True, text="          LOG IN          ", state="normal", text_color="#fbf4ed"))
            
if __name__ == "__main__":
    app = App()
    app.after(0, lambda: app.state("zoomed"))
    app.WindowHandler(1)
    app.mainloop() 