import streamlit as st
import pandas as pd

# Load the dataset
@st.cache
def load_data():
    df = pd.read_csv('arrivals.csv')  # Replace 'your_dataset.csv' with the path to your dataset
    return df

df = load_data()

# Convert country codes to full names (you may need to load a mapping)
# Assuming you have a CSV file containing country codes and full names
country_mapping = pd.read_csv('country_mapping.csv',encoding='auto')  # Load your country mapping file
df = df.merge(country_mapping, left_on='country', right_on='code', how='right')
df.drop(columns=['country'], inplace=True)
df.rename(columns={'name': 'country'}, inplace=True)

# Create a Streamlit app
st.title('Arrivals Dashboard')

# Dropdown menu to select a country
selected_country = st.selectbox('Select a Country', df['country'].unique())

# Filter the data for the selected country
filtered_df = df[df['country'] == selected_country]

# Add option to change view to graphical
chart_view = st.radio("Select Chart View", ("Line Chart", "Bar Chart"))

# Line chart showing arrivals over time segmented by gender
if chart_view == "Line Chart":
    try:
        import plotly.express as px
        fig = px.line(filtered_df, x='date', y=['arrivals_male', 'arrivals_female', 'arrivals'],
                      title=f'Arrivals Over Time in {selected_country}',
                      labels={'date': 'Date', 'value': 'Number of Arrivals', 'variable': 'Gender'},
                      color_discrete_map={'arrivals_male': 'blue', 'arrivals_female': 'red', 'arrivals': 'green'})
        st.plotly_chart(fig)
    except ImportError:
        st.error("This feature requires the Plotly library. Please install it by running `pip install plotly`.")

# Bar chart showing total arrivals by gender
elif chart_view == "Bar Chart":
    try:
        import plotly.express as px
        fig = px.bar(filtered_df, x='date', y=['arrivals_male', 'arrivals_female'],
                     title=f'Arrivals by Gender in {selected_country}',
                     labels={'date': 'Date', 'value': 'Number of Arrivals', 'variable': 'Gender'},
                     color_discrete_map={'arrivals_male': 'blue', 'arrivals_female': 'red'})
        st.plotly_chart(fig)
    except ImportError:
        st.error("This feature requires the Plotly library. Please install it by running `pip install plotly`.")
