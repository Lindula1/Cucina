"""
===CUCINA APPLICATION GUI===
Author: Lindula Pallawela Appuhamilage
Contributors: -
Date Created: 09/07/2024
Last Edited: 25/07/2024 
Version: 1.0.6.2 (Alpha Release)
Description:
PLEASE READ THIS BEFORE ATTEMPTING TO UNDERSTAND MY CODE
My ctk widget naming format:
    Example [self.btnA1]
    btn/lbl/ety refers to the type of widget, button/label/entry respectively
    A/B/C/BB refers to the frame the widget is a 'slave' of.
    number 0-9 refers to the widget number
    SPECIAL CASES
    'self.sfr'/'sfr' refers to a scrollable frame
    'afr' without the 'self.' prefix is an alignment frame only mapped within that
    window and not callable in any other window.
    A widget lacking the perfix 'self.' is usually mapped through a loop and is not
    called outside of the window.

This method is used because within the object these variables are universal and can be
called and re-assigned anywhere. 

pyinstaller --noconfirm --onedir --noconsole Cucina_App.py
"""

# Module import check of all imported scripts
try:
    import customtkinter as CTK
    import tkinter as TK 
    import tkinter.font as Font
    from PIL import Image
    import sys
    import os
    import datetime
    from CTkPDFViewer import *
    import ctypes
    import PDFHandler as PDF

except ModuleNotFoundError as missing:
    print("\033[31mERROR. Dependenant modules missing.\nThe software must terminate\033[0m")
    print(f"You're missing: {missing.name}\nTry running: pip install -r requirements.txt")
    exit()

# A unique validation check to prevent entry of Chinese characters
alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

sys.path.insert(0, "../Cucina/Images")
sys.path.insert(0, "../Cucina/PDFs")

class App(CTK.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("CUCINA")
        self.attributes("-fullscreen", "True") 
        self.item = ["0","0","0","0","0"]
        self.loaded = False
        self.itemNames = [" Cal", "g", " Left", " Days to use", "Name: "]
        self.key = 0
        self.saveLogin = ""
        self.enbSaveLogin = False
        # Creating main frames. These frames are used all throughout the code and are constant
        self.frA = CTK.CTkFrame(self, fg_color= "transparent")
        self.frB = CTK.CTkFrame(self, fg_color= "transparent")
        self.frC = CTK.CTkFrame(self, fg_color= "transparent")
        self.sfrBA = CTK.CTkScrollableFrame(self.frB, fg_color="#eee9e1", height=700, width=660)
        self.frBB = CTK.CTkFrame(self.frB, bg_color= "transparent")
    
    """
    INPUTS: None
    PROCESS:
    Scans image directory for possible pngs and appends the names to a list.
    Iterates through the list and loads all images as a PIL object which
    is appended to a list. If a file is not found an error is sent.
    OUTPUTS: (bool) - If an error is detected True is passed.
    """
    def LoadImages(self):
        self.images = []
        items = []
        try:
            with os.scandir("../Cucina/Images/") as files:
                for item in files: items.append(item.name)
            for i in range(len(items)):
                img = Image.open(f"../Cucina/Images/{i}.png")
                w, h = img.size
                self.images.append(CTK.CTkImage(img, size=(w,h)))
            return False
        except FileNotFoundError:
            return True
        
    """
    INPUTS: next (int) - The index of the next window to display.

    PROCESS:
        Unbinds all current bindings and unmaps all frames.
        Depending on the value of 'next' set a new window to display after a delay of 0 milliseconds:
        - 0: AdminPage
        - 1: LoginWindow and binds the Enter key to the Login function
        - 2: RegistrationWindow and binds the Enter key to the Register function
        - 3: HomePage
        - 4: PantryPage
        - 5: RecipePage
        - other: LoadingScreen

    OUTPUTS: None
    """
    def WindowHandler(self, next):
        self.unbind_all(self.Login)
        self.unbind_all(self.Register)
        self.unbind_all(self.Click)
        self.UnmapFrames()
        if next == 0:
            print(self.account)
            if len(self.account[1]) < 4:
                self.after(0, self.AdminPage())
            else:
                self.after(0, self.AccountPage())
        elif next == 1:
            self.after(0, self.LoginWindow())
            self.bind('<Return>', self.Login)
        elif next == 2:
            self.after(0, self.RegistrationWindow())
            self.bind('<Return>', self.Register)
        elif next == 3:
            self.after(0, self.HomePage())
        elif next == 4:
            self.after(0, self.PantryPage())
        elif next == 5:
            self.after(0, self.RecipePage())
        else:
            self.after(0, self.LoadingScreen())

    def AccountPage(self):
        # Fonts
        TtlFont = CTK.CTkFont(family="Arial Black", size=80, weight=Font.BOLD)
        LblFont = CTK.CTkFont(family="Arial Bold", size=54, weight=Font.BOLD)
        EtyFont = CTK.CTkFont(family="Helvetica", size=39, weight=Font.NORMAL)
        BtnFont = CTK.CTkFont(family="Times Bold", size=32, weight=Font.BOLD)
        # Texts
        titles = ["ACCOUNT SETTINGS", "BACK", "CONTINUE?"]
        # Frames
        self.frA.pack(fill="x", side="top")
        self.frB.pack(fill="both", side="left", padx=20)
        self.frC.pack(fill="both", side="right", padx=20)
        # Title
        self.lblB1 = CTK.CTkLabel(self.frA, text=titles[0], font=TtlFont, justify="center", width=780, text_color="#cc5308")
        self.lblB1.pack(padx=12, pady=46)
        # Headers
        for key in self.account[1]:
            afr0 = CTK.CTkFrame(self.frB, width=600)
            afr0.pack(side="top", pady=40, anchor="e")
            self.lblA1 = CTK.CTkLabel(afr0, text=key, font=LblFont, justify="right", width=340)
            self.lblA1.pack(side="right", anchor="e")

    def LoadingScreen(self):
        # Fonts
        LblFont = CTK.CTkFont(family="Arial Bold", size=54, weight=Font.BOLD)
        BtnFont = CTK.CTkFont(family="Times Bold", size=32, weight=Font.BOLD)
        titles = ["LOADING...", "TERMINATE", "CONTINUE?"]
        # Frames
        self.frA.pack(fill="both", side="top")
        afr0 = CTK.CTkFrame(self.frA, fg_color= "transparent")
        afr0.pack(fill="x", side="top", pady=300)
        # Progress Label
        self.lblA1 = CTK.CTkLabel(afr0, text=titles[0], font=LblFont, justify="center", width=780)
        self.lblA1.pack(side="top")
        # Progress Bar
        self.progressBar = CTK.CTkProgressBar(afr0, orientation="horizontal", width=1680, height=45, determinate_speed=6)
        self.progressBar.set(0)
        self.progressBar.pack(side="top")
        # Navigation Buttons
        self.btnA0 = CTK.CTkButton(afr0, text=titles[1], font=BtnFont, width=280, text_color="black", height=70, command=self.destroy, corner_radius=30)
        self.btnA1 = CTK.CTkButton(afr0, text=titles[2], font=BtnFont, width=280, height=70, command= lambda: self.WindowHandler(1), corner_radius=30)
        self.loaded = True
        self.after(60, self.Load)
                
    def Load(self):
        for i in range(5):
            if i == 0 and self.loaded:
                global cucina
                from CUCINA import app as cucina
                lambda: self.Progress(cucina.disableLogin, i)
            elif i == 1 and self.loaded:
                self.Progress(self.LoadImages(), i)
            elif i == 2 and self.loaded:
                global dataBase
                from DataStoreModel import run as dataBase
                # Save Login Data
                self.Progress(dataBase.checks, i)
            elif i == 3 and self.loaded:
                global pantry
                from IngredientDataStore import pantry
                self.Progress(pantry.checks, i)
            if self.loaded and i == 4:
                self.after(10, lambda: self.WindowHandler(1))

    """
    INPUTS: 
        result (bool) - The result status of a loading process.
        i (int) - The index corresponding to the current process (0: Database, 1: Accounts, 2: Images, 3: Pantry).

    PROCESS:
        Updates the label and progress bar based on the result of the loading process.
        If an error is detected (result is True), it configures the label with an error message and displays buttons for further actions. It also sets the progress bar color to indicate an issue.
        If no error is detected (result is False), it updates the label to show the successful loading of the current process and advances the progress bar.

    OUTPUTS: None
    """
    def Progress(self, result, i):
        results = ["Database", "Accounts", "Images", "Pantry"]
        errors = ["FATAL ERROR: Cucina Functionality failed to load\nThe software MUST be terminated", "ERROR: Images did not load properly\nThe software should be terminated", "FATAL ERROR: Database not load\nThe software should be terminated", "Pantry file missing\nNew pantry file can be made"]
        if result:
            self.lblA1.configure(text=errors[i], text_color="red")
            self.btnA0.pack(side="top", pady=20)
            self.btnA1.pack(side="top", pady=20)
            self.progressBar.configure(progress_color="#dd8d3c")
            self.loaded = False
        else:
            self.lblA1.configure(text=f"Loaded {results[i]}")
            self.progressBar.step()
            self.loaded = True
    """
    INPUTS: None

    PROCESS:
        Iterates through a predefined list of frames.
        For each frame, calls the UnpackWidgets function.
        If UnpackWidgets returns True, the frame is hidden and its background color and border width are configured to be transparent and zero, respectively.

    OUTPUTS: None
    """
    def UnmapFrames(self):
        frames = [self.sfrBA, self.frBB, self.frA, self.frB, self.frC]
        for i in frames:
            if self.UnpackWidgets(i):
                i.pack_forget()
                i.configure(bg_color= "transparent", border_width=0)
    
    def EnableSaveLogin(self):
        if self.enbSaveLogin == False:
            self.btnB3.configure(text_color="green", text="LOGIN INFORMATION SAVED")
            self.enbSaveLogin = True
        elif self.enbSaveLogin == True:
            self.btnB3.configure(text_color="black", text="SAVE LOGIN INFORMATION")
            self.enbSaveLogin = False
            self.LoginInfo(self.enbSaveLogin)
    
    def LoginWindow(self):
        self.logindta = dataBase.LoadLoginInfo()
        textVal = (self.register(self.TextCallback))
        TtlFont = CTK.CTkFont(family="Arial Black", size=80, weight=Font.BOLD)
        LblFont = CTK.CTkFont(family="Arial Bold", size=54, weight=Font.BOLD)
        BtnFont = CTK.CTkFont(family="Times Bold", size=32, weight=Font.BOLD)
        BtnFont1 = CTK.CTkFont(family="Times Bold", size=24, weight=Font.BOLD)
        EtyFont = CTK.CTkFont(family="Helvetica", size=39, weight=Font.NORMAL)
        # Texts
        titles = ["USER LOG-IN","ENTER USERNAME BELOW" ,"USERNAME", "ENTER PASSWORD BELOW", "PASSWORD", "          LOG IN          ", "REGISTER NEW","SAVE LOGIN INFORMATION"]
        # Frames
        self.frA.pack(fill="both", expand=True, side="left")
        self.frB.pack(fill="both", expand=True, side="left")
        self.frC.pack(fill="both", expand=True, side="right")
        # Images
        self.btnA1 = CTK.CTkButton(self.frA, image=self.images[2], text=None, fg_color="transparent", hover_color="grey90", command=lambda: self.WindowHandler(1))
        self.btnA1.pack(padx=12, pady=32, side="top", anchor="nw")
        self.btnA2 = CTK.CTkButton(self.frA, image=self.images[4], text=None, fg_color="transparent", width=420, hover=False)
        self.btnA2.pack(padx=12, pady=160)
        self.btnC3 = CTK.CTkButton(self.frC, text="CLOSE APP", font=BtnFont, command=self.destroy, height=80, width=200, corner_radius=30)
        self.btnC3.pack(padx=24, pady=24, side="top", anchor="ne")
        self.btnC4 = CTK.CTkButton(self.frC, image=self.images[5], text=None, fg_color="transparent", width=420, hover=False)
        self.btnC4.pack(padx=12, pady=200)
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
        # Save login button
        self.btnB3 = CTK.CTkButton(self.frB, text=titles[7], font=BtnFont1, command=self.EnableSaveLogin, fg_color="transparent", hover_color="#f3e8c6", text_color="black")
        self.btnB3.pack(padx=12, pady=2)
        # Log In button
        self.btnB1 = CTK.CTkButton(self.frB, text=titles[5], font=BtnFont, command=lambda: self.Login(), corner_radius=30, height=80)
        self.btnB1.pack(padx=12, pady=30)
        # Register button
        self.btnB2 = CTK.CTkButton(self.frB, text=titles[6], font=BtnFont, command=lambda: self.WindowHandler(2), corner_radius=30, height=80)
        self.btnB2.pack(padx=12, pady=12, anchor="n")
        if self.logindta != None:
            self.etyB1.insert(0, str(self.logindta))
            self.btnB3.configure(text_color="green", text="LOGIN INFORMATION SAVED")
            self.enbSaveLogin = True

    """
    INPUTS: parent (widget) - The parent widget containing child widgets to be unpacked.

    PROCESS:
        Checks if the parent widget is currently mapped (visible).
        If the parent widget is mapped:
            Iterates through all child widgets of the parent.
            Hides each child widget using pack_forget().
            Returns True.
        If the parent widget is not mapped:
            Returns False.

    OUTPUTS: (bool) - True if the parent widget was mapped and its children were unpacked, otherwise False.
    """
    def UnpackWidgets(self, parent):
        if parent.winfo_ismapped():
            for widget in parent.winfo_children():
                widget.pack_forget()
            return True
        else:
            return False

    """
    INPUTS: None

    PROCESS:
        Retrieves the current value of the radio button variable `rdbBB1Var` and increments it by 1 to determine the filter.
        Calls the UnpackWidgets method on the frame `sfrBA` to hide any currently displayed widgets.
        Sorts the pantry array `pantry.arr` using the SortFunc method with the determined filter.
        Calls the GridFormatList method to display the sorted array in a grid format within the `sfrBA` frame.

    OUTPUTS: None
    """
    def Filter(self):
        filter = int(self.rdbBB1Var.get()) + 1
        self.UnpackWidgets(self.sfrBA)
        arr = pantry.SortFunc(pantry.arr, filter)
        self.after(0, self.GridFormatList(self.sfrBA, arr, self.itemNames))

    """
    INPUTS: item (list) - The selected item to be displayed and updated.

    PROCESS:
        Sets the instance variable `self.item` to the selected item.
        Extracts the relevant portion of the item (item[1:6]) for display.
        Configures the button `btnBB2` to display "UPDATE" and binds it to the Update method.
        Iterates through the extracted item values:
            If the current value index is 3, converts the date using the DateRevert method and splits it into components to populate multiple entry fields.
            For other values, clears the respective entry field and inserts the corresponding item value.

    OUTPUTS: None
    """
    def Select(self, item):
        # Display Item Values
        self.item = item
        itemx = item[1:6]
        self.btnBB2.configure(text="UPDATE", command=self.Update)
        for value in range(len(itemx)):
            if value == 3:
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
    """
    INPUTS: T (str) - The text input to be checked.

    PROCESS:
        Checks if the text input `T` is an empty string:
            If it is empty, returns True.
        If the text is not empty, performs the following checks:
            Checks if the first character of `T` (converted to uppercase) is not in the `alpha` set or if the length of `T` exceeds 28 characters:
                If either condition is met, returns False.
            If none of the conditions are met, returns True.

    OUTPUTS: (bool) - Returns True if the input is either an empty string or meets the type and range checks, otherwise returns False.
    """
    def TextCallback(self, T):
        # Existance check
        if T == "":
            return True
        # Type and Range checks
        elif (T[0].upper() not in alpha) or len(T) > 28:
            return False
        return True
    
    """
    INPUTS: T (str) - The text input to be checked.

    PROCESS:
    Checks if the text input `T` is an empty string:
        If it is empty, returns True.
    If the text is not empty, performs the following checks:
        Checks if the stripped text is non-empty and its first character is a digit:
            If so, returns False.
        Checks if the length of `T` exceeds 22 characters:
            If so, returns False.
    If none of the conditions are met, returns True.

    OUTPUTS: (bool) - Returns True if the input is either an empty string, or meets the type and range checks, otherwise returns False.
    """
    def NameCallback(self, T):
        # Existance check
        if T == "":
            return True
        # Type and range check
        elif len(T.strip()) > 0:
            if T.strip()[0].isdigit(): return False
        elif len(T) > 22:
            return False
        return True
    
    """
    INPUTS: X (str) - The text input to be checked.

    PROCESS:
    Checks if the text input `X` is either a digit or an empty string and its length is less than 7 characters:
        If both conditions are met, returns True.
        If either condition is not met, returns False.

    OUTPUTS: (bool) - Returns True if the input is either a digit or an empty string and its length is less than 7, otherwise returns False.
    """
    def NumCallback(self, X):
        # Type, Existance and Range check
        if (str.isdigit(X) or X == "") and len(X) < 7:
            return True
        else:
            return False
    
    """
    INPUTS: D (str) - The text input to be checked.

    PROCESS:
    Checks if the text input `D` is either a digit or an empty string and its length is less than 3 characters:
        If both conditions are met, returns True.
        If either condition is not met, returns False.

    OUTPUTS: (bool) - Returns True if the input is either a digit or an empty string and its length is less than 3, otherwise returns False.
    """
    def DMCallback(self, D):
        # Type, Existance and Range check
        if (str.isdigit(D) or D == "") and len(D) < 3:
            return True
        else:
            return False

    """
    INPUTS: Y (str) - The text input to be checked.

    PROCESS:
        Checks if the text input `Y` is either a digit or an empty string and its length is less than 5 characters:
            If both conditions are met, returns True.
            If either condition is not met, returns False.

    OUTPUTS: (bool) - Returns True if the input is either a digit or an empty string and its length is less than 5, otherwise returns False.
    """
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
        LblFont1 = CTK.CTkFont(family="Arial Bold", size=38, weight=Font.BOLD)
        BtnFont = CTK.CTkFont(family="Times Bold", size=32, weight=Font.BOLD)
        RdbFont = CTK.CTkFont(family="Helvetica", size=28, weight=Font.NORMAL)
        EtyFont = CTK.CTkFont(family="Helvetica", size=34, weight=Font.NORMAL) 
        EtyFont1 = CTK.CTkFont(family="Helvetica", size=29, weight=Font.NORMAL) 
        # Text
        titles = ["YOUR PANTRY", "RECIPES", "HOME", "ADD AN ITEM", "ITEM COUNT", "ADD NEW", "CANCEL", "SHOWING ASCENDING"]
        filters = ["SORT BY NUTRITION", "SORT BY WEIGHT", "SORT BY COUNT", "SORT BY EXPIRY"]
        # Frame mapping
        self.frA.pack(fill="both", side="top")
        self.frB.pack(fill="both", expand=True, side="top", padx=80, pady=80)
        self.frB.configure(border_color="#cb9c44", border_width=7)
        self.sfrBA.pack(fill="both", expand=True, side="left", padx=7, pady=7)
        self.frBB.pack(fill="both", expand=True, side="right", padx=7, pady=7)
        # Recipe finder button
        self.btnA1 = CTK.CTkButton(self.frA, text=titles[1], font=BtnFont, width=280, command=lambda: self.WindowHandler(5), corner_radius=30, height=80)
        self.btnA1.pack(padx=20, pady=20, anchor="nw", side='left')
        # Title
        self.lblA1 = CTK.CTkLabel(self.frA, text=titles[0], font=TtlFont, justify="center", width=780, text_color="#cc5308")
        self.lblA1.pack(padx=266, pady=10, side="left", anchor="n")
        # Home button
        self.btnA2 = CTK.CTkButton(self.frA, text=titles[2], font=BtnFont, width=280, command=lambda: self.WindowHandler(3), corner_radius=30, height=80)
        self.btnA2.pack(padx=20, pady=20, anchor="ne", side="left")
        # Item View
        self.entries = []
        fields = ["NUTRITION", "ITEM WEIGHT", "ITEM COUNT", "EXPIRY DATE", "ITEM NAME"]
        dateLbl = ["0000", "00", "00"]
        units = ["cal", "g", "x"]
        for i in range(5):
            afr = CTK.CTkFrame(self.frBB, fg_color="#eee9e1", width=680)
            afr.pack(side="top", anchor="n", padx=20, fill="x", pady=4)
            lbl = CTK.CTkLabel(afr, text=fields[i], font=LblFont1, width=200, justify="left")
            lbl.pack(side="left", pady=10, padx=12, anchor="w")
            if i == 3:
                l = []
                for j in range(3):
                    dEty = CTK.CTkEntry(afr, placeholder_text=dateLbl[j], validate="all", validatecommand=(dMVal, "%P"), font=EtyFont, width=len(dateLbl[j])*69, justify="center")
                    if j == 0:
                        dEty.configure(validatecommand=(yearVal, "%P"))
                    dEty.pack(side="right", pady=10, padx=12, anchor="e")
                    l.append(dEty)
                self.entries.append(l)
            elif i == 4:
                ety = CTK.CTkEntry(afr, validate="all", validatecommand=(textVal, "%P"), placeholder_text="SELECT OR ADD", font=EtyFont, width=600, justify="center")
                ety.pack(side="right", pady=10, padx=12, anchor="e")
                self.entries.append(ety)
            else:
                unt = CTK.CTkLabel(afr, font=EtyFont1, anchor="w", text=units[i], width=52, fg_color="#d9d9d9", height=46, corner_radius=6)
                unt.pack(side="right", pady=10, anchor="w", padx=12)
                ety = CTK.CTkEntry(afr, placeholder_text="000000", validate="all", validatecommand=(numVal, "%P"), font=EtyFont, width=536, justify="center")
                ety.pack(side="right", pady=10, anchor="e")
                self.entries.append(ety)
        # Special frame
        afr0 = CTK.CTkFrame(self.frBB, fg_color="transparent")
        afr0.pack(side="top", padx=20, fill="x", expand=True, anchor="n")
        # Add/Update button
        self.btnBB2 = CTK.CTkButton(afr0, text=titles[5], font=BtnFont, width=280, command=self.Add, corner_radius=30, height=80)
        self.btnBB2.pack(pady=12, anchor="n", side="left")
        # Clear button
        self.btnBB3 = CTK.CTkButton(afr0, text=titles[6], font=BtnFont, width=280, command=self.ClearItem, corner_radius=30, height=80)
        self.btnBB3.pack(pady=12, anchor="n", side="right")
        # Image
        #self.lblBB1 = CTK.CTkLabel(self.frBB, text="", image=self.images[10])
        #self.lblBB1.pack(side="top", fill="x", padx=12)
        # Filters
        aFr4 = CTK.CTkFrame(self.frBB, fg_color="transparent")
        aFr4.pack(side="top", anchor="n", fill="x", expand=True)
        self.rdbBB1Var = CTK.StringVar(value=-1)
        cnt = 0
        for x in range(2):
            horiz = ["left", "left"]
            aFr2 = CTK.CTkFrame(aFr4, fg_color="transparent", width=400)
            aFr2.pack(side=horiz[x], pady=10, padx=100)
            for z in range(2):
                snap = ["w", "w"]
                aFr3 = CTK.CTkFrame(aFr2, fg_color="transparent", width=400)
                aFr3.pack(side="top", anchor=snap[x])
                #lblBB1 = CTK.CTkLabel(aFr3, text=filters[cnt], font=RdbFont, width=300, height=40)
                #lblBB1.pack(padx=48, pady=12, side=horiz[x], anchor=snap[x])
                self.rdbBB1 = CTK.CTkRadioButton(aFr3, text=filters[cnt], font=RdbFont, value=cnt, variable=self.rdbBB1Var, command=self.Filter)
                self.rdbBB1.pack(pady=12, side=horiz[x], anchor=snap[x])
                cnt += 1
        # Load Pantry
        self.btnBB4 = CTK.CTkButton(master=self.frBB, text=titles[7], font=BtnFont, width=400, command=self.Descending, corner_radius=30, height=60)
        self.btnBB4.pack(side="top", pady=10)
        self.after(0,self.GridFormatList(self.sfrBA, pantry.PantryList(), self.itemNames))
    
    """
    INPUTS: None

    PROCESS:
        Retrieves the current value of the radio button variable `rdbBB1Var` and increments it by 1 to determine the filter.
        Calls the UnpackWidgets method on the frame `sfrBA` to hide any currently displayed widgets.
        Sorts the pantry array `pantry.arr` using the SortFunc method with the determined filter.
        Configures the button `btnBB4` to display "SHOWING DESCENDING" and binds it to the Ascending method.
        Reverses the sorted array and calls the GridFormatList method to display the reversed array in a grid format within the `sfrBA` frame.

    OUTPUTS: None
    """
    def Descending(self):
        filter = int(self.rdbBB1Var.get()) + 1
        self.UnpackWidgets(self.sfrBA)
        arr = pantry.SortFunc(pantry.arr, filter)
        self.btnBB4.configure(text="SHOWING DESCENDING", command=self.Ascending)
        self.after(0, self.GridFormatList(self.sfrBA, arr[::-1], self.itemNames))
    
    """
    INPUTS: None

    PROCESS:
        Retrieves the current value of the radio button variable `rdbBB1Var` and increments it by 1 to determine the filter.
        Calls the UnpackWidgets method on the frame `sfrBA` to hide any currently displayed widgets.
        Sorts the pantry array `pantry.arr` using the SortFunc method with the determined filter.
        Configures the button `btnBB4` to display "SHOWING ASCENDING" and binds it to the Descending method.
        Reverses the sorted array and calls the GridFormatList method to display the reversed array in a grid format within the `sfrBA` frame.

    OUTPUTS: None
    """
    def Ascending(self):
        filter = int(self.rdbBB1Var.get()) + 1
        self.UnpackWidgets(self.sfrBA)
        arr = pantry.SortFunc(pantry.arr, filter)
        self.btnBB4.configure(text="SHOWING ASCENDING", command=self.Descending)
        self.after(0, self.GridFormatList(self.sfrBA, arr, self.itemNames))

    """
    INPUTS: None

    PROCESS:
        Disables the button `btnBB2` to prevent further actions during the operation.
        Initializes a variable `s` to True, which will be used to track the validity of the input.
        Iterates through each entry widget in `self.entries`:
            - Checks if the entry widget is empty:
                If any widget is empty, sets `s` to False and breaks the loop.
            - For the entry at index 3, which is expected to be a date:
                Validates each date component, ensuring they are non-empty and valid:
                    - If any component is invalid, sets `s` to False and breaks the loop.
                    - Attempts to create a `datetime.date` object with the components:
                        If this raises a ValueError, sets `s` to False and breaks the loop.
                Appends the valid date components to the `item` list.
            - For other entries, checks if they are empty:
                If any are empty, sets `s` to False and breaks the loop.
                Appends the entry values to the `item` list.
        Re-enables the button `btnBB2` and resets its command to None.
        Checks if `pantry.arr` has fewer than 1 item:
            If so, sets `s` to False.
        If all validations pass (`s` is True):
            Updates the button `btnBB2` text to "SUCCESS".
            Calls `cucina.AddToPantry(item)` to add the item to the pantry.
            Resets `self.item` to a default value.
        Otherwise:
            Updates the button `btnBB2` text to "FAILED".
            If `self.item` is not equal to the default value, calls `pantry.AddRaw(self.item)` to handle the failed addition.
        After a delay of 320 milliseconds, calls `self.ClearItem` to clear the item fields.

    OUTPUTS: None
    """
    def Add(self):
        s = True
        self.btnBB2.configure(state="disabled")
        item = []
        for entry in range(len(self.entries)):
            for e in self.entries:
                try:
                    if e.get() == "":
                        s = False 
                        break
                except AttributeError:
                    for l in e:
                        if l.get() == "":
                            s = False
                        break
            if entry == 3:
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
        if s != False and item != ["0","0","0","0","0"] or item != []:
            if pantry.Search(item[-1])[-1] == item[-1]: s = False
        if s:
            self.btnBB2.configure(text="SUCCESS")
            cucina.AddToPantry(item)
            self.item = ["0","0","0","0","0"]
        else:
            self.btnBB2.configure(text="FAILED")
            if self.item != ["0","0","0","0","0"] and pantry.Search(self.item[-1]) == ["0","0","0","0","0"]: 
                pantry.AddRaw(self.item)
        self.after(320, self.ClearItem)

    def Update(self):
        if self.entries[2].get() != "":
            if int(self.entries[2].get()) == 0:
                self.btnBB2.configure(state="disabled")
                pantry.Remove(self.item[-1])
                self.after(420, lambda: self.btnBB2.configure(state="normal", command=None))
                self.after(420, self.ClearItem)
            else:
                pantry.Remove(self.item[-1])
                self.Add()                
        else:
            self.btnBB2.configure(text="FAILED")
            self.after(520, self.ClearItem)

    """
    INPUTS: None

    PROCESS:
        Checks if the entry at index 2 in `self.entries` is not empty:
            If it is not empty and its value is 0:
                - Disables the button `btnBB2` to prevent further actions.
                - Calls `pantry.Remove(self.item[5])` to remove the item from the pantry.
                - Re-enables the button `btnBB2` and resets its command to None.
                - After a delay of 320 milliseconds, calls `self.ClearItem` to clear the item fields.
            If the value is not 0:
                - Removes the item from the pantry.
                - Calls the `Add` method to update the item.
        If the entry at index 2 is empty:
            - Updates the button `btnBB2` text to "FAILED".
            - After a delay of 320 milliseconds, calls `self.ClearItem` to clear the item fields.

    OUTPUTS: None
    """

    """
    INPUTS: None

    PROCESS:
        Calls the `UnpackWidgets` method on the frame `sfrBA` to hide any currently displayed widgets.
        Updates the display in the `sfrBA` frame by calling `GridFormatList` with the pantry list and item names.
        Resets the value of the radio button variable `rdbBB1Var` to -1.
        Calls the `Ascending` method to refresh the display with ascending sorted items.
        Clears all entry fields in `self.entries`:
            For the entry at index 3 (expected to be a date), clears each sub-entry.
            For other entries, clears the text.
        Updates the button `btnBB2` text to "ADD NEW" and binds it to the `Add` method.

    OUTPUTS: None
    """
    def ClearItem(self):
        self.UnpackWidgets(self.sfrBA)
        self.GridFormatList(self.sfrBA, pantry.PantryList(), self.itemNames)
        self.rdbBB1Var.set(-1)
        self.Ascending()
        for entry in range(len(self.entries)):
            if entry == 3:
                for i in range(len(self.entries[entry])):
                    self.entries[entry][i].delete(0,"end")
            else:
                self.entries[entry].delete(0,"end")
        self.btnBB2.configure(text="ADD NEW", command=self.Add)

    """
    INPUTS:
        window (CTK.CTkFrame) - The frame where the formatted list will be displayed.
        arr (list) - A list of items to be formatted and displayed.
        fields (list) - A list of field labels to be used in formatting the display.

    PROCESS:
        Creates a font object `BtnFont1` for button text.
        Checks if the input list `arr` is not empty:
            If not empty:
                Iterates over the items in `arr` and formats each item:
                    Constructs a title string for each item based on its fields.
                    Formats date fields and calculates days past expiry.
                    Creates a frame (`bracket`) for each item.
                    Adds a button (`cell1`) with the item title and binds it to the `Select` method.
                    Adds a label (`cell0`) with the formatted title string.
                    Packs these elements into the frame.
            If empty:
                Creates a default message indicating that the pantry is empty:
                    Constructs a frame (`bracket`) with default text.
                    Adds a button (`cell1`) and a label (`cell0`) with the default message.

    OUTPUTS: None
    """
    def GridFormatList(self, window, arr, fields):
        BtnFont1 = CTK.CTkFont(family="Helvetica", size=15, weight=Font.NORMAL)
        arrayLength = len(arr)
        if arrayLength > 0:
            for ind in range(arrayLength):
                btnTitle = ""
                title = ""
                for field in range(len(fields)):
                    if field == 3:
                        d, ds = pantry.DateRevert(arr[ind])
                        if ds > 0:
                            title += str(ds) + fields[field]
                        else:
                            days = str(abs(ds))
                            title += f"{days} Days past expiry"
                    elif field == 4:
                        btnTitle = str(arr[ind][field+1])
                    else:
                        title += str(arr[ind][field+1]) + fields[field] +  ",  "
                bracket = CTK.CTkFrame(master=window, fg_color="#d9d9d9", width=680, corner_radius=6)
                bracket.pack(side="top", pady=12, padx=1, anchor="w")
                cell1 = CTK.CTkButton(master=bracket, text=btnTitle, font=BtnFont1, width=260, corner_radius=6, fg_color="#cd9b45", text_color="black", command=lambda x = arr[ind]: self.Select(x))
                cell1.pack(anchor="w", side="left", pady=4, padx=4)
                cell0 = CTK.CTkLabel(master=bracket, text=title, font=BtnFont1, width=400, corner_radius=6, fg_color="#eee9e1", text_color="black", anchor="w")
                cell0.pack(anchor="w", side="left", padx=4, pady=6)
        else:
            btnTitle = "Pantry is Empty"
            title = "Enter some items into your pantry to get started"
            bracket = CTK.CTkFrame(master=window, fg_color="#d9d9d9", width=680, corner_radius=6)
            bracket.pack(side="top", pady=12, padx=1, anchor="w")
            cell1 = CTK.CTkButton(master=bracket, text=btnTitle, font=BtnFont1, width=260, corner_radius=6, fg_color="#cd9b45", text_color="black")
            cell1.pack(anchor="w", side="left", pady=4, padx=4)
            cell0 = CTK.CTkLabel(master=bracket, text=title, font=BtnFont1, width=400, corner_radius=6, fg_color="#eee9e1", text_color="black", anchor="w")
            cell0.pack(anchor="w", side="left", padx=4, pady=6)
            
    """
    INPUTS:
        win (CTK.CTkFrame) - The frame where the grid cell will be placed.
        entry (str) - The text to be displayed in the grid cell.
        row (int) - The row position in the grid layout where the cell will be placed.
        column (int) - The column position in the grid layout where the cell will be placed.
        font (CTK.CTkFont) - The font to be used for the text in the cell.

    PROCESS:
        Creates a grid cell as an instance of `CTK.CTkEntry` with the specified font, width, and corner radius.
        Places the cell in the specified row and column of the grid layout with padding and sticky alignment.
        Inserts the provided text `entry` into the cell.
        Configures the cell to be in a disabled state to prevent user modification.

    OUTPUTS: None
    """
    def GridCell(self, win, entry, row, column, font):
        cell = CTK.CTkEntry(win, font=font, width=156, corner_radius=2)
        cell.grid(row=row, column=column, padx=1, pady=2, sticky="N")
        cell.insert("end", entry)
        cell.configure(state="disable")
    
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
            self.btnA0 = CTK.CTkButton(self.frA, text="ACCOUNT", font=BtnFont, corner_radius=30, height=80, command=lambda: self.WindowHandler(0))
        except KeyError:
            titles = ["Admin Access", "DISCOVER RECIPES", "SEARCH YOUR PANTRY", "LOGOUT"]
            self.btnA0 = CTK.CTkButton(self.frA, text=" ADMIN ", font=BtnFont, corner_radius=30, height=80, command=lambda: self.WindowHandler(0))
        # Frames
        self.frA.pack(fill="both", expand=True, side="top")
        self.frB.pack(fill="both", expand=True, side="left")
        self.frC.pack(fill="both", expand=True, side="right")
        # IMAGES
        self.btnB1 = CTK.CTkButton(self.frB, image=self.images[8], text=None, fg_color="transparent", hover=False, width=650, command=lambda: self.WindowHandler(5))
        self.btnB1.pack(padx=12, pady=10, side="top", fill="y")
        self.btnC2 = CTK.CTkButton(self.frC, image=self.images[9], text=None, fg_color="transparent", hover=False, width=650, command=lambda: self.WindowHandler(4))
        self.btnC2.pack(padx=12, pady=10, side="top", fill="y")
        # Alignment button
        self.btnA0.pack(padx=20, pady=20, side="left", anchor="ne")
        # Title
        self.lblA1 = CTK.CTkLabel(self.frA, text=titles[0], font=TtlFont, justify="center", text_color="#cc5308")
        self.lblA1.pack(padx=12, pady=20, side="left", anchor="n", fill="x", expand=True)
        # Log Out button
        self.btnA1 = CTK.CTkButton(self.frA, text=titles[3], font=BtnFont, command=lambda: self.WindowHandler(1), corner_radius=30, height=80)
        self.btnA1.pack(padx=20, pady=20, side="right", anchor="ne")
        # Navigation buttons
        self.btnB2 = CTK.CTkButton(self.frB, text=titles[1], font=BtnFont, corner_radius=30, height=80, command=lambda: self.WindowHandler(5))
        self.btnB2.pack(padx=12, pady=80)
        self.btnC2 = CTK.CTkButton(self.frC, text=titles[2], font=BtnFont, corner_radius=30, height=80, command=lambda: self.WindowHandler(4))
        self.btnC2.pack(padx=12, pady=80)

    def RecipePage(self):
        # Fonts
        TtlFont = CTK.CTkFont(family="Arial Black", size=80, weight=Font.BOLD)
        LblFont = CTK.CTkFont(family="Arial Bold", size=54, weight=Font.BOLD)
        BtnFont = CTK.CTkFont(family="Times Bold", size=32, weight=Font.BOLD)
        EtyFont = CTK.CTkFont(family="Helvetica", size=39, weight=Font.NORMAL) 
        # Text
        titles = ["RECIPE FINDER", "RECIPE PREVIEW", "ENLARGE", "CLEAR", "HOME"]
        # Frames
        self.frA.pack(fill="both", expand=True, side="top")
        frAA = CTK.CTkFrame(self.frA, fg_color= "transparent")
        frAA.pack(side="left", fill="both", expand=True)
        frAB = CTK.CTkFrame(self.frA, fg_color= "transparent")
        frAB.pack(side="right", fill="both", expand=True)
        # Navigation buttons
        frABA = CTK.CTkFrame(frAB, fg_color= "transparent")
        frABA.pack(side="top", fill="x", anchor="n")
        self.btnAA2 = CTK.CTkButton(frABA, text=titles[3], font=BtnFont, command=self.ClearRecipe, corner_radius=30, height=80, width=180)
        self.btnAA2.pack(padx=24, pady=24, side="right", anchor="ne")
        self.btnAA3 = CTK.CTkButton(frAA, text=titles[4], font=BtnFont, corner_radius=30, height=80, width=180, command=lambda: self.WindowHandler(3))
        self.btnAA3.pack(padx=24, pady=24, side="top", anchor="nw")
        # Titles
        self.lblAA1 = CTK.CTkLabel(frAA, text=titles[0], font=TtlFont, justify="center", text_color="#cc5308")
        self.lblAA1.pack(padx=12, side="top", anchor="n")
        self.lblAB1 = CTK.CTkLabel(frAB, text=titles[1], font=TtlFont, justify="center", text_color="#cc5308")
        self.lblAB1.pack(padx=12, side="top", anchor="n")
        # Scrollable frames
        sfrAAA = CTK.CTkScrollableFrame(frAA, fg_color="#eee9e1", height=720, width=680)
        sfrAAA.pack(side="top", anchor="n", pady=10, padx=6)
        self.frABA = CTK.CTkFrame(frAB, fg_color="#eee9e1", height=720, width=820)
        self.frABA.pack(side="top", pady=10, padx=6)
        # PDF display
        self.pdfFr = CTkPDFViewer(self.frABA, file=f"../Cucina/CTkPDFViewer/0.pdf", height=620, page_height=1122, page_width=794, width=800, fg_color="transparent")
        self.pdfFr.pack(pady=10, padx=10)
        self.ListRecipes(sfrAAA, PDF.ListPDFs())
        self.btnAA1 = CTK.CTkButton(self.frABA, text=titles[2], font=BtnFont, corner_radius=30, height=60, width=720)
        self.btnAA1.pack(padx=4, pady=4, side="top", anchor="n")

    """
    INPUTS:
        window (CTK.CTkFrame) - The frame where the recipe buttons will be displayed.
        arr (list) - A list of recipe filenames (assumed to be in PDF format).

    PROCESS:
        Creates a font object `BtnFont1` for button text with specified family, size, and weight.
        Iterates through the list of recipe filenames `arr`:
            - For each filename, removes the ".pdf" suffix and replaces underscores with spaces to create a readable title.
            - Creates a button (`cell`) for each recipe with the formatted title and binds it to the `LoadPDF` method.
            - Configures the button with specified dimensions, font, color, and text.
            - Packs the button into the `window` frame with padding and alignment.

    OUTPUTS: None
    """
    def ListRecipes(self, window, arr):
        BtnFont1 = CTK.CTkFont(family="Helvetica", size=32, weight=Font.NORMAL)
        for i in arr:
            title = i.removesuffix(".pdf").replace("_"," ")
            cell = CTK.CTkButton(master=window, text=title, font=BtnFont1, width=680, height=80, corner_radius=8, fg_color="#cf9a41", text_color="#f9f2eb", command=lambda x = i: self.LoadPDF(x))
            cell.pack(padx=1, pady=16, anchor="w")
    
    """
    INPUTS: None

    PROCESS:
        Checks if `self.pdfFr` (a PDF viewer widget) is currently mapped (visible) in the UI:
            If it is visible:
                - Hides the `self.pdfFr` widget by calling `pack_forget`.
                - Reinitializes `self.pdfFr` as a `CTkPDFViewer` with a default PDF file and specified dimensions.
                - Packs the newly initialized `self.pdfFr` into its parent frame `self.frABA` with padding.
                - Checks if the button `self.btnAA1` is currently mapped:
                    If it is visible:
                        - Hides the button by calling `pack_forget`.
                        - Repacks the button with new padding and alignment settings.

    OUTPUTS: None
    """
    def ClearRecipe(self):
        if self.pdfFr.winfo_ismapped():
            self.pdfFr.pack_forget()
            self.pdfFr = CTkPDFViewer(self.frABA, file=f"../Cucina/CTkPDFViewer/0.pdf", height=620, page_height=1122, page_width=794, width=800, fg_color="transparent")
            self.pdfFr.pack(pady=10, padx=10)
            if self.btnAA1.winfo_ismapped():
                self.btnAA1.pack_forget()
                self.btnAA1.pack(padx=4, pady=4, side="top", anchor="n")

    """
    INPUTS:
        item (str) - The filename of the PDF to be loaded and displayed.

    PROCESS:
        Checks if `self.pdfFr` (a PDF viewer widget) is currently mapped (visible) in the UI:
            If it is visible:
                - Hides the `self.pdfFr` widget by calling `pack_forget`.
        Updates the `self.btnAA1` button's command to call `FocusPDF` with the `item` as a parameter when clicked.
        Initializes `self.pdfFr` as a `CTkPDFViewer` with the specified PDF file path, dimensions, and color settings.
        Packs the newly initialized `self.pdfFr` into its parent frame `self.frABA` with padding.
        Updates `self.loadedPdf` to the current `item` (the loaded PDF).
        Checks if `self.btnAA1` is currently mapped:
            If it is visible:
                - Hides the button by calling `pack_forget`.
                - Repacks the button with new padding and alignment settings.

    OUTPUTS: None
    """
    def LoadPDF(self, item):
        if self.pdfFr.winfo_ismapped():
            self.pdfFr.pack_forget()
        self.btnAA1.configure(command=lambda x = item: self.FocusPDF(x))
        self.pdfFr = CTkPDFViewer(self.frABA, file=f"../Cucina/PDFs/{item}", height=620, page_height=1122, page_width=794, width=800, fg_color="transparent")
        self.pdfFr.pack(pady=10, padx=10)
        self.loadedPdf = item
        if self.btnAA1.winfo_ismapped():
            self.btnAA1.pack_forget()
            self.btnAA1.pack(padx=4, pady=4, side="top", anchor="n")

    # A unique page that parses a value
    """
    INPUT: item (str) - Name of the pdf that is currently loaded
    PROCESS: Displays the pdf the user selected.
    """
    def FocusPDF(self, item):
        self.UnmapFrames()
        TtlFont = CTK.CTkFont(family="Arial Black", size=62, weight=Font.BOLD)
        BtnFont = CTK.CTkFont(family="Times Bold", size=28, weight=Font.BOLD)
        self.frA.pack(fill="both", expand=True, side="left")
        self.frB.pack(fill="both", expand=True, side="right")
        title = ["RECIPE FOCUS", "BACK", "PANTRY MATCH", "REFRESH"]
        self.btnA1 = CTK.CTkButton(self.frA, text=title[1], width=200, font=BtnFont, height=60, corner_radius=12, command=lambda: self.WindowHandler(5))
        self.btnA1.pack(side="top", pady=12, padx=12, anchor="nw")
        self.btnB2 = CTK.CTkButton(self.frB, text=title[3], width=200, font=BtnFont, height=60, corner_radius=12)
        self.btnB2.pack(side="top", pady=12, padx=12, anchor="ne")
        self.lblA1 = CTK.CTkLabel(self.frA, text=title[0], width=1280, font=TtlFont)
        self.lblA1.pack(side="top", pady=10, padx=10)
        self.pdfFr = CTkPDFViewer(self.frA, file=f"../Cucina/PDFs/{item}", height=820, page_height=1683, page_width=1191, width=1220, fg_color="#eee9e1")
        self.pdfFr.pack(side="top", padx=6)
        self.lblB1 = CTK.CTkLabel(self.frB, text=title[2], width=640, font=TtlFont)
        self.lblB1.pack(side="top", pady=10, padx=6)
        self.sfrBA = CTK.CTkScrollableFrame(self.frB, fg_color="#eee9e1", width=640, height=820)
        self.sfrBA.pack(side="top", padx=6)
        self.ListMatches(self.sfrBA, item)

    """
    INPUTS:
        window (CTK.CTkFrame) - The frame where the match and opposite items will be displayed.
        item (str) - The filename of the PDF, which will be used to search for recipe ingredients.

    PROCESS:
        Creates font objects `BtnFont1` and `TtlFont` for button and label text, respectively.
        Extracts the recipe name from the filename by removing the ".pdf" suffix and replacing underscores with spaces.
        Uses the `cucina.DishSearch` method to find ingredients that match (in pantry) and those that are missing (opposite).
        Constructs and displays a title label (`ttl`) for the matched ingredients with formatted text.
        If no matching ingredients are found:
            - Displays a label indicating that no items in the pantry match.
        If there are matching ingredients:
            - Creates and displays a button for each matched ingredient.
        Constructs and displays another title label (`ttl`) for ingredients that need to be acquired.
        If no missing ingredients are found:
            - Displays a label indicating that everything needed is already in the pantry.
        If there are missing ingredients:
            - Creates and displays a button for each ingredient that needs to be acquired.

    OUTPUTS: None
    """
    def ListMatches(self, window, item):
        BtnFont1 = CTK.CTkFont(family="Helvetica", size=22, weight=Font.NORMAL)
        TtlFont = CTK.CTkFont(family="Helvetica", size=30, weight=Font.BOLD)
        recipe = item.removesuffix(".pdf")
        opposite, match = cucina.DishSearch(recipe)
        recipe = recipe.replace("_"," ")
        title = f"Ingredients you may have for your\n{recipe}:"
        ttl = CTK.CTkLabel(master=window, text=title, font=TtlFont, width=675, corner_radius=2, fg_color="#747474", text_color="#eee9e1")
        ttl.pack(padx=1, pady=3, anchor="n")
        if len(match) < 1:
            cell = CTK.CTkLabel(master=window, text="No Items in your pantry match", font=BtnFont1, width=675, corner_radius=2, fg_color="#747474", text_color="black")
            cell.pack(padx=1, pady=3, anchor="w")
        for i in match:
            title = i
            cell = CTK.CTkButton(master=window, text=title, font=BtnFont1, width=675, corner_radius=2, fg_color="#cf9a41", text_color="black")
            cell.pack(padx=1, pady=3, anchor="w")
        title = f"Ingredients you may need to get:"
        ttl = CTK.CTkLabel(master=window, text=title, font=TtlFont, width=675, corner_radius=2, fg_color="#747474", text_color="#eee9e1")
        ttl.pack(padx=1, pady=3, anchor="n")
        if len(opposite) < 1:
            cell = CTK.CTkLabel(master=window, text="Looks like you have everything you need :)", font=BtnFont1, width=675, corner_radius=2, fg_color="#747474", text_color="black")
            cell.pack(padx=1, pady=3, anchor="w")
        for i in opposite:
            title = i
            cell = CTK.CTkButton(master=window, text=title, font=BtnFont1, width=675, corner_radius=2, fg_color="#cf9a41", text_color="black")
            cell.pack(padx=1, pady=3, anchor="w")
    
    def RegistrationWindow(self):
        # Entry validation
        textVal = (self.register(self.TextCallback))
        # Fonts
        TtlFont = CTK.CTkFont(family="Arial Black", size=68, weight=Font.BOLD)
        LblFont = CTK.CTkFont(family="Arial Bold", size=42, weight=Font.BOLD)
        LblFont1 = CTK.CTkFont(family="Arial Bold", size=14, weight=Font.NORMAL)
        BtnFont = CTK.CTkFont(family="Times Bold", size=32, weight=Font.BOLD)
        EtyFont = CTK.CTkFont(family="Helvetica", size=34, weight=Font.NORMAL) 
        titles = [ "ACCOUNT REGISTRATION","ENTER YOUR OWN NAME BELOW" ,"NAME", "ENTER A UNIQUE USERNAME BELOW", "USERNAME", "ENTER A SECURE PASSWORD BELOW", "PASSWORD", "          REGISTER          ", "CONFIRM YOUR PASSWORD", "PASSWORD"]
        prompts = ["• Do not enter numbers", "• Must be longer than 3 letters", "• Must contain atleast one non-alaphabetical character\n• Must be longer than 3 letters", "• Re-enter the same password to confirm."]
        # Frames
        self.frA.pack(fill="both", expand=True, side="left")
        self.frB.pack(fill="both", expand=True, side="left")
        self.frC.pack(fill="both", expand=True, side="right")
        # IMAGES
        self.btnA1 = CTK.CTkButton(self.frA, image=self.images[2], text=None, fg_color="transparent", hover_color="grey90", command=lambda: self.WindowHandler(1))
        self.btnA1.pack(padx=12, pady=32, side="top", anchor="nw")
        self.btnA2 = CTK.CTkButton(self.frA, image=self.images[6], text=None, fg_color="transparent", hover=False, width=420)
        self.btnA2.pack(padx=20, pady=144)
        self.btnC3 = CTK.CTkButton(self.frC, text="SECURITY INFORMATION\n\nTERMS OF SERVICE", fg_color="transparent", hover_color="grey90", text_color="grey4",anchor="e")
        self.btnC3.pack(padx=30, pady=32, side="top", anchor="ne")
        self.btnC4 = CTK.CTkButton(self.frC, image=self.images[7], text=None, fg_color="transparent", hover=False, width=420)
        self.btnC4.pack(padx=20, pady=166)
        # Title
        self.lblB1 = CTK.CTkLabel(self.frB, text=titles[0], font=TtlFont, justify="center", width=780, text_color="#cc5308")
        self.lblB1.pack(padx=12, pady=40)
        # Name Entry Field
        self.lblB2 = CTK.CTkLabel(self.frB, text=titles[1], font=LblFont, justify="center", width=780)
        self.lblB2.pack(padx=12, pady=12)
        self.etyB1 = CTK.CTkEntry(self.frB, validate="all", validatecommand=(textVal, "%P"), placeholder_text=titles[2], font=EtyFont, width=620, justify="center", height=68, corner_radius=240)
        self.etyB1.pack(padx=12, pady=2)
        # Username Entry Field
        self.lblB3 = CTK.CTkLabel(self.frB, text=titles[3], font=LblFont, justify="center", width=780)
        self.lblB3.pack(padx=12, pady=12)
        self.etyB2 = CTK.CTkEntry(self.frB, validate="all", validatecommand=(textVal, "%P"), placeholder_text=titles[4], font=EtyFont, width=620, justify="center", height=68, corner_radius=240)
        self.etyB2.pack(padx=12, pady=2)
        self.lblB6 = CTK.CTkLabel(self.frB, text=prompts[1], font=LblFont1, justify="center", width=780)
        self.lblB6.pack(padx=12, pady=2)
        # Password Entry Field
        self.lblB4 = CTK.CTkLabel(self.frB, text=titles[5], font=LblFont, justify="center", width=780)
        self.lblB4.pack(padx=12, pady=12)
        self.etyB3 = CTK.CTkEntry(self.frB, placeholder_text=titles[6], font=EtyFont, show="*", width=620, justify="center", height=68, corner_radius=240)
        self.etyB3.pack(padx=12, pady=2)
        self.lblB7 = CTK.CTkLabel(self.frB, text=prompts[2], font=LblFont1, justify="center", width=780)
        self.lblB7.pack(padx=12, pady=2)
        # Confirm Password Entry Field
        self.lblB5 = CTK.CTkLabel(self.frB, text=titles[8], font=LblFont, justify="center", width=780)
        self.lblB5.pack(padx=12, pady=12)
        self.etyB4 = CTK.CTkEntry(self.frB, placeholder_text=titles[9], font=EtyFont, show="*", width=620, justify="center", height=68, corner_radius=240)
        self.etyB4.pack(padx=12, pady=2)
        self.lblB8 = CTK.CTkLabel(self.frB, text=prompts[3], font=LblFont1, justify="center", width=780)
        self.lblB8.pack(padx=12, pady=2)
        # Register button
        self.btnB1 = CTK.CTkButton(self.frB, text=titles[7], font=BtnFont, command=lambda: self.Register(), corner_radius=30, height=80)
        self.btnB1.pack(padx=12, pady=60)

    """
    INPUTS:
        event (optional) - An optional event parameter, typically used for event-driven calls (e.g., button clicks). Default is None.

    PROCESS:
        Disables the `btnB1` button immediately upon entering the function.
        Retrieves the values from the entry fields `etyB1`, `etyB2`, and `etyB3` for the name, username, and password, respectively.
        Checks if any of the retrieved values are empty:
            If any field is empty, no action is taken.
            If all fields have values:
                - Calls `cucina.RegisterAccount` with the username, password, and name.
                - If the registration is successful:
                    - Clears the entry fields.
                    - Updates `btnB1` to display a success message and disables the button.
                    - Schedules a call to `WindowHandler` to switch to the login window after a short delay.
                - If the registration fails due to username issues:
                    - Highlights the username entry field in red and updates `btnB1` to display an error message.
                    - Resets the username field color and reverts the button state after delays.
                - If the registration fails due to password issues:
                    - Highlights the password entry field in red and updates `btnB1` to display an error message.
                    - Resets the password field color and reverts the button state after delays.

    OUTPUTS: None
    """      
    def Register(self, event=None):
        self.after(0, lambda: self.btnB1.configure(state="disabled"))
        name = self.etyB1.get()
        usrm = self.etyB2.get()
        pwrd = self.etyB3.get()
        cpwrd = self.etyB4.get()
       
        if name == "" or usrm == "" or pwrd == "":
            self.btnB1.configure(True, state="disabled")
        else:
            if cpwrd == pwrd:
                result = cucina.RegisterAccount(usrm, pwrd, name)
                if result == "Success":
                    self.etyB1.delete(0, CTK.END)
                    self.etyB3.delete(0, CTK.END)
                    self.etyB2.delete(0, CTK.END)
                    self.etyB4.delete(0, CTK.END)
                    self.btnB1.configure(True, text=result.upper(), state="disabled", text_color_disabled="black")
                    self.after(700, lambda: self.WindowHandler(1))
                    return None
                elif "username" in result.lower():
                    self.etyB2.configure(text_color="red")
                    self.btnB1.configure(True, text=result.upper(), state="disabled", text_color_disabled="black")
                    self.after(1000, lambda: self.etyB2.configure(text_color="#0d0c0a"))
                    self.after(1000, lambda: self.btnB1.configure(True, text="REGISTER", state="normal", text_color="#fbf4ed"))
                elif "password" in result.lower():
                    self.etyB3.configure(text_color="red")
                    self.btnB1.configure(True, text=result.upper(), state="disabled", text_color_disabled="black")
                    self.after(1000, lambda: self.etyB3.configure(text_color="#0d0c0a"))
                    self.after(1000, lambda: self.btnB1.configure(True, text="REGISTER", state="normal", text_color="#fbf4ed"))
            else:
                self.btnB1.configure(True, text="Passwords Mismatch", state="disabled", text_color_disabled="black")
                self.after(1000, lambda: self.btnB1.configure(True, text="REGISTER", state="normal", text_color="#fbf4ed"))
        self.after(200, lambda: self.btnB1.configure(state="normal"))
    """
    INPUTS:
        event (optional) - An optional event parameter, typically used for event-driven calls (e.g., button clicks). Default is None.

    PROCESS:
        Retrieves the values from the entry fields `etyB1` (username) and `etyB2` (password).
        Checks if either the username or password fields are empty:
            If either field is empty, no action is taken.
            If both fields have values:
                - Calls `cucina.LogIn` with the username and password.
                - If the login is successful and returns "Logged in as Admin" or "Login successful":
                    - Clears the entry fields.
                    - Updates `btnB1` to display a success message and disables the button.
                    - Sets the `account` attribute to the result of `cucina.Search` with the username.
                    - Calls `WindowHandler` to switch to the home page (denoted by `3`).
                - If the login fails due to incorrect password:
                    - Highlights the password entry field in red and updates `btnB1` to display an error message.
                    - Resets the button and password field colors after delays.
                - If the login fails due to incorrect username:
                    - Highlights the username entry field in red and updates `btnB1` to display an error message.
                    - Resets the button and username field colors after delays.
                - For any other errors:
                    - Updates `btnB1` to display the error message and disables the button.
                    - Resets the button state after a delay.

    OUTPUTS: None
    """
    def LoginInfo(self, enable):
        if self.saveLogin != "" and enable:
            dataBase.SaveLoginInfo(self.saveLogin)
        elif not enable:
            dataBase.ClearLoginInfo()

    def Login(self, event=None):
        usrm = self.etyB1.get()
        pwrd = self.etyB2.get()
        self.after(0, lambda: self.btnB1.configure(state="disabled"))
        if usrm == "" or pwrd == "":
            pass
        else:
            result = cucina.LogIn(usrm, pwrd)
            if result == "Logged in as Admin" or result == "Login successful":
                self.etyB1.delete(0, CTK.END)
                self.etyB2.delete(0, CTK.END)
                self.btnB1.configure(True, text=result.upper(), state="disabled", text_color_disabled="black")
                self.account = cucina.Search(usrm)
                self.saveLogin = usrm
                self.LoginInfo(self.enbSaveLogin)
                self.WindowHandler(3)
            elif "password" in result.lower():
                self.etyB2.configure(text_color="red")
                self.btnB1.configure(True, text=result.upper(), state="disabled", text_color_disabled="black")
                self.after(1000, lambda: self.btnB1.configure(True, text="          LOG IN          ", state="normal", text_color="#fbf4ed"))
                self.after(2000, lambda: self.etyB2.configure(text_color="#0d0c0a"))
                self.after(2000, lambda: self.etyB1.configure(text_color="#0d0c0a"))
            elif "username" in result.lower():
                self.etyB1.configure(text_color="red")
                self.btnB1.configure(True, text=result.upper(), state="disabled", text_color_disabled="black")
                self.after(1000, lambda: self.btnB1.configure(True, text="          LOG IN          ", state="normal", text_color="#fbf4ed"))
                self.after(2000, lambda: self.etyB1.configure(text_color="#0d0c0a"))
                self.after(2000, lambda: self.etyB2.configure(text_color="#0d0c0a"))
            else:
                self.btnB1.configure(True, text=result.upper(), state="disabled", text_color_disabled="black")
                self.after(1000, lambda: self.btnB1.configure(True, text="          LOG IN          ", state="normal", text_color="#fbf4ed"))
        self.after(200, lambda: self.btnB1.configure(state="normal"))
if __name__ == "__main__":
    CTK.set_appearance_mode("light")
    CTK.set_default_color_theme("bisque-theme.json")
    scaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
    app = App()
    w = app.winfo_screenwidth()
    factor = w/1920 * scaleFactor
    CTK.deactivate_automatic_dpi_awareness()
    CTK.set_widget_scaling(factor)
    CTK.set_window_scaling(factor)
    app.after(0, lambda: app.state("zoomed"))
    app.WindowHandler(-1)
    app.mainloop()