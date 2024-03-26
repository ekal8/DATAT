import streamlit as st
import pandas as pd

# Load your dataset
df = pd.read_csv('arrivals.csv')  # Replace 'your_dataset.csv' with the path to your dataset

# Sidebar with country selection
selected_country = st.sidebar.selectbox('Select a Country', sorted(df['country'].unique()))

# Filter the dataframe based on selected country
filtered_df = df[df['country'] == selected_country]

# Display the filtered dataframe
st.write("### Data for Selected Country:", selected_country)
st.write(filtered_df)

# Show the number of people entering the selected country
total_arrivals = filtered_df['arrivals'].sum()
st.write("### Total Arrivals:", total_arrivals)

# Show arrivals by gender
st.write("### Arrivals by Gender:")
st.write("Male:", filtered_df['arrivals_male'].sum())
st.write("Female:", filtered_df['arrivals_female'].sum())
