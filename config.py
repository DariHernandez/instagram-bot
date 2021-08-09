import os
import json

current_file = os.path.basename(__file__)
current_folder = os.path.dirname(__file__)  
config_path = os.path.join(current_folder, "config.json")

def get_credential (credential=""): 
    """
    Get specific credential from config file
    """
    
    config_exist = os.path.isfile(config_path)
    if not config_exist: 
        return None
    
    with open (config_path, "r") as config_file: 
        try:
            config_data = json.loads(config_file.read())
            return (config_data[credential])
        except: 
            return ""

def create_config (credentials): 
    """
    Create a config file with default credentials
    """
    
    with open (config_path, "a") as config_file:
        config_file.write(json.dumps(credentials))
        

def update_credential (credential="", value=""): 
    """
    Update specific credential in config file
    """
    
    with open (config_path, "r") as config_file: 
        config_data = json.loads(config_file.read())
        config_data[credential] = value
    
    with open (config_path, "w") as config_file:
        config_file.write(json.dumps(config_data))

def update_credentials (credentials, values): 
    """
    Update credentials
    """
    
    for cred_config, cred_gui in credentials.items(): 
        
        new_credential = values[cred_gui]
        update_credential (cred_config, new_credential)