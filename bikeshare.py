import time
import pandas as pd
import numpy as np

CITY_DATA = { 
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv' 
}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Get user input for city
    while True:
        city = input("Would you like to see data for Chicago, New York City, or Washington?\n").strip().lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid input. Please choose from Chicago, New York City, or Washington.")

    # Get user input for filter type
    while True:
        filter_type = input("Would you like to filter the data by month, day, or not at all? Type 'none' for no filter.\n").strip().lower()
        if filter_type in ['month', 'day', 'none']:
            break
        else:
            print("Invalid input. Please choose 'month', 'day', or 'none'.")

    month = 'all'
    day = 'all'

    # If filtering by month
    if filter_type == 'month':
        while True:
            month = input("Which month - January, February, March, April, May, or June?\n").strip().lower()
            if month in ['january', 'february', 'march', 'april', 'may', 'june']:
                break
            else:
                print("Invalid input. Please choose a valid month.")

    # If filtering by day
    if filter_type == 'day':
        while True:
            day = input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n").strip().lower()
            if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                break
            else:
                print("Invalid input. Please choose a valid day.")

    print('-' * 40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()

    # Filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    # Filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df

def display_raw_data(df):
    """
    Prompts the user to display raw data 5 rows at a time.
    """
    start_row = 0
    while True:
        show_data = input("Would you like to see raw data? Enter yes or no.\n").strip().lower()
        if show_data == 'yes':
            print(df.iloc[start_row:start_row + 5])
            start_row += 5
        elif show_data == 'no':
            break
        else:
            print("Invalid input. Please type 'yes' or 'no'.")

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    common_month = df['month'].mode()[0]
    print(f"Most Common Month: {common_month}")

    # Display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print(f"Most Common Day of Week: {common_day.title()}")

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print(f"Most Common Start Hour: {common_hour}")

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)

# Similar statistical functions go here for station_stats, trip_duration_stats, and user_stats.

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_raw_data(df)

        time_stats(df)
        # Additional statistics calls like station_stats(df), trip_duration_stats(df), user_stats(df) go here.

        # Export option
        export = input("\nWould you like to save the filtered data to a CSV file? Enter yes or no.\n").strip().lower()
        if export == 'yes':
            file_name = f"{city}_filtered_data.csv"
            df.to_csv(file_name, index=False)
            print(f"\nFiltered data has been successfully saved to {file_name}.\n")

        restart = input('\nWould you like to restart? Enter yes or no.\n').strip().lower()
        if restart != 'yes':
            break

if __name__ == "__main__":
    main()
