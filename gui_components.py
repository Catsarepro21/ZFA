import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import os
from data_manager import DataManager
from utils import validate_input
import subprocess

class PasswordDialog(tk.Toplevel):
    def __init__(self, parent, change_password=False):
        super().__init__(parent)
        self.title("Change Password" if change_password else "Enter Password")
        self.geometry("300x250" if change_password else "300x150")
        self.resizable(False, False)

        # Make dialog modal
        self.transient(parent)
        self.grab_set()

        # Center the dialog
        self.center_on_parent()

        # Add password entry
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill="both", expand=True)

        if change_password:
            ttk.Label(main_frame, text="Current Password:", font=('Arial', 10)).pack(pady=(0, 5))
            self.current_password = ttk.Entry(main_frame, show="*")
            self.current_password.pack(fill="x", pady=(0, 10))

            ttk.Label(main_frame, text="New Password:", font=('Arial', 10)).pack(pady=(0, 5))
            self.new_password = ttk.Entry(main_frame, show="*")
            self.new_password.pack(fill="x", pady=(0, 10))

            ttk.Label(main_frame, text="Confirm Password:", font=('Arial', 10)).pack(pady=(0, 5))
            self.confirm_password = ttk.Entry(main_frame, show="*")
            self.confirm_password.pack(fill="x", pady=(0, 10))

            # Set focus to current password entry
            self.current_password.focus_set()
        else:
            ttk.Label(main_frame, text="Password:", font=('Arial', 10)).pack(pady=(0, 10))
            self.password_entry = ttk.Entry(main_frame, show="*")
            self.password_entry.pack(fill="x", pady=(0, 20))
            # Set focus to password entry
            self.password_entry.focus_set()

        # Buttons
        ttk.Button(main_frame, text="Submit", command=self.submit).pack(side="left", padx=10)
        ttk.Button(main_frame, text="Cancel", command=self.cancel).pack(side="right", padx=10)

    def center_on_parent(self):
        self.update_idletasks()
        parent = self.master
        x = parent.winfo_x() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")

    def submit(self):
        if hasattr(self, 'password_entry'):
            self.result = self.password_entry.get()
        else:
            if self.new_password.get() != self.confirm_password.get():
                messagebox.showerror("Error", "New passwords do not match!")
                return
            self.result = {
                'current': self.current_password.get(),
                'new': self.new_password.get()
            }
        self.destroy()

    def cancel(self):
        self.result = None
        self.destroy()

class InfoDialog(tk.Toplevel):
    def __init__(self, parent, person_name):
        super().__init__(parent)
        self.title(f"Enter Information for {person_name}")
        self.person_name = person_name


        # Set up the dialog
        self.geometry("400x300")  # Increased height for additional field
        self.resizable(False, False)

        # Ensure the dialog appears on top
        self.transient(parent)
        self.focus_set()

        # Add some padding and a main frame
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill="both", expand=True)

        # Create form fields with better spacing and labels
        ttk.Label(main_frame, text="Location:", font=('Arial', 10)).grid(row=0, column=0, pady=10, padx=5, sticky="w")
        self.location_entry = ttk.Entry(main_frame, width=30)
        self.location_entry.grid(row=0, column=1, pady=10, padx=5)
        # Add placeholder text
        self.location_entry.insert(0, "e.g., ZF Center, Terrace Apartments, etc.")
        self.location_entry.config(foreground='gray')
        # Set up focus events
        self.location_entry.bind("<FocusIn>", self.on_location_focus_in)
        self.location_entry.bind("<FocusOut>", self.on_location_focus_out)

        ttk.Label(main_frame, text="Event:", font=('Arial', 10)).grid(row=1, column=0, pady=10, padx=5, sticky="w")
        self.event_entry = ttk.Entry(main_frame, width=30)
        self.event_entry.grid(row=1, column=1, pady=10, padx=5)
        # Add placeholder text
        self.event_entry.insert(0, "e.g., Packing, Distribution, etc.")
        self.event_entry.config(foreground='gray')
        # Set up focus events
        self.event_entry.bind("<FocusIn>", self.on_event_focus_in)
        self.event_entry.bind("<FocusOut>", self.on_event_focus_out)

        ttk.Label(main_frame, text="Hours (HH:MM):", font=('Arial', 10)).grid(row=2, column=0, pady=10, padx=5, sticky="w")
        self.hours_entry = ttk.Entry(main_frame, width=30)
        self.hours_entry.grid(row=2, column=1, pady=10, padx=5)
        # Add placeholder text
        self.hours_entry.insert(0, "e.g., 2:30")
        self.hours_entry.config(foreground='gray')
        # Set up focus events for placeholder
        self.hours_entry.bind("<FocusIn>", self.on_hours_focus_in)
        self.hours_entry.bind("<FocusOut>", self.on_hours_focus_out)

        # Add date field and current date checkbox
        ttk.Label(main_frame, text="Date:", font=('Arial', 10)).grid(row=3, column=0, pady=10, padx=5, sticky="w")

        # Frame to hold date entry and checkbox
        date_frame = ttk.Frame(main_frame)
        date_frame.grid(row=3, column=1, pady=10, padx=5, sticky="w")

        # Date entry field
        self.date_entry = ttk.Entry(date_frame, width=20)
        self.date_entry.pack(side="left", padx=(0, 5))

        # Current date variable and checkbox
        self.use_current_date = tk.BooleanVar(value=True)
        self.date_checkbox = ttk.Checkbutton(
            date_frame, 
            text="Use Current Date", 
            variable=self.use_current_date,
            command=self.toggle_date_entry
        )
        self.date_checkbox.pack(side="left")

        # Set default value to current date and disable entry initially
        current_date = datetime.now().strftime("%Y-%m-%d")
        self.date_entry.insert(0, current_date)
        self.date_entry.configure(state="disabled")

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Save", command=self.save, width=10).pack(side="left", padx=10)
        ttk.Button(button_frame, text="Cancel", command=self.cancel, width=10).pack(side="left", padx=10)

        # Center the dialog on the parent window
        self.center_on_parent()

    def toggle_date_entry(self):
        """Enable or disable date entry based on checkbox state"""
        from datetime import datetime

        if self.use_current_date.get():
            # Update with current date and disable
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
            self.date_entry.configure(state="disabled")
        else:
            # Enable for manual entry
            self.date_entry.configure(state="normal")
            
    def on_location_focus_in(self, event):
        """Clear placeholder text when entry gets focus"""
        if self.location_entry.get() == "e.g., ZF Center, Terrace Apartments, etc.":
            self.location_entry.delete(0, tk.END)
            self.location_entry.config(foreground='black')
            
    def on_location_focus_out(self, event):
        """Add placeholder text if entry is empty and loses focus"""
        if not self.location_entry.get():
            self.location_entry.insert(0, "e.g., ZF Center, Terrace Apartments, etc.")
            self.location_entry.config(foreground='gray')

    def on_event_focus_in(self, event):
        """Clear placeholder text when entry gets focus"""
        if self.event_entry.get() == "e.g., Packing, Distribution, etc.":
            self.event_entry.delete(0, tk.END)
            self.event_entry.config(foreground='black')
            
    def on_event_focus_out(self, event):
        """Add placeholder text if entry is empty and loses focus"""
        if not self.event_entry.get():
            self.event_entry.insert(0, "e.g., Packing, Distribution, etc.")
            self.event_entry.config(foreground='gray')

    def on_hours_focus_in(self, event):
        """Clear placeholder text when entry gets focus"""
        if self.hours_entry.get() == "e.g., 2:30":
            self.hours_entry.delete(0, tk.END)
            self.hours_entry.config(foreground='black')
            
    def on_hours_focus_out(self, event):
        """Add placeholder text if entry is empty and loses focus"""
        if not self.hours_entry.get():
            self.hours_entry.insert(0, "e.g., 2:30")
            self.hours_entry.config(foreground='gray')

    def center_on_parent(self):
        self.update_idletasks()
        parent = self.master
        x = parent.winfo_x() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")

    def save(self):
        # Get values, removing placeholders
        location = self.location_entry.get().strip()
        event = self.event_entry.get().strip()
        hours = self.hours_entry.get().strip()
        date_value = self.date_entry.get().strip() if not self.use_current_date.get() else datetime.now().strftime("%Y-%m-%d")
        
        # Remove placeholders if they are still there
        if location == "e.g., ZF Center, Terrace Apartments, etc.":
            location = ""
        if event == "e.g., Packing, Distribution, etc.":
            event = ""
        if hours == "e.g., 2:30":
            hours = ""
            
        # Check hours format (HH:MM)
        import re
        if hours and not re.match(r'^([0-9]{1,2}):([0-5][0-9])$', hours):
            tk.messagebox.showwarning("Invalid Format", "Hours must be in HH:MM format (e.g., 2:30, 10:15)")
            self.hours_entry.focus_set()
            return
        
        # Check if all main fields are empty
        if not location and not event and not hours:
            # Show warning
            tk.messagebox.showwarning("Empty Information", "All fields are empty. No entry will be added.")
            self.result = None
            self.destroy()
            return
            
        # Check if there's meaningful information to save
        has_data = False
        if (location and location.strip()) or (event and event.strip()) or (hours and hours.strip()):
            has_data = True
            
        if not has_data:
            tk.messagebox.showwarning("Empty Information", "All fields are empty. No entry will be added.")
            self.result = None
            self.destroy()
            return
            
        # Proceed with save - ensure empty strings instead of None or NaN
        self.result = {
            'location': location if location else '',
            'event': event if event else '',
            'hours': hours if hours else '',
            'date': date_value if date_value else datetime.now().strftime("%Y-%m-%d")
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
        # Load password from file via DataManager
        self.ADMIN_PASSWORD = self.data_manager.get_password()
        # Track deleted entries for undo functionality
        self.deleted_entries = []

        # Check if using Google Sheets
        self.using_google_sheets = self.data_manager.use_google_sheets

        self.create_widgets()
        self.refresh_people_list()

    def create_widgets(self):
        # Create main containers
        self.left_frame = ttk.Frame(self, relief="solid", borderwidth=1)
        self.right_frame = ttk.Frame(self, relief="solid", borderwidth=1)

        self.left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Left frame contents - People List
        list_label = ttk.Label(self.left_frame, text="People List", font=('Arial', 12, 'bold'))
        list_label.pack(anchor="w", pady=(0, 5))

        # Don't See Your Name button
        self.show_add_button = ttk.Button(self.left_frame, text="Don't See Your Name?", 
                                         command=self.toggle_add_person_form)
        self.show_add_button.pack(fill="x", pady=(0, 10))

        # Add new person section - initially hidden
        self.add_frame = ttk.Frame(self.left_frame)
        # Don't pack the frame initially to hide it

        self.new_person_entry = ttk.Entry(self.add_frame)
        self.new_person_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

        # Add menu bar
        self.parent.option_add('*tearOff', False)
        menubar = tk.Menu(self.parent)
        self.parent.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.parent.destroy)

        # Add placeholder text
        self.placeholder_text = "e.g., First and Last name"
        self.new_person_entry.insert(0, self.placeholder_text)
        self.new_person_entry.configure(foreground='gray')

        # Bind focus events to handle placeholder behavior
        self.new_person_entry.bind("<FocusIn>", self.on_entry_focus_in)
        self.new_person_entry.bind("<FocusOut>", self.on_entry_focus_out)

        add_button = ttk.Button(self.add_frame, text="Add Person", 
                              command=self.add_new_person, style='Accent.TButton')
        add_button.pack(side="right")

        # People listbox with scrollbar
        listbox_frame = ttk.Frame(self.left_frame)
        listbox_frame.pack(fill="both", expand=True)

        self.people_listbox = tk.Listbox(listbox_frame, height=15, font=('Arial', 10))
        scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical", command=self.people_listbox.yview)
        self.people_listbox.configure(yscrollcommand=scrollbar.set)

        self.people_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.people_listbox.bind('<Double-Button-1>', self.on_double_click)

        # Add buttons frame for view buttons
        buttons_frame = ttk.Frame(self.left_frame)
        buttons_frame.pack(side="bottom", fill="x", pady=10)

        # Add view all entries button
        view_all_button = ttk.Button(buttons_frame, text="View All Entries", 
                                   command=self.view_all_entries, width=20)
        view_all_button.pack(side="left", padx=(0, 5), expand=True, fill="x")

        # Add view selected entries button
        view_selected_button = ttk.Button(buttons_frame, text="View Selected Entries", 
                                        command=self.view_selected_entries, width=20)
        view_selected_button.pack(side="right", padx=(5, 0), expand=True, fill="x")

        # Right frame contents - Information Display with TreeView
        self.entries_frame = ttk.Frame(self.right_frame)

        info_label = ttk.Label(self.entries_frame, text="Previous Entries", font=('Arial', 12, 'bold'))
        info_label.pack(anchor="w", pady=(0, 5))

        # Add buttons frame in entries view
        self.buttons_frame = ttk.Frame(self.entries_frame)
        self.buttons_frame.pack(fill="x", pady=(10, 0))

        # Add change password button
        change_password_button = ttk.Button(self.buttons_frame, text="Change Password", 
                                          command=self.change_password, width=15)
        change_password_button.pack(side="left", padx=5)

        # Add delete button
        self.delete_button = ttk.Button(self.buttons_frame, text="Delete Selected", 
                                     command=self.delete_selected_entries, width=15)
        self.delete_button.pack(side="left", padx=5)

        # Add undo button (initially disabled)
        self.undo_button = ttk.Button(self.buttons_frame, text="Undo Delete", 
                                    command=self.undo_delete, width=15, state="disabled")
        self.undo_button.pack(side="left", padx=5)

        # Add export button with dropdown menu
        export_button = ttk.Button(self.buttons_frame, text="Export", width=10)
        export_button.pack(side="right", padx=5)

        # Create a popup menu for export options
        self.export_menu = tk.Menu(self.parent, tearoff=0)
        self.export_menu.add_command(label="Export to CSV", command=self.export_to_csv)
        self.export_menu.add_command(label="Export to Excel", command=self.export_to_excel)
        self.export_menu.add_separator()
        self.export_menu.add_command(label="Setup Auto Excel Update", command=self.setup_auto_excel)
        self.export_menu.add_command(label="Export Current View", command=self.export_entries)

        # Bind the export button to show the export menu
        export_button.bind("<Button-1>", self.show_export_menu)

        # Add close button
        close_button = ttk.Button(self.buttons_frame, text="Close", 
                                command=self.close_entries_view, width=10)
        close_button.pack(side="right", padx=5)
        # Add clean data button
        clean_button = ttk.Button(self.buttons_frame, text="Clean Data", 
                               command=self.clean_empty_entries, width=15)
        clean_button.pack(side="right", padx=5)

        # Add import button with dropdown menu
        import_button = ttk.Button(self.buttons_frame, text="Import", width=10)
        import_button.pack(side="right", padx=5)

        # Create a popup menu for import options
        self.import_menu = tk.Menu(self.parent, tearoff=0)
        self.import_menu.add_command(label="Import from CSV (App Format)", command=self.import_entries)
        self.import_menu.add_command(label="Import from CSV (Generic)", command=self.import_from_csv)

        # Bind the import button to show the import menu
        import_button.bind("<Button-1>", self.show_import_menu)


        # Create Treeview for spreadsheet-like display
        self.tree = ttk.Treeview(self.entries_frame, columns=('Name', 'Date', 'Location', 'Event', 'Hours'), show='headings')

        # Define column headings
        self.tree.heading('Name', text='Name')
        self.tree.heading('Date', text='Date')
        self.tree.heading('Location', text='Location')
        self.tree.heading('Event', text='Event')
        self.tree.heading('Hours', text='Hours')

        # Configure column widths
        self.tree.column('Name', width=150)
        self.tree.column('Date', width=150)
        self.tree.column('Location', width=150)
        self.tree.column('Event', width=150)
        self.tree.column('Hours', width=100)

        # Add scrollbar to treeview
        tree_scroll = ttk.Scrollbar(self.entries_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)

        self.tree.pack(side="left", fill="both", expand=True)
        tree_scroll.pack(side="right", fill="y")

        # Initially hide the entries frame and right frame
        self.entries_frame.pack_forget()
        # Don't pack the right frame initially


    def view_all_entries(self):
        """Show all entries regardless of selection"""
        if not self.verify_password():
            messagebox.showerror("Error", "Incorrect password!")
            return

        # Show the entries view if not already visible
        if not self.entries_frame.winfo_ismapped():
            self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
            self.entries_frame.pack(fill="both", expand=True)

        # Display all entries
        self.display_all_entries()

    def view_selected_entries(self):
        """Show entries only for the selected person"""
        if not self.verify_password():
            messagebox.showerror("Error", "Incorrect password!")
            return

        # Check if a person is selected
        if not self.people_listbox.curselection():
            messagebox.showinfo("Information", "Please select a person first.")
            return

        # Show the entries view if not already visible
        if not self.entries_frame.winfo_ismapped():
            self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
            self.entries_frame.pack(fill="both", expand=True)

        # Display selected person's info
        selected_person = self.people_listbox.get(self.people_listbox.curselection())
        self.display_person_info(selected_person)

    def toggle_entries_view(self):
        """Legacy method for backward compatibility"""
        if self.entries_frame.winfo_ismapped():
            self.close_entries_view()
        else:
            self.view_all_entries()

    def close_entries_view(self):
        self.entries_frame.pack_forget()
        self.right_frame.pack_forget()
        self.left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    def toggle_add_person_form(self):
        if self.add_frame.winfo_ismapped():
            self.add_frame.pack_forget()
            self.show_add_button.configure(text="Don't See Your Name?")
        else:
            self.add_frame.pack(fill="x", pady=(0, 10))
            self.show_add_button.configure(text="Hide Add Person")
            self.new_person_entry.focus_set()

    def export_entries(self):
        from tkinter import filedialog, simpledialog
        import csv

        # Ask if user wants to export all entries or just selected person
        has_selection = bool(self.people_listbox.curselection())

        if has_selection:
            selected_person = self.people_listbox.get(self.people_listbox.curselection())
            options = ["Selected Person", "All Entries"]
            choice = simpledialog.askstring(
                "Export Options", 
                f"Export entries for {selected_person} or all entries?",
                initialvalue="Selected Person"
            )

            if not choice:  # User canceled
                return

            export_all = (choice.lower() == "all entries")
        else:
            export_all = True

        # Get the records
        if export_all:
            records = self.data_manager.get_all_entries()
            if not records:
                messagebox.showinfo("Information", "No records to export")
                return
            export_title = "All Entries"
        else:
            records = self.data_manager.get_person_info(selected_person)
            if not records:
                messagebox.showinfo("Information", "No records to export for this person")
                return
            export_title = f"Entries for {selected_person}"

        # Ask user for file location with a default filename
        default_filename = f"exported_{export_title.replace(' ', '_')}.csv"
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title=f"Export {export_title}",
            initialfile=default_filename
        )

        if not filename:  # If user cancels the save dialog
            return

        # Show message about file location
        messagebox.showinfo("Export Complete", 
            f"File saved as: {filename}\n\n" +
            "To download this file from Replit to your computer:\n" +
            "1. Look for the file in the Files panel (left side)\n" +
            "2. Right-click on the file and select 'Download'")

        try:
            with open(filename, 'w', newline='') as csvfile:
                if export_all:
                    fieldnames = ['Name', 'Timestamp', 'Location', 'Event', 'Hours']
                else:
                    fieldnames = ['Timestamp', 'Location', 'Event', 'Hours']

                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for record in records:
                    # Only write the specified fields
                    filtered_record = {k: record[k] for k in fieldnames if k in record}
                    writer.writerow(filtered_record)

            messagebox.showinfo("Success", f"{export_title} exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")

    def refresh_people_list(self):
        self.people_listbox.delete(0, tk.END)
        people = self.data_manager.get_all_people()
        for person in people:
            self.people_listbox.insert(tk.END, person)

    def on_entry_focus_in(self, event):
        """Remove placeholder text when entry gets focus"""
        if self.new_person_entry.get() == self.placeholder_text:
            self.new_person_entry.delete(0, tk.END)
            self.new_person_entry.configure(foreground='black')

    def on_entry_focus_out(self, event):
        """Add placeholder text if entry is empty and loses focus"""
        if not self.new_person_entry.get():
            self.new_person_entry.insert(0, self.placeholder_text)
            self.new_person_entry.configure(foreground='gray')

    def add_new_person(self):
        name = self.new_person_entry.get().strip()
        # Check if text is placeholder or empty
        if not name or name == self.placeholder_text:
            messagebox.showerror("Error", "Please enter a name!")
            return

        success, message = self.data_manager.add_new_person(name)
        if success:
            self.new_person_entry.delete(0, tk.END)
            # Refresh the list and select the newly added person
            self.refresh_people_list()
            
            # Find and select the newly added person in the listbox
            for i in range(self.people_listbox.size()):
                if self.people_listbox.get(i).lower() == name.lower():
                    self.people_listbox.selection_clear(0, tk.END)
                    self.people_listbox.selection_set(i)
                    self.people_listbox.see(i)
                    break
                    
            messagebox.showinfo("Success", message)
            # Hide the add person form after successful addition
            self.toggle_add_person_form()
            
            # Prompt user to add information for the new person
            if messagebox.askyesno("Add Information", f"Would you like to add information for {name} now?"):
                self.show_info_dialog(name)
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
                dialog.result['hours'],
                dialog.result['date']
            )
            if success:
                if self.entries_frame.winfo_ismapped():
                    self.display_person_info(name)
                messagebox.showinfo("Success", message)
            else:
                messagebox.showerror("Error", message)

    def verify_password(self):
        dialog = PasswordDialog(self)
        self.wait_window(dialog)
        if hasattr(dialog, 'result') and dialog.result == self.ADMIN_PASSWORD:
            return True
        return False

    # Google Sheets setup method removed

    def export_to_csv(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Export data to CSV"
        )

        if file_path:
            if self.data_manager.export_to_csv(file_path):
                messagebox.showinfo("Export Successful", f"Data exported to {file_path}")
            else:
                messagebox.showerror("Export Failed", "Failed to export data")

    def export_to_excel(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            title="Export data to Excel"
        )

        if file_path:
            if self.data_manager.export_to_excel(file_path):
                messagebox.showinfo("Export Successful", f"Data exported to {file_path}")
            else:
                messagebox.showerror("Export Failed", "Failed to export data")

    def setup_auto_excel(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            title="Select Excel file for automatic updates"
        )

        if file_path:
            success, message = self.data_manager.setup_auto_excel_export(file_path)
            if success:
                messagebox.showinfo("Auto Excel Update", 
                                   f"Auto Excel update enabled. The file {file_path} will be automatically updated whenever data changes.")
            else:
                messagebox.showerror("Auto Excel Update Failed", message)

    def import_from_csv(self):
        """Import data from CSV file"""
        try:
            # Check if admin password is correct
            if not self.verify_password():
                messagebox.showinfo("Access Denied", "Administrator password required to import data.")
                return

            # Get file path
            file_path = filedialog.askopenfilename(
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Import Data from CSV"
            )

            if not file_path:
                return

            success, message = self.data_manager.import_and_merge_entries(file_path)

            if success:
                messagebox.showinfo("Success", message)
                # Refresh the display
                self.refresh_people_list()
                if hasattr(self, 'active_person') and self.active_person:
                    self.display_person_info(self.active_person)
            else:
                messagebox.showerror("Error", message)
        except Exception as e:
            messagebox.showerror("Error", f"Import failed: {str(e)}")

    def display_person_info(self, name):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Get and display the records
        info_records = self.data_manager.get_person_info(name)
        # Sort records by name (case-insensitive)
        info_records = sorted(info_records, key=lambda x: x['Name'].lower())
        for record in info_records:
            # Format the timestamp to show only the date if it has time component
            timestamp = record['Timestamp']
            if ' ' in timestamp:  # Check if timestamp has date and time
                timestamp = timestamp.split(' ')[0]  # Get only the date part

            self.tree.insert('', 'end', values=(
                record['Name'],
                timestamp,
                record['Location'],
                record['Event'],
                record['Hours']
            ))

    def change_password(self):
        dialog = PasswordDialog(self, change_password=True)
        self.wait_window(dialog)
        if hasattr(dialog, 'result') and dialog.result:
            success, message = self.data_manager.change_password(
                dialog.result['current'],
                dialog.result['new']
            )
            if success:
                self.ADMIN_PASSWORD = dialog.result['new']
                messagebox.showinfo("Success", message)
            else:
                messagebox.showerror("Error", message)

    def display_all_entries(self):
        """Display all entries sorted by name"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Get all records and sort them by name
        all_records = self.data_manager.get_all_entries()
        all_records = sorted(all_records, key=lambda x: x['Name'].lower())

        for record in all_records:
            # Format the timestamp to show only the date if it has time component
            timestamp = record['Timestamp']
            if ' ' in timestamp:  # Check if timestamp has date and time
                timestamp = timestamp.split(' ')[0]  # Get only the date part

            self.tree.insert('', 'end', values=(
                record['Name'],
                timestamp,
                record['Location'],
                record['Event'],
                record['Hours']
            ))

    def import_entries(self):
        import csv
        filename = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not filename:
            return

        try:
            with open(filename, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    self.data_manager.add_entry(row['Name'], row['Timestamp'], row['Location'], row['Event'], row['Hours'])
            self.refresh_people_list()
            self.display_all_entries()
            messagebox.showinfo("Success", "Entries imported successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import entries: {e}")

    def delete_selected_entries(self):
        """Delete selected entries from the treeview and database"""
        # Get selected items
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showinfo("Information", "Please select entries to delete")
            return

        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Deletion", 
                                      f"Are you sure you want to delete {len(selected_items)} selected entries?")
        if not confirm:
            return

        # Clear previous deleted entries if any
        self.deleted_entries = []

        # For each selected item, get the values and delete from database
        for item_id in selected_items:
            # Get the values from the treeview
            values = self.tree.item(item_id, 'values')
            name, timestamp, location, event, hours = values

            # Store for potential undo
            self.deleted_entries.append({
                'Name': name,
                'Timestamp': timestamp,
                'Location': location,
                'Event': event,
                'Hours': hours
            })

            # Delete from database
            self.data_manager.delete_entry(name, timestamp, location, event, hours)

            # Delete from treeview
            self.tree.delete(item_id)

        # Enable undo button
        self.undo_button.configure(state="normal")

        messagebox.showinfo("Success", f"{len(selected_items)} entries deleted successfully")

    def undo_delete(self):
        """Restore previously deleted entries"""
        if not self.deleted_entries:
            messagebox.showinfo("Information", "No deleted entries to restore")
            return

        # Restore each deleted entry
        for entry in self.deleted_entries:
            # Add back to database
            self.data_manager.add_entry(
                entry['Name'],
                entry['Timestamp'],
                entry['Location'],
                entry['Event'],
                entry['Hours']
            )

            # Add back to treeview
            self.tree.insert('', 'end', values=(
                entry['Name'],
                entry['Timestamp'],
                entry['Location'],
                entry['Event'],
                entry['Hours']
            ))

        count = len(self.deleted_entries)
        self.deleted_entries = []  # Clear the deleted entries list
        self.undo_button.configure(state="disabled")  # Disable undo button

        messagebox.showinfo("Success", f"{count} entries restored successfully")

    def show_export_menu(self, event):
        """Show the export menu dropdown when export button is clicked"""
        # Get the button that was clicked
        button = event.widget

        # Calculate position for popup menu (below the button)
        x = button.winfo_rootx()
        y = button.winfo_rooty() + button.winfo_height()

        # Display the menu at calculated position
        self.export_menu.post(x, y)

    def show_import_menu(self, event):
        """Show the import menu dropdown when import button is clicked"""
        # Get the button that was clicked
        button = event.widget

        # Calculate position for popup menu (below the button)
        x = button.winfo_rootx()
        y = button.winfo_rooty() + button.winfo_height()

        # Display the menu at calculated position
        self.import_menu.post(x, y)
        
    def clean_empty_entries(self):
        """Clean entries that don't have all required fields filled"""
        # Check if admin password is correct
        if not self.verify_password():
            messagebox.showinfo("Access Denied", "Administrator password required to clean data.")
            return
            
        # Confirm before cleaning
        confirm = messagebox.askyesno(
            "Confirm Data Cleaning", 
            "This will permanently delete all entries that don't have data in all required fields (Location, Event, and Hours).\n\nAre you sure you want to continue?"
        )
        
        if not confirm:
            return
            
        # Clean the data
        success, message = self.data_manager.clean_empty_entries()
        
        if success:
            messagebox.showinfo("Success", message)
            # Refresh the display
            self.refresh_people_list()
            if self.entries_frame.winfo_ismapped():
                if hasattr(self, 'active_person') and self.active_person:
                    self.display_person_info(self.active_person)
                else:
                    self.display_all_entries()
        else:
            messagebox.showerror("Error", message)