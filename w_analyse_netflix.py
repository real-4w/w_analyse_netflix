import pandas as pd
import pathlib, pytz


#check the location of the CSV file. I used a data subdirectory, followed by Netflix' directory structure.

#=Main programme ===============================================================================================
if __name__ == "__main__":                                      # only run this as standalone script
    path = pathlib.Path.cwd() / 'data/CONTENT_INTERACTION/ViewingActivity.csv'
    df = pd.read_csv(path)
    df.shape
    df.head(1)
    #dropping some columns
    df = df.drop(['Profile Name', 'Attributes', 'Supplemental Video Type', 'Device Type', 'Bookmark', 'Latest Bookmark', 'Country'], axis=1)
    df.head(1)
    df.dtypes
    df['Start Time'] = pd.to_datetime(df['Start Time'], utc=True)
    df.dtypes  
    # change the Start Time column into the dataframe's index
    df = df.set_index('Start Time')

    # convert from UTC timezone to eastern time
    df.index = df.index.tz_convert('Pacific/Auckland')

    # reset the index so that Start Time becomes a column again
    df = df.reset_index()

    #double-check that it worked
    df.head(1)
    
    shameless = df[df['Title'].str.contains('Shameless', regex=False)]
    shameless.shape
    shameless = shameless[(shameless['Duration'] > '0 days 00:01:00')]
    shameless.shape
    shameless['Duration'].sum()
    print (shameless)
    shameless['weekday'] = shameless['Start Time'].dt.weekday
    shameless['hour'] = shameless['Start Time'].dt.hour
    shameless.head(1)  