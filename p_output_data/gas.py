import numpy as np
import matplotlib.pyplot as plt

"""Each function in supply files generates a random farm size within real-life limits with UK params.
Idea is to import these functions and use them to generate x farms/generators in main code"""

# Function to generate a skewed random number, favoring higher values
# Based on real UK gas power plants

def skewed_random(low, high, skew_factor=0.65):
    return int(low + (high - low) * np.random.beta(skew_factor * 5, (1 - skew_factor) * 5))

# Gas power plant model based on UK gas power plants ranging from 0.41GW to 2.2GW

def gas_power_plant_output(hours=24):
    """Calculate the hourly power output and cost of a gas power plant."""
    peak_power = skewed_random(410, 2200) * 1000  # Peak power in kW
    
    # Gas plants provide steady power with minimal variation
    power_outputs = np.full(hours, peak_power)
    
    capital_cost = peak_power * 500  # Example: $500 per kW capacity
    maintenance_cost_per_mwh = 50  # Higher O&M cost compared to renewables
    
    cost_outputs = (power_outputs / 1000) * maintenance_cost_per_mwh
    
    return peak_power, power_outputs, cost_outputs, capital_cost

def gas_power_plant_simulation(hours=24):
    """Simulate and plot the hourly power output and cost of a gas power plant."""
    peak_power, power_outputs, cost_outputs, capital_cost = gas_power_plant_output(hours)
    title = f'Hourly Power Output for {peak_power // 1000} MW Gas Power Plant'
    
    # Plot the power output over time
    plt.figure(figsize=(10, 5))
    plt.plot(range(hours), power_outputs, marker='o', linestyle='-', label='Gas Power Plant Output')
    plt.xlabel('Hour')
    plt.ylabel('Power Output (kW)')
    plt.title(title)
    plt.legend()
    plt.grid()
    plt.show()
    
    # Print cost information
    print(f'Total Capital Cost: ${capital_cost:,}')
    print(f'Hourly Cost Array: {cost_outputs}')
    print(f'Hourly Power Output Array: {power_outputs}')
    
    return power_outputs, cost_outputs

# Example: Simulate a gas power plant over 24 hours
gas_power_plant_simulation(hours=24)