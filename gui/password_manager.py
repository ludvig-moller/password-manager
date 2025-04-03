import customtkinter as ctk
import secrets

from storage import *

class PasswordManager(ctk.CTkFrame):
    def __init__(self, parent, name, key):
        super().__init__(parent)
        self.parent = parent
        self.name = name
        self.key = key

        self.navbar = Navbar(self, self.name)
        self.current_screen = PasswordList(self, self.name, self.key)
        
        self.navbar.pack(side="top", fill="x", ipady=5, pady=5, padx=5)
        self.current_screen.pack(side="top", fill="both", expand=True, padx=5, pady=5)
    
    def switchScreen(self, screen):
        if type(screen) == type(self.current_screen):
            self.current_screen.pack_forget()
            del self.current_screen
            self.current_screen = PasswordList(self, self.name, self.key)
        else:
            self.current_screen.pack_forget()
            del self.current_screen
            self.current_screen = screen
        self.current_screen.pack(side="top", fill="both", expand=True, padx=5, pady=5)

class Navbar(ctk.CTkFrame):
    def __init__(self, parent, name):
        super().__init__(parent)
        self.parent = parent
        self.name = name

        # Widgets
        self.title_label = ctk.CTkLabel(self, text=name)
        self.back_button = ctk.CTkButton(self, text="Back", command=self.parent.parent.loginPasswordManager)
        self.add_password_button = ctk.CTkButton(
            self, text="Add Password", command=lambda: self.parent.switchScreen(NewPassword(self.parent))
        )

        # Layout
        self.back_button.pack(side="left", padx=5)
        self.title_label.place(anchor="center", relx=0.5, rely=0.5)
        self.add_password_button.pack(side="right", padx=5)

class PasswordList(ctk.CTkScrollableFrame):
    def __init__(self, parent, name, key):
        super().__init__(parent)
        self.parent = parent
        self.name = name
        self.key = key

        self.addPasswordFrames()
    
    def addPasswordFrames(self):
        passwords = get_passwords(self.name, self.key)

        for password_id in passwords.keys():
            password = passwords[password_id]

            # Widgets
            frame = ctk.CTkFrame(self)

            def createLambda(func, *args):
                return lambda: func(*args)

            top_frame = ctk.CTkFrame(frame, fg_color="transparent")
            edit_button = ctk.CTkButton(
                top_frame, text="Edit",
                command=createLambda(self.parent.switchScreen, EditPassword(self.parent, password_id, password["site"], password["email"], password["password"]))
                )
            delete_button = ctk.CTkButton(
                top_frame, text="Delete",
                command=createLambda(self.parent.switchScreen, DeletePassword(self.parent, self.name, password_id, password["site"]))
            )
            site_label = ctk.CTkLabel(top_frame, text=password["site"])

            email_frame = ctk.CTkFrame(frame, fg_color="transparent")
            email_title_label = ctk.CTkLabel(email_frame, text="Email/Username")
            email_label = ctk.CTkLabel(email_frame, text=password["email"])

            password_frame = ctk.CTkFrame(frame, fg_color="transparent")
            password_title_label = ctk.CTkLabel(password_frame, text="Password")
            password_entry = ctk.CTkLabel(password_frame, text=password["password"])

            # Layout
            top_frame.pack(side="top", fill="x", padx=5, pady=5)
            edit_button.pack(side="left")
            site_label.place(anchor="center", relx=0.5, rely=0.5)
            delete_button.pack(side="right")

            email_frame.pack(side="top", fill="x", padx=5, pady=1)
            email_title_label.pack(side="left")
            email_label.pack(side="right")

            password_frame.pack(side="top", fill="x", padx=5, pady=1)
            password_title_label.pack(side="left")
            password_entry.pack(side="right")

            frame.pack(side="top", fill="x", pady=5, padx=5)

class NewPassword(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Widgets
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.title_label = ctk.CTkLabel(self.top_frame, text="Create a new password")
        self.back_button = ctk.CTkButton(self.top_frame, text="Back", command=self.back)
        self.site_entry = ctk.CTkEntry(self, placeholder_text="Website/App")
        self.email_entry = ctk.CTkEntry(self, placeholder_text="Email/Username")
        self.password_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.password_entry = ctk.CTkEntry(self.password_frame, placeholder_text="Password")
        self.random_password = ctk.CTkButton(self.password_frame, text="Random", command=self.random)
        self.create_button = ctk.CTkButton(self, text="Create", command=self.create)

        # Layout
        self.top_frame.pack(side="top", fill="x", padx=5, pady=5)
        self.title_label.place(anchor="center", relx=0.5, rely=0.5)
        self.back_button.pack(side="left")
        self.site_entry.pack(side="top", fill="x", padx=5, pady=5)
        self.email_entry.pack(side="top", fill="x", padx=5, pady=5)
        self.password_frame.pack(side="top", fill="x", padx=5, pady=5)
        self.password_entry.pack(side="left", fill="x", expand=True, padx=(0,5))
        self.random_password.pack(side="right")
        self.create_button.pack(side="top", fill="x", padx=5, pady=5)

    def random(self):
        password = secrets.token_urlsafe(16)
        self.password_entry.delete(0, "end")
        self.password_entry.insert(0, password)

    def create(self):
        site = self.site_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        if site == "" or email == "" or password == "":
            return
        
        add_password(self.parent.name, self.parent.key, site, email, password)
        self.back()

    def back(self):
        self.parent.switchScreen(self)

class DeletePassword(ctk.CTkFrame):
    def __init__(self, parent, name, password_id, site):
        super().__init__(parent)
        self.parent = parent
        self.name = name
        self.password_id = password_id
        self.site = site

        # Widgets
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.title_label = ctk.CTkLabel(self.top_frame, text=f"Are you sure you want to delete the password for {self.site}?")
        self.back_button = ctk.CTkButton(self.top_frame, text="Back", command=self.back)
        self.delete_button = ctk.CTkButton(self, text="Delete", command=self.delete)

        # Layout
        self.top_frame.pack(side="top", fill="x", padx=5, pady=5)
        self.title_label.place(anchor="center", relx=0.5, rely=0.5)
        self.back_button.pack(side="left")
        self.delete_button.pack(side="top", fill="x", padx=5, pady=5)
    
    def delete(self):
        delete_password(self.name, self.password_id)
        self.back()
    
    def back(self):
        self.parent.switchScreen(self)

class EditPassword(ctk.CTkFrame):
    def __init__(self, parent, password_id, site, email, password):
        super().__init__(parent)
        self.parent = parent
        self.password_id = password_id
        self.site = site
        self.email = email
        self.password = password

        # Widgets
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.title_label = ctk.CTkLabel(self.top_frame, text="Edit Password")
        self.back_button = ctk.CTkButton(self.top_frame, text="Back", command=self.back)
        self.site_entry = ctk.CTkEntry(self)
        self.site_entry.insert(0, self.site)
        self.email_entry = ctk.CTkEntry(self)
        self.email_entry.insert(0, self.email)
        self.password_entry = ctk.CTkEntry(self)
        self.password_entry.insert(0, self.password)
        self.edit_button = ctk.CTkButton(self, text="Edit", command=self.editPassword)

        # Layout
        self.top_frame.pack(side="top", fill="x", padx=5, pady=5)
        self.title_label.place(anchor="center", relx=0.5, rely=0.5)
        self.back_button.pack(side="left")
        self.site_entry.pack(side="top", fill="x", padx=5, pady=5)
        self.email_entry.pack(side="top", fill="x", padx=5, pady=5)
        self.password_entry.pack(side="top", fill="x", padx=5, pady=5)
        self.edit_button.pack(side="top", fill="x", padx=5, pady=5)
    
    def editPassword(self):
        new_site = self.site_entry.get()
        if new_site == self.site or new_site == "":
            new_site = None
        
        new_email = self.email_entry.get()
        if new_email == self.email or new_email == "":
            new_email = None
        
        new_password = self.password_entry.get()
        if new_password == self.password or new_password == "":
            new_password = None
        
        if new_site == None and new_email == None and new_password == None:
            return
        
        edit_password(
            self.parent.name, self.parent.key, self.password_id,
            new_site, new_email, new_password
        )
        self.back()

    def back(self):
        self.parent.switchScreen(self)
