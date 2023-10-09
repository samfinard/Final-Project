import os
import pandas as pd


# def getMasterDataset(root_file_path):
#     # Set the path to the folder containing your CSV files
#     folder_path = f"{root_file_path}/articles"

#     # Get a list of all CSV files in the folder
#     csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

#     # Initialize an empty list to store DataFrames of each CSV
#     data_frames = []

#     # Loop through each CSV file and read its content into a DataFrame
#     for file in csv_files:
#         file_path = os.path.join(folder_path, file)
#         data = pd.read_csv(file_path)
#         data_frames.append(data)

#     # Concatenate all DataFrames into one
#     combined_data = pd.concat(data_frames, ignore_index=True)

#     # Save the combined data to a new CSV file
#     output_file_path = f"{root_file_path}/combined_data.csv"
#     combined_data.to_csv(output_file_path, index=False)

#     print("Files combined successfully!")

def getMasterDataset(root_file_path):
    # Get a list of all CSV files in the folder
    csv_files = [file for file in os.listdir(root_file_path) if file.endswith('.csv')]

    # Initialize an empty list to store DataFrames of each CSV
    data_frames = []

    # New Comment.

    # Loop through each CSV file and read its content into a DataFrame
    for file in csv_files:
        file_path = os.path.join(root_file_path, file)
        df = pd.read_csv(file_path)
        data_frames.append(df)

    # Concatenate all DataFrames into one
    combined_data = pd.concat(data_frames, ignore_index=True)

    # Save the combined data to a new CSV file
    output_file_path = "combined_data.csv"
    combined_data.to_csv(output_file_path, index=False)

    print("Files combined successfully!")

def getDailyAverages(root_file_path):
    # Read the master CSV file (combined_data.csv)
    master_file_path = f"f{root_file_path}/combined_data.csv"
    master_data = pd.read_csv(master_file_path)

    # Convert the 'date' column to datetime type for easier manipulation
    master_data['date'] = pd.to_datetime(master_data['date'])

    # Calculate the daily average for 'vader_SA' and 'textblob_SA'
    daily_average_data = master_data.groupby('date').agg({
        'vader_SA': 'mean',
        'textblob_SA': 'mean'
    }).reset_index()

    # Rename the columns
    daily_average_data.columns = ['date', 'vader_SA_daily_average', 'textblob_SA_daily_average']

    # Save the daily average data to a new CSV file
    output_file_path = f"{root_file_path}/daily_average_SA.csv"
    daily_average_data.to_csv(output_file_path, index=False)

    print("Daily average data computed and saved successfully!")

def combineWithDJIA(root_file_path):
    # Read the daily_average_SA.csv file
    daily_average_file_path = f"{root_file_path}/daily_average_SA.csv"
    daily_average_data = pd.read_csv(daily_average_file_path)

    # Convert the 'date' column to datetime type for easier manipulation
    daily_average_data['date'] = pd.to_datetime(daily_average_data['date'])

    # Read the HistoricalPrices.csv file
    historical_prices_file_path = f"{root_file_path}/HistoricalPrices.csv"
    historical_prices_data = pd.read_csv(historical_prices_file_path)

    # Convert the 'Date' column in HistoricalPrices.csv to datetime type for merging
    historical_prices_data['Date'] = pd.to_datetime(historical_prices_data['Date'])

    # Merge daily_average_data and historical_prices_data based on the 'date' column (left merge)
    combined_data = pd.merge(daily_average_data, historical_prices_data[['Date', ' Close']], left_on='date', right_on='Date', how='left')

    # Drop the duplicated 'Date' column from the merge
    combined_data.drop('Date', axis=1, inplace=True)

    # Save the combined data to a new CSV file
    output_file_path = f"{root_file_path}/SA_DJIA_combined.csv"
    combined_data.to_csv(output_file_path, index=False)

    print("Files combined successfully!")

def makeSample(root_file_path):
    df = pd.read_csv(root_file_path)
    df['date'] = pd.to_datetime(df['date'])

    sample_df = df.groupby(df['date'].dt.time, group_keys = False).apply(lambda x: x.sample(10))
    sample_df.reset_index(drop=True, inplace=True)
    sample_df.to_csv("sample.csv", index=False)
def main(): 
    # root_file_path = "../data/articles"
    root_file_path = "articles"
    # print(len(pd.read_csv(root_file_path + "/combined_data.csv")))
    getMasterDataset(root_file_path)
    # getDailyAverages(root_file_path)
    
    # combineWithDJIA(root_file_path)
   
    # DJIA_file_path = f"{root_file_path}/SA_DJIA_combined.csv"
    # DJIA_df = pd.read_csv(DJIA_file_path)
    # new_column_names = {'textblob_SA_daily': 'NYT_textblob_daily'}
    # DJIA_df.rename(columns=new_column_names, inplace=True)
    # DJIA_df.to_csv(DJIA_file_path, index=False)
    # print(DJIA_df.columns.tolist())

    # root_file_path = "../data/NYTarticles_all.csv"
    # makeSample(root_file_path)

if __name__ == "__main__":
    main()
