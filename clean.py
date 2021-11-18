"Step 1: Understanding your data"

import pandas as pd # Statement to import pandas into our project

data = pd.read_csv('artwork_sample.csv', low_memory = False) # Saves our csv file into a variable

def viewing_and_converting_types():
    data.year = pd.to_numeric(data.year, errors = "coerce") # Converts the year column to a float. Error statements converts data that is not numeric to NaN
    data.height = pd.to_numeric(data.height, errors = "coerce") # Converts the height column to a float. Error statements converts data that is not numeric to NaN
    data.width = pd.to_numeric(data.width, errors = "coerce") # Converts the width column to a float. Error statements converts data that is not numeric to NaN
    print(data.dtypes) # Prints the types of data that are stored in each column

def aggregating():
    # If neccesary we could aggregate our data using functions such as max, mean, min, sum. For example, data.artist.sum()
    # We could also use the data.agg function to aggregate a funciton across all our columns in the data set. For example, data.agg('min')
    
    print(data.agg(['min', 'max', 'mean', 'std'])) # Here we are aggregating all of our data to get a good sense of the data.

def normalizing():
    height = data.height # Creates a height variable to use with normalization
    minimax = (height - height.min()) / (height.max() - height.min()) # Normalizes the data in the height column between 0 and 1
    data['standardized_height'] = minimax # Creates a new column to store the standardized height

def transforming():
    data.height = data.height.transform(lambda x: x / 10) # Uses a lambda function to convert the height column from centimeters to meters
    print(data.groupby('artist').transform('nunique')) # This groups the data by the artist, and returns the number of unique values in the group for each column
    print(data.groupby('artist')['height'].transform('mean')) # This returns the average height for the painting for each group

def filtering():
    data.filter(items = ['id', 'artist']) # Filters only to the columns that we want to look at
    data.filter(like = 'artist') # Filters all columns that contain the word "artist"
    data.filter(regex="(?i)year") # Uses regex to filter all columns that have the word "year" without the parameter being case sensitive
    # We also can set axis=0 to filter through the rows in our dataset
