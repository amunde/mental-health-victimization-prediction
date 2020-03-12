from matplotlib import rc

import matplotlib.pyplot as plt

import numpy as np


def line_chart(dataframe_name, rate):

    dataframe_name["Year"] = dataframe_name["Year"].astype("int64")

    dataframe_name[rate] = dataframe_name[rate].astype(float)


    plt.figure(figsize=(12,7))

    df = dataframe_name.pivot(index='Year', columns='State', values = rate)

    plt.plot(df, marker = 'o')

    plt.xlabel("Year")

    plt.ylabel(rate)

    plt.legend(["Alaska", "California","Florida","New York","Pennsylvania"])

    plt.title("Yearly Analysis of "+ rate.split("_")[0]+" "+rate.split("_")[1])

    plt.savefig("Analysis/"+rate+"_line_plot.png")




def stacked_bar_yearly(p, poverty_data_relevant, suicide_rate_relevant, unemployment_data_relevant_new):

#     p=0;

    bar2r = poverty_data_relevant.sort_values(['Year'], ascending = False).iloc[p:p+5]
    bar2r = bar2r.sort_values("State")
    bar2 = []
    for i in bar2r['Poverty_Rate']:
        bar2.append(i)

    bar3r = suicide_rate_relevant.sort_values(['Year'], ascending = False).iloc[p:p+5]
    bar3r = bar3r.sort_values("State")
    bar3 = []
    for i in bar3r['Suicide_Rate']:
        bar3.append(i)

    bar4r = unemployment_data_relevant_new.sort_values(['Year'], ascending = False).iloc[p:p+5]
    bar4r = bar4r.sort_values("State")
    bar4 = []
    for i in bar4r['Unemployment_Rate']:
        bar4.append(i)


    return np.array(bar2).astype(float),np.array(bar3).astype(float),np.array(bar4).astype(float)




def bar_chart( poverty_data_relevant, suicide_rate_relevant, unemployment_data_relevant_new):

    year_dictionary = {"2018": 0, "2017": 5, "2016": 10, "2015": 15, "2014": 20}

    year = input("Enter the Year from 2014 - 2018: ")

    while(year not in year_dictionary):

        print("Enter valid year")

        year = input("Enter the Year from 2014 - 2018: ")

    year_index = year_dictionary[year]

    # y-axis in bold
    rc('font', weight='bold')

    bar2, bar3, bar4 = stacked_bar_yearly(year_index, poverty_data_relevant, suicide_rate_relevant, unemployment_data_relevant_new)

    bars3 = np.add(bar2, bar3).tolist()

    # The position of the bars on the x-axis
    r = [0, 2, 4, 6, 8]

    # Names of group and bar width
    names = ['AL', 'CA', 'FL', 'NY', 'PA']
    barWidth = 1
    plt.figure(figsize=(12, 7))

    plt.bar(r, bar2, color='#26DB32', edgecolor='white', width=barWidth)

    plt.bar(r, bar3, bottom=bar2, color='#4169E1', edgecolor='white', width=barWidth)

    plt.bar(r, bar4, bottom=bars3, color='#FF0000', edgecolor='white', width=barWidth)

    # Custom X axis
    plt.xticks(r, names, fontweight='bold')

    # Setting X axis label
    plt.xlabel("State")


    plt.legend(['Poverty', 'Suicide', 'Unemployment'])

    plt.title("Features Analysis State wise for "  + year)

    plt.savefig("Analysis/"+str(year)+"_bar_chart.png")

    # Show graphic
    # plt.show()



def state_bar_plot(final_dataframe):


    state = input("Enter state: ['AK', 'CA', 'FL', 'NY', 'PA']").upper()




    # Defining the title of the plot
    title = 'Time series representing indexes for ' + state
    df = final_dataframe
    # Defining the data for Y axis
    data = [df[df['State'] == state]['Crime_Rate'],
            df[df['State'] == state]['Unemployment_Rate'],
            df[df['State'] == state]['Poverty_Rate'],
            df[df['State'] == state]['Suicide_Rate']]

    # X axis is the years from 2014 - 2018

    plt.figure(figsize=(12, 7))
    barWidth = 0.20

    #df[df['State'] == state]['Year']

    # Set position of bar on X axis
    r1 = [2014, 2015, 2016, 2017, 2018]
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]
    r4 = [x + barWidth for x in r3]

    # PLotting the bar graph
    plt.bar(r1, data[0], color='#ff8c69', width=barWidth, edgecolor='white', label='Crime_Rate')
    plt.bar(r2, data[1], color='#98fb98', width=barWidth, edgecolor='white', label='Unemployment_Rate')
    plt.bar(r3, data[2], color='lightskyblue', width=barWidth, edgecolor='white', label='Poverty_Rate')
    plt.bar(r4, data[3], color='#008080', width=barWidth, edgecolor='white', label='Suicide_Rate')

    # Add axes labels and legend
    plt.legend(loc='best')
    plt.xlabel('Years')
    plt.ylabel('Rate Percentage')
    plt.title(title)


    plt.savefig("Analysis/"+str(state)+"_bar_chart.png")

    #plt.show()



if __name__ == "__main__":
    print("This file stores all the methods to visualize the data")