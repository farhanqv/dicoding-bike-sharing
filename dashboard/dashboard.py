import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from scipy.stats import linregress
sns.set(style='dark')

all_main_df = pd.read_csv("main_data.csv")

datetime_columns = ["dteday"]

for column in datetime_columns:
    all_main_df[column] = pd.to_datetime(all_main_df[column])

min_date = all_main_df["dteday"].min()
max_date = all_main_df["dteday"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    #st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_main_df[(all_main_df["dteday"] >= str(start_date)) & 
                (all_main_df["dteday"] <= str(end_date))]


st.header('BikeSharing Dashboard')

st.subheader('Daily Rentals')
 
total_rentals = main_df['cnt'].sum()
st.metric("Total rentals", value=total_rentals)
 

tab1, tab2, tab3 = st.tabs(["Total Rentals", "Registered Users", "Casual Users"])

# Tab 1: Total Count
with tab1:
    st.header("Total Count Over Time")
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(
        main_df["dteday"],
        main_df["cnt"],
        marker='o',
        linewidth=2,
        color="#90CAF9",
        label='Total Count'
    )
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
    ax.legend(fontsize=15)
    st.pyplot(fig)

# Tab 2: Registered Users
with tab2:
    st.header("Registered Users Over Time")
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(
        main_df["dteday"],
        main_df["registered"],
        marker='o',
        linewidth=2,
        color="#FF4081",
        label='Registered Users'
    )
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
    ax.legend(fontsize=15)
    st.pyplot(fig)

# Tab 3: Casual Users
with tab3:
    st.header("Casual Users Over Time")
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(
        main_df["dteday"],
        main_df["casual"],
        marker='o',
        linewidth=2,
        color="#FFAB40",
        label='Casual Users'
    )
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
    ax.legend(fontsize=15)
    st.pyplot(fig)


st.subheader("Customer Types")

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

fig, ax = plt.subplots(figsize=(20, 10))

types_df = main_df[['casual', 'registered']].sum().reset_index()
types_df.columns = ['user_type', 'rental_count']


sns.barplot(
    x="user_type", 
    y="rental_count",
    data=types_df,
    palette=colors,
    ax=ax
)
ax.set_title("",loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)


st.subheader('Bike Rentals Analysis')

tab1, tab2 = st.tabs(["Temperature vs. Rentals", "Feels-Like Temperature vs. Rentals"])

# Tab 1: Temperature vs. Total Rentals
with tab1:
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.set_title("Average Total Bike Rentals vs. Temperature", loc="center", fontsize=15)
    sns.scatterplot(data=main_df, x='temp_actual', y='cnt', ax=ax, color='blue', alpha=0.6)
    ax.set_xlabel('Temperature (°C)')
    ax.set_ylabel('Avg. Total Rentals')

    # Add a regression line
    slope, intercept, r_value, p_value, std_err = linregress(main_df['temp_actual'], main_df['cnt'])
    ax.plot(main_df['temp_actual'], slope * main_df['temp_actual'] + intercept, color='red', label='Trend Line')
    ax.legend()

    st.pyplot(fig)

# Tab 2: Feels-Like Temperature vs. Total Rentals
with tab2:
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.set_title("Average Total Bike Rentals vs. Feels-Like Temperature", loc="center", fontsize=15)
    sns.scatterplot(data=main_df, x='atemp_actual', y='cnt', ax=ax, color='green', alpha=0.6)
    ax.set_xlabel('Feels-Like Temperature (°C)')
    ax.set_ylabel('Avg. Total Rentals')

    # Add a regression line
    slope, intercept, r_value, p_value, std_err = linregress(main_df['atemp_actual'], main_df['cnt'])
    ax.plot(main_df['atemp_actual'], slope * main_df['atemp_actual'] + intercept, color='red', label='Trend Line')
    ax.legend()

    st.pyplot(fig)