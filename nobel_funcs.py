from datetime import date
import numpy as np
import pandas as pd
import requests


def get_current_year():
    current_year = date.today().year
    
    return current_year
    
    
def get_nobel_data(endpoint='laureates', limit=9999, yearFrom=1901, yearTo=get_current_year(), category=None):
    """
    Retrieves Nobel prize data from the REST API at nobelprize.org and returs a json dictionary
    
    Parameters
    ----------
    endpoint (str, optional): 
        "laureates": sorts the output based on Nobel Laureates (persons and/or organizations). 
            Returns all information about Laureates and Nobel Prizes. Defaults to "laureates".
        "nobelPrizes": sorts the output based on Nobel Prizes returning a shorter result. Use in 
            conjunction with the Laureates endpoint to get the full response. Links provided in 
            the result to facilitate this.
    limit (int, optional): 
        The numbers of items to return. Defaults to 9999.
    yearFrom (int, optional): 
        The year the Nobel Prize was awarded, in the form YYYY. Defaults to 1901.
    yearTo (int, optional): 
        Use in combination with yearFrom (required) to specify a range of years. Defaults to current year.
    category (str, optional): filter by Nobel Prize category (Chemistry: "che", Ecnomics: "eco", 
        literature: "lit", Peace: "pea", Physics: "phy", Medicine: "med". Defaults to None.
    """
    url = f'https://api.nobelprize.org/2.1/{endpoint}'
    params = {'limit': limit,
              'nobelPrizeYear': yearFrom,
              'yearTo': yearTo,
              'nobelPrizeCategory': category}
    
    response = requests.get(url, params=params)
    print('Status: OK' if response.status_code == 200 else 'Status: Error')
    data = response.json()

    return data

def find_and_drop_cols(df):
    """
    Takes a DataFrame as an argument, makes a list of column names ending in ".no", ".se", and ".sameAs"
    for Norwegian and Swedish translations and Wikidata links and drops them from the DataFrame
    """
    cols_to_drop = [col for col in df.columns if col[-3:] == '.no' or col[-3:] == '.se' or col[-6:] == 'sameAs']
    df.drop(cols_to_drop, axis=1, inplace=True)
    
    return df

def strip_en(df):
    """
    Takes a DataFrame as an argument, makes a list of column names ending in ".en" indicating 
    Engish translations, strips the ending from the column name, and returns an updated DataFrame
    """
    cols_to_rename = {}
    for col in df.columns:
        if col.endswith('.en'):
            cols_to_rename[col] = col[:-3]
    
    df.rename(cols_to_rename, axis=1, inplace=True)
    
    return df

if __name__ == "__main__":
    laureates_data = get_nobel_data('laureates')
