import customtkinter as CTK
import tkinter as TK

CTK.set_appearance_mode("System")
CTK.set_default_color_theme("green")

aWidth, aHeight = "1920", "1080"
class App(CTK.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("CUCINA")
        self.geometry(f"{aWidth}x{aHeight}")
        
        self.topFrame = CTK.CTkFrame(self, bg_color= "transparent")
        self.topFrame.pack(fill="x", anchor="n", expand=True)
        # Username Label
        self.nameLbl = CTK.CTkLabel(self.topFrame, text="USERNAME", font=('Helvetica', 38))
        self.nameLbl.pack(side="top", expand=True)
 
        # Username Entry Field
        self.nameEntry = CTK.CTkEntry(self.topFrame, placeholder_text="ENTER YOUR USERNAME", font=('Helvetica', 28))
        self.nameEntry.pack(side="top", expand=True)
    
if __name__ == "__main__":
    app = App()
    app.mainloop() 