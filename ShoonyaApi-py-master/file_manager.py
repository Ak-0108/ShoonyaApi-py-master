
import yaml

class MyConfigReader:
 def __init__(self):
        try:
         with open('myconfig.yml', 'r') as f:
            config_value = yaml.safe_load(f)
            self.root_folder=config_value['mainfolder']
            self.root_web_folder=config_value['webfolder']
            self.api_key=config_value['apikey']
            self.option_file=self.root_folder+ "\\trade-master-fno.csv"
            self.stock_file= self.root_folder+ "\\trade-master-stock.csv"
        except FileNotFoundError:
         print("Error: config.yaml not found.")
         exit()
        except yaml.YAMLError as e:
         print(f"Error: Invalid YAML format in config.yaml: {e}")
        
def get_root_folder(self):
   return self.root_folder
 
def get_api_key(self):
   return self.api_key



# Read the YAML file
# def get_config_row():
#     try:
#         with open('myconfig.yml', 'r') as f:
#             config_data = yaml.safe_load(f)
#             return config_data
#     except FileNotFoundError:
#         print("Error: config.yaml not found.")
#         exit()
#     except yaml.YAMLError as e:
#         print(f"Error: Invalid YAML format in config.yaml: {e}")


# Access values
