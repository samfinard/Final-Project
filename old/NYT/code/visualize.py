import pandas as pd
import matplotlib.pyplot as plt

def visualize_daily():
    # Read the daily_average_SA.csv file
    daily_average_file_path = "/Users/samfinard/desktop/NYT/daily_average_SA.csv"
    daily_average_data = pd.read_csv(daily_average_file_path)

    # Convert the 'date' column to datetime type for plotting
    daily_average_data['date'] = pd.to_datetime(daily_average_data['date'])

    # Create a figure and axis objects
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot Vader scores in red
    ax.plot(daily_average_data['date'], daily_average_data['vader_SA_daily_average'], color='red', label='Vader')

    # Plot TextBlob scores in blue
    ax.plot(daily_average_data['date'], daily_average_data['textblob_SA_daily_average'], color='blue', label='TextBlob')

    # Set plot title and labels
    ax.set_title('Daily Sentiment Analysis Averages')
    ax.set_xlabel('Date')
    ax.set_ylabel('Sentiment Score')
    ax.legend()

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)

    # Display the plot
    plt.tight_layout()
    plt.show()

def visualize_weekly():
    # Read the daily_average_SA.csv file
    daily_average_file_path = "/Users/samfinard/desktop/NYT/daily_average_SA.csv"
    daily_average_data = pd.read_csv(daily_average_file_path)

    # Convert the 'date' column to datetime type
    daily_average_data['date'] = pd.to_datetime(daily_average_data['date'])

    # Set the 'date' column as the index for easier resampling
    daily_average_data.set_index('date', inplace=True)

    # Resample the data into weekly averages starting on Tuesday
    weekly_data = daily_average_data.resample('W-TUE').mean()

    # Create a figure and axis objects
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot Vader scores in red
    ax.plot(weekly_data.index, weekly_data['vader_SA_daily_average'], color='red', label='Vader')

    # Plot TextBlob scores in blue
    ax.plot(weekly_data.index, weekly_data['textblob_SA_daily_average'], color='blue', label='TextBlob')

    # Set plot title and labels
    ax.set_title('Weekly Sentiment Analysis Averages (Tuesday to Tuesday)')
    ax.set_xlabel('Date')
    ax.set_ylabel('Sentiment Score')
    ax.legend()

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)

    # Display the plot
    plt.tight_layout()
    plt.show()

def main():
    # visualize_daily()
    visualize_weekly()

if __name__ == "__main__":
    main()