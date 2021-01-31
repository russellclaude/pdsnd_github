import time
import pandas as pd
import numpy as np

#additonal libraries. See references.txt
import sys

#this is a dictionary of keys and values
#CITY_DATA["chicago"]
# ...will yield the value chicago.csv
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    For example:
    city = input('Which city would you like to explore? [chicago, new york city, washington]')

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('*'*50+'\n **Hello! Let\'s explore some US bikeshare data!**\n'+'*'*50 + '\n\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    #prime the input loop
    getcity = ""
    while getcity == "":
        getcity = input('Which *city* would you like to explore? Chicago, New York City, Washington or None (exit)?\n[CHI, NYC, DC, NA]\n').title()
        #allow the users to be lazy or creative, up to a point
        if getcity == "Chicago" or getcity == "Chi":
            city = "chicago"
        elif getcity == "New York City" or getcity == "New York" or getcity == "Nyc" or getcity == "Ny":
            city = "new york city"
        elif getcity == "Washington" or getcity == "Washington DC".title() or getcity == "DC".title() or getcity == "D.C.".title() or getcity == "Washington D.C.".title():
            city = "washington"
        elif getcity == "None" or getcity == "Na" or getcity == "Exit":
            city = "none"
            sys.exit('\n Okay... BYE! (exiting the Bike Share database.)\n')

        else:
            #okay, I give up... I don't know what they want. Ask again.
            getcity = ""
            print("\nYour response was not understood. Please check your spelling, or use the given prompts.\n")

    print('\nCITY- You chose: {} \n'.format(city))


    # get user input for which filter to use:
    # Would you like to filter the data by month, day, or not at all?

    getOpts = "--nothing yet--"
    Opts = ['Month', 'Day', 'Na', 'Both']
    sAlert = ""
    while getOpts not in Opts:
        getOpts = input('\n{} Would you like to filter the data by Month, Day, Both, or Not at all (type `NA`) ?\n'.format(sAlert)).title()
        sAlert = "Doh! I didn't understand."

    print('\nFilter?- Your selection: {} \n'.format(getOpts))

    # get user input for month (all, january, february, ... , june)
    #prime the input loop
    getmonth = ""
    month = -1
    while getmonth == "" and (getOpts == "Month" or getOpts == "Both"):
        getmonth = input('\nWhich *month* would you like to explore? All, None, January, February, ... , June?\n[All, JAN, FEB, MAR, APR, MAY, JUN]\n').title()
        #allow the users to be lazy or creative, up to a point
        if getmonth == "All" or getmonth == "None" or getmonth == "Na":
            month = "All"
        elif getmonth == "January" or getmonth == "Jan":
            month = 0
        elif getmonth == "February" or getmonth == "Feb":
            month = 1
        elif getmonth == "March" or getmonth == "Mar":
            month = 2
        elif getmonth == "April" or getmonth == "Apr":
            month = 3
        elif getmonth == "May" or getmonth == "May":
            month = 4
        elif getmonth == "June" or getmonth == "Jun":
            month = 5
        else:
            #let's ask again. they weren't very helpful
            getmonth = ""
            print("\nYour response was not understood. Please check your spelling, or use the given prompts.\n")

    #give them some feedback that you understand what they want
    if getOpts == "Month" or getOpts == "Both":
        print('\nMONTH- You chose: {} \n'.format(getmonth))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    getday = ""
    day = -1
    while getday == "" and (getOpts == "Day" or getOpts == "Both"):
        getday = input('\nWhich *day* of the week would you like to explore?\n All, Monday, Tuesday, ... Sunday?\n[ALL, MON, TUE, WED, THR, FRI, SAT, SUN]\n').title()
        if getday == "All" or getday == "None":
            day = -1
        elif getday == "Monday" or getday == "Mon":
            day = 0
        elif getday == "Tuesday" or getday == "Tue":
            day = 1
        elif getday == "Wednesday" or getday == "Wed":
            day = 2
        elif getday == "Thursday" or getday == "Thr" or getday == "Thu":
            day = 3
        elif getday == "Friday" or getday == "Fri":
            day = 4
        elif getday == "Saturday" or getday == "Sat":
            day = 5
        elif getday == "Sunday" or getday == "Sun":
            day = 6
        else:
            getday = ""
            print("\nYour response was not understood. Please check your spelling, or use the given prompts.\n")

    #give them some feedback that you understand what they want
    if getOpts == "Day" or getOpts == "Both":
        print('\nDAY-You chose {}:'.format(getday))


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (int) month - month-number to filter by, or -1 to apply no month filter
        (int) day - number representing the day of week to filter by, or -1 to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and/or day
    """

    df = pd.read_csv(city + ".csv")

    #lets not forget what city we are dealing with. Make it a column
    df['city'] = city

    #convert datetime columns so we can do date stuff
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    #create a month column to filter on.... for speed
    df['month'] = df['Start Time'].dt.month -1

    #create a day of week column to filter on.... for speed
    df['dow'] = df['Start Time'].dt.dayofweek

    #create a start_hr column.... for speed
    df['start_hr'] = df['Start Time'].dt.hour

    #fix the missing data in Gender with 'Unknown' if necessary
    if 'Gender' in list(df.columns):
        df[['Gender']] = df[['Gender']].fillna(value='Unknown')

    #filter by day if required
    if day != -1: df = df[df['dow']==day]
    #filter by month if required
    if month != -1: df = df[df['month']==month]

    #print('<==df has shape:', df.shape)
    #print('<==df has dimension:', df.ndim)
    #print('<==df has a total of:', df.size, 'elements')
    #print('<==The minimum/MAX MONTH in df is:\n', df['month'].min(), df['month'].max())
    #print('The row index in df is:', df.index)
    #print('The column index in df is:', df.columns)

    return df


def time_stats(df, month, day):
    #print('time_stats <=={}  {}==>'.format(month, day))
    """Displays statistics on the most frequent times of travel."""


    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #we need to be able to show users words instead of indexes
    daysoweek = ('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')
    monthsoyear = ('January','February','March','April','May','June','July','August', 'September', 'October', 'November', 'December')

    # display the most common month, unless they are already filtered on a month... that would be redernt
    if month == -1:
        #get the first record of a sorted group-by that shows the month with the most records
        tdf = df.groupby(['month'])['month'].count().sort_values(ascending=False).head(1)
        intVal = tdf.values[0]
        strIndex = monthsoyear[tdf.index[0]]
        print("> The most common month was {} for {} occurances.".format(strIndex, intVal))
    else:
        print('> You chose {}, if you had forgotten.'.format(monthsoyear[month]))

    # display the most common day of week, if necessary
    if day == -1:
        #get the first record of a sorted group-by that shows the day-of-week with the most records
        tdf = df.groupby(['dow'])['dow'].count().sort_values(ascending=False).head(1)
        intVal = tdf.values[0]
        strIndex = daysoweek[tdf.index[0]]
        print("> The most common day of the week was {} for {} occurances.".format(strIndex, intVal))
    else:
        print('> You chose {}, if you had forgotten.'.format(daysoweek[day]))

    # display the most common start hour
    #get the first record of a sorted group-by that shows the Start-hour with the most records
    tdf = df.groupby(['start_hr'])['start_hr'].count().sort_values(ascending=False).head(1)
    strVal = tdf.values[0]
    strIndex = tdf.index[0]
    print("> The most common start hour was {} for {} occurances.".format(strIndex, strVal))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trips...\n')
    start_time = time.time()

    # display most commonly used start station
    #get the first record of a sorted group-by that shows the Start-station with the most records
    tdf = df.groupby(['Start Station'])['Start Station'].count().sort_values(ascending=False).head(1)
    strVal = tdf.values[0]
    strIndex = tdf.index[0]
    print("> The most common Start Station was {} for {} occurances.".format(strIndex, strVal))

    # display most commonly used end station
    #get the first record of a sorted group-by that shows the End Station with the most records
    tdf = df.groupby(['End Station'])['End Station'].count().sort_values(ascending=False).head(1)
    strVal = tdf.values[0]
    strIndex = tdf.index[0]
    print("> The most common End Station was {} for {} occurances.".format(strIndex, strVal))

    # display most frequent combination of start station and end station trip
    #get the first record of a sorted group-by that shows the Start-Station and End-Station combo with the most records
    tdf = df.groupby(['Start Station', 'End Station'])['Start Station'].count().sort_values(ascending=False).head(1)
    strVal = tdf.values[0]
    strIndex = tdf.index[0][0] + ' ==>> ' + tdf.index[0][1]
    print("> The most common Start/End Station combo was [{}] for {} occurances.".format(strIndex, strVal))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time (in minutes)
    #see https://stackoverflow.com/questions/22923775/calculate-pandas-dataframe-time-difference-between-two-columns-in-hours-and-minu
    #dates are a pain in the rear... usually
    iInt = (df['End Time'] - df['Start Time']).astype('timedelta64[m]').sum()
    print("> Total Rental-minutes logged: {}".format(iInt))

    # display mean travel time - sum(from above)/count and round to 2 decis
    iFlt = int(iInt / (df['End Time'] - df['Start Time']).astype('timedelta64[m]').count()*100)/100
    print("> Average Rental-time was {} minutes.".format(iFlt))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    #groupbys..... they are just the best. Loop through them!
    tdf = df.groupby(['User Type'])['User Type'].count().sort_values(ascending=False)
    #loop through each User Type
    for i in tdf.index:
        print('{}\'s rented {} times.'.format(i, tdf.loc[i]))

    print()

    # Display counts of gender - NOT AVAILABLE FOR ALL CITIES
    if 'Gender' in list(df.columns):
        tdf = df.groupby(['Gender'])['Gender'].count().sort_values(ascending=False)
        #loop through each Gender
        for i in tdf.index:
            print('{}\'s rented {} times.'.format(i, tdf.loc[i]))


    # Display earliest, most recent, and most common year of birth - NOT AVAILABLE FOR ALL CITIES
    if 'Birth Year' in list(df.columns):
        #focus on the Birth Year, nothing else, and kill the NaN's
        tdf = df['Birth Year'].dropna(axis=0)
        iMin = int(tdf.min())
        iMax = int(tdf.max())
        iMode = int(tdf.mode()[0])
        print('\nBirth years range from {} to {} with {} being the most common year.'.format(iMin, iMax, iMode))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    #print 5 rows
    iRange = df.shape[0]
    iLast = 0
    bolBreak = False
    #we're gonna slice and dice our way, serving raw data to all-comers
    for i in range(5, iRange, 5):
        #print("<==was:{} is: {} will be: {}".format(iLast, i, iRange))
        #display the daw data, but not the columns we cooked in
        print(df.iloc[iLast:i,1:-4])
        #we dont really want to see the last record again
        iLast = i
        getraw = ""
        while getraw.lower() == "":
            #ask for more
            getraw = input('\nWould you like to see MORE raw data from your selections? Enter yes or no.\n').lower()
            if getraw == 'yes' or getraw == 'y':
                print()#keep going
            elif getraw == 'no' or getraw == 'n':
                #i = iRange * 2
                print('\nNo more raw data for you!\n')
                bolBreak = True
                #get out of while
                break
            else:
                print('\n Gah! I didn\'t understand.\n' )
                getraw == ""

        if bolBreak == True:
            #get out of For
            break


def main():
    while True:
        city, month, day = get_filters()
        #print('Main<=={}    {}  {}==>'.format(city, month, day))
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        getraw = ""
        while getraw.lower() == "":
            getraw = input('\nWould you like to see the raw data from your selections? Enter yes or no.\n').lower()
            if getraw == 'yes' or getraw == 'y':
                display_raw_data(df)
            elif getraw == 'no' or getraw == 'n':
                print('\n mkay. I didn\'t want to show you anyway.\n' )
            else:
                print('\n Dern. I didn\'t understand.\n' )
                getraw == ""

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
