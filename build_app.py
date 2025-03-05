
import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox

def build_executable():
    """Build the executable package using PyInstaller"""
    # Install PyInstaller if not already installed
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Failed to install PyInstaller")
        return False
    
    # Build the executable
    try:
        # Create a spec file first for more control
        subprocess.run([
            sys.executable, 
            "-m", 
            "PyInstaller",
            "--name=ZF_Volunteer_Hours",
            "--windowed",  # No console window
            "--add-data=personal_data.csv:.",  # Include the data file
            "--onefile",  # Create a single executable file
            "app.py"
        ], check=True)
        
        # Show success message
        messagebox.showinfo("Success", 
            "Application built successfully!\n\n"
            "Look for the executable in the 'dist' folder.\n"
            "You can download this file from the Files panel in Replit.")
        return True
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to build executable: {e}")
        return False

if __name__ == "__main__":
    # Create a simple GUI for the build process
    root = tk.Tk()
    root.title("Build ZF Volunteer Hours App")
    root.geometry("400x200")
    
    # Add some instructions
    tk.Label(root, text="Build Standalone Application", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(root, text="This will create an executable file that can be run\non computers without Python installed.").pack(pady=5)
    
    # Add build button
    tk.Button(
        root, 
        text="Build Application", 
        command=lambda: build_executable() and root.destroy(),
        font=("Arial", 12),
        bg="#4CAF50",
        fg="white",
        padx=10,
        pady=5
    ).pack(pady=20)
    
    root.mainloop()
