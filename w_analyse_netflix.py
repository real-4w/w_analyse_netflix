import pandas as pd
import pathlib
#check the location of the CSV file. I used a data subdirectory, followed by Netflix' directory structure.

#=Main programme ===============================================================================================
if __name__ == "__main__":                                      # only run this as standalone script
    path = pathlib.Path.cwd() / 'data/CONTENT_INTERACTION/ViewingActivity.csv'
    df = pd.read_csv(path)
    df.shape