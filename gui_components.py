import tkinter as tk
from tkinter import ttk, messagebox
from data_manager import DataManager
from utils import validate_input

class MainApplication(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.data_manager = DataManager()
        
        self.create_widgets()
        self.refresh_people_list()
        
    def create_widgets(self):
        # Create main containers
        left_frame = ttk.Frame(self)
        right_frame = ttk.Frame(self)
        
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Left frame contents - People List
        ttk.Label(left_frame, text="People List").pack(anchor="w")
        
        # People listbox
        self.people_listbox = tk.Listbox(left_frame, height=15)
        self.people_listbox.pack(fill="both", expand=True)
        self.people_listbox.bind('<<ListboxSelect>>', self.on_select_person)
        
        # Add new person section
        add_frame = ttk.Frame(left_frame)
        add_frame.pack(fill="x", pady=(10, 0))
        
        self.new_person_entry = ttk.Entry(add_frame)
        self.new_person_entry.pack(side="left", fill="x", expand=True)
        
        ttk.Button(add_frame, text="Add Person", 
                   command=self.add_new_person).pack(side="right", padx=(5, 0))
        
        # Right frame contents - Information Input
        ttk.Label(right_frame, text="Add Information").pack(anchor="w")
        
        self.info_text = tk.Text(right_frame, height=10)
        self.info_text.pack(fill="both", expand=True)
        
        ttk.Button(right_frame, text="Save Information", 
                   command=self.save_information).pack(pady=(10, 0))
        
        # Information display section
        ttk.Label(right_frame, text="Previous Entries:").pack(anchor="w", pady=(10, 0))
        self.info_display = tk.Text(right_frame, height=10, state='disabled')
        self.info_display.pack(fill="both", expand=True)
        
    def refresh_people_list(self):
        self.people_listbox.delete(0, tk.END)
        people = self.data_manager.get_all_people()
        for person in people:
            self.people_listbox.insert(tk.END, person)
            
    def add_new_person(self):
        name = self.new_person_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter a name!")
            return
            
        success, message = self.data_manager.add_new_person(name)
        if success:
            self.new_person_entry.delete(0, tk.END)
            self.refresh_people_list()
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)
            
    def on_select_person(self, event):
        if not self.people_listbox.curselection():
            return
            
        selected_person = self.people_listbox.get(self.people_listbox.curselection())
        self.display_person_info(selected_person)
        
    def display_person_info(self, name):
        info_records = self.data_manager.get_person_info(name)
        
        self.info_display.config(state='normal')
        self.info_display.delete(1.0, tk.END)
        
        for record in info_records:
            entry = f"[{record['Timestamp']}]\n{record['Information']}\n\n"
            self.info_display.insert(tk.END, entry)
            
        self.info_display.config(state='disabled')
        
    def save_information(self):
        if not self.people_listbox.curselection():
            messagebox.showerror("Error", "Please select a person first!")
            return
            
        selected_person = self.people_listbox.get(self.people_listbox.curselection())
        information = self.info_text.get(1.0, tk.END).strip()
        
        if not information:
            messagebox.showerror("Error", "Please enter some information!")
            return
            
        if not validate_input(information):
            messagebox.showerror("Error", "Invalid input! Please check your text.")
            return
            
        success, message = self.data_manager.add_person_info(selected_person, information)
        if success:
            self.info_text.delete(1.0, tk.END)
            self.display_person_info(selected_person)
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)
