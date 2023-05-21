import streamlit as st
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

# Set page title
st.set_page_config(page_title='TfL Cooling Project',
                   layout="wide",
                   page_icon=":lower_left_paintbrush:",
                   menu_items={
    'Report a bug': "mailto:OOsakwe1@icloud.com?subject=Bug%20found%20in%20Outpainting",
    'About': "# Built by Olisa Osakwe."
    })

# Load sample data
df = pd.read_csv('https://data.london.gov.uk/download/london-underground-average-monthly-temperatures/b01c7853-fff2-4781-9755-9b5e1404d78c/lu-average-monthly-temperatures.csv')
df.rename(columns={"Sub-surface_lines": "Subsurface_lines"}, inplace=True)

# Creating a column to combine the Month and Year columns
df["Period"] = df["Month"] + ' ' + df["Year"].astype(str)

# Sidebar - Input form
# st.sidebar.header('Input Data')
# station_name = st.sidebar.selectbox('Select Station', sample_data['Station'])
# cooling_capacity = st.sidebar.number_input('Cooling Capacity (kW)', min_value=0)
# cooling_efficiency = st.sidebar.slider('Cooling Efficiency', min_value=0.0, max_value=1.0, step=0.01, value=0.5)


# Update sample data with user input
ldn_weather=pd.read_csv('data/london_weather.csv')
ldn_weather.drop(columns=['global_radiation', 'pressure', 'snow_depth'],
                 inplace=True)
ldn_weather['date']=pd.to_datetime(ldn_weather['date'], format='%Y%m%d')
ldn_weather["new_date"]=list(zip(ldn_weather.date.dt.year, ldn_weather.date.dt.month))
ldn_weather['Month']=list(ldn_weather.date.dt.month)
ldn_weather['Year']=list(ldn_weather.date.dt.year)
weather_grpd=ldn_weather.groupby(['new_date']).mean(numeric_only=True).reset_index()
weather_grpd['Month'].replace({1: 'January',
                               2: 'February',
                               3: 'March',
                               4: 'April',
                               5: 'May',
                               6: 'June',
                               7: 'July',
                               8: 'August',
                               9: 'September',
                               10: 'October',
                               11: 'November',
                               12: 'December'},
                              inplace=True)
weather_grpd=weather_grpd[weather_grpd['Year'] > 2012].reset_index()
weather_grpd.Year=weather_grpd.Year.astype(int)
weather_grpd["Period"] = weather_grpd["Month"] + ' ' + weather_grpd["Year"].astype(str)
# weather_grpd


df_merged=df.merge(weather_grpd.drop(columns=['Year',
                                              'Month',
                                              'new_date']),
                   on='Period',
                   how='outer')
# df_merged

# Main content - Display data and visualizations
st.title('The London Underground has a cooling problem')

st.markdown('''Welcome to my analysis of the average monthly temperatures on Transport for London's (TfL) underground trains!
        ''')

st.markdown("We'll be taking a closer look at how temperature affects both our comfort as passengers and the functioning of the trains themselves 🌡️.")

# Display updated data
st.subheader('Temperatures on the London Underground')
st.dataframe(df)

df_byyears_max=df_merged.groupby('Year').max(numeric_only=True).reset_index()
df_byyears_mean=df_merged.groupby('Year').mean(numeric_only=True).reset_index()


df = px.data.gapminder()

fig1 = px.scatter(
    df_byyears_mean,
    x="Year",
    y=["Bakerloo",
       "Central",
       "Jubilee",
       "Northern",
       "Piccadilly",
       "Victoria",
       "Waterloo_and_City",
       "Subsurface_lines"],
       color_discrete_map=
       {"Bakerloo": 'rgb(179,98,5)',
        "Central": 'rgb(227,13,23)',
        "Jubilee": 'rgb(160,165,169)',
        "Northern": 'rgb(0,0,0)',
        "Piccadilly": 'rgb(0,54,136)',
        "Victoria": 'rgb(0,152,212)',
        "Waterloo_and_City": 'rgb(149,205,186)',
        "Subsurface_lines":'rgb(255,211,0)'},
        labels={"period": "Month & year",
                "value": "Temperature (˚C)",
                "variable": "Underground lines"
               },
        trendline='lowess',
        title='Mean Temperature on TFL Underground lines'
          )

fig2 = px.scatter(
    df_byyears_max,
    x="Year",
    y=["Bakerloo",
       "Central",
       "Jubilee",
       "Northern",
       "Piccadilly",
       "Victoria",
       "Waterloo_and_City",
       "Subsurface_lines"],
       color_discrete_map=
       {"Bakerloo": 'rgb(179,98,5)',
        "Central": 'rgb(227,13,23)',
        "Jubilee": 'rgb(160,165,169)',
        "Northern": 'rgb(0,0,0)',
        "Piccadilly": 'rgb(0,54,136)',
        "Victoria": 'rgb(0,152,212)',
        "Waterloo_and_City": 'rgb(149,205,186)',
        "Subsurface_lines":'rgb(255,211,0)'},
        labels={"period": "Month & year",
                "value": "Temperature (˚C)",
                "variable": "Underground lines"
               },
        trendline='lowess',
        title='Max Temperature on TFL Underground lines'
          )


tab1, tab2 = st.tabs(["Mean Annual Temperature", "Max Annual Temperature"])
with tab1:
    # Use the Streamlit theme.
    # This is the default. So you can also omit the theme argument.
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)
with tab2:
    # Use the native Plotly theme.
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

st.subheader('Observations')
st.markdown('''
* A reason for the significant drop in avg. temperature in 2020 is likely due to the reduced travel caused by COVID-19 restrictions resulting in less heat on trains.
* It is likely that changes to climate are impacting the temperatures experienced on trains.
* The Subsurface lines (Circle, District, Metropolitan, Hammersmith & City lines) are stocked by the 'S Stock' S7 & S8 trains which are air-conditioned throughout. The subsurface tunnels also allow the exhausted hot air to disperse.
* It seems that the avg. temperature of the Victoria line is going up by __0.72 degrees__ yearly! This is significantly higher than other deep-level tube lines. There seems to be no sufficient explanation for this. The Victoria line is also one of two lines [to be wholly-underground](https://www.mylondon.news/news/zone-1-news/london-underground-employee-explains-victoria-24708836) (the other being the Waterloo & City line) so one might postulate that trapped heat would have a hard time escaping and sink into the tunnel walls.
''')
st.markdown('Here is a [map of the TfL network](https://content.tfl.gov.uk/tube-map-with-tunnels.pdf) with all tunnels shown')

st.divider()

st.subheader('Can the weather tell us anything about the tube temperatures? 🌧️')
# Heatmap of correlations
st.set_option('deprecation.showPyplotGlobalUse', False)

correlation_matrix = df_merged.drop(columns=['Year',
                                             'Month',
                                             'max_temp',
                                             'min_temp']).corr(numeric_only=True)
plt.figure(figsize=(4, 3))
sns.heatmap(correlation_matrix, annot=False, cmap='bwr')
st.pyplot()

st.subheader('Observations')
st.markdown('''
* The weather factors predictably have particularly poor correlation with the underground temperatures, especially precipitation and cloud cover.
* Sunshine has weak but noticeable correlation but is more indicative of ambient temperature so will not ultimately be useful.
''')

st.divider()

st.subheader('How does ambient temperature correspond to tube temperatures? 🚇')
# Define the data
y = ["Bakerloo", "Central", "Jubilee", "Northern", "Piccadilly", "Victoria", "Waterloo_and_City", "Subsurface_lines"]
colors = [(0.701, 0.384, 0.019), (0.890, 0.051, 0.090), (0.627, 0.647, 0.662), (0.0, 0.0, 0.0), (0.0, 0.211, 0.533),
          (0.0, 0.596, 0.831), (0.584, 0.803, 0.729), (1.0, 0.827, 0.0)]

# Create the subplots using Streamlit
fig, ax = plt.subplots(nrows=2, ncols=4, sharex=True, sharey=True, figsize=(15, 10))

# Loop through the data and create the plots
for i in range(8):
    row = i // 4  # Assigns the row of the plots by floor division
    col = i % 4  # Assigns the column of the plots by modulo
    sns.regplot(df_merged[0:83], x="mean_temp", y=y[i], color=colors[i], ax=ax[row][col])
    ax[row][col].set_title(
        y[i] + " Line\n" + "R-squared = " + str(round(df_merged[0:83].corr(numeric_only=True).loc["mean_temp", y[i]] ** 2, 3))
    )

# Display the plots in Streamlit
st.pyplot(fig)

st.markdown('''
As we can see from the plots, the ambient temperature in London is generally predictive of the temperature on different TfL Underground lines. However, how predictive it is varies for each line.
* The Subsurface Lines have an R-squared number of 0.976. These lines are fully air-conditioned with [very specific thermostat settings](https://tfl.gov.uk/corporate/transparency/freedom-of-information/foi-request-detail?referenceId=FOI-0659-1920) which would explain the strong correlation.
* Most lines are generally within **0.75** to **0.95** with variation from the ambient (how much hotter the tube is than ambient) between 2 and 14˚C.
* The most erratic line is the Victoria line only registering an R-squared number of **0.6**. It has been very challenging to find any data or reasonable explanations for the trends exhibited by the Victoria line data. It has the newest stock of any line besides the Subsurface lines and is equipped with regenerative braking. As of 2019, the line also became the 2nd average hottest line on the Underground network.
* As mentioned earlier, the fact the Victoria line is the only wholly-undergound line could be a factor but without further data or context, it is hard to ascertain what causes this.
''')

st.divider()

st.subheader("TfL Underground Train Stock and Heat Issues")

# Displaying the article content
st.markdown("An article published by [Rail Engineering](https://assets.markallengroup.com//article-images/23757/cooling.pdf) gave detail of computer modelling run on the Victoria line and found the major heat sources and sinks as follows:")

heat_data = {
    "Heat source": [
        "Braking losses",
        "Mechanical losses",
        "Drive losses",
        "Train auxiliaries",
        "Tunnel systems",
        "Station systems and passengers",
        "Train passengers"
    ],
    "%": [38, 22, 16, 13, 4, 4, 3],
    "Heat Sinks": [
        "Tunnel Walls",
        "Tunnels",
        "Ventilation Shafts",
        "",
        "",
        "",
        ""
    ],
    "% ": [79, 11, 10, "", "", "", ""]
}

heat_df = pd.DataFrame(heat_data)

st.table(heat_df)

st.markdown("That puts _89%_ of all heated generated in tube systems on the train itself. The article also goes on to suggest that the root of the problem is that the biggest heat sink is failing as the temperature behind the walls rises into the clay, storing the heat. The issue of cooling the tube is so complex that the former mayor of London, Ken Livingstone, offered a prize of __£100,000__ to anyone who could put forward a viable solution. After several years of the reward being on offer, TfL announced that *[none of the 3,500 submissions were suitable.](https://www.standard.co.uk/hp/front/aps100-000-prize-for-cooling-tube-goes-unclaimed-7204222.html)*")

st.markdown("18 years on from then, temperatures have only risen and it is deeply worrying that the high temperatures have led to further medical emergencies on the underground.")
st.markdown("As of today, the current stock of TfL trains is as follows:")

data = [
    ["TfL Underground line", "Operating Stock", "Regenerative Braking", "Air-Conditioning", "Planned Restock?"],
    ["Bakerloo", "1972 Stock", "No - Stock pre-dates technology", "No", "Yes - No timeline*"],
    ["Central", "1992 Stock", "Yes - 790VDC", "No", "Yes - No timeline*"],
    ["Jubilee", "1996 Stock", "Yes - 790VDC**", "No", "None"],
    ["Northern", "1995 Stock", "Yes - 790VDC", "No", "None"],
    ["Piccadilly", "1973 Stock", "No - Stock pre-dates technology", "No", "Yes - Expected 2025"],
    ["Victoria", "2009 Stock", "Yes - 890VDC", "No", "None"],
    ["Waterloo & City", "1992 Stock", "Yes - 790VDC", "No", "Yes - No timeline*"],
    ["SubSurface Lines***", "S7/S8 (2012-2014)", "Yes - 650/790/890 VDC****", "Yes", "None"],
]

df = pd.DataFrame(data[1:], columns=data[0])
st.table(df)

notes = [
    "Notes:",
    ":------:",
    "*All to be restocked under the New Tube for London project, no up-to-date timeline.",
    "**Soon to be upgraded to 890VDC, to be more in line with the Victoria line",
    "***Subsurface Lines include the Circle, District, Metropolitan and Hammersmith & City lines.",
    "****Depends on the location of the train and other assets operating in those areas."
]

sources = [
    "Sources:",
    "[FOI-2080-2021](https://tfl.gov.uk/corporate/transparency/freedom-of-information/foi-request-detail?referenceId=FOI-2080-2021)",
    "[Piccadilly Upgrade](https://tfl.gov.uk/travel-information/improvements-and-projects/piccadilly-line-upgrade)",
    "[New Tube for London](https://tfl.gov.uk/info-for/media/press-releases/2014/october/design-for-the-new-tube-for-london-revealed)"
]

st.markdown("\n".join(notes))
st.markdown("\n".join(sources))

st.markdown("TfL is in the early stages of upgrading the Piccadilly, Bakerloo, Central and Waterloo & City lines under the New Tube for London project. All these lines are expected to be stocked with the [Siemens Mobility 'InspiroLondon'](https://www.mobility.siemens.com/global/en/portfolio/references/metro-london.html) trains.")

st.markdown("The Piccadilly line will be the first to see upgrades and is expected to have [new trains installed by 2025](https://tfl.gov.uk/info-for/media/press-releases/2021/march/tfl-and-siemens-mobility-unveil-detailed-design-of-new-piccadilly-line-trains) to serve the public, although this is already well behind schedule.")

st.markdown("The Bakerloo line, which [operates the oldest train stock in the nation](https://www.mylondon.news/news/zone-1-news/london-underground-trains-officially-oldest-20672857) is expected to have new trains ordered in the financial year 2023/24. This, ignoring the potential for delays or setbacks, would mean that new trains would not be installed until the mid-2030s. This also goes for the notoriously busy Central line. These two lines have routinely ranked as the hottest lines on the tube network and will potentially be without stock upgrades for at least the next decade.")

st.markdown("Without proper monitoring and mitigation measures, it is very likely this could lead to further exacerbation of these issues, putting passengers and train performance at risk. Realistically, there is only so much that can be done with the TfL Network still reeling from the effects of the COVID-19 pandemic as it seeks to post an operating surplus for the financial year 2022/23.")

st.markdown("To learn more about the TfL underground rolling train stock, [see this document](https://www.whatdotheyknow.com/request/239641/response/590412/attach/3/RS%20Info%20Sheets%204%20Edition.pdf)")


st.markdown("Thank you for your interest in this project! Check out what I'm working on next on [GitHub](https://github.com/Osakwe1)")
