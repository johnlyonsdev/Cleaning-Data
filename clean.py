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

"Step 2: Removing and Fixing Columns"

def dropping_columns():
    data.drop(0, inplace = True) # Drops the row with the index of 0
    data.drop('id', axis = 1, inplace = True) # Drops the column with the name 'id'. Axis = 1 means we are using columns
    data.drop(columns = ['height', 'width', 'depth'], inplace = True) # We can also select columns by using the columns keyword
    data.drop(labels = [1,2,3], inplace = True) # We can also select rows by using the labels keyword

    # We can use  "usecols=['artist', 'title"] as an additional parameter in our read statement to only load in the columns that we want to load.

def changing_casing():
    data.columns = data.columns.str.lower() # Changes all the column names to lowercase
    data.columns = [x.lower() for x in data.columns] # Does the same thing but gives us room for additional logic
    data.columns = map(lambda x: x.lower(), data.columns) # We can also do this by using the map function
    import re # Imports re for our next line
    data.columns = [re.sub(r'([A-Z])', r'_\1', x).lower() for x in data.columns] # Converts our column case to snake casing

def renaming_columns():
    data.rename(columns={"thumbnailUrl": "thumbnail"}, inplace = True) # Renames the specific columns that we want renamed
    # We can also rename all columns at once, by setting data.columns = to an array of all the column names we want to use
    # We can also set the column names when we load in the file by adding a parameter where name = our array in the read statement, we also have to add in header = 0 into the read statement if we are doing this

"Step 3: Indexing and Filtering Data"

def direct_filtering():
    data['id'] # We can directly filter a column as a series using []
    data['id'][1] # Because [] returns a series, we can access a specfic item in this series using extra []
    data[1:3] # We can filter specific rows like this. The first row is included, the second row is excluded
    data[1:5]['artist'] # We can add an extra filter to only see specific columns in each row
    data[data['year'] > 1800]['year'] # We can also filter for specific results

def loc_filtering():
    data.loc[0:2,:] # Returns a slice of rows for all columns. The range here is inclusive
    data.loc[[1,4] , ['artist', 'title']] # We can also identify specific rows and columns by passing in arrays
    data.loc[data.artist == 'Blake, Robert', :] # We can pass in arguments to only return specific data that fits the parameters

def iloc_filtering():
    data.iloc[0:3, 2:4] # returns based off of the index position. The second number is no longer inclusive
    data.set_index('id', inplace = True) # Lets us customize what our index is.

def str_contains_filtering():
    data.loc[data.medium.str.contains('Graphite', case=False), ['artist', 'medium']] # We can use str.contains to only select the rows that contain certain strings. Case=False means that we aren't doing a case sensitive search
    data.loc[data.medium.str.contains('Graphite', case=False) | data.medium.str.contains('Line', case=False), ['artist', 'medium']] # We can also use or statements to select multiple str.contain items
    data.loc[data.year.astype(str).str.contains('1826'), 'year'] # If we want to use str.contains on a column that is not an object type, we have to make sure that we first convert it to a string

"Step 4: Handling Bad Data"

def strip_white_space():
    data.loc[data.title.str.contains('\s$', regex = True)] # Filters for lines that end with white space
    data.title = data.title.str.strip() # Strips white space from the end of the titles
    data.title = data.title.transform(lambda x: x.strip()) # This does the same thing using the transform function

def replacing_bad_data():
    pd.isna(data.loc[:, 'dateText']) # Checks if the values we have filtered are equal to NaN
    from numpy import nan #imports nan from numpy
    data.replace({'dateText': {'date not known': nan}}, inplace = True) # Replaces all bad values in the datetext column with nan
    data.loc[data.dateText == 'date not known', ['dateText']] = nan # This uses another method to accomplish the same task

def filling_missing_values():
    data.fillna(value = {'depth': 0}, inplace = True) # This allows us to use key value pairs to replace nan with values of our choice

def dropping_rows():
    data.dropna(how = 'any', inplace = True) # Drops a row if any of the data is nan
    data.dropna(how = 'all', inplace = True) # Drops a row if all of the data is nan
    data.dropna(thresh = 10, inplace = True) # Drops a row if the number of data items that are nan is equal to the threshold
    data.dropna(subset=['year', 'acquistionYear'], inplace = True) # Drops a row if any of the listed columns are nan
    data.dropna(subset=['year', 'acquistionYear'], how = 'all', inplace = True) # Drops a row if all of the listed columns are nan

def handling_duplicates():
    data.drop_duplicates() # Drops all duplicate rows
    data.drop_duplicates(subset=['artist'], keep = 'first', inplace = True) # Lets us choose the parameters that we are seeing if there are duplicates. Keep decides which duplicate we keep
    data.drop_duplicates(subset=['artist'], keep = False, inplace = True) # keep = False means that we keep none of the duplicates
    data.loc[data.duplicated(subset = ['artist', 'title'], keep = False)] # We can filter all the duplicates that we want to look at to decide if we want to drop them or not