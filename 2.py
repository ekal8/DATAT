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
country_mapping = pd.read_csv('country_mapping.csv')  # Load your country mapping file
df = df.merge(country_mapping, left_on='country', right_on='code', how='right')
df.drop(columns=['country'], inplace=True)
df.rename(columns={'name': 'country'}, inplace=True)

# Create a Streamlit app
st.title('Arrivals Dashboard')

# Calculate the sum of all arrivals in the DataFrame and convert it to an integer
total_all_arrivals = int(df['arrivals'].sum())

# Display the total arrivals using Streamlit
st.write("### Total Arrivals:", total_all_arrivals,"Migrans from around the world")

# Dropdown menu to select a country
selected_country = st.selectbox('Select a Country', df['country'].unique())

# Filter the data for the selected country
filtered_df = df[df['country'] == selected_country]

# Add option to change view to graphical
chart_view = st.radio("Select Chart View", ("Line Chart", "Bar Chart", "Data Frame"))

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
# Display data frame and summary statistics
elif chart_view == "Data Frame":

     # Convert numerical columns to integers
    integer_columns = ['arrivals', 'arrivals_male', 'arrivals_female']
    for col in integer_columns:
        filtered_df[col] = filtered_df[col].astype(int)
    
    st.write(filtered_df)


    # Show the number of people entering the selected country
    total_arrivals = filtered_df['arrivals'].sum()
    st.write("### Total Arrivals:", total_arrivals)
    
    # Show arrivals by gender
    st.write("### Arrivals by Gender:")
    st.write("Male:", filtered_df['arrivals_male'].sum())
    st.write("Female:", filtered_df['arrivals_female'].sum())

# Interactive map visualization
st.header("Interactive Map Visualization")
st.write("Here's an interactive map showing the geographical distribution of arrivals:")
fig = px.scatter_geo(filtered_df, locations="country", locationmode="country names", color="arrivals",
                     hover_name="country", size="arrivals", projection="natural earth")
st.plotly_chart(fig)

# Statistical analysis
st.header("Statistical Analysis")
# Round summary statistics to two decimal places
summary_stats = filtered_df.describe().round(2)

for col in summary_stats.columns:
    if summary_stats[col].dtype == "float64":
        summary_stats[col] = summary_stats[col].apply(lambda x: int(x) if x.is_integer() else x)

# Display summary statistics
st.write(summary_stats)
