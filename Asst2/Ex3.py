# Read in a csv file an create a dataframe. Print some info.
import pandas as pd
import numpy as np
import pyarrow
import time

# Comments below display a temporarily fix a certificate error using ssl, do not use in production.
# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context

pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', '{:.2f}'.format)


def load_csv(file_path):
    print(f"Reading csv file from {file_path}...")
    start_time = time.time()

    try:
        df = pd.read_csv(file_path, engine="pyarrow")
        end_time = time.time()
        load_time = end_time - start_time
        print(f"CSV file loaded successfully in {load_time:.2f} seconds.")
        print(f"Number of rows: {len(df)}")
        print(f"Columns: {df.columns.tolist()}")

        df['order_date'] = pd.to_datetime(df['order_date'], format = '%m/%d/%y', errors='coerce')
        df.fillna(0, inplace=True)

        df['sales'] = df['quantity'] * df['unit_price']
        required_columns = ['quantity', 'unit_price', 'order_date']
        # Check if required columns are in df
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"Warning: Missing required columns: {missing_columns}")
        else:
            print("All required columns are present.")
        return df
        
    except FileNotFoundError as e:
        print(f"Error: The file {file_path} was not found. {e}")

    except pd.errors.EmptyDataError as e:
        print(f"Error: The file {file_path} is empty. {e}")
        return None
    
    except pd.errors.ParserError as e:
        print(f"Error: There was an error parsing CSV file {file_path}: {e}")
        return None
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def display_rows(dataframe):
    while(True):
        print("\nEnter the number of rows to display")
        print(f" - Enter a number 1 to {len(dataframe)}")
        print(" - To see all rows, enter 'all'")
        print(" - To skip preview, press Enter")
        user_input = input("Your choice: ").strip().lower()

        if user_input == '':
            print("Skipping preview.")
            break
        elif user_input == 'all':
            print("Displaying all rows:")
            print(dataframe)
            break
        elif user_input.isdigit() and 1 <= int(user_input) < len(dataframe):
            num_rows = int(user_input)
            print(f"Displaying first {num_rows} rows:")
            print(dataframe.head(num_rows))
            break
        else:
            print("Invalid input. Please try again.")


url = "https://drive.google.com/uc?id=1ujY0WCcePdotG2xdbLyeECFW9lCJ4t-K"
sales_data = load_csv(url)

def main():
    # Main program loop
    while True:
        display_rows(sales_data)

if __name__ == "__main__":
    main()
