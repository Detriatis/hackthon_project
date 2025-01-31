from .simulator_base import SimulatorBase
import numpy as np
import matplotlib.pyplot as plt

"""
Each function in this module generates a random farm size within real-life limits with UK parameters.
The idea is to import these functions and use them to generate x farms/generators in the main code.
"""

class WindPowerSimulator(SimulatorBase):
    """Simulates wind power generation for onshore and offshore wind farms."""
    
    def __init__(self, time_range, offshore):
        """
        Initialize the wind power simulator.

        Parameters
        ----------
        time_range : int
            The number of hours for which power generation is simulated.
        offshore : bool
            If True, simulates an offshore wind farm; otherwise, an onshore wind farm.
        """
        super().__init__(time_range)
        self.offshore = offshore
    
    def power_output(self):
        """
        Calculate the hourly power output and cost of an onshore wind farm.

        Returns
        -------
        tuple
            A tuple containing:
            - num_turbines (int): Number of turbines in the wind farm.
            - wind_speeds (ndarray): Hourly wind speeds in m/s.
            - power_outputs (ndarray): Hourly power output in kW.
            - cost_outputs (ndarray): Hourly maintenance costs in USD.
            - capital_cost (float): Total capital cost in USD.
        """
        hours = self.time_range 
        num_turbines = self.skewed_random(20, 150)
        wind_speeds = np.clip(np.random.normal(8, 2, hours), 0, None)
        power_outputs = np.zeros(hours)
        cost_outputs = np.zeros(hours)
        
        capital_cost = num_turbines * 1_000_000  # Example: $1M per turbine
        maintenance_cost_per_mwh = 10  # Example: $10 per MWh
        
        for i in range(hours):
            if wind_speeds[i] < 3.5:
                power_outputs[i] = 0
            elif wind_speeds[i] >= 25:
                power_outputs[i] = 0
            elif wind_speeds[i] >= 13:
                power_outputs[i] = 2300
            else:
                power_outputs[i] = (2300 / 13**3) * wind_speeds[i]**3
            
            cost_outputs[i] = (power_outputs[i] / 1000) * (maintenance_cost_per_mwh * 1000) 
        
        power_outputs *= num_turbines
        cost_outputs *= num_turbines
        
        self.num_turbines = num_turbines
        self.wind_speeds = wind_speeds
        self.power_outputs = power_outputs / 1e6
        self.cost_outputs = cost_outputs
        self.capital_cost = capital_cost
        self.plot_figure()

    def plot_figure(self):
        """
        Calculate and plot the hourly power output and cost of a wind farm.

        Returns
        -------
        tuple
            A tuple containing:
            - power_outputs (ndarray): Hourly power output in kW.
            - cost_outputs (ndarray): Hourly maintenance costs in USD.
        """
        savepath = "../../data/figures/windoutput.png"
        
        if self.offshore:
            title = f'Hourly Power Output for {self.num_turbines} Turbine Offshore Farm'
            label = 'Predicted windpower'
            # self.plot_power_data(title, label, savepath)
        else:
            title = f'Hourly Power Output for {self.num_turbines} Turbine Onshore Wind Farms'
            label = 'Predicted windpower'
            # self.plot_power_data(title, label, savepath)
        
