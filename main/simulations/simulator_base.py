from abc import abstractmethod
import numpy as np
import matplotlib.pyplot as plt 

class SimulatorBase():
    """
    Simulator base class for source node power simulation.

    Parameters
    ----------
    time_range : float, optional
        The time frame over which to generate simulator values

    Attributes
    ----------
    time_range : float
        The time frame for the simulation
    power_outputs : np.array
        Array of power output values over time range
    cost_outputs : np.array
        Array of the power costs over time range 
    capital_costs : float 
        Initial cost for infrastructure 
    """
    
    def __init__(self, time_range: np.float = 24.00): 
        self.time_range = time_range
        self.power_outputs = None
        self.cost_outputs = None
        self.capital_cost = None 

    @staticmethod
    def skewed_random(low, high, skew_factor=0.65):
        """
        Generate a skewed random number of solar panels, favoring higher values.

        Parameters
        ----------
        low : int
            Minimum value.
        high : int
            Maximum value.
        skew_factor : float, optional
            Skew factor, default is 0.65.

        Returns
        -------
        int
            A randomly generated integer within the specified range.
        """
        return int(low + (high - low) * np.random.beta(skew_factor * 5, (1 - skew_factor) * 5))
 
    @classmethod  
    def plot_power_data(self, title, label, savepath):
                
        plt.figure(figsize=(10, 5))
        plt.plot(range(self.hours), self.power_outputs, marker='o', linestyle='-', label=label)
        plt.xlabel('Hour')
        plt.ylabel('Power Output (kW)')
        plt.title(title)
        plt.legend()
        plt.grid()
        plt.savefig(savepath, format='png')
        
        # Print cost information
        print(f'Total Capital Cost: ${self.capital_cost:,}')
        print(f'Hourly Cost Array: {self.cost_outputs}')
        print(f'Hourly Power Output Array: {self.power_outputs}')

    @abstractmethod
    def compute_output(self) -> tuple[np.array, np.array]:
        """
        Compute the output for a given simulator

        Returns
        -------
        Tuple of [np.array, np.array]
            Tuple of arrays corresponding to the power output
            and associated power cost  
        """
        return 
    
     

        