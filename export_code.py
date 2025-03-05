
import os
import zipfile
import tkinter as tk
from tkinter import filedialog, messagebox

def export_code_to_zip():
    """Export all code files in the project to a zip file"""
    # List of common file extensions to include
    code_extensions = ['.py', '.csv', '.toml', '.nix', '.replit']
    
    # Get the root directory of the project
    root_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Ask user for zip file location
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    
    # Get the save file name
    zip_file = filedialog.asksaveasfilename(
        defaultextension=".zip",
        filetypes=[("Zip files", "*.zip"), ("All files", "*.*")],
        title="Save Code Archive"
    )
    
    if not zip_file:  # User canceled
        return
    
    try:
        # Create a zip file
        with zipfile.ZipFile(zip_file, 'w') as zipf:
            # Walk through all directories and subdirectories
            for root, dirs, files in os.walk(root_dir):
                for file in files:
                    # Check if the file has a code extension
                    _, ext = os.path.splitext(file)
                    if ext in code_extensions:
                        file_path = os.path.join(root, file)
                        # Add file to zip with relative path
                        rel_path = os.path.relpath(file_path, root_dir)
                        zipf.write(file_path, rel_path)
        
        # Inform user about success
        messagebox.showinfo("Export Complete", 
            f"Code exported to: {zip_file}\n\n" +
            "The zip file contains all your Python code and project files.")
            
    except Exception as e:
        messagebox.showerror("Export Error", f"Failed to export code: {str(e)}")

if __name__ == "__main__":
    export_code_to_zip()
