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
#- FUnctions on CONTENT_INTERACTION ==========================================================================
def ProfileList(df_netflix) :
    '''This function returns all Netflix profiles in a list.'''
    return(list(df_netflix['Profile Name'].unique()))

def Profile(df_netflix, profile):
    '''This function returns all Netflix data for the profile requested.'''
    df2 = df_netflix.loc[(df_netflix['Profile Name'] == profile)]
    return (df2)

def TotalTimePerProfile(df_netflix):
    '''This function returns total duration view of all Netflix profiles in a df.'''
    df2 = df_netflix.loc[:, ['Profile Name','Duration']]
    #df2 = df[['Profile Name','Duration']] #throws a warning
    #df2 = df.loc[(df['Profile Name'] == "Alex"), ['Profile Name','Duration']]
    df2['Duration'] = pd.to_timedelta(df2['Duration'])
    df2 = df2.groupby(['Profile Name'])['Duration'].sum()
    return (df2)

def TotalTimeForAProfile(df_netflix, profile):
    '''This function returns total duration view for a sprecific Netflix profiles in a df.'''
    df2 = df_netflix.loc[(df_netflix['Profile Name'] == profile), ['Profile Name','Duration']]
    df2['Duration'] = pd.to_timedelta(df2['Duration'])
    df2 = df2.groupby(['Profile Name'])['Duration'].sum()
    return (df2)

#- FUnctions on CONTENT_INTERACTION ==========================================================================

#= Main programme ===============================================================================================
if __name__ == "__main__":                                      # only run this as standalone script
    debug, yaml_data = ProcessYAML('netflix.yaml') 
    file = yaml_data['view']
    path = pathlib.Path.cwd() / file
    
    df = pd.read_csv(path)
    print(df)
    print(ProfileList(df))
    
    df2 = TotalTimePerProfile(df)
    print (df2)

    df3 = TotalTimeForAProfile(df, 'Alex')
    print(df3)

    df4 = Profile(df, 'Alex')
    print(df4)
    