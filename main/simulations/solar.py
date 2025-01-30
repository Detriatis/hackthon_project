import numpy as np
import matplotlib.pyplot as plt
from .simulator_base import SimulatorBase

"""
Each function in this module generates a random farm size within real-life limits with UK parameters.
The idea is to import these functions and use them to generate x farms/generators in the main code.
"""

class SolarPowerSimulator(SimulatorBase):
    """Simulates solar power generation for a solar farm."""
    
    def __init__(self, time_range):
        """
        Initialize the solar power simulator.

        Parameters
        ----------
        hours : int, optional
            The number of hours for which power generation is simulated (default is 24).
        """
        super().__init__(time_range)
       
    def power_output(self):
        """
        Calculate the hourly power output and cost of a solar farm.

        Returns
        -------
        tuple
            A tuple containing:
            - num_panels (int): Number of solar panels in the farm.
            - power_outputs (ndarray): Hourly power output in kW.
            - cost_outputs (ndarray): Hourly maintenance costs in USD.
            - capital_cost (float): Total capital cost in USD.
        """
        self.hours = self.time_range
        peak_power = self.skewed_random(72, 840) * 1000  # Peak power in kW
        num_panels = int(peak_power / 0.4)  # Approximate assumption: 400W per panel
        
        # Generate solar irradiance pattern (stochastic sine wave for UK daylight hours)
        time = np.linspace(0, np.pi, self.hours)  # Simulating a daily solar cycle
        irradiance = np.maximum(0, np.sin(time) + np.random.normal(0, 0.05, self.hours))
        
        # Power output based on irradiance and peak power
        power_outputs = peak_power * irradiance
        
        capital_cost = num_panels * 300  # Example: $300 per panel
        maintenance_cost_per_mwh = 5  # Example: $5 per MWh
        
        cost_outputs = (power_outputs / 1000) * (maintenance_cost_per_mwh * 1000) 

        self.num_panels = num_panels 
        self.power_outputs = power_outputs / 1e6
        self.cost_outputs = cost_outputs
        self.capital_cost = capital_cost
        self.plot_data() 
    
    def plot_data(self):
        """
        Simulate and plot the hourly power output and cost of a solar farm.

        Returns
        -------
        tuple
            A tuple containing:
            - power_outputs (ndarray): Hourly power output in kW.
            - cost_outputs (ndarray): Hourly maintenance costs in USD.
        """
        savepath = '../../data/figures/solarpower.png'
        title = f'Hourly Power Output for {self.num_panels} Panel Solar Farm'
        label = 'Hourly power output for panel solar farm'
        self.plot_power_data(title=title, label=label, savepath=savepath)

