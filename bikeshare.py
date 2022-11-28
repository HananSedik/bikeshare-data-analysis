import time
import pandas as pd

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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("what is the city?, ['chicago', 'new york city', 'washington'] \n").lower().strip()
    cities = ['chicago', 'new york city', 'washington']
    while city not in cities:
        city = input("Incorrect Selection, Please select chicago, new york city or washington \n").lower().strip()

    # get user input for month (all, january, february, ... , june)
    month = input("Which month? ['All', 'January', 'February', 'March', 'April', 'May', 'June'] \n").capitalize().strip()
    months = ['All', 'January', 'February', 'March', 'April', 'May', 'June']
    while month not in months:
        month = input("Incorrect Selection, Please Select one of the following values 'All', 'January', 'February', 'March', 'April', 'May', 'June' \n").capitalize().strip()
        
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Which day? ['All', 'Saturday', 'Sunday', 'Monday', 'Tuesday','Wednesday', 'Thursday', 'Friday'] \n").capitalize().strip()
    days = ['All', 'Saturday', 'Sunday', 'Monday', 'Tuesday','Wednesday', 'Thursday', 'Friday']
    while day not in days:
        day = input("Incorrect Selection, Please Select one of the following values 'All', 'Saturday', 'Sunday', 'Monday', 'Tuesday','Wednesday', 'Thursday', 'Friday' \n").capitalize().strip()

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

    print("Loading Data For %s" % city)
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'], format='%Y-%m-%d %H:%M:%S')
    if month != 'All':
        df = df[df['Start Time'].dt.month_name() == month]
    if day != 'All':    
        df = df[df['Start Time'].dt.day_name() == day]

    return df

def time_stats(df, month, day):
    """
    Displays statistics on the most frequent times of travel.
    
    Args:
        df - Pandas DataFrame containing city data filtered by month and day
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == "All":
        print("The Most Common Month For Travel Is: %s" % removeHeaders(df['Start Time'].dt.month_name().mode()))

    # display the most common day of week
    if day == "All":
        print("The Most Common Day For Travel Is: %s" % removeHeaders(df['Start Time'].dt.day_name().mode()))


    # display the most common start hour
    print("The Most Common Hour For Travel Is: %s" % removeHeaders(df['Start Time'].dt.hour.mode()) )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)    


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    
    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print ("The most common used start station is : %s" % removeHeaders(df['Start Station'].mode() ) )

    # display most commonly used end station
    print ("The most common used end station is : %s" % removeHeaders(df['End Station'].mode() ) )


    # Increase Column Width
    pd.set_option('display.max_colwidth', 255)

    # display most frequent combination of start station and end station trip
    df['startEndStation'] = df['Start Station'] + ' To ' + df['End Station']
    print("The most frequent combination of start station and end station is : %s" % removeHeaders(df['startEndStation'].mode() )  )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
        
    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total Travel Time: %d Seconds" % (df['Trip Duration'].sum()))

    # display mean travel time
    print("Average Travel Time: %d Seconds" % (df['Trip Duration'].mean()))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """
    Displays statistics on bikeshare users.
        
    Args:
        df - Pandas DataFrame containing city data filtered by month and day
        (str) city - name of the city to analyze
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Counts of user types:")
    print(removeHeaders( df.groupby(['User Type']).size(), True))

    print("")
    # Display counts of gender
    if city != 'washington':
        print("Counts of Gender: ")
        print(removeHeaders(df.groupby(['Gender']).size(), True))

        print("")
    # Display earliest, most recent, and most common year of birth
        print("Earliest Year Of Birth: %d" % int(df.sort_values(['Birth Year'])['Birth Year'].iloc[0]))
        print("Most Recent Year Of Birth: %d" % int(df.sort_values(['Birth Year']).dropna()['Birth Year'].iloc[-1]))
        print("Most Common Year Of Birth: %d" % int(df['Birth Year'].mode()))



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """
    Displays raw data on user request.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    seeRawData = input('\nWould you like to see the raw data? Enter yes or no.\n')
    if seeRawData.lower().strip() == 'yes':
        print(df.head())
        next = 0
        while True:
            viewMoreRawData = input('\nWould you like to view the next five rows of raw data? Enter yes or no.\n')
            if viewMoreRawData.lower().strip() != 'yes':
                return
            next = next + 5
            print(df.iloc[next:next+5])            

def removeHeaders(data, index= False):
    """
    Remove Header and Index from dataframe result
    Args:
        data - Pandas DataFrame
        (bool) index - remove index
    """
    return data.to_string(index= index, header=False) 

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_raw_data(df)

        restart = input(f'\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()