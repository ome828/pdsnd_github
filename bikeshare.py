import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # create lists for all the valid inputs
    cities = ('chicago', 'new york city', 'washington')
    filters = ('none', 'month', 'day')
    months = ('all', 'january', 'february', 'march', 'april', 'may', 'june')
    day_of_week = ('all','sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday')
    while True:
        city = input("\nWould you like to see data for Chicago, New York City or Washington?\n")
        city = city.lower()
        if city not in cities:
            print("You've entered an invalid city. Try again.")
            continue
        else:
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input("\nWhich month? January, February, March, April, May or June? Or type all for no filter on month. \n")
        month = month.lower()
        if month not in months:
            print("You've entered an invalid month. Try again.")
            continue
        else:
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\nWhich day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? If no preference, type 'all.' \n")
        day = day.lower()
        if day not in day_of_week:
            print("Invalid input for day of the week. Try again.")
            continue
        else:
            break
    print('-'*40)
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
    #loading in city info first
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.day_name()
    
    #Change name of 'Unnamed: 0' column to 'Unique Identifier'
    df.rename(columns = {'Unnamed: 0': 'Unique Identifier'}, inplace = True)

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['Month'] == month]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['Day of Week'] == day.title()]                                   
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # TO DO: display the most common month
    common_month = df['Month'].value_counts().nlargest(1).index[0]
    print(f"Most popular month is: {common_month}.")

    # TO DO: display the most common day of week
    common_day = df['Day of Week'].value_counts().nlargest(1).index[0]
    print(f"Most popular day is: {common_day}.")
    # TO DO: display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    common_hour = df['Hour'].value_counts().nlargest(1).index[0]
    print(f"Most popular hour is: {common_hour}.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station = df['Start Station'].value_counts().nlargest(1).index[0]
    print(f"Most common start station: {start_station}.")

    # TO DO: display most commonly used end station
    end_station = df['End Station'].value_counts().nlargest(1).index[0]
    print(f"Most common end station: {end_station}.")

    # TO DO: display most frequent combination of start station and end station trip
    # adding [0] because groupby.size.idxmax returns a tuple, which has '' & parantheses around output
    common_combo = df.groupby(['Start Station', 'End Station']).size().idxmax()[0]
    print(f"Most common start-end station combo: {common_combo}.")
    print(df.keys())
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = round(df['Trip Duration'].sum() / 86400, 2)
    print(f"Total travel time: {total_travel_time} days.")

    # TO DO: display mean travel time (of a trip)
    mean_travel_time = round(df['Trip Duration'].mean() / 60, 2)
    print(f"Mean travel time: {mean_travel_time} minutes.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    users = df['User Type'].value_counts()
    print(f"The types of users are: \n{users.to_string()}\n")

    # TO DO: Display counts of gender
    # Washington doesn't have gender info but New York City does so use try/except clause
    try:
        gender_info = df['Gender'].value_counts()
        print(f"Gender info is as follows: \n{gender_info.to_string()}\n")
    except KeyError:
        print("No gender information for requested trip.\n")

    # TO DO: Display earliest birth year
    try:
        oldest_traveler = df['Birth Year'].min()
        print(f"Earliest birth year on record: {int(oldest_traveler)}\n")
    except KeyError:
        print("No information on oldest Birth Year available.\n")
    
    # TO DO: Display most recent birth year
    try:
        youngest_traveler = df['Birth Year'].max()
        print(f"Most recent birth year on record: {int(youngest_traveler)}\n")
    except KeyError:
        print("No information on youngest Birth Year available.\n")
        
    # TO DO: Display the most common birth year
    try:
        common_birth_year = df['Birth Year'].value_counts().nlargest(1).index[0]
        print(f"Most common birth year: {int(common_birth_year)}\n")
    except KeyError:
        print("No information on most common Birth Year available.\n")
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
  
def print_raw_data(df):
    '''
    Get a yes/no input from user and print lines of the df based on input. Start printing from line 1
    and increment in sections of 5.
    '''
    counter = 0
    while True:
        want_input = input("Would you like to see raw data from the database? ")
        if want_input.lower() == 'yes' or want_input.lower() == 'no':
            if want_input.lower() == 'yes':
                print(df[counter:counter+5])
                counter +=5
            else:
                print("Understood! You would not like to see (anymore) raw data.")
                break
        else:
            print("Invalid input. Please respond with a 'yes' or 'no'.")
            continue


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        print_raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() == 'yes' or restart.lower() == 'no':
            if restart.lower() == 'yes':
                print("Okay! Restarting now!\n")
            else: 
                print("Thanks for visiting! See you again!")
                break
        else:
            print("Invalid input. Please type 'yes' or 'no'.")
            continue


if __name__ == "__main__":
	main()
    
'''
Resources Used:
https://practicaldatascience.co.uk/data-science/how-to-find-the-most-common-value-in-a-pandas-column

https://learn.udacity.com/nanodegrees/nd104/parts/cd0024/lessons/ls1727/concepts/2d64a03d-e921-4c75-92f8-b188611ee3cf

https://realpython.com/python-f-strings/

https://saturncloud.io/blog/how-to-handle-pandas-keyerror-value-not-in-index/#:~:text=The%20Pandas%20KeyError%20occurs%20when,differently%20from%20the%20actual%20key.

https://docs.python.org/3/library/exceptions.html

https://stackoverflow.com/questions/29645153/remove-name-dtype-from-pandas-output-of-dataframe-or-series

https://stackoverflow.com/questions/71487195/how-do-i-change-column-name-in-a-dataframe-in-python-pandas

https://pillow.readthedocs.io/en/stable/handbook/tutorial.html
'''
