import customtkinter as CTK
import tkinter as TK
from CUCINA import app as cucina

CTK.set_appearance_mode("System")
CTK.set_default_color_theme("green")

aWidth, aHeight = "1920", "1080"
class App(CTK.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("CUCINA")
        self.geometry(f"{aWidth}x{aHeight}")
    
    def LoginWindow(self):
        # Top Frame
        self.frA = CTK.CTkFrame(self, bg_color= "transparent")
        self.frA.pack(fill="both", padx=20, pady=60, expand=True)
        # Username Label
        self.lblA1 = CTK.CTkLabel(self.frA, text="USERNAME", font=('Helvetica', 38))
        self.lblA1.pack(padx=12, pady=10)
 
        # Username Entry Field
        self.etyA1 = CTK.CTkEntry(self.frA, placeholder_text="USERNAME", font=('Helvetica', 28))
        self.etyA1.pack(padx=12, pady=10)
        # Password Entry Field
        self.etyA2 = CTK.CTkEntry(self.frA, placeholder_text="PASSWORD", font=('Helvetica', 28))
        self.etyA2.pack(padx=12, pady=10)
        # Log In button
        self.btnA1 = CTK.CTkButton(self.frA, text="Login", command=lambda: self.Login())
        self.btnA1.pack(padx=12, pady=12)

    def Login(self):
        usrm = self.etyA1.get()
        pwrd = self.etyA2.get()
        if usrm == "" or pwrd == "":
            pass
        else:
            result = cucina.LogIn(usrm, pwrd)
            self.btnA1.configure(True, text=result)
    
if __name__ == "__main__":
    app = App()
    app.LoginWindow()
    app.mainloop() 