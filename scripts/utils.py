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

def ploat_temperature_analysis(data_frame):
    # Scatter plots: RH vs Temperature, RH vs Solar Radiation
    plt.figure(figsize=(16, 10))

    # RH vs TModA
    plt.subplot(2, 2, 1)
    sns.scatterplot(x=data_frame['RH'], y=data_frame['TModA'])
    plt.title('Relative Humidity vs TModA')
    plt.xlabel('Relative Humidity (%)')
    plt.ylabel('Temperature (TModA)')

    # RH vs TModB
    plt.subplot(2, 2, 2)
    sns.scatterplot(x=data_frame['RH'], y=data_frame['TModB'])
    plt.title('Relative Humidity vs TModB')
    plt.xlabel('Relative Humidity (%)')
    plt.ylabel('Temperature (TModB)')

    # RH vs GHI
    plt.subplot(2, 2, 3)
    sns.scatterplot(x=data_frame['RH'], y=data_frame['GHI'])
    plt.title('Relative Humidity vs GHI')
    plt.xlabel('Relative Humidity (%)')
    plt.ylabel('Global Horizontal Irradiance (GHI)')

    # RH vs DNI
    plt.subplot(2, 2, 4)
    sns.scatterplot(x=data_frame['RH'], y=data_frame['DNI'])
    plt.title('Relative Humidity vs DNI')
    plt.xlabel('Relative Humidity (%)')
    plt.ylabel('Direct Normal Irradiance (DNI)')

    plt.tight_layout()
    plt.show()

    # Correlation matrix for RH, Temperature, and Solar Radiation components
    corr_matrix = data_frame[['RH', 'TModA', 'TModB', 'GHI', 'DNI', 'DHI']].corr()

    plt.figure(figsize=(10, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Correlation Heatmap: RH, Temperature, and Solar Radiation Components')
    plt.show()

    # Trend Analysis with Line Plots
    plt.figure(figsize=(16, 10))

    # RH and TModA over time
    plt.subplot(2, 1, 1)
    plt.plot(data_frame['Timestamp'], data_frame['RH'], label='Relative Humidity (%)', color='blue', alpha=0.6)
    plt.plot(data_frame['Timestamp'], data_frame['TModA'], label='Temperature (TModA)', color='red', alpha=0.6)
    plt.legend(loc='upper right')
    plt.title('Relative Humidity and TModA Over Time')
    plt.xlabel('Time')
    plt.ylabel('Values')

    # RH and GHI over time
    plt.subplot(2, 1, 2)
    plt.plot(data_frame['Timestamp'], data_frame['RH'], label='Relative Humidity (%)', color='blue', alpha=0.6)
    plt.plot(data_frame['Timestamp'], data_frame['GHI'], label='Global Horizontal Irradiance (GHI)', color='green', alpha=0.6)
    plt.legend(loc='upper right')
    plt.title('Relative Humidity and GHI Over Time')
    plt.xlabel('Time')
    plt.ylabel('Values')

    plt.tight_layout()
    plt.show()

