import pandas as pd
#import requests

# Define the URL of the CSV file
url = "http://mstocktrade.in/csvdb/trade-master-fno.csv" # Replace with your actual URL

try:
    # Read the CSV file directly into a pandas DataFrame
    df = pd.read_csv(url)

    # Display the first few rows of the DataFrame
    print(df.head())
    # Iterate through each row using iterrows()
    for index, row in df.iterrows():
        # 'index' will be the row's index
        # 'row' will be a Pandas Series containing the row's data
        print(f"Row Index: {index}")
        print(f"Name: {row['ExpiryDt']}, Age: {row['CallPutType']}, City: {row['StrikePrice']}")
        #print(row) # tabulare form

except Exception as e:
    print(f"An error occurred: {e}")

 
#below should not used
# response = requests.get(url)
# html_content = response.text
# print(html_content)