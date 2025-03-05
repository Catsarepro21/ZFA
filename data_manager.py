import pandas as pd
import os
from datetime import datetime

class DataManager:
    def __init__(self):
        self.file_path = "personal_data.csv"
        self.create_file_if_not_exists()

    def create_file_if_not_exists(self):
        if not os.path.exists(self.file_path):
            # Create an empty DataFrame with the required columns
            df = pd.DataFrame(columns=['Name', 'Location', 'Event', 'Hours', 'Timestamp'])
            df.to_csv(self.file_path, index=False)

    def get_all_people(self):
        df = pd.read_csv(self.file_path)
        # Convert all names to lowercase for comparison, then use unique with case preservation
        unique_names = []
        seen_lower = set()
        
        for name in df['Name']:
            if name.lower() not in seen_lower:
                seen_lower.add(name.lower())
                unique_names.append(name)
                
        # Sort alphabetically (case-insensitive)
        return sorted(unique_names, key=lambda x: x.lower())

    def add_person_info(self, name, location, event, hours):
        try:
            df = pd.read_csv(self.file_path)
            
            # Check if name exists (case-insensitive), use the original case if found
            matching_names = df[df['Name'].str.lower() == name.lower()]['Name'].unique()
            if len(matching_names) > 0:
                # Use the first instance we found to maintain case consistency
                name_to_use = matching_names[0]
            else:
                name_to_use = name
                
            new_data = {
                'Name': [name_to_use],
                'Location': [location],
                'Event': [event],
                'Hours': [hours],
                'Timestamp': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
            }
            df = pd.concat([df, pd.DataFrame(new_data)], ignore_index=True)
            df.to_csv(self.file_path, index=False)
            return True, "Information added successfully!"
        except Exception as e:
            return False, f"Error saving data: {str(e)}"

    def get_person_info(self, name):
        df = pd.read_csv(self.file_path)
        # Case-insensitive match
        person_data = df[df['Name'].str.lower() == name.lower()]
        return person_data.to_dict('records')

    def add_new_person(self, name):
        if not name.strip():
            return False, "Name cannot be empty!"

        df = pd.read_csv(self.file_path)
        # Case-insensitive check for duplicates
        if any(existing_name.lower() == name.lower() for existing_name in df['Name'].unique()):
            return False, "Person already exists (name is case-insensitive)!"

        # Add the person with initial empty information
        new_data = {
            'Name': [name],
            'Location': [''],
            'Event': [''],
            'Hours': [''],
            'Timestamp': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        }
        df = pd.concat([df, pd.DataFrame(new_data)], ignore_index=True)
        df.to_csv(self.file_path, index=False)
        return True, "Person added successfully!"
        
    def get_all_entries(self):
        """Get all entries in the database"""
        df = pd.read_csv(self.file_path)
        return df.to_dict('records')