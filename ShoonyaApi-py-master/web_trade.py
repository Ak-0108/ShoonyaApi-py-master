import time
import datetime
from file_manager import MyConfigReader
import web_reader
import os
import subprocess


os.system(f'title Downloading_Trade')
objConfig=MyConfigReader()
root_folder=objConfig.root_web_folder
web_url="http://mstocktrade.in/api/"
nifty_breakout_data=web_url+"nifty_breakout.php" 
 
db_option_file= root_folder+ "trade-master-fno.csv" #created based on admin setting
db_stocks_file= root_folder + 'trade-master-stock.csv'   #created based on admin setting

# Run with arguments
       #subprocess.run(["python", "script_to_run.py", "arg1", "arg2"])
       #print(f"Running script_to_run.py with arguments: {sys.argv[1:]}")

def countdown():  
     fl_download=False
     while v_counter<3:
        #Actual function is here    
         #os.system('cls')
           #CE or PE to be entered by admin 
          lst_options=web_reader.readweb_options(web_url,db_option_file)  

         #Trade Stock Only   
          lst_stocks=web_reader.readweb_stocks(web_url,db_stocks_file) 
          # if fl_download==False:
          #      fl_download=True
          #      subprocess.run(["python", "web_run_trade.py"]) 

        #wait for 10 second
          time.sleep(10)
          curr_time=curr_date.now().time()
          print("Download completed: "+str(curr_time))
     

     print("Place Enter to Close!")


  

curr_date=datetime.datetime.now()
v_counter=0 
  
countdown()
