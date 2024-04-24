import pandas as pd
import folium
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
from streamlit_folium import folium_static


# Load dataset
df = pd.read_csv('museums.csv')


# Data Cleaning
df.drop(['Museum ID'], axis=1, inplace=True)  # remove unnecessary column
df.drop(['Legal Name'], axis=1, inplace=True)
df.drop(['Alternate Name'], axis=1, inplace=True)
df.drop(['Institution Name'], axis=1, inplace=True)
df.drop(['Street Address (Administrative Location)'], axis=1, inplace=True)
df.drop(['Street Address (Physical Location)'], axis=1, inplace=True)
df.drop(['City (Physical Location)'], axis=1, inplace=True)
df.drop(['State (Physical Location)'], axis=1, inplace=True)
df.drop(['Zip Code (Physical Location)'], axis=1, inplace=True)
df.drop(['Phone Number'], axis=1, inplace=True)
df.drop(['Locale Code (NCES)'], axis=1, inplace=True)
df.drop(['County Code (FIPS)'], axis=1, inplace=True)
df.drop(['State Code (FIPS)'], axis=1, inplace=True)
df.drop(['Region Code (AAM)'], axis=1, inplace=True)
df.drop(['Employer ID Number'], axis=1, inplace=True)
df.drop(['Tax Period'], axis=1, inplace=True)


# Input specific values for missing data
income_impute_value = 106968188.9  # value for 'Income' column
revenue_impute_value = 20976046.74  # value for 'Revenue' column

df.replace(0, np.nan, inplace=True)

df['Income'].fillna(income_impute_value, inplace=True)
df['Revenue'].fillna(revenue_impute_value, inplace=True)
df['Income'].fillna(income_impute_value, inplace=True)
df['Revenue'].fillna(revenue_impute_value, inplace=True)

df['Latitude'].fillna(0, inplace=True)
df['Longitude'].fillna(0, inplace=True)

st.write(df)

# Data Summarization
total_museums = len(df)
average_income_per_type = df.groupby('Museum Type')['Income'].mean()

# Outlier Detection
Q1 = df['Income'].quantile(0.25)
Q3 = df['Income'].quantile(0.75)
IQR = Q3 - Q1
outliers = df[(df['Income'] < (Q1 - 1.5 * IQR)) | (df['Income'] > (Q3 + 1.5 * IQR))]

# # Output Results
# print(f"Total number of museums: {total_museums}")
# print("Average income per museum type:")
# print(average_income_per_type)
# print(f"Number of outliers in income: {len(outliers)}")
# print(outliers)

st.header('Museum Data Summary')
st.subheader(f'Total Museums: {total_museums}')
st.write(average_income_per_type.apply(lambda x: f'${x:,.2f}').to_frame('Average Income'))



#Pie Chart
museum_counts = df['Museum Type'].value_counts()

plt.figure(figsize=(10, 7))
plt.pie(museum_counts, labels=museum_counts.index, autopct='%1.1f%%', startangle=90)
plt.title('Distribution of Museums by Type')
plt.axis('equal') 
plt.show()

st.bar_chart(df[['Income', 'Revenue']])



# Create a base map
m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=5)

# Define color map
museum_type_colors = {
    'ARBORETUM, BOTANICAL GARDEN, OR NATURE CENTER': 'green',
    'ART MUSEUM': 'yellow',
    'CHILDRENS MUSEUM': 'blue',
    'GENERAL MUSEUM ': 'red',
    'HISTORIC PRESERVATION': 'orange',
    'HISTORY MUSEUM': 'purple',
    'NATURAL HISTORY MUSEUM': 'beige',
    'SCIENCE & TECHNOLOGY MUSEUM OR PLANETARIUM': 'black',
    'SCIENCE & TECHNOLOGY MUSEUM OR PLANETARIUM': 'white',
    'ZOO, AQUARIUM, OR WILDLIFE CONSERVATION': 'pink',
}

# Assuming 'df' is your DataFrame containing the museum data

# Create a new map object
m = folium.Map(location=[39.50, -98.35], zoom_start=4)  # Central location of the USA

# Counter to keep track of how many markers have been added
count = 0

# Iterate over the DataFrame rows
for _, row in df.iterrows():
    if count < 100:  # Check if less than 100 markers have been added
        # Add a marker for each museum
        folium.Marker(
            [row['Latitude'], row['Longitude']],
            popup=f"{row['Museum Name']}<br>Type: {row['Museum Type']}<br>Income: ${row['Income']:.2f}",
            icon=folium.Icon(color='blue')  # You can modify color based on other criteria if desired
        ).add_to(m)
        count += 1  # Increment the counter
    else:
        break  # Stop adding markers once 100 have been added

# Display the map in the Streamlit app
folium_static(m)

