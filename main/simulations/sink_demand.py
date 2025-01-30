import numpy as np
import matplotlib.pyplot as plt
import os
import random
from .simulator_base import SimulatorBase

class SinkPowerDemandSimulator(SimulatorBase):
    """Simulates power demand for a sink (consumer region)."""
    
    def __init__(self, time_range=24):
        """
        Initialize the sink power demand simulator.

        Parameters
        ----------
        time_range : int, optional
            The number of hours for which power demand is simulated (default is 24).
        """
        self.time_range = time_range
  

    def power_demand(self):
        """
        Generate the hourly power demand levels

        Returns
        -------
        ndarray
            Hourly power demand in MWh for a typical 24-hour period.
        """ 
        # Annual electricity consumption in GWh
        annual_demand_gwh = {
            "East Midlands": 19_459, "East of England": 26_130, "Greater London": 39_337,
            "North East": 10_573, "North West": 31_519, "South East": 37_655,
            "South West": 23_551, "Yorkshire and The Humber": 21_865, "West Midlands": 22_839,
            "Scotland": 24_976, "Wales": 13_524, "England": 232_927, "Great Britain": 274_801
        }
        
        #data: https://assets.publishing.service.gov.uk/media/5a7ca608e5274a2f304ef341/Sub-national_electricity_consumption_factsheet_2012.pdf
        # Step 1: Select a random region
        region = random.choice(list(annual_demand_gwh.keys()))
        
        # Step 2: Calculate the average hourly demand in GWh
        average_hourly_demand_gwh = annual_demand_gwh[region] / 8760  # Convert GWh/year to GWh/hour

        # Step 3: Generate a correctly oriented duck curve (afternoon peak)
        time = np.linspace(0, np.pi * 2, self.time_range)  # Simulate 24-hour cycle
        duck_curve = 0.9 + 1.1 * np.sin(time - np.pi/2) ** 3  # Peak in the afternoon

        # Scale so the mean of the distribution matches the correct value
        daily_demand = duck_curve / np.mean(duck_curve) * average_hourly_demand_gwh

        # Step 4: Apply stochastic variation (±5% random noise)
        noise = np.random.normal(1, 0.05, self.time_range)
        hourly_demand = daily_demand * noise

        # Step 5: Ensure no demand goes below 0.1× mean (prevents near-zero values)
        min_demand_threshold = 0.1 * average_hourly_demand_gwh
        hourly_demand = np.maximum(hourly_demand, min_demand_threshold)
        self.hourly_demand = hourly_demand 
        return hourly_demand


    def plot_data(self, hourly_demand):
        """
        Plot the hourly power demand.

        Parameters
        ----------
        hourly_demand : ndarray
            Hourly power demand in MWh.
        """
        # Plot settings
        savepath = '../../data/figures'
        os.makedirs(savepath, exist_ok=True)  # Ensure directory exists
        title = 'Hourly Power Demand'
        label = 'Hourly Power Demand (GWh)'

        # Create the figure
        plt.figure(figsize=(10, 5))
        plt.plot(range(24), hourly_demand, marker='o', linestyle='-', label=label)
        
        # Aesthetics
        plt.xlabel('Hour of the Day')
        plt.ylabel('Power Demand (GWh)')
        plt.title(title)
        plt.legend()
        plt.grid(True)
        
        # Save the figure
        filepath = os.path.join(savepath, 'power_demand.png')
        plt.savefig(filepath)
        plt.show()

        print("Hourly demand:", hourly_demand)


if __name__ == "__main__":
    simulator = SinkPowerDemandSimulator(time_range=24)
    hourly_demand = simulator.power_demand()  # Only returns demand now
    simulator.plot_data(hourly_demand)  # Pass only hourly_demand (region removed)
