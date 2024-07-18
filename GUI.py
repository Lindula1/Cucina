"""
===CUCINA APPLICATION GUI===
Author: Lindula Pallawela Appuhamilage
Contributors: -
Date Created: 09/07/2024
Last Edited: 15/07/2024 
Version: 0.0.2.3
Description:
**PLEASE USE DISPLAY SCALE OF 100% TO ENSURE BEST RESULTS**
"""
import customtkinter as CTK
import tkinter as TK
from CUCINA import app as cucina
import tkinter.font as Font
from PIL import Image, ImageTk
import sys
import os
import keyboard
from DataStoreModel import run as dataBase
from IngredientDataStore import pantry
import ttkbootstrap as Tb
import datetime
import PDFHandler as PDF
from CTkPDFViewer import *

sys.path.insert(0, "../Cucina/Images")
sys.path.insert(0, "../Cucina/PDFs")

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
        self.item = [0,0,0,0]
        self.key = 0
        self.frA = CTK.CTkFrame(self, bg_color= "transparent")
        self.frB = CTK.CTkFrame(self, bg_color= "transparent")
        self.frC = CTK.CTkFrame(self, bg_color= "transparent")
        self.sfrBA = CTK.CTkScrollableFrame(self.frB, fg_color="#eee9e1", height=700, width=660)
        self.frBB = CTK.CTkFrame(self.frB, bg_color= "transparent")
    
    """
    INPUTS: None
    PROCESS: Loads all images from the directory to be used in the GUI.
    OUTPUTS: None
    """
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
    
    """
    INPUTS: next (int) - 
    """
    def WindowHandler(self, next):
        self.unbind_all(self.Login)
        self.unbind_all(self.Register)
        self.unbind_all(self.Click)
        self.UnmapFrames()
        if next == 0:
            self.after(0, self.AdminPage())
        elif next == 1:
            self.after(0, self.LoginWindow())
            self.after(0, self.bind('<Return>', self.Login))
        elif next == 2:
            self.after(0, self.RegistrationWindow())
            self.after(0, self.bind('<Return>', self.Register))
        elif next == 3:
            self.after(0, self.HomePage())
        elif next == 4:
            self.after(0, self.PantryPage())
        elif next == 5:
            self.after(0, self.RecipePage())

    def UnmapFrames(self):
        frames = [self.sfrBA, self.frBB, self.frA, self.frB, self.frC]
        for i in frames:
            if self.UnpackWidgets(i):
                i.pack_forget()
                i.configure(bg_color= "transparent", border_width=0)
        
    
    def LoginWindow(self):
        textVal = (self.register(self.TextCallback))
        TtlFont = CTK.CTkFont(family="Arial Black", size=80, weight=Font.BOLD)
        LblFont = CTK.CTkFont(family="Arial Bold", size=54, weight=Font.BOLD)
        BtnFont = CTK.CTkFont(family="Times Bold", size=32, weight=Font.BOLD)
        EtyFont = CTK.CTkFont(family="Helvetica", size=39, weight=Font.NORMAL) 
        titles = ["USER LOG-IN","ENTER USERNAME BELOW" ,"USERNAME", "ENTER PASSWORD BELOW", "PASSWORD", "          LOG IN          ", "      REGISTER      "]
        # Frames
        self.frA.pack(fill="both", expand=True, side="left")
        self.frB.pack(fill="both", expand=True, side="left")
        self.frC.pack(fill="both", expand=True, side="right")
        # Images
        self.btnA1 = CTK.CTkButton(self.frA, image=self.images[2], text=None, fg_color="transparent", hover_color="grey90", command=lambda: self.WindowHandler(1))
        self.btnA1.pack(padx=12, pady=32, side="top", anchor="nw")
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
        self.etyB1 = CTK.CTkEntry(self.frB, validate="all", validatecommand=(textVal, "%P"), placeholder_text=titles[2], font=EtyFont, width=760, justify="center", height=78, corner_radius=240)
        self.etyB1.pack(padx=12, pady=10)
        # Password Entry Field
        self.lblB3 = CTK.CTkLabel(self.frB, text=titles[3], font=LblFont, justify="center", width=780)
        self.lblB3.pack(padx=12, pady=10)
        self.etyB2 = CTK.CTkEntry(self.frB, placeholder_text=titles[4], font=EtyFont, show="*", width=760, justify="center", height=78, corner_radius=240)
        self.etyB2.pack(padx=12, pady=10)
        # Log In button
        self.btnB1 = CTK.CTkButton(self.frB, text=titles[5], font=BtnFont, command=lambda: self.Login(), corner_radius=30, height=80)
        self.btnB1.pack(padx=12, pady=30)
        # Register button
        self.btnB2 = CTK.CTkButton(self.frB, text=titles[6], font=BtnFont, command=lambda: self.WindowHandler(2), corner_radius=30, height=80)
        self.btnB2.pack(padx=12, pady=10, anchor="n")

    def UnpackWidgets(self, parent):
        if parent.winfo_ismapped():
            for widget in parent.winfo_children():
                widget.pack_forget()
            return True
        else:
            return False

    def Filter(self):
        filter = int(self.rdbBB1Var.get())
        self.UnpackWidgets(self.sfrBA)
        arr = pantry.SortFunc(pantry.arr, filter)
        self.after(0, self.GridFormatList(self.sfrBA, arr, [" KJ", "g", "Expiry: ", "Name: "]))

    def Select(self, item):
        # Display Item Values
        self.item = item
        itemx = item[1:5]
        self.btnBB2.configure(text="UPDATE", command=self.Update)
        for value in range(len(itemx)):
            if value == 2:
                date, days = pantry.DateRevert(item)
                date = date.split("/")
                x = self.entries[value]
                for i in range(len(x)):
                    x[i].delete(0,"end")
                    x[i].insert(0,date[i])
            else:
                self.entries[value].delete(0,"end")
                self.entries[value].insert(0,itemx[value])

    # TKinter Validation checks
    def TextCallback(self, T):
        # Existance check
        if T == "":
            return True
        # Type and Range checks
        elif T[0].isdigit() or len(T) > 34:
            return False
        return True
    
    def NameCallback(self, T):
        # Existance check
        if T == "":
            return True
        # Type and range check
        elif T[0].isdigit() or len(T) > 22:
            return False
        return True
    
    def NumCallback(self, X):
        # Type, Existance and Range check
        if (str.isdigit(X) or X == "") and len(X) < 7:
            return True
        else:
            return False
        
    def DMCallback(self, D):
        # Type, Existance and Range check
        if (str.isdigit(D) or D == "") and len(D) < 3:
            return True
        else:
            return False

    def YearCallback(self, Y):
        # Type, Existance and Range check
        if (str.isdigit(Y) or Y == "") and len(Y) < 5:
            return True
        else:
            return False
    
    def PantryPage(self):
        # Entry Box Validation
        textVal = (self.register(self.NameCallback))
        numVal = (self.register(self.NumCallback))
        dMVal = (self.register(self.DMCallback))
        yearVal = (self.register(self.YearCallback))
        # Fonts
        TtlFont = CTK.CTkFont(family="Arial Black", size=80, weight=Font.BOLD)
        LblFont = CTK.CTkFont(family="Arial Bold", size=54, weight=Font.BOLD)
        LblFont1 = CTK.CTkFont(family="Arial Bold", size=38, weight=Font.BOLD)
        BtnFont = CTK.CTkFont(family="Times Bold", size=32, weight=Font.BOLD)
        BtnFont1 = CTK.CTkFont(family="Helvetica", size=24, weight=Font.NORMAL)
        RdbFont = CTK.CTkFont(family="Helvetica", size=28, weight=Font.NORMAL)
        EtyFont = CTK.CTkFont(family="Helvetica", size=34, weight=Font.NORMAL) 
        # Text
        titles = ["YOUR PANTRY", "RECIPES", "HOME", "ADD AN ITEM", "ITEM COUNT", "ADD NEW", "CANCEL"]
        filters = ["FILTER BY NAME", "FILTER BY NUTRITION", "FILTER BY QUANTITY", "FILTER EXPIRY"]
        # Frame mapping
        self.frA.pack(fill="both", side="top")
        self.frB.pack(fill="both", expand=True, side="top", padx=80, pady=80)
        self.frB.configure(border_color="#cb9c44", border_width=7)
        self.sfrBA.pack(fill="both", expand=True, side="left", padx=7, pady=7)
        self.frBB.pack(fill="both", expand=True, side="right", padx=7, pady=7)
        # Recipe finder button
        self.btnA1 = CTK.CTkButton(self.frA, text=titles[1], font=BtnFont, width=280, command=lambda: self.WindowHandler(5), corner_radius=30, height=80)
        self.btnA1.pack(padx=12, pady=12, anchor="nw", side='left')
        # Title
        self.lblA1 = CTK.CTkLabel(self.frA, text=titles[0], font=TtlFont, justify="center", width=780, text_color="#cc5308")
        self.lblA1.pack(padx=266, pady=10, side="left", anchor="n")
        # Home button
        self.btnA2 = CTK.CTkButton(self.frA, text=titles[2], font=BtnFont, width=280, command=lambda: self.WindowHandler(3), corner_radius=30, height=80)
        self.btnA2.pack(padx=12, pady=12, anchor="ne", side="left")
        # Item View
        self.entries = []
        fields = ["NUTRITION", "ITEM COUNT", "EXPIRY DATE", "ITEM NAME"]
        dateLbl = ["0000", "00", "00"]
        for i in range(4):
            afr = CTK.CTkFrame(self.frBB, fg_color="transparent", width=680)
            afr.pack(side="top", anchor="w", padx=20, fill="x")
            lbl = CTK.CTkLabel(afr, text=fields[i], font=LblFont1, width=200, justify="left")
            lbl.pack(side="left", pady=10, padx=12, anchor="w")
            if i == 2:
                l = []
                for j in range(3):
                    dEty = CTK.CTkEntry(afr, placeholder_text=dateLbl[j], validate="all", validatecommand=(dMVal, "%P"), font=EtyFont, width=len(dateLbl[j])*69, justify="center")
                    if j == 0:
                        dEty.configure(validatecommand=(yearVal, "%P"))
                    dEty.pack(side="right", pady=10, padx=12, anchor="e")
                    l.append(dEty)
                self.entries.append(l)
            elif i == 3:
                ety = CTK.CTkEntry(afr, validate="all", validatecommand=(textVal, "%P"), placeholder_text="SELECT OR ADD", font=EtyFont, width=600, justify="center")
                ety.pack(side="right", pady=10, padx=12, anchor="e")
                self.entries.append(ety)
            else:
                ety = CTK.CTkEntry(afr, placeholder_text="0000", validate="all", validatecommand=(numVal, "%P"), font=EtyFont, width=600, justify="center")
                ety.pack(side="right", pady=10, padx=12, anchor="e")
                self.entries.append(ety)
        # Special frame
        afr0 = CTK.CTkFrame(self.frBB, fg_color="transparent", width=300)
        afr0.pack(side="top", padx=20, fill="x", expand=True, anchor="n")
        # Add/Update button
        self.btnBB2 = CTK.CTkButton(afr0, text=titles[5], font=BtnFont, width=280, command=self.Add, corner_radius=30, height=80)
        self.btnBB2.pack(pady=12, anchor="n", side="left")
        # Clear button
        self.btnBB3 = CTK.CTkButton(afr0, text=titles[6], font=BtnFont, width=280, command=self.ClearItem, corner_radius=30, height=80)
        self.btnBB3.pack(pady=12, anchor="n", side="right")
        # Filters
        self.rdbBB1Var = CTK.StringVar(value=4)
        for x in range(2):
            horiz = ["left", "right"]
            aFr2 = CTK.CTkFrame(self.frBB, fg_color="transparent", width=400)
            aFr2.pack(side=horiz[x], pady=40, padx=20)
            for z in range(2):
                snap = ["e", "w"]
                aFr3 = CTK.CTkFrame(aFr2, fg_color="transparent", width=400)
                aFr3.pack(side="top")
                lblBB1 = CTK.CTkLabel(aFr3, text=filters[x+z], font=RdbFont, width=300, height=40)
                lblBB1.pack(padx=48, pady=12, side=horiz[x], anchor=snap[x])
                self.rdbBB1 = CTK.CTkRadioButton(aFr3, text="", font=RdbFont, value=x+z, variable=self.rdbBB1Var, command=self.Filter)
                self.rdbBB1.pack(pady=12, side=horiz[x], anchor=snap[x])
        # Load Pantry
        self.after(0,self.GridFormatList(self.sfrBA, pantry.PantryList(), [" KJ", "g", "Expiry: ", "Name: "]))
    
    def Add(self):
        s = True
        self.btnBB2.configure(state="disabled")
        item = []
        for entry in range(len(self.entries)):
            if entry == 2:
                l = []
                for i in range(len(self.entries[entry])):
                    if str(self.entries[entry][i].get()) == "" or len(self.entries[entry][i].get()) < 1:
                        s = False
                        break
                    l.append(int(self.entries[entry][i].get()))
                if s:
                    try: datetime.date(int(l[0]), int(l[1]), int(l[2]))
                    except ValueError:
                        s = False
                        break
                    item.append(l)
            else:
                if str(self.entries[entry].get()) == "":
                    s = False
                    break
                item.append(self.entries[entry].get())
        self.btnBB2.configure(state="normal", command=None)
        if s:
            self.btnBB2.configure(text="SUCESS")
            cucina.AddToPantry(item)
            self.item = [0,0,0,0]
        else:
            self.btnBB2.configure(text="FAILED")
            if self.item != [0,0,0,0]: 
                print("men")
                pantry.AddRaw(self.item)
        self.after(320, self.ClearItem)

    def Update(self):
        if int(self.entries[1].get()) == 0:
            self.btnBB2.configure(state="disabled")
            pantry.Remove(self.item[4])
            self.btnBB2.configure(state="normal", command=None)
            self.after(320, self.ClearItem)
        else:
            pantry.Remove(self.item[4])
            self.Add()

    def ClearItem(self):
        self.UnpackWidgets(self.sfrBA)
        self.GridFormatList(self.sfrBA, pantry.PantryList(), [" KJ", "g", "Expiry: ", "Name: "])
        for entry in range(len(self.entries)):
            if entry == 2:
                for i in range(len(self.entries[entry])):
                    self.entries[entry][i].delete(0,"end")
            else:
                self.entries[entry].delete(0,"end")
        self.btnBB2.configure(text="ADD NEW", command=self.Add)

    def GridFormatList(self, window, arr, fields):
        BtnFont1 = CTK.CTkFont(family="Helvetica", size=16, weight=Font.NORMAL)
        for ind in range(len(arr)):
            btnTitle = ""
            title = ""
            for field in range(len(fields)):
                if field == 2:
                    d, ds = pantry.DateRevert(arr[ind])
                    date = "/".join(d.split("/")[::-1])
                    title += "[ " + fields[field] + date + "] "
                elif field == 3:
                    btnTitle = str(arr[ind][field+1])
                else:
                    title += " [" + str(arr[ind][field+1]) + fields[field] +  "] "
            bracket = CTK.CTkFrame(master=window, fg_color="transparent", width=680)
            bracket.pack(side="top", pady=12, padx=1, anchor="w")
            cell1 = CTK.CTkButton(master=bracket, text=btnTitle, font=BtnFont1, width=260, corner_radius=5, fg_color="#cd9b45", text_color="black", command=lambda x = arr[ind]: self.Select(x))
            cell1.pack(anchor="w", side="left")
            cell0 = CTK.CTkLabel(master=bracket, text=title, font=BtnFont1, width=400, corner_radius=2, fg_color="#eee9e1", text_color="black", anchor="w")
            cell0.pack(anchor="w", side="left")
            
    
    def GridCell(self, win, entry, row, column, font):
        cell = CTK.CTkEntry(win, font=font, width=156, corner_radius=2)
        cell.grid(row=row, column=column, padx=1, pady=2, sticky="N")
        cell.insert("end", entry)
        cell.configure(state="disable")
    
    def ListAccounts(self, win, accList):
        EtyFont = CTK.CTkFont(family="Helvetica", size=12, weight=Font.NORMAL)
        arr = []
        fields = ["uid", "username", "password", "name"]
        for acc in accList:
            if acc[1]["username"] == "Lindt":
                pass
            else:
                arr.append([acc[1][x] for x in acc[1]])
        for k in range(len(fields)):
            self.GridCell(win, fields[k], 0, k, EtyFont)
        for r in range(len(arr)):
            for c in range(4):
                self.GridCell(win, arr[r][c], r+1, c, EtyFont)
    
    # Following code is not part of the SRS and is added Admin functionality that is still in development
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
        self.ListAccounts(self.frD, dataBase.arr)
        lbl1 = CTK.CTkLabel(self.newCtk, text=txt[0], font=LblFont)
        lbl1.grid(row=0, column=5, sticky="n", columnspan=2)
        self.ety1 = CTK.CTkEntry(self.newCtk, placeholder_text=txt[1], font=EtyFont1, width=320)
        self.ety1.grid(row=1, column=5, sticky="n", padx=5)
        self.ety1.bind("<Key>", self.Click)
        #self.ety1.bind("<BackSpace>", self.Click)
        btn1 = CTK.CTkButton(self.newCtk, text=txt[2], font=BtnFont, command=lambda: self.AccountSearch(self.ety1.get()))
        btn1.grid(row=1, column=6, sticky="n", padx=5)
        self.newCtk.mainloop()

    def Click(self, event):
        for child in self.frD.winfo_children():
            child.grid_forget()
        input = self.ety1.get()
        if not input == "":
            arr, pos, ran = dataBase.BulkSearch(input)
            self.ListAccounts(self.frD, arr)
        else:
            self.ListAccounts(self.frD, dataBase.arr)
            
    def AccountSearch(self, entry):
        accounts, pos, posRange = dataBase.BulkSearch(entry)
        EtyFont = CTK.CTkFont(family="Helvetica", size=12, weight=Font.NORMAL)
        for child in self.frD.winfo_children():
            child.grid_forget()
        self.ListAccounts(self.frD, EtyFont, accounts)

    def HomePage(self):
        # Fonts
        TtlFont = CTK.CTkFont(family="Arial Black", size=80, weight=Font.BOLD)
        LblFont = CTK.CTkFont(family="Arial Bold", size=54, weight=Font.BOLD)
        BtnFont = CTK.CTkFont(family="Times Bold", size=32, weight=Font.BOLD)
        EtyFont = CTK.CTkFont(family="Helvetica", size=39, weight=Font.NORMAL) 
        # Admin validation
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
        self.btnA1.pack(padx=12, pady=20, side="right", anchor="ne")
        # Navigation buttons
        self.btnB2 = CTK.CTkButton(self.frB, text=titles[1], font=BtnFont, corner_radius=30, height=80, command=lambda: self.WindowHandler(5))
        self.btnB2.pack(padx=12, pady=120)
        self.btnC2 = CTK.CTkButton(self.frC, text=titles[2], font=BtnFont, corner_radius=30, height=80, command=lambda: self.WindowHandler(4))
        self.btnC2.pack(padx=12, pady=120)

    def RecipePage(self):
        # Fonts
        TtlFont = CTK.CTkFont(family="Arial Black", size=80, weight=Font.BOLD)
        LblFont = CTK.CTkFont(family="Arial Bold", size=54, weight=Font.BOLD)
        BtnFont = CTK.CTkFont(family="Times Bold", size=32, weight=Font.BOLD)
        EtyFont = CTK.CTkFont(family="Helvetica", size=39, weight=Font.NORMAL) 
        # Text
        titles = ["RECIPE FINDER", "RECIPE PREVIEW", "FOCUS", "CLEAR"]
        # Frames
        self.frA.pack(fill="both", expand=True, side="top")
        frAA = CTK.CTkFrame(self.frA, fg_color= "transparent")
        frAA.pack(side="left", fill="both", expand=True)
        frAB = CTK.CTkFrame(self.frA, fg_color= "transparent")
        frAB.pack(side="right", fill="both", expand=True)
        # Titles
        self.lblAA1 = CTK.CTkLabel(frAA, text=titles[0], font=TtlFont, justify="center", text_color="#cc5308")
        self.lblAA1.pack(padx=12, side="top", anchor="n")
        self.lblAB1 = CTK.CTkLabel(frAB, text=titles[1], font=TtlFont, justify="center", text_color="#cc5308")
        self.lblAB1.pack(padx=12, side="top", anchor="n")
        # Scrollable frames
        sfrAAA = CTK.CTkScrollableFrame(frAA, fg_color="#eee9e1", height=820, width=820)
        sfrAAA.pack(side="top", anchor="n", pady=10, padx=6)
        self.frABA = CTK.CTkFrame(frAB, fg_color="#eee9e1", height=720, width=820)
        self.frABA.pack(side="top", pady=10, padx=6)
        # Navigation buttons
        self.btnAA1 = CTK.CTkButton(frAB, text=titles[2], font=BtnFont, corner_radius=30, height=80, width=180)
        self.btnAA1.pack(padx=84, pady=24, side="left", anchor="ne")
        self.btnAA2 = CTK.CTkButton(frAB, text=titles[3], font=BtnFont, command=self.ClearRecipe, corner_radius=30, height=80, width=180)
        self.btnAA2.pack(padx=84, pady=24, side="right", anchor="nw")
        # PDF display
        self.pdfFr = CTkPDFViewer(self.frABA, file=f"../Cucina/CTkPDFViewer/0.pdf", height=700, page_height=1122, page_width=794, width=800, fg_color="transparent")
        self.pdfFr.pack(pady=10, padx=10)
        self.ListRecipes(sfrAAA, PDF.ListPDFs())

    def ListRecipes(self, window, arr):
        BtnFont1 = CTK.CTkFont(family="Helvetica", size=62, weight=Font.NORMAL)
        for i in arr:
            title = i.removesuffix(".pdf").replace("_"," ")
            cell = CTK.CTkButton(master=window, text=title, font=BtnFont1, width=800, corner_radius=2, fg_color="#eee9e1", text_color="black", anchor="w", command=lambda x = i: self.LoadPDF(x))
            cell.pack(padx=1, pady=3, anchor="w")
    
    def ClearRecipe(self):
        if self.pdfFr.winfo_ismapped():
            self.pdfFr.pack_forget()

    def LoadPDF(self, item):
        self.ClearRecipe()
        self.btnAA1.configure(command=lambda x = item: self.FocusPDF(x))
        self.pdfFr = CTkPDFViewer(self.frABA, file=f"../Cucina/PDFs/{item}", height=700, page_height=1122, page_width=794, width=800, fg_color="transparent")
        self.pdfFr.pack(pady=10, padx=10)
        self.loadedPdf = item

    # A unique page that parses a value
    """
    INPUT: item (str) - Name of the pdf that is currently loaded
    PROCESS: Displays the pdf the user selected.
    """
    def FocusPDF(self, item):
        self.UnmapFrames()
        TtlFont = CTK.CTkFont(family="Arial Black", size=62, weight=Font.BOLD)
        BtnFont = CTK.CTkFont(family="Times Bold", size=56, weight=Font.BOLD)
        self.frA.pack(fill="both", expand=True, side="left")
        self.frB.pack(fill="both", expand=True, side="right")
        title = ["RECIPE FOCUS", "BACK", "PANTRY MATCH"]
        self.lblA1 = CTK.CTkLabel(self.frA, text=title[0], width=1280, font=TtlFont)
        self.lblA1.pack(side="top", pady=10, padx=10)
        self.pdfFr = CTkPDFViewer(self.frA, file=f"../Cucina/PDFs/{item}", height=820, page_height=1683, page_width=1191, width=1220, fg_color="#eee9e1")
        self.pdfFr.pack(side="top", padx=10)
        self.btnA1 = CTK.CTkButton(self.frA, text=title[1], width=240, font=BtnFont, height=60, corner_radius=25, command=lambda: self.WindowHandler(5))
        self.btnA1.pack(side="top", pady=12, padx=46, anchor="w")
        self.lblB1 = CTK.CTkLabel(self.frB, text=title[2], width=680, font=TtlFont)
        self.lblB1.pack(side="top", pady=10, padx=10)
        self.sfrBA = CTK.CTkScrollableFrame(self.frB, fg_color="#eee9e1", width=680, height=820)
        self.sfrBA.pack(side="top")
        self.ListMatches(self.sfrBA, item)

    def ListMatches(self, window, item):
        BtnFont1 = CTK.CTkFont(family="Helvetica", size=32, weight=Font.NORMAL)
        recipe = item.removesuffix(".pdf")
        arr, match = cucina.RecipeCompare(recipe)
        for i in arr:
            title = i
            cell = CTK.CTkButton(master=window, text=title, font=BtnFont1, width=675, corner_radius=2, fg_color="#cf9a41", text_color="black", anchor="w", command=lambda x = i: self.LoadPDF(x))
            cell.pack(padx=1, pady=3, anchor="w")
    
    def RegistrationWindow(self):
        # Entry validation
        textVal = (self.register(self.TextCallback))
        # Fonts
        TtlFont = CTK.CTkFont(family="Arial Black", size=54, weight=Font.BOLD)
        LblFont = CTK.CTkFont(family="Arial Bold", size=36, weight=Font.BOLD)
        LblFont1 = CTK.CTkFont(family="Arial Bold", size=14, weight=Font.NORMAL)
        BtnFont = CTK.CTkFont(family="Times Bold", size=24, weight=Font.BOLD)
        EtyFont = CTK.CTkFont(family="Helvetica", size=28, weight=Font.NORMAL) 
        titles = [ "ACCOUNT REGISTRATION","ENTER YOUR OWN NAME BELOW" ,"NAME", "ENTER A UNIQUE USERNAME BELOW", "USERNAME", "ENTER A SECURE PASSWORD BELOW", "PASSWORD", "          REGISTER          ", "          LOGIN          "]
        prompts = ["• Do not enter numbers", "• Must be longer than 3 letters", "• Must contain atleast one non-alaphabetical character\n• Must be longer than 3 letters"]
        # Frames
        self.frA.pack(fill="both", expand=True, side="left")
        self.frB.pack(fill="both", expand=True, side="left")
        self.frC.pack(fill="both", expand=True, side="right")
        # IMAGES
        self.btnA1 = CTK.CTkButton(self.frA, image=self.images[2], text=None, fg_color="transparent", hover_color="grey90", command=lambda: self.WindowHandler(1))
        self.btnA1.pack(padx=12, pady=32, side="top", anchor="nw")
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
        self.etyB1 = CTK.CTkEntry(self.frB, validate="all", validatecommand=(textVal, "%P"), placeholder_text=titles[2], font=EtyFont, width=620, justify="center", height=68, corner_radius=240)
        self.etyB1.pack(padx=12, pady=2)
        # Username Entry Field
        self.lblB3 = CTK.CTkLabel(self.frB, text=titles[3], font=LblFont, justify="center", width=780)
        self.lblB3.pack(padx=12, pady=8)
        self.etyB2 = CTK.CTkEntry(self.frB, validate="all", validatecommand=(textVal, "%P"), placeholder_text=titles[4], font=EtyFont, width=620, justify="center", height=68, corner_radius=240)
        self.etyB2.pack(padx=12, pady=2)
        self.lblB6 = CTK.CTkLabel(self.frB, text=prompts[1], font=LblFont1, justify="center", width=780)
        self.lblB6.pack(padx=12, pady=2)
        # Password Entry Field
        self.lblB4 = CTK.CTkLabel(self.frB, text=titles[5], font=LblFont, justify="center", width=780)
        self.lblB4.pack(padx=12, pady=8)
        self.etyB3 = CTK.CTkEntry(self.frB, placeholder_text=titles[6], font=EtyFont, show="*", width=620, justify="center", height=68, corner_radius=240)
        self.etyB3.pack(padx=12, pady=2)
        self.lblB7 = CTK.CTkLabel(self.frB, text=prompts[2], font=LblFont1, justify="center", width=780)
        self.lblB7.pack(padx=12, pady=2)
        # Register button
        self.btnB1 = CTK.CTkButton(self.frB, text=titles[7], font=BtnFont, command=lambda: self.Register(), corner_radius=30, height=58)
        self.btnB1.pack(padx=12, pady=60)
       
    def Register(self, event=None):
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
            else:
                self.btnB1.configure(True, text=result.upper(), state="disabled", text_color_disabled="cornflower blue")
                self.after(640, lambda: self.btnB1.configure(True, text="REGISTER", state="normal", text_color="#fbf4ed"))

    def Login(self, event=None):
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
            else:
                self.btnB1.configure(True, text=result.upper(), state="disabled", text_color_disabled="cornflower blue")
                self.after(640, lambda: self.btnB1.configure(True, text="          LOG IN          ", state="normal", text_color="#fbf4ed"))
            
if __name__ == "__main__":
    app = App()
    app.after(0, lambda: app.state("zoomed"))
    app.WindowHandler(1)
    app.mainloop() 