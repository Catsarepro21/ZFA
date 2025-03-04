import tkinter as tk
from tkinter import ttk, messagebox
from data_manager import DataManager
from utils import validate_input

class InfoDialog(tk.Toplevel):
    def __init__(self, parent, person_name):
        super().__init__(parent)
        self.title(f"Enter Information for {person_name}")
        self.person_name = person_name

        # Make dialog modal
        self.transient(parent)
        self.grab_set()

        # Create form fields
        ttk.Label(self, text="Location:").grid(row=0, column=0, pady=5, padx=5, sticky="w")
        self.location_entry = ttk.Entry(self, width=30)
        self.location_entry.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(self, text="Event:").grid(row=1, column=0, pady=5, padx=5, sticky="w")
        self.event_entry = ttk.Entry(self, width=30)
        self.event_entry.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(self, text="Hours:").grid(row=2, column=0, pady=5, padx=5, sticky="w")
        self.hours_entry = ttk.Entry(self, width=30)
        self.hours_entry.grid(row=2, column=1, pady=5, padx=5)

        # Buttons
        button_frame = ttk.Frame(self)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Save", command=self.save).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side="left", padx=5)

        # Center the dialog
        self.geometry("300x200")
        self.resizable(False, False)

    def save(self):
        self.result = {
            'location': self.location_entry.get().strip(),
            'event': self.event_entry.get().strip(),
            'hours': self.hours_entry.get().strip()
        }
        self.destroy()

    def cancel(self):
        self.result = None
        self.destroy()

class MainApplication(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.data_manager = DataManager()

        self.create_widgets()
        self.refresh_people_list()

    def create_widgets(self):
        # Create main containers
        left_frame = ttk.Frame(self, relief="solid", borderwidth=1)
        right_frame = ttk.Frame(self, relief="solid", borderwidth=1)

        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Left frame contents - People List
        list_label = ttk.Label(left_frame, text="People List", font=('Arial', 12, 'bold'))
        list_label.pack(anchor="w", pady=(0, 5))

        # Add new person section at the top
        add_frame = ttk.Frame(left_frame)
        add_frame.pack(fill="x", pady=(0, 10))

        self.new_person_entry = ttk.Entry(add_frame)
        self.new_person_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

        add_button = ttk.Button(add_frame, text="Add Person", 
                              command=self.add_new_person, style='Accent.TButton')
        add_button.pack(side="right")

        # People listbox with scrollbar
        listbox_frame = ttk.Frame(left_frame)
        listbox_frame.pack(fill="both", expand=True)

        self.people_listbox = tk.Listbox(listbox_frame, height=15, font=('Arial', 10))
        scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical", command=self.people_listbox.yview)
        self.people_listbox.configure(yscrollcommand=scrollbar.set)

        self.people_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.people_listbox.bind('<Double-Button-1>', self.on_double_click)

        # Right frame contents - Information Display
        info_label = ttk.Label(right_frame, text="Previous Entries:", font=('Arial', 12, 'bold'))
        info_label.pack(anchor="w", pady=(0, 5))

        # Add scrollbar to info display
        info_frame = ttk.Frame(right_frame)
        info_frame.pack(fill="both", expand=True)

        self.info_display = tk.Text(info_frame, height=20, state='disabled', font=('Arial', 10))
        info_scrollbar = ttk.Scrollbar(info_frame, orient="vertical", command=self.info_display.yview)
        self.info_display.configure(yscrollcommand=info_scrollbar.set)

        self.info_display.pack(side="left", fill="both", expand=True)
        info_scrollbar.pack(side="right", fill="y")

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

    def on_double_click(self, event):
        if not self.people_listbox.curselection():
            return

        selected_person = self.people_listbox.get(self.people_listbox.curselection())
        self.show_info_dialog(selected_person)

    def show_info_dialog(self, name):
        dialog = InfoDialog(self, name)
        self.wait_window(dialog)
        if hasattr(dialog, 'result') and dialog.result is not None:
            success, message = self.data_manager.add_person_info(
                name,
                dialog.result['location'],
                dialog.result['event'],
                dialog.result['hours']
            )
            if success:
                self.display_person_info(name)
                messagebox.showinfo("Success", message)
            else:
                messagebox.showerror("Error", message)

    def display_person_info(self, name):
        info_records = self.data_manager.get_person_info(name)

        self.info_display.config(state='normal')
        self.info_display.delete(1.0, tk.END)

        for record in info_records:
            entry = f"[{record['Timestamp']}]\n"
            entry += f"Location: {record['Location']}\n"
            entry += f"Event: {record['Event']}\n"
            entry += f"Hours: {record['Hours']}\n\n"
            self.info_display.insert(tk.END, entry)

        self.info_display.config(state='disabled')