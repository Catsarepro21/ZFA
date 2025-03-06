import pandas as pd
import csv
import json
import os
import datetime
import time
import traceback

class DataManager:
    def __init__(self):
        self.file_path = "personal_data.csv"
        self.use_google_sheets = False # Removed sheets_manager
        self.excel_file_path = None

        # Try to load Excel configuration
        if os.path.exists('excel_config.json'):
            try:
                with open('excel_config.json', 'r') as f:
                    config = json.load(f)
                    if 'excel_file_path' in config:
                        self.excel_file_path = config['excel_file_path']
                        print(f"Excel auto-update configured for: {self.excel_file_path}")
            except Exception as e:
                print(f"Failed to load Excel configuration: {str(e)}")

        # Always ensure the local file exists as a fallback
        self.create_file_if_not_exists()

    def create_file_if_not_exists(self):
        if not os.path.exists(self.file_path):
            # Create an empty DataFrame with the required columns
            df = pd.DataFrame(columns=['Name', 'Location', 'Event', 'Hours', 'Timestamp'])
            df.to_csv(self.file_path, index=False)
        else:
            # Ensure file has correct columns
            df = pd.read_csv(self.file_path)
            required_columns = ['Name', 'Location', 'Event', 'Hours', 'Timestamp']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                # Fix missing columns
                for col in missing_columns:
                    df[col] = ""
                df.to_csv(self.file_path, index=False)

    def get_all_people(self):
        # Removed Google Sheets logic
        # Use local file
        df = pd.read_csv(self.file_path)
        
        # Check if dataframe is empty or 'Name' column doesn't exist
        if df.empty or 'Name' not in df.columns:
            return []
            
        # Convert all names to lowercase for comparison, then use unique with case preservation
        unique_names = []
        seen_lower = set()

        for name in df['Name']:
            # Skip NaN or non-string values
            if not isinstance(name, str) or not name.strip():
                continue
                
            if name.lower() not in seen_lower:
                seen_lower.add(name.lower())
                unique_names.append(name)

        # Sort alphabetically (case-insensitive)
        return sorted(unique_names, key=lambda x: x.lower())

    def add_person_info(self, name, location, event, hours, date=None):
        # Removed Google Sheets logic
        # Use local file
        try:
            # Skip if all meaningful fields are empty
            if not location and not event and not hours:
                return False, "No information to add - all fields are empty"
                
            df = pd.read_csv(self.file_path)

            # Check if name exists (case-insensitive), use the original case if found
            matching_names = df[df['Name'].str.lower() == name.lower()]['Name'].unique()
            if len(matching_names) > 0:
                # Use the first instance we found to maintain case consistency
                name_to_use = matching_names[0]
            else:
                name_to_use = name

            # Generate timestamp - if date is provided, use it as the date part
            if date and date.strip():
                try:
                    # Parse the provided date
                    date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
                    # Use only the date portion without time
                    timestamp = date_obj.strftime("%Y-%m-%d")
                except ValueError:
                    # If date parsing fails, use current datetime
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
            else:
                # Use current date only (no time) if no date provided
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d")

            # Only proceed if there's actual data to add
            if (location and location.strip()) or (event and event.strip()) or (hours and hours.strip()):
                # First, check if there are any empty entries (placeholders) for this person that we can reuse
                empty_entries_mask = (
                    (df['Name'].str.lower() == name.lower()) & 
                    (df['Location'].fillna('') == '') & 
                    (df['Event'].fillna('') == '') & 
                    (df['Hours'].fillna('') == '')
                )
                
                # If there's an empty entry, update the first one instead of adding a new row
                if empty_entries_mask.any():
                    # Get the index of the first empty entry
                    first_empty_idx = df.index[empty_entries_mask].tolist()[0]
                    
                    # Update this row
                    df.at[first_empty_idx, 'Location'] = str(location) if location else ''
                    df.at[first_empty_idx, 'Event'] = str(event) if event else ''
                    df.at[first_empty_idx, 'Hours'] = str(hours) if hours else ''
                    df.at[first_empty_idx, 'Timestamp'] = str(timestamp)
                else:
                    # No empty entries, add a new row
                    new_data = {
                        'Name': [str(name_to_use)],
                        'Location': [str(location) if location else ''],
                        'Event': [str(event) if event else ''],
                        'Hours': [str(hours) if hours else ''],
                        'Timestamp': [str(timestamp)]
                    }
                    df = pd.concat([df, pd.DataFrame(new_data)], ignore_index=True)
                
                df.to_csv(self.file_path, index=False)
                self.update_excel()
                return True, "Information added successfully!"
            else:
                return False, "No information to add - all fields are empty"
        except Exception as e:
            return False, f"Error saving data: {str(e)}"

    def get_person_info(self, name):
        # Removed Google Sheets logic
        # Use local file
        df = pd.read_csv(self.file_path)
        # Case-insensitive match
        person_data = df[df['Name'].str.lower() == name.lower()]
        
        # Convert NaN values to empty strings
        records = person_data.fillna('').to_dict('records')
        return records

    def add_new_person(self, name):
        if not name.strip():
            return False, "Name cannot be empty!"

        # Removed Google Sheets logic
        # Use local file
        df = pd.read_csv(self.file_path)
        # Case-insensitive check for duplicates
        if any(existing_name.lower() == name.lower() for existing_name in df['Name'].unique()):
            return False, "Person already exists (name is case-insensitive)!"

        # Add the person with an initial entry to make sure they appear in the list
        # But don't add a timestamp yet - this will be added when actual data is entered
        timestamp = ""  # Empty timestamp until actual data is added
        new_data = {
            'Name': [name],
            'Location': [''],
            'Event': [''],
            'Hours': [''],
            'Timestamp': [timestamp]
        }
        df = pd.concat([df, pd.DataFrame(new_data)], ignore_index=True)
        df.to_csv(self.file_path, index=False)
        self.update_excel()
        
        return True, "Person added successfully!"

    def get_all_entries(self):
        # Removed Google Sheets logic
        # Use local file
        df = pd.read_csv(self.file_path)
        # Convert NaN values to empty strings
        return df.fillna('').to_dict('records')

    def import_and_merge_entries(self, import_file_path):
        # Removed Google Sheets logic
        # Use local file
        try:
            # Check if the import file exists
            if not os.path.exists(import_file_path):
                return False, "Import file not found!"

            # Read the current data and the import data
            current_df = pd.read_csv(self.file_path)
            import_df = pd.read_csv(import_file_path)

            # Ensure the import file has the required columns
            required_columns = ['Name', 'Location', 'Event', 'Hours', 'Timestamp']
            missing_columns = [col for col in required_columns if col not in import_df.columns]
            if missing_columns:
                return False, f"Import file is missing required columns: {', '.join(missing_columns)}"

            # Merge the dataframes
            merged_df = pd.concat([current_df, import_df], ignore_index=True)

            # Remove exact duplicates
            merged_df = merged_df.drop_duplicates()

            # Save the merged data
            merged_df.to_csv(self.file_path, index=False)
            self.update_excel()
            return True, f"Successfully imported {len(import_df)} entries. After removing duplicates, database now has {len(merged_df)} entries."
        except Exception as e:
            return False, f"Error importing data: {str(e)}"

    def delete_entry(self, name, timestamp, location, event, hours):
        # Removed Google Sheets logic
        # Use local file
        try:
            df = pd.read_csv(self.file_path)

            # Create a mask for the exact entry to delete
            mask = (
                (df['Name'] == name) & 
                (df['Timestamp'] == timestamp) & 
                (df['Location'] == location) & 
                (df['Event'] == event) & 
                (df['Hours'] == hours)
            )

            # Delete the matching row(s)
            df = df[~mask]

            # Save the updated dataframe
            df.to_csv(self.file_path, index=False)
            self.update_excel()
            return True
        except Exception as e:
            print(f"Error deleting entry: {str(e)}")
            return False

    def add_entry(self, name, timestamp, location, event, hours):
        # Removed Google Sheets logic
        # Use local file
        try:
            df = pd.read_csv(self.file_path)

            new_data = {
                'Name': [name],
                'Location': [location],
                'Event': [event],
                'Hours': [hours],
                'Timestamp': [timestamp]
            }

            df = pd.concat([df, pd.DataFrame(new_data)], ignore_index=True)
            df.to_csv(self.file_path, index=False)
            self.update_excel()
            return True
        except Exception as e:
            print(f"Error adding entry: {str(e)}")
            return False

    def get_password(self):
        """Get the saved admin password or return default if not set"""
        password_file = "admin_password.txt"
        default_password = "admin123"

        if not os.path.exists(password_file):
            # Create password file with default password
            with open(password_file, 'w') as f:
                f.write(default_password)
            return default_password

        # Read password from file
        try:
            with open(password_file, 'r') as f:
                password = f.read().strip()
                return password if password else default_password
        except:
            return default_password

    def change_password(self, current_password, new_password):
        """Change the admin password"""
        saved_password = self.get_password()

        if current_password != saved_password:
            return False, "Current password is incorrect"

        try:
            with open("admin_password.txt", 'w') as f:
                f.write(new_password)
            return True, "Password changed successfully"
        except Exception as e:
            return False, f"Error changing password: {str(e)}"

    def export_to_csv(self, file_path):
        # Removed Google Sheets logic
        # Use local file - just copy the file
        try:
            df = pd.read_csv(self.file_path)
            df.to_csv(file_path, index=False)
            return True
        except Exception as e:
            print(f"Error exporting to CSV: {str(e)}")
            return False

    def update_excel(self):
        # Update Excel file if configured
        if hasattr(self, 'excel_file_path') and self.excel_file_path:
            try:
                # Read all data
                df = pd.read_csv(self.file_path)
                
                # Fill NaN values with empty strings
                df = df.fillna('')
                
                # Create a Pandas Excel writer using openpyxl as the engine
                with pd.ExcelWriter(self.excel_file_path, engine='openpyxl') as writer:
                    # First create the main sheet with all data
                    df.to_excel(writer, sheet_name='All Data', index=False)
                    
                    # Get all unique people with proper case preservation
                    unique_names = []
                    seen_lower = set()
                    
                    for name in df['Name']:
                        if isinstance(name, str) and name.strip() and name.lower() not in seen_lower:
                            seen_lower.add(name.lower())
                            unique_names.append(name)
                    
                    # Create separate sheets for each person
                    for person in unique_names:
                        # Get person's data (case-insensitive match)
                        person_df = df[df['Name'].str.lower() == person.lower()]
                        
                        if len(person_df) == 0:
                            continue  # Skip if no data for this person
                        
                        # Create sheet name (limit to 31 chars which is Excel's max length)
                        # Replace invalid sheet name characters with underscore
                        invalid_chars = [':', '\\', '/', '?', '*', '[', ']']
                        sheet_name = str(person)[:31]
                        for char in invalid_chars:
                            sheet_name = sheet_name.replace(char, '_')
                        
                        if not sheet_name:
                            continue  # Skip empty sheet names
                        
                        # Write to Excel with index=False
                        person_df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                print(f"Excel file updated with separate sheets: {self.excel_file_path}")
            except Exception as e:
                print(f"Error updating Excel file: {str(e)}")
                import traceback
                traceback_info = traceback.format_exc()
                print(traceback_info)

    def setup_auto_excel_export(self, excel_file_path):
        """Configure automatic Excel export to a specified file."""
        try:
            # Store the Excel file path
            self.excel_file_path = excel_file_path

            # Create Excel file if it doesn't exist or update it if it does
            df = pd.read_csv(self.file_path)
            df.to_excel(excel_file_path, index=False, engine='openpyxl')

            # Save the configuration to a file
            with open('excel_config.json', 'w') as f:
                json.dump({'excel_file_path': excel_file_path}, f)

            return True, "Auto Excel update configured successfully!"
        except Exception as e:
            return False, f"Error configuring Excel auto-update: {str(e)}"

    def clean_empty_entries(self):
        """Delete entries that have empty columns (Location, Event, and Hours)."""
        try:
            df = pd.read_csv(self.file_path)
            
            # Count rows before cleaning
            total_rows_before = len(df)
            
            # Find rows where all three main data columns are empty
            empty_mask = (
                (df['Location'].fillna('') == '') & 
                (df['Event'].fillna('') == '') & 
                (df['Hours'].fillna('') == '')
            )
            
            # Count empty rows
            empty_rows_count = empty_mask.sum()
            
            # Keep only rows that are not empty
            df = df[~empty_mask]
            
            # Save the updated dataframe
            df.to_csv(self.file_path, index=False)
            self.update_excel()
            
            return True, f"Deleted {empty_rows_count} entries because not all required fields were filled."
        except Exception as e:
            print(f"Error cleaning empty entries: {str(e)}")
            return False, f"Error cleaning empty entries: {str(e)}"
            
    def export_to_excel(self, file_path):
        """Export data to Excel file with separate sheets for each person."""
        try:
            # Read all data
            df = pd.read_csv(self.file_path)
            
            # Fill NaN values with empty strings
            df = df.fillna('')
            
            # Create a Pandas Excel writer using openpyxl as the engine
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                # First create the main sheet with all data
                df.to_excel(writer, sheet_name='All Data', index=False)
                
                # Get all unique people with proper case preservation
                unique_names = []
                seen_lower = set()
                
                for name in df['Name']:
                    if isinstance(name, str) and name.strip() and name.lower() not in seen_lower:
                        seen_lower.add(name.lower())
                        unique_names.append(name)
                
                # Create separate sheets for each person
                for person in unique_names:
                    # Get person's data (case-insensitive match)
                    person_df = df[df['Name'].str.lower() == person.lower()]
                    
                    if len(person_df) == 0:
                        continue  # Skip if no data for this person
                    
                    # Create sheet name (limit to 31 chars which is Excel's max length)
                    # Replace invalid sheet name characters with underscore
                    invalid_chars = [':', '\\', '/', '?', '*', '[', ']']
                    sheet_name = str(person)[:31]
                    for char in invalid_chars:
                        sheet_name = sheet_name.replace(char, '_')
                    
                    if not sheet_name:
                        continue  # Skip empty sheet names
                    
                    # Write to Excel
                    person_df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            print(f"Excel export completed successfully to {file_path}")
            return True
        except Exception as e:
            print(f"Error exporting to Excel: {str(e)}")
            traceback_info = traceback.format_exc()
            print(traceback_info)
            return False