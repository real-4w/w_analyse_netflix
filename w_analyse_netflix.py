import pandas as pd
import pathlib, pytz, matplotlib, yaml
#=============================================================================================================
def ProcessYAML (yaml_file) :
    '''This function opens the yaml file and returns the data object'''
    with open(yaml_file) as f:
        y_data = yaml.load(f, Loader=yaml.FullLoader)
        debug = y_data['debug']
        if debug == True : print("YAML file:\n", y_data)
    return (debug, y_data) 
def ReturnTotalTimePerProfile(df_netflix):
    df2 = df_netflix.loc[:, ['Profile Name','Duration']]
    #df2 = df[['Profile Name','Duration']] #throws a warning
    #df2 = df.loc[(df['Profile Name'] == "Alex"), ['Profile Name','Duration']]
    df2['Duration'] = pd.to_timedelta(df2['Duration'])
    df2 = df2.groupby(['Profile Name'])['Duration'].sum()
    return (df2)

#= Main programme ===============================================================================================
if __name__ == "__main__":                                      # only run this as standalone script
    debug, yaml_data = ProcessYAML('netflix.yaml') 
    file = yaml_data['view']
    path = pathlib.Path.cwd() / file
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
    # set our categorical and define the order so the days are plotted Monday-Sunday
    shameless['weekday'] = pd.Categorical(shameless['weekday'], categories= [0,1,2,3,4,5,6], ordered=True)
    # create shameless_by_day and count the rows for each weekday, assigning the result to that variable
    shameless_by_day = shameless['weekday'].value_counts()

    # sort the index using our categorical, so that Monday (0) is first, Tuesday (1) is second, etc.
    shameless_by_day = shameless_by_day.sort_index()

    # optional: update the font size to make it a bit larger and easier to read
    matplotlib.rcParams.update({'font.size': 22})

    # plot shameless_by_day as a bar chart with the listed size and title
    shameless_by_day.plot(kind='bar', figsize=(20,10), title='Shameless Episodes Watched by Day')

    # set our categorical and define the order so the hours are plotted 0-23
    shameless['hour'] = pd.Categorical(shameless['hour'], categories= [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23], ordered=True)

    # create shameless_by_hour and count the rows for each hour, assigning the result to that variable
    shameless_by_hour = shameless['hour'].value_counts()

    # sort the index using our categorical, so that midnight (0) is first, 1 a.m. (1) is second, etc.
    shameless_by_hour = shameless_by_hour.sort_index()

    # plot shameless_by_hour as a bar chart with the listed size and title
    shameless_by_hour.plot(kind='bar', figsize=(20,10), title='shameless Episodes Watched by Hour')