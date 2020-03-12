from urllib.request import urlopen  # b_soup_1.py
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome


import numpy as np

import pandas as pd

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Palau': 'PW',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}

# This function accepts state names as the argument, fetches the data for the states by scraping the website
# http://www.disastercenter.com and then returns a Dataframe containing the required data
def fetch_crime_data(state_list):


    crime_dataframe = pd.DataFrame([], columns=['Year', 'Population', 'Index', 'Violent', 'Property', 'Murder', 'Rape',
                                                'Robbery', 'Assault', 'Burglary', 'Larceny', 'Vehicle Theft'])

    # For each state in the list, fetch the data from the Url
    for state in state_list:

        html = urlopen('http://www.disastercenter.com/crime/' + state + 'crime.htm')

        # Using Beautiful soup to parse through the http file
        bsyc = BeautifulSoup(html.read(), "lxml")

        table = bsyc.findAll('table', attrs={'style': "text-align: left; width: 100%; height: 177px;"})

        found = False

        relevant_value = table[0].findAll('tr')[4].findAll('td')[0].findAll('table')[0]

        final_rows = []

        # Traversing to find the relevant data from the webpage
        for tr in relevant_value.findAll('tr'):

            req_rows = []

            for td in tr.findAll('td'):

                if ('2014' in td.text):

                    found = True

                if (found == True):

                    req_rows.append(td.text)

            if (len(req_rows) > 0):

                final_rows.append(req_rows)

        # Creating a dataframe from the scraped data
        state_dataframe = pd.DataFrame(final_rows, columns=['Year', 'Population', 'Index', 'Violent', 'Property', 'Murder', 'Rape','Robbery', 'Assault', 'Burglary', 'Larceny', 'Vehicle Theft'])

        # Converting state to upper case for easy linking across different dataframes
        state_dataframe["State"] = state.upper()

        crime_dataframe = crime_dataframe.append(state_dataframe, sort=False)


    # Converting the data to appropriate formats to preform operations later
    crime_dataframe["Index"] = crime_dataframe["Index"].str.replace(",","").astype("int64")
    crime_dataframe["Population"] = crime_dataframe["Population"].str.replace(",","").astype("int64")
    crime_dataframe["Crime_Rate"] = ((crime_dataframe["Index"]/crime_dataframe["Population"])*100).round(2)
    crime_dataframe["Year"] = crime_dataframe["Year"].astype("int64")

    crime_dataframe.reset_index(drop = True, inplace = True)
    crime_dataframe.drop(crime_dataframe.index[4], inplace = True)

    # Returning the relevant part of the dataframe
    return crime_dataframe[["Year", "State", "Crime_Rate", "Population"]]

# Fetched data from "http://datacensus.gov" and cleaned it. Loaded it into the file "Poverty_Rate_v3.csv".
def fetch_poverty_data(state_list):

    # name of the file
    poverty_df = pd.read_csv('Poverty_Rate_v3.csv')

    # S1701_C03_001E is the column name for the poverty rate dataset
    poverty_dataframe = poverty_df.loc[1:,['NAME','Year','S1701_C03_001E']]

    # Changes the column names to make intuitive sense
    poverty_dataframe.columns = ['State','Year','Poverty_Rate']

    # Downcasts the datatype of year to integer
    poverty_dataframe["Year"] = pd.to_numeric(poverty_dataframe["Year"], downcast = "integer")

    # Sorts the dataframe by state and year
    poverty_dataframe = poverty_dataframe.sort_values(['State','Year'])

    poverty_dataframe.reset_index(drop = True, inplace = True)

    # Converting the name of the states to abbreviated format for consistency
    abbrev_list = []
    for row in poverty_dataframe.values:
        abbrev_list.append(us_state_abbrev[row[0]])

    poverty_dataframe["State"] = pd.DataFrame(abbrev_list)

    poverty_dataframe["Poverty_Rate"] = poverty_dataframe["Poverty_Rate"].astype(float)

    # Returning the dataframe
    return poverty_dataframe

# Fetched data from "https://www.cdc.gov/" and created StatewiseSuicideRatesUSA.csv.
# Imported and cleaned data imported from the file.
def fetch_suicide_data(states):


    suicide_rates = pd.read_csv('StatewiseSuicideRatesUSA.csv')

    suicide_rates.columns = ['Year','State','Suicide_Rate','Deaths','URL']

    #Drop extra columns
    suicide_rates = suicide_rates.drop(['Deaths','URL'], axis=1)

    #Creating new DataFrame for given states
    suicide_dataframe = pd.DataFrame(columns=['Year','State','Suicide_Rate'])

    states = ['AK','CA','FL','NY','PA'] # or state_list

    for i in suicide_rates.index:
        if suicide_rates.loc[i,'State'] in states:
            suicide_dataframe = suicide_dataframe.append(suicide_rates.loc[i,:])

    # Converts the datatype of year to integer
    suicide_dataframe["Year"] = suicide_dataframe["Year"].astype("int64")

    # Eliminates the data prior to 2014
    suicide_dataframe = suicide_dataframe[suicide_dataframe["Year"] >= 2014]

    # Sorts the dataframe by state and year
    suicide_dataframe = suicide_dataframe.sort_values(['State','Year']).reset_index(drop = True)

    # Returns the formatted dataframe
    return suicide_dataframe


def fetch_unemployment_data(states):

    webdriver = "/Users/akshaymunde/PycharmProjects/DFP Final Project/venv/src/chromedriver"
    # Need to install chrome driver
    # https://chromedriver.chromium.org/downloads

    driver = Chrome(webdriver)

    # Dictionary to save the dataset
    year_dict = {}

    # Fetching data for years 2014 - 2018
    for year in range(14,19):

        url = "https://www.bls.gov/lau/laucnty" + str(year) + ".xlsx"

        county_wise = pd.read_excel(url)

        year_dict[year] = county_wise # dictionary of dataframes

    # Using the chrome web driver to open Seleniun in the background and access the website
    driver.close()

    #df_final = pd.DataFrame(columns=['State','Year','Unemployment_Rate'])
    #states = ['AK','CA','FL','NY','PA']

    unemployment_dataframe = pd.DataFrame(columns=['State','Year','Unemployment_Rate'])

    states = ['AK','CA','FL','NY','PA']

    for key,value in year_dict.items():

        year_dict[key] = value.loc[5:3223, ['Unnamed: 3','Unnamed: 4','Unnamed: 9']]

        year_dict[key].columns = ['State','Year','Unemployment_Rate']

        year_dict[key][['County','State']] = year_dict[key].State.str.split(",",expand = True)

        # Deleting unnecessary columns
        del year_dict[key]['County']

        year_dict[key] = year_dict[key].astype({'Year': 'int64', 'Unemployment_Rate': 'float64'})

        year_dict[key] = year_dict[key].apply(lambda x: x.str.strip() if x.dtype == "object" else x)

        unemployment_dataframe = unemployment_dataframe.append(year_dict[key])

    unemployment_dataframe = unemployment_dataframe[unemployment_dataframe['State'].isin(states)]

    unemployment_dataframe.reset_index(drop = True, inplace = True)  # resets the index

    # Takes the average of all counties
    # Groups by state and years
    unemployment_dataframe = unemployment_dataframe.groupby(["State", "Year"]).mean().round(2)

    unemployment_dataframe.reset_index(inplace=True)

    # Returns the unemployment dataframe
    return unemployment_dataframe


if __name__ == '__main__':

    print("This is fetch data used to get data from all the sources")
