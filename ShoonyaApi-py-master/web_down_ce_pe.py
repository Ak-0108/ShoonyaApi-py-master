import time
import datetime
from file_manager import MyConfigReader
import web_reader
import os
import csv_manager
import order1


os.system(f'title DownLoad_CE_PE')
objConfig=MyConfigReader()
root_folder=objConfig.root_web_folder
web_url="http://mstocktrade.in/api/"
nifty_breakout_data=web_url+"nifty_breakout.php" 
 
db_buy_file= root_folder+ "diary_buy.csv" #created based on admin setting
db_sell_file= root_folder + 'diary_sell.csv'   #created based on admin settingbuy

download_ce_url=web_url+"trade_diary_buy.php"
download_pe_url=web_url+"trade_diary_sale.php"

# Run with arguments
       #subprocess.run(["python", "script_to_run.py", "arg1", "arg2"])
       #print(f"Running script_to_run.py with arguments: {sys.argv[1:]}")

def countdown():  
     fl_download=False
     while v_counter<3:
        #Actual function is here    
         #os.system('cls')
           #CE or PE to be entered by admin 
          lst_call=web_reader.readweb_ce(download_ce_url,db_buy_file)  

          for objY2 in lst_call:
          #if check_add_order(objY.name,objY.buy,lstOrder)==False:
           if check_add_order(1,objY2.mobile)==False:         
                    data_insert= order1.MyClass() 
                 
                    activeOrderId=data_insert.place_NSE_Option_Order(objY2.name,objY2.buy,objY2.quantity) 
                    csv_data=[1,1,objY2.stop,objY2.mobile]
                    csv_manager.write_call_put_csv(csv_data)

         #Sell Nifty  
          lst_put=web_reader.readweb_pe(download_pe_url,db_sell_file) 
          for objY1 in lst_put:
          #if check_add_order(objY.name,objY.buy,lstOrder)==False:
           if check_add_order(2,objY1.mobile)==False:         
                    data_insert= order1.MyClass() 
                 
                    activeOrderId=data_insert.place_NSE_Option_Order(objY2.name,objY2.buy,objY2.quantity) 
                    csv_data1=[2,1,objY1.stop,objY1.mobile]
                    csv_manager.write_call_put_csv(csv_data1)


        #wait for 10 second
          time.sleep(10)
          curr_time=curr_date.now().time()
          print("Download completed: "+str(curr_time))
     

     print("Place Enter to Close!")


  

curr_date=datetime.datetime.now()
v_counter=0 

#order to be place only once
def check_add_order(ce_pe_type,mobile):
   found = False
   myList=csv_manager.read_call_put_csv()
   for item in myList:
       if item.mobile==mobile and item.cepe_type==ce_pe_type:
           found = True
           break
   return found

def check_sale_order(ce_pe_type,mobile):
   found = False
   myList=csv_manager.read_call_put_csv()
   for item in myList:
       if item.mobile==mobile and item.cepe_type==ce_pe_type and item.stop==1:
           found = True
           break
   return found
  
countdown()
