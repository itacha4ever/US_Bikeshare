import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'all']


def get_filter_city():
    """ Get the filter of the City """
    while True:
        city = input("Please enter one of the following cities you want to see data for:"
                     "\n- Chicago\n- New York\n-Washington\n:-").lower()
        if city in CITY_DATA.keys():
            break
        else:
            print("That's Invalid City Please  Try Again.")
    return city


def get_filter_month():
    """ Get the filter of the Months """
    while True:
        month = input("Please enter a Month name from January to June or Choose All for All Months by using of month "
                      "\n:-").lower()
        if month in months:
            break
        else:
            print("That's Invalid month Please Try Again")
    return month


def get_filter_day():
    """ Get the filter of the days """
    while True:
        day = input("Please enter a Day of the week or Choose All for All Days by use the days names "
                    "\n:-").lower()
        if day in days:
            break
        else:
            print("That's Invalid Day Please Try Again")

    return day


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US Bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = get_filter_city()

    # get user input for month (all, january, february, ... , june)
    month = get_filter_month()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_filter_day()

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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print("The Most Common Month from the Filtered Data is:", common_month)

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print("The Most Common Day of Week from the Filtered Data is:", common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_start_hour = df['hour'].mode()[0]
    print("The Most Common Start Hour from the Filtered data is: ", common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    commonly_start = df['Start Station'].mode()[0]
    print("The Most Common Start Station is: \n", commonly_start)
    # display most commonly used end station
    commonly_end = df['End Station'].mode()[0]
    print("The Most Common End Station is: \n", commonly_end)
    # display most frequent combination of start station and end station trip
    combination_station = df['Start Station'] + " to " + df['End Station']
    combination_start_end = combination_station.mode()[0]
    print("The Most Common Trip from Start to End is :\n {}".format(combination_start_end))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print("The Total Travel Time  is: ", total_time, "\nThe Total Travel Time in Hour is: ", total_time / 3600)

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print("The Mean Travel Time is: ", mean_time, "\nThe Mean Travel Time in Hour is: ", mean_time / 3600)

    print("\nThis took %s Seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    type_of_user = df['User Type'].value_counts()
    print('Counts Types of User is:\n', type_of_user, '\n')

    # Display counts of gender
    # used this because washington don't have Gender in the sheet
    if 'Gender' in df:
        gender_counts = df['Gender'].value_counts()
        print('Gender Counts is:\n', gender_counts, '\n')
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        birth_most_common = df['Birth Year'].mode()
        print('Most Common Year of Birth is:\n', birth_most_common, '\n')
        birth_most_recent = df['Birth Year'].max()
        print('Recent Year of Birth is:\n', birth_most_recent, '\n')
        birth_earliest = df['Birth Year'].min()
        print('Earliest Year of Birth is:\n', birth_earliest, '\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_raw_data(df):
    """Displays the Raw Data on user request due filtration.
        Asks if the user would like to see some lines of data from the filtered dataset.
    Displays 5 (show_rows) lines, then asks if they would like to see 5 more.
    Continues asking until they say stop.
    """
    next_row = 0
    question = input('\nWould you like to see some raw data from the current dataset? yes/no\n:-').lower()
    while True:
        if question == 'no':
            break
        else:
            answer = df[next_row:next_row + 5]
            print(answer)
            question = input('\nWould you like to see more raw data from the current dataset? yes/no\n:-').lower()
            next_row += 5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
