import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pandas.plotting import scatter_matrix

def plot_time_series(df):
    # Ensure 'Timestamp' column is in datetime format
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    # Plot GHI, DNI, DHI, and Tamb over time
    plt.figure(figsize=(10,6))
    plt.plot(df['Timestamp'], df['GHI'], label='GHI')
    plt.plot(df['Timestamp'], df['DNI'], label='DNI')
    plt.plot(df['Timestamp'], df['DHI'], label='DHI')
    plt.plot(df['Timestamp'], df['Tamb'], label='Tamb')
    plt.xlabel('Timestamp')
    plt.ylabel('Values')
    plt.title('Change of Variables over Time')
    plt.legend(loc='upper right')
    plt.xticks(rotation=45)
    plt.tight_layout() 
    plt.show()

def ploat_correlation_analysis(data_frame):
    # Limit the data to the first 1000 rows
    data_frame = data_frame.head(1000)
    
    # Define columns related to solar radiation and temperature
    solar_temperature_cols = ['GHI', 'DNI', 'DHI', 'TModA', 'TModB']
    wind_measurement_cols = ['WS', 'WSgust', 'WD']

    # Compute the correlation matrix for solar radiation and temperature columns
    correlation_matrix = data_frame[solar_temperature_cols].corr()

    # Plot the heatmap for the correlation matrix
    plt.figure(figsize=(10, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Correlation Heatmap: Solar Radiation and Temperature')
    plt.show()

    # Generate a pair plot to visualize relationships between solar radiation and temperature measures
    sns.pairplot(data_frame[solar_temperature_cols])
    plt.suptitle('Pair Plot: Solar Radiation and Temperature Measures', y=1.02)
    plt.show()

    # Create a scatter matrix for wind measurements and solar irradiance
    scatter_matrix(data_frame[wind_measurement_cols + ['GHI', 'DNI', 'DHI']], figsize=(12, 12), diagonal='kde', alpha=0.6)
    plt.suptitle('Scatter Matrix: Wind Conditions and Solar Irradiance', y=1.02)
    plt.show()

def ploat_wind_analysis(data, ws_col='WS', wd_col='WD', title='Wind Speed and Direction Analysis'):
    # Convert wind direction from degrees to radians
    data['Wind_Direction_Radians'] = np.deg2rad(data[wd_col])

    # Create a polar plot
    plt.figure(figsize=(10, 8))
    ax = plt.subplot(111, polar=True)
    
    # Scatter plot of wind speed and direction
    sc = ax.scatter(data['Wind_Direction_Radians'], data[ws_col], 
                    c=data[ws_col], cmap='viridis', alpha=0.75)

    # Add a colorbar for wind speed
    plt.colorbar(sc, label='Wind Speed (m/s)')

    # Set plot title and labels
    ax.set_title(title, va='bottom')
    ax.set_theta_zero_location('N')  # Set 0 degrees at North
    ax.set_theta_direction(-1)       # Set degrees to increase clockwise

    # Show the plot
    plt.show()

    # Analysis of variability in wind direction
    wind_direction_variability = data[wd_col].std()
    print(f"Wind Direction Variability (Standard Deviation): {wind_direction_variability:.2f} degrees")
