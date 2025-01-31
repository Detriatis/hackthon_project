import numpy as np
import matplotlib.pyplot as plt
from .simulator_base import SimulatorBase

"""
Each function in this module generates a random farm size within real-life limits with UK parameters.
The idea is to import these functions and use them to generate x farms/generators in the main code.
"""

class GasPowerSimulator(SimulatorBase):
    """
    Simulates gas power generation for a gas power plant.
        
    Parameters
    ----------
    hours : int, optional
        The number of hours for which power generation is simulated (default is 24).
        
    """
    
    def __init__(self, time_range):
        super().__init__(time_range) 
    
    def power_output(self):
        """
        Calculate the hourly power output and cost of a gas power plant.

        Returns
        -------
        tuple
            A tuple containing:
            - peak_power (int): Peak power output in kW.
            - power_outputs (ndarray): Hourly power output in kW.
            - cost_outputs (ndarray): Hourly maintenance costs in USD.
            - capital_cost (float): Total capital cost in USD.
        """
        self.hours = self.time_range

        peak_power = self.skewed_random(410, 2200) * 1000  # Peak power in kW
        
        # Gas plants provide steady power with minimal variation
        power_outputs = np.full(self.hours, peak_power)
        
        capital_cost = peak_power * 500  # Example: $500 per kW capacity
        maintenance_cost_per_mwh = 50  # Higher O&M cost compared to renewables
        
        cost_outputs = (power_outputs / 1000) * (maintenance_cost_per_mwh * 1000) 
        

        self.power_outputs = power_outputs / 1e6 
        self.capital_cost = capital_cost
        self.cost_outputs = cost_outputs
        self.peak_power = peak_power
        # self.plot_data()
    
    def plot_data(self):
        """
        Simulate and plot the hourly power output and cost of a gas power plant.

        Returns
        -------
        tuple
            A tuple containing:
            - power_outputs (ndarray): Hourly power output in kW.
            - cost_outputs (ndarray): Hourly maintenance costs in USD.
        """
        savepath = "../../data/figures/gaspowerplantoutputs.png"
        title = f'Hourly Power Output for {self.peak_power // 1000} MW Gas Power Plant'
        label = 'Power output for gas power plant'
        self.plot_power_data(title, label=label, savepath=savepath)

