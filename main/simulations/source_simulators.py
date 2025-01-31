"""
source_simulators.py
=====================

This module contains classes for simulating different types of power generators:
solar, gas, and wind. Each class inherits from a common base class, 
`SimulatorBase`, and implements its own logic for generating hourly power 
outputs, capital costs, and maintenance costs.

Classes
-------
SolarPowerSimulator
    Simulates solar power generation over a specified time range.
GasPowerSimulator
    Simulates gas power generation over a specified time range.
WindPowerSimulator
    Simulates wind power generation (onshore or offshore) over a specified time range.

Examples
--------
>>> from power_generators import SolarPowerSimulator, GasPowerSimulator, WindPowerSimulator
>>> # Solar
>>> solar_sim = SolarPowerSimulator(time_range=24)
>>> solar_sim.power_output()
>>> solar_sim.plot_data()
>>>
>>> # Gas
>>> gas_sim = GasPowerSimulator(time_range=24)
>>> gas_sim.power_output()
>>> gas_sim.plot_data()
>>>
>>> # Wind (onshore)
>>> wind_sim = WindPowerSimulator(time_range=24, offshore=False)
>>> wind_sim.power_output()
>>> wind_sim.plot_figure()
"""

import numpy as np
import matplotlib.pyplot as plt
from .simulator_base import SimulatorBase


class SolarPowerSimulator(SimulatorBase):
    """
    Simulates solar power generation for a solar farm.

    Parameters
    ----------
    time_range : int
        The number of hours over which to simulate power generation.

    Attributes
    ----------
    time_range : int
        The number of hours for the simulation.
    num_panels : int
        The number of solar panels in the farm (calculated).
    power_outputs : ndarray of shape (time_range,)
        Hourly power output in MW (calculated).
    cost_outputs : ndarray of shape (time_range,)
        Hourly maintenance costs in USD (calculated).
    capital_cost : float
        Total capital cost in USD for the solar farm.
    """

    def __init__(self, time_range):
        """
        Initialize the solar power simulator.

        Parameters
        ----------
        time_range : int
            The number of hours for which power generation is simulated.
        """
        super().__init__(time_range)

    def power_output(self):
        """
        Calculate the hourly power output and cost of a solar farm.

        This method calculates:
          - The number of solar panels based on a randomly generated peak power.
          - Hourly power output based on a sine-wave-like irradiance pattern.
          - Maintenance costs based on the generated power.
          - The total capital cost of the farm.

        Returns
        -------
        tuple
            A tuple containing:
            num_panels : int
                Number of solar panels in the farm.
            power_outputs : ndarray
                Hourly power output in kW.
            cost_outputs : ndarray
                Hourly maintenance costs in USD.
            capital_cost : float
                Total capital cost in USD.
        """
        self.hours = self.time_range
        peak_power = self.skewed_random(72, 840) * 1000  # Peak power in kW
        num_panels = int(peak_power / 0.4)  # Approximate assumption: 400W per panel

        # Generate solar irradiance pattern (stochastic sine wave for daylight hours)
        time = np.linspace(0, np.pi, self.hours)  # Simulating a daily solar cycle
        irradiance = np.maximum(0, np.sin(time) + np.random.normal(0, 0.05, self.hours))

        # Power output (kW) based on irradiance
        power_outputs = (peak_power * irradiance) 

        # Capital cost and maintenance cost
        capital_cost = num_panels * 300       # Example: $300 per panel
        
        lcoe = 45
        cost_outputs = self.get_costs(power_outputs, lcoe)

        cost_outputs = np.full_like(power_outputs, lcoe)
        # Store internal states
        self.num_panels = num_panels
        # Convert power_outputs to MW for internal storage/plotting
        self.power_outputs = power_outputs 
        self.cost_outputs = cost_outputs
        self.capital_cost = capital_cost

        return num_panels, power_outputs, cost_outputs, capital_cost

    def plot_data(self):
        """
        Simulate and plot the hourly power output and cost of a solar farm.

        This method uses the existing power output data (generated by
        `power_output`) or regenerates them if they do not exist. It
        then plots the results and saves the figure to a file.

        Returns
        -------
        tuple
            A tuple containing:
            power_outputs : ndarray
                Hourly power output in kW.
            cost_outputs : ndarray
                Hourly maintenance costs in USD.
        """
        savepath = '../../data/figures/solarpower.png'
        title = f'Hourly Power Output for {self.num_panels} Panel Solar Farm'
        label = 'Hourly power output for solar farm'

        self.plot_power_data(title, label, savepath)
        return self.power_outputs, self.cost_outputs


class GasPowerSimulator(SimulatorBase):
    """
    Simulates gas power generation for a gas power plant.

    Parameters
    ----------
    time_range : int
        The number of hours over which to simulate power generation.

    Attributes
    ----------
    time_range : int
        The number of hours for the simulation.
    peak_power : int
        The peak power output of the plant in kW (calculated).
    power_outputs : ndarray of shape (time_range,)
        Hourly power output in MW (calculated).
    cost_outputs : ndarray of shape (time_range,)
        Hourly maintenance costs in USD (calculated).
    capital_cost : float
        Total capital cost in USD for the gas power plant.
    """

    def __init__(self, time_range):
        """
        Initialize the gas power simulator.

        Parameters
        ----------
        time_range : int
            The number of hours for which power generation is simulated.
        """
        super().__init__(time_range)

    def power_output(self):
        """
        Calculate the hourly power output and cost of a gas power plant.

        This method:
          - Randomly determines a peak power rating for the gas plant.
          - Assumes constant power output at that peak rating for all hours.
          - Calculates capital cost and hourly maintenance cost.

        Returns
        -------
        tuple
            A tuple containing:
            peak_power : int
                Peak power output in kW.
            power_outputs : ndarray
                Hourly power output in kW.
            cost_outputs : ndarray
                Hourly maintenance costs in USD.
            capital_cost : float
                Total capital cost in USD.
        """
        self.hours = self.time_range

        peak_power = self.skewed_random(410, 2200) * 1000  # Peak power in kW

        # Gas plants typically run at a constant output (no variation)
        power_outputs = np.full(self.hours, peak_power)

        # Costs
        capital_cost = peak_power * 500        # Example: $500 per kW capacity
        lcoe = 80    # dollar per kw hour
        
        cost_outputs = self.get_costs(power_outputs, lcoe) 
        cost_outputs = np.full_like(power_outputs, lcoe)
        # Store internal states
        self.power_outputs = power_outputs
        self.capital_cost = capital_cost
        self.cost_outputs = cost_outputs
        self.peak_power = peak_power

        return peak_power, power_outputs, cost_outputs, capital_cost

    def plot_data(self):
        """
        Simulate and plot the hourly power output and cost of a gas power plant.

        This method uses the existing power output data (generated by
        `power_output`) or regenerates them if they do not exist. It
        then plots the results and saves the figure to a file.

        Returns
        -------
        tuple
            A tuple containing:
            power_outputs : ndarray
                Hourly power output in kW.
            cost_outputs : ndarray
                Hourly maintenance costs in USD.
        """
        savepath = "../../data/figures/gaspowerplantoutputs.png"
        title = f'Hourly Power Output for {self.peak_power // 1000} MW Gas Power Plant'
        label = 'Power output for gas power plant'

        self.plot_power_data(title, label=label, savepath=savepath)
        return self.power_outputs, self.cost_outputs


class WindPowerSimulator(SimulatorBase):
    """
    Simulates wind power generation for onshore or offshore wind farms.

    Parameters
    ----------
    time_range : int
        The number of hours over which to simulate power generation.
    offshore : bool
        If True, simulates an offshore wind farm; otherwise, an onshore wind farm.

    Attributes
    ----------
    time_range : int
        The number of hours for the simulation.
    offshore : bool
        Indicates if the simulation is for an offshore (True) or onshore (False) wind farm.
    num_turbines : int
        The number of turbines in the wind farm (calculated).
    wind_speeds : ndarray of shape (time_range,)
        Hourly wind speeds in m/s (generated).
    power_outputs : ndarray of shape (time_range,)
        Hourly power output in MW (calculated).
    cost_outputs : ndarray of shape (time_range,)
        Hourly maintenance costs in USD (calculated).
    capital_cost : float
        Total capital cost in USD for the wind farm.
    """

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
        Calculate the hourly power output and cost of a wind farm.

        The method:
          - Randomly determines the number of turbines.
          - Generates wind speed data for each hour.
          - Applies a power curve approximation where output is 0 below 
            a certain cut-in speed and above a cut-out speed (3.5 m/s and 
            25 m/s, respectively), and is limited by the rated speed (13 m/s).
          - Calculates hourly maintenance cost.
          - Calculates total capital cost assuming a fixed cost per turbine.

        Returns
        -------
        tuple
            A tuple containing:
            num_turbines : int
                Number of turbines in the wind farm.
            wind_speeds : ndarray
                Hourly wind speeds in m/s.
            power_outputs : ndarray
                Hourly power output in kW.
            cost_outputs : ndarray
                Hourly maintenance costs in USD.
            capital_cost : float
                Total capital cost in USD.
        """
        hours = self.time_range
        num_turbines = self.skewed_random(20, 150)  # Random count of turbines
        wind_speeds = np.clip(np.random.normal(8, 2, hours), 0, None)
        power_outputs = np.zeros(hours)
        cost_outputs = np.zeros(hours)

        # Costs
        capital_cost = num_turbines * 1_000_000      # $1M per turbine
        maintenance_cost_per_mwh = 10               # $10 per MWh

        # Calculate power output based on wind speed ranges
        for i in range(hours):
            if wind_speeds[i] < 3.5 or wind_speeds[i] >= 25:
                power_outputs[i] = 0
            elif wind_speeds[i] >= 13:
                power_outputs[i] = 2300
            else:
                # Assume a cubic relationship up to rated speed
                power_outputs[i] = ((2300 / 13**3) * wind_speeds[i]**3) 
        if self.offshore:
            lcoe = 75
        else:
            lcoe = 35

        cost_outputs = self.get_costs(power_outputs, lcoe)
        # Scale by the number of turbines
        power_outputs *= num_turbines
        cost_outputs *= num_turbines
        cost_outputs = np.full_like(power_outputs, lcoe)

        # Store internal states
        self.num_turbines = num_turbines
        self.wind_speeds = wind_speeds
        # Convert kW to MW for internal storage/plotting
        self.power_outputs = power_outputs
        self.cost_outputs = cost_outputs
        self.capital_cost = capital_cost

        return num_turbines, wind_speeds, power_outputs, cost_outputs, capital_cost

    def plot_figure(self):
        """
        Calculate and plot the hourly power output and cost of a wind farm.

        This method uses the existing power output data (generated by
        `power_output`) or regenerates them if they do not exist. It
        then plots the results and saves the figure to a file. The plot
        title indicates whether it is an onshore or offshore wind farm.

        Returns
        -------
        tuple
            A tuple containing:
            power_outputs : ndarray
                Hourly power output in kW.
            cost_outputs : ndarray
                Hourly maintenance costs in USD.
        """
        savepath = "../../data/figures/windoutput.png"

        if self.offshore:
            title = f'Hourly Power Output for {self.num_turbines} Turbine Offshore Wind Farm'
            label = 'Predicted offshore windpower'
        else:
            title = f'Hourly Power Output for {self.num_turbines} Turbine Onshore Wind Farm'
            label = 'Predicted onshore windpower'

        self.plot_power_data(title, label, savepath)
        return self.power_outputs, self.cost_outputs
