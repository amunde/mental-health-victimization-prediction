
# Authors:
# Akshay Tatyarao Munde
# Varsha Jain
# Prasun Srestha
# Sonal Singh
# Pranav Banthia

import fetch_data

import visualize_data

import numpy as np

from sklearn.preprocessing import PolynomialFeatures

from sklearn.model_selection import train_test_split

from sklearn.linear_model import LinearRegression

import pandas as pd

import plotly.graph_objects as go

import os


# This fetches data from all the required sources and returns the Dataframes
def fetch_all_data(state_list):

    crime_dataframe = fetch_data.fetch_crime_data(state_list)

    unemployment_dataframe = fetch_data.fetch_unemployment_data(state_list)

    poverty_dataframe = fetch_data.fetch_poverty_data(state_list)

    suicide_dataframe = fetch_data.fetch_suicide_data(state_list)

    # Merging data from all the dataframes available
    merged_data_1 = pd.merge(unemployment_dataframe, poverty_dataframe, how = "left", on=["Year", "State"] )

    merged_data_2 = pd.merge(merged_data_1, suicide_dataframe, how = "left", on=["Year", "State"] )

    final_dataframe = pd.merge(merged_data_2, crime_dataframe, how = "left", on=["Year", "State"] )

    return crime_dataframe, unemployment_dataframe, poverty_dataframe, suicide_dataframe, final_dataframe




# Selecting features and test/train split for the model
def initialize_data(train_dataframe):

    # The column being predicted - Happiness Index in this case
    y = train_dataframe["Happiness Index"]

    # Excluding these values since they don't contribute to calculating the Happiness Index
    X = train_dataframe.drop(["Year", "State", "Happiness Index"], axis=1)

    # Splitting data in test and train sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.01, random_state=1)

    return X_train, X_test, y_train, y_test



def calculate_training_testing_error(algorithm, X_train, y_train):

    #Fitting model to the data
    algorithm.fit(X_train, y_train)

    return algorithm



def train_model():

    train_dataframe = pd.read_excel("Training_data.xlsx")

    # Using linear regressor with polynomial features to predict the index
    linear_regression = LinearRegression()

    polynomial_features_train = PolynomialFeatures(degree=1, include_bias=False)

    # Extracting the relevant values from the input dataframe
    X_train, X_test, y_train, y_test = initialize_data(train_dataframe)

    # Comverting to polynomial features
    X_train_polynomial = polynomial_features_train.fit_transform(X_train)

    # Training the model
    fitted_model = calculate_training_testing_error(linear_regression, X_train_polynomial, y_train)

    return fitted_model

def visualize_all_graphs(crime_dataframe, unemployment_dataframe, poverty_dataframe, suicide_dataframe, final_dataframe):


    # Creating a new directory if it does not already exists for storing the generated graphs
    if not os.path.exists('Analysis'):
        os.makedirs('Analysis')

    visualize_data.line_chart(crime_dataframe, "Crime_Rate")

    visualize_data.line_chart(unemployment_dataframe, "Unemployment_Rate")

    visualize_data.line_chart(poverty_dataframe, "Poverty_Rate")

    visualize_data.line_chart(suicide_dataframe, "Suicide_Rate")

    visualize_data.bar_chart(poverty_dataframe, suicide_dataframe, unemployment_dataframe)

    visualize_data.state_bar_plot(final_dataframe)


def descriptive_statistics(final_dataframe):

    df = final_dataframe.round(2)

    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df.State, df.Year, df.Crime_Rate, df.Poverty_Rate, df.Unemployment_Rate, df.Suicide_Rate, df.Population, df.Happiness_Index_Predicted],
                   fill_color='lavender',
                   align='left'))
    ])

    fig.show()


    df_mean = final_dataframe.groupby(["State"]).mean().reset_index().round(2)

    fig = go.Figure(data=[go.Table(
        header=dict(values=list(["State", "Unemployment Rate Mean", "Poverty Rate Mean", "Suicide Rate Mean", "Crime Rate Mean", "Population Mean", "Happiness Index Mean"]),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df_mean.State, df_mean.Unemployment_Rate, df_mean.Poverty_Rate, df_mean.Suicide_Rate, df_mean.Crime_Rate, df_mean.Population, df_mean.Happiness_Index_Predicted],
                   fill_color='lavender',
                   align='left'))
    ])

    fig.show()


    df_median = final_dataframe.groupby(["State"]).median().reset_index().round(2)

    fig = go.Figure(data=[go.Table(
        header=dict(values=list(["State", "Unemployment Rate Median", "Poverty Rate Median", "Suicide Rate Median", "Crime Rate Median", "Population Median", "Happiness Index Median"]),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df_median.State, df_median.Unemployment_Rate, df_median.Poverty_Rate, df_median.Suicide_Rate, df_median.Crime_Rate, df_median.Population, df_median.Happiness_Index_Predicted],
                   fill_color='lavender',
                   align='left'))
    ])

    fig.show()



if __name__ == '__main__':

    state_list = ['ak','ca','fl','ny','pa']

    # Train the model to calculate the happiness index
    fitted_model = train_model()

    # Fetching the data from the sources
    crime_dataframe, unemployment_dataframe, poverty_dataframe, suicide_dataframe, final_dataframe = fetch_all_data(state_list)

    predicted_values = fitted_model.predict(final_dataframe[["Crime_Rate", "Unemployment_Rate", "Poverty_Rate", "Suicide_Rate"]])

    # Predicting the Happiness Index for the states considering Crime_Rate, Unemployment_Rate, Poverty_Rate, Suicide_Rate
    final_dataframe["Happiness_Index_Predicted"] = pd.DataFrame(predicted_values)

    descriptive_statistics(final_dataframe)

    visualize_all_graphs(crime_dataframe, unemployment_dataframe, poverty_dataframe, suicide_dataframe, final_dataframe)




