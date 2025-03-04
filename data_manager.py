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
            df = pd.DataFrame(columns=['Name', 'Information', 'Timestamp'])
            df.to_csv(self.file_path, index=False)
    
    def get_all_people(self):
        df = pd.read_csv(self.file_path)
        return sorted(df['Name'].unique())
    
    def add_person_info(self, name, information):
        try:
            df = pd.read_csv(self.file_path)
            new_data = {
                'Name': [name],
                'Information': [information],
                'Timestamp': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
            }
            df = pd.concat([df, pd.DataFrame(new_data)], ignore_index=True)
            df.to_csv(self.file_path, index=False)
            return True, "Information added successfully!"
        except Exception as e:
            return False, f"Error saving data: {str(e)}"
    
    def get_person_info(self, name):
        df = pd.read_csv(self.file_path)
        person_data = df[df['Name'] == name]
        return person_data.to_dict('records')
    
    def add_new_person(self, name):
        if not name.strip():
            return False, "Name cannot be empty!"
        
        df = pd.read_csv(self.file_path)
        if name in df['Name'].unique():
            return False, "Person already exists!"
            
        # Add the person with an initial empty information
        new_data = {
            'Name': [name],
            'Information': ['Initial entry'],
            'Timestamp': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        }
        df = pd.concat([df, pd.DataFrame(new_data)], ignore_index=True)
        df.to_csv(self.file_path, index=False)
        return True, "Person added successfully!"
