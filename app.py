import tkinter as tk
from gui_components import MainApplication

def main():
    root = tk.Tk()
    root.title("ZF Volunteer Hours")
    # Set a reasonable default size for the application
    root.geometry("800x600")
    # Make the window resizable
    root.resizable(True, True)
    
    app = MainApplication(root)
    app.pack(fill="both", expand=True)
    
    root.mainloop()

if __name__ == "__main__":
    main()
