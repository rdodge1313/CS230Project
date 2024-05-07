'''
Name: Ryan Dodge
CS230: Section 1
Data: Bridges in Georgia (first 10000)

Description: This project utilizes data about bridges in Georgia to
generate various visuals. There are multiple widget options that allow
for users to specify certain parameters so that they can see what they
want. For example, there is a map, bar chart, pie chart, and images
embedded into the program.

In this project, I used documentation for the libraries and packages used.
For example, this included docs.streamlit.io, matplotlib.org, 
deckgl.readthedocs.io, and pandas.pydata.org. These resources were used 
in addition to the class notes to find more parameters that would help 
improve the customization of my project.
'''

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import pydeck as pdk

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 1000)

dfBridges = pd.read_csv("C:\\Users\\rdodg\\eclipse-workspace\\Project\\BridgesData.csv")


def bridgeMap(df):
    #Sorting data frame by bridge age from oldest to newest
    dfMapInfo = df.sort_values(by = "Bridge Age (yr)", ascending = False)
    
    #Renaming columns so that they can be used in the map fuction for coordinates
    dfMapInfo = dfMapInfo.rename(columns={"16 - Latitude (decimal)": "LATITUDE"})
    dfMapInfo = dfMapInfo.rename(columns={"17 - Longitude (decimal)": "LONGITUDE"})
    
    st.write("How many of the oldest bridges would you like to see?")
    oldestNumber = st.number_input("Enter your selection (up to 500):", 0, 500)
    
    #Selecting only the columns that I will use for the coordinates and the tool tip
    dfSelectedBridges = dfMapInfo.iloc[:oldestNumber, [18, 2, 5, 9, 23, 24]]
    
    #For this part, I referenced the CIS Sandbox tutorial and the
    #PyDeck website (deckgl.readthedocs.io)
    #I originally used st.map() but did not have the ability to do tooltip
    
    #Used to set the display of the map and the scatterplot for data points
    view_state = pdk.ViewState(latitude = 32.1574, longitude = -82.9071, zoom = 5)
    layer = pdk.Layer("ScatterplotLayer", data = dfSelectedBridges, 
                      get_position = '[LONGITUDE, LATITUDE]', get_radius = 10000, 
                      get_color = [255, 51, 51], pickable = True)
    
    #Captures structure number, county located in, and year built
    tool_tip = {'html': 'Bridge<br/>Structure Number: {8 - Structure Number}<br/>County Name: {3 - County Name}<br/>Year Built: {27 - Year Built}', 'style':{'backgroundColor': 'lightblue', 'color': 'black'}}
    
    #Plotting the map
    map = pdk.Deck(map_style = 'light',
                   initial_view_state = view_state,
                   layers = [layer],
                   tooltip = tool_tip)
    
    st.pydeck_chart(map)


def barChartOwnerAgency(df, bar_color = "green"):
    fig = plt.figure()
    
    ownerAgencies = list(sorted(set(df["22 - Owner Agency"])))
    #Removes duplicates, sorts agencies and arranges in a list
    
    displayAgencies = st.multiselect("Select owner agencies:", ownerAgencies)
    
    selectedAgencies = df[df["22 - Owner Agency"].isin(displayAgencies)]
    
    totalByOwnerAgency = selectedAgencies.groupby(by = ["22 - Owner Agency"]).size()
    
    #Establishing the bar chart and adding labels
    plt.bar(totalByOwnerAgency.index, totalByOwnerAgency.values, color = bar_color)
    plt.title("Number of Bridges by Owner Agency")
    plt.xlabel("Owner Agency")
    plt.ylabel("Number of Bridges")
    
    #Rotates the x labels to be diagonal so they do not overlap when multiple are selected
    plt.xticks(rotation=45, ha="right")
    
    plt.style.use("ggplot")
    
    return fig

def pieChartAverageTraffic(df):
    fig = plt.figure()
    
    dfTrafficAndMaterial = df[["29 - Average Daily Traffic", "43A - Main Span Material"]]
    
    #Removes any duplicates and sorts
    materialTypes = sorted(set(df["43A - Main Span Material"]))
    
    #Creating a dictionary where each key is a material type
    #Starting at 0 for values because I will add traffic later
    materialDict = {}
    for material in materialTypes:
        if material not in materialDict:
            materialDict[material] = 0
    
    #Looked this up on pandas.pydata.org
    #Goal is to go through each record and add the traffic to the dictionary
    #Was not exactly sure how to do it with a df so I used the documentation as a reference
    for index, row in dfTrafficAndMaterial.iterrows():
        materialType = row["43A - Main Span Material"]
        trafficAmount = row["29 - Average Daily Traffic"]
        materialDict[materialType] += trafficAmount
    
    #Dictionary now has traffic as values associated with each material key
    
    #Creating lists to use as inputs for the pie chart
    labelNames = list(materialDict.keys())
    valueAmounts = list(materialDict.values())
    
    #Customizing colors with a list
    colorList = ["yellow", "orange", "olive", "magenta", "gold", "lavender", "red", "blue", "silver", "sienna"]
    
    #Making the pie chart and formatting for presentation
    plt.pie(valueAmounts, autopct='%1.1f%%', pctdistance = 1.5, radius = 0.4, center = (0.5, 1), colors = colorList)
    plt.legend(labelNames, loc = "lower right", fontsize = 4)
    plt.title("Pie Chart (Total Traffic Based on Material Type)")
    
    return fig

def bridgeSelect():
    imageOptions = ["Talmadge Memorial Bridge", "Sidney Lanier Bridge", "Archibald Butt Memorial Bridge"]
    selection = st.radio("Select a famous Georgia bridge", imageOptions)
    
    #Links to the images used
    talmadge_memorial_bridge = "C:\\Users\\rdodg\\eclipse-workspace\\Project\\TalmadgeMemorialBridge.jpg"
    sidney_lanier_bridge = "C:\\Users\\rdodg\\eclipse-workspace\\Project\\SidneyLanierBridge.jpg"
    archibald_butt_memorial_bridge = "C:\\Users\\rdodg\\eclipse-workspace\\Project\\ArchibaldButtMemorialBridge.jpg"
    
    #If statement that displays the image that corresponds with the radio selection
    if selection == imageOptions[0]:
        st.image(talmadge_memorial_bridge, caption = "Source: https://en.wikipedia.org/wiki/Talmadge_Memorial_Bridge")
    elif selection == imageOptions[1]:
        st.image(sidney_lanier_bridge, caption = "Source: https://en.wikipedia.org/wiki/Sidney_Lanier_Bridge")
    else:
        st.image(archibald_butt_memorial_bridge, caption = "Source: https://www.tripadvisor.com/LocationPhotoDirectLink-g29212-d290511-i252815017-Augusta_Canal_Discovery_Center-Augusta_Georgia.html")
    
    
def main():
    
    st.title("CS230 Final Project (Bridges in Georgia")
    st.subheader("Ryan Dodge")
    
    st.header("Map:")
    bridgeMap(dfBridges)
    
    st.header("Bar Chart:")
    barChart = barChartOwnerAgency(dfBridges)
    st.pyplot(barChart)
    
    st.header("Pie Chart:")
    pieChart = pieChartAverageTraffic(dfBridges)
    st.pyplot(pieChart)
    
    st.header("Image Selection:")
    bridgeSelect()
    
main()