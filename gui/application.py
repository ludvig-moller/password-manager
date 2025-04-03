import customtkinter as ctk

from gui.login_password_manager import LoginPasswordManager
from gui.password_manager import PasswordManager

from storage import *

class Application(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Password Manager")
        self.minsize(width=800, height=500)

        self.iconbitmap("icon.ico")

        self.login_password_manager = LoginPasswordManager(self)

        self.login_password_manager.pack(side="top", fill="both", expand=True)

        self.mainloop()

    def createPasswordManager(self, name, password):
        create_password_manager(name, password)
        self.openPasswordManager(name, password)
    
    def openPasswordManager(self, name, password):
        key = get_password_manager_key(name, password)

        if key == False:
            return False
        
        self.login_password_manager.destroy()   
        self.password_manager = PasswordManager(self, name, key)
        self.password_manager.pack(side="top", fill="both", expand=True)

    def loginPasswordManager(self):
        self.password_manager.destroy()
        self.login_password_manager = LoginPasswordManager(self)
        self.login_password_manager.pack(side="top", fill="both", expand=True)
