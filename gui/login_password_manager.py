import customtkinter as ctk
from tkinter.filedialog import askdirectory, askopenfile

from storage import delete_password_manager, get_password_manager_names, import_password_manager, export_password_manager

class LoginPasswordManager(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Widgets
        self.navbar = Navbar(self)
        self.current_screen = PasswordManagerList(self)

        # Layout
        self.navbar.pack(side="top", fill="x", padx=5, pady=5, ipadx=5, ipady=5)
        self.current_screen.pack(side="top", fill="both", expand=True, padx=5, pady=5)
    
    def switchScreen(self, screen):
        if type(screen) == type(self.current_screen):
            self.current_screen.pack_forget()
            del self.current_screen
            self.current_screen = PasswordManagerList(self)
        else:
            self.current_screen.pack_forget()
            del self.current_screen
            self.current_screen = screen
        self.current_screen.pack(side="top", fill="both", expand=True, padx=5, pady=5)

class Navbar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Widgets
        self.title_label = ctk.CTkLabel(self, text="Password Manager")
        self.import_button = ctk.CTkButton(
            self, text="Import", command=lambda: self.parent.switchScreen(ImportFrame(self.parent))
        )
        self.new_password_manager_button = ctk.CTkButton(
            self, text="New", command=lambda: self.parent.switchScreen(NewPasswordManager(self.parent))
        )

        # Layout
        self.title_label.place(anchor="center", relx=0.5, rely=0.5)
        self.import_button.pack(side="left", padx=5)
        self.new_password_manager_button.pack(side="right", padx=5)

class PasswordManagerList(ctk.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.password_manager_names = get_password_manager_names()

        self.addPasswordManagerFrames()

    def addPasswordManagerFrames(self):
        for name in self.password_manager_names:
            frame = ctk.CTkFrame(self)

            top_frame = ctk.CTkFrame(frame, fg_color="transparent")
            name_label = ctk.CTkLabel(top_frame, text=name)

            def createLambda(func, *args):
                return lambda: func(*args)
            
            export_button = ctk.CTkButton(
                top_frame, text="Export",
                command=createLambda(self.parent.switchScreen, ExportFrame(self.parent, name))
            )
            delete_button = ctk.CTkButton(
                top_frame, text="Delete",
                command=createLambda(self.parent.switchScreen, DeleteFrame(self.parent, name))
            )
            login_button = ctk.CTkButton(
                frame, text="Login", 
                command=createLambda(self.parent.switchScreen, LoginFrame(self.parent, name))
            )

            top_frame.pack(side="top", fill="x", padx=5, pady=5)
            name_label.place(anchor="center", relx=0.5, rely=0.5)
            export_button.pack(side="left")
            delete_button.pack(side="right")
            login_button.pack(side="top", padx=5, pady=5)

            frame.pack(side="top", fill="x", pady=5)

class NewPasswordManager(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        # Widgets
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.title_label = ctk.CTkLabel(self.top_frame, text="Create a Password Manager")
        self.back_button = ctk.CTkButton(self.top_frame, text="Back", command=self.back)

        self.name_entry = ctk.CTkEntry(self, placeholder_text="Name")

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password")

        self.create_button = ctk.CTkButton(self, text="Create", command=self.createPasswordManager)
        self.error_message = ctk.CTkLabel(self, text="", text_color="red")

        # Layout
        self.top_frame.pack(side="top", fill="x", padx=5, pady=5)
        self.title_label.place(anchor="center", relx=0.5, rely=0.5)
        self.back_button.pack(side="left")
        self.name_entry.pack(side="top", fill="x", padx=5, pady=5)
        self.password_entry.pack(side="top", fill="x", padx=5, pady=5)
        self.create_button.pack(side="top", fill="x", padx=5, pady=5)
        self.error_message.pack(side="top", padx=5, pady=5)
    
    def createPasswordManager(self):
        name = self.name_entry.get()
        password = self.password_entry.get()

        if name == "":
            self.error_message.configure(text="Name needs to be atleast 1 character long.")
            return
        
        if name in get_password_manager_names():
            self.error_message.configure(text="Name already exists.")
            return

        if len(password) < 8:
            self.error_message.configure(text="Password needs to be atleast 8 characters long.")
            return
        
        self.parent.parent.createPasswordManager(name, password)
    
    def togglePasswordShow(self):
        if self.password_entry.cget("show") == "":
            self.password_entry.configure(show="*")
            self.toggle_show_password_button.configure(image=self.show_image)
            self.is_showing_password = False
        else:
            self.password_entry.configure(show="")
            self.toggle_show_password_button.configure(image=self.hide_image)
            self.is_showing_password = True

    def back(self):
        self.error_message.configure(text="")
        self.parent.switchScreen(PasswordManagerList(self.parent))

class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, manager_name):
        super().__init__(parent)
        self.parent = parent
        self.manager_name = manager_name

        # Widgets
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.name_label = ctk.CTkLabel(self.top_frame, text=f"Login to {self.manager_name}")
        self.back_button = ctk.CTkButton(self.top_frame, text="Back", command=self.back)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.login_button = ctk.CTkButton(self, text="Login", command=self.login)
        self.error_message = ctk.CTkLabel(self, text="", text_color="red")

        # Layout
        self.top_frame.pack(side="top", fill="x", padx=5, pady=5)
        self.name_label.place(anchor="center", relx=0.5, rely=0.5)
        self.back_button.pack(side="left")
        self.password_entry.pack(side="top", fill="x", padx=5, pady=5)
        self.login_button.pack(side="top", fill="x", padx=5, pady=5)
        self.error_message.pack(side="top", padx=5, pady=5)
    
    def back(self):
        self.error_message.configure(text="")
        self.parent.switchScreen(self)
    
    def login(self):
        returned = self.parent.parent.openPasswordManager(self.manager_name, self.password_entry.get())
        if (returned == False):
            self.error_message.configure(text="Wrong password.")

class DeleteFrame(ctk.CTkFrame):
    def __init__(self, parent, name):
        super().__init__(parent)
        self.parent = parent
        self.name = name
        
        # Widgets
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.title_label = ctk.CTkLabel(self.top_frame, text=f"Are you sure you want to delete {name}?")
        self.back_button = ctk.CTkButton(self.top_frame, text="Back", command=self.back)
        self.delete_button = ctk.CTkButton(self, text="Delete", command=self.delete)

        # Layout
        self.top_frame.pack(side="top", fill="x", padx=5, pady=5)
        self.title_label.place(anchor="center", relx=0.5, rely=0.5)
        self.back_button.pack(side="left")
        self.delete_button.pack(side="top", fill="x", padx=5, pady=5)
    
    def delete(self):
        delete_password_manager(self.name)
        self.back()
    
    def back(self):
        self.parent.switchScreen(PasswordManagerList(self.parent))

class ImportFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.filepath = None
        self.filename = None

        # Widgets
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.title_label = ctk.CTkLabel(self.top_frame, text="Import a password manager")
        self.back_button = ctk.CTkButton(self.top_frame, text="Back", command=self.back)
        self.middle_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.choose_file_button = ctk.CTkButton(self.middle_frame, text="Choose a file", command=self.chooseFile)
        self.file_label = ctk.CTkLabel(self.middle_frame, text="No file selected")
        self.import_button = ctk.CTkButton(self, text="Import", command=self.importFile)
        self.error_message = ctk.CTkLabel(self, text="", text_color="red")

        # Layout
        self.top_frame.pack(side="top", fill="x", padx=5, pady=5)
        self.title_label.place(anchor="center", relx=0.5, rely=0.5)
        self.back_button.pack(side="left")
        self.middle_frame.pack(side="top", padx=5, pady=5)
        self.choose_file_button.pack(side="left", padx=5)
        self.file_label.pack(side="left", padx=5)
        self.import_button.pack(side="top", fill="x", padx=5, pady=5)
        self.error_message.pack(side="top", padx=5, pady=5)
    
    def chooseFile(self):
        file = askopenfile(title="Import your Password Manager file")

        if file == None:
            return
        
        self.filepath = file.name
        self.filename = file.name.split("/")[-1]

        if ".dat" not in self.filename:
            self.filepath = None
            self.filename = None
            return
        
        self.filename = self.filename.replace(".dat", "")

        self.file_label.configure(text=self.filename)
    
    def importFile(self):
        if self.filepath == None:
            return
        
        if self.filename in get_password_manager_names():
            self.error_message.configure(text="Name already exists.")
            return

        if import_password_manager(self.filepath) == True:
            self.back()

    def back(self):
        self.error_message.configure(text="")
        self.parent.switchScreen(PasswordManagerList(self.parent))

class ExportFrame(ctk.CTkFrame):
    def __init__(self, parent, name):
        super().__init__(parent)
        self.parent = parent
        self.name = name

        self.dirpath = None

        # Widgets
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.title_label = ctk.CTkLabel(self.top_frame, text=f"Export password manager {self.name}")
        self.back_button = ctk.CTkButton(self.top_frame, text="Back", command=self.back)
        self.middle_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.choose_directory_button = ctk.CTkButton(
            self.middle_frame, text="Choose directory", command=self.chooseDirectory
        )
        self.directory_label = ctk.CTkLabel(self.middle_frame, text="No directory selected")
        self.export_button = ctk.CTkButton(self, text="Export", command=self.exportFile)

        # Layout
        self.top_frame.pack(side="top", fill="x", padx=5, pady=5)
        self.title_label.place(anchor="center", relx=0.5, rely=0.5)
        self.back_button.pack(side="left")
        self.middle_frame.pack(side="top", padx=5, pady=5)
        self.choose_directory_button.pack(side="left", padx=5)
        self.directory_label.pack(side="left", padx=5)
        self.export_button.pack(side="top", fill="x", padx=5, pady=5)
    
    def chooseDirectory(self):
        directory = askdirectory()

        if directory == "":
            return
        
        self.dirpath = directory
        
        dirname = self.dirpath.split("/")[-1]
        self.directory_label.configure(text=dirname)
    
    def exportFile(self):
        if self.dirpath == None:
            return
        
        returned = export_password_manager(self.name, self.dirpath)
        if returned == True:
            self.back()
    
    def back(self):
        self.parent.switchScreen(PasswordManagerList(self.parent))
