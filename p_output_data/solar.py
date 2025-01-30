import numpy as np
import matplotlib.pyplot as plt

"""Each function in supply files generates a random farm size within real-life limits with UK params.
Idea is to import these functions and use them to generate x farms/generators in main code"""

# Function to generate a skewed random number of solar panels, favoring higher values
# Based on real UK solar farms ranging from 72MW to 840MW

def skewed_random(low, high, skew_factor=0.65):
    return int(low + (high - low) * np.random.beta(skew_factor * 5, (1 - skew_factor) * 5))

# Solar farm model based on UK sun data
# Using realistic UK solar farm capacity distribution from 72MW to 840MW

def solar_farm_output(hours=24):
    """Calculate the hourly power output and cost of a solar farm."""
    peak_power = skewed_random(72, 840) * 1000  # Peak power in kW
    num_panels = int(peak_power / 0.4)  # Approximate assumption: 400W per panel
    
    # Generate solar irradiance pattern (stochastic sine wave for UK daylight hours)
    time = np.linspace(0, np.pi, hours)  # Simulating a daily solar cycle
    irradiance = np.maximum(0, np.sin(time) + np.random.normal(0, 0.05, hours))
    
    # Power output based on irradiance and peak power
    power_outputs = peak_power * irradiance
    
    capital_cost = num_panels * 300  # Example: $300 per panel
    maintenance_cost_per_mwh = 5  # Example: $5 per MWh
    
    cost_outputs = (power_outputs / 1000) * maintenance_cost_per_mwh
    
    return num_panels, power_outputs, cost_outputs, capital_cost

def solar_farm_simulation(hours=24):
    """Simulate and plot the hourly power output and cost of a solar farm."""
    num_panels, power_outputs, cost_outputs, capital_cost = solar_farm_output(hours)
    title = f'Hourly Power Output for {num_panels} Panel Solar Farm'
    
    # Plot the power output over time
    plt.figure(figsize=(10, 5))
    plt.plot(range(hours), power_outputs, marker='o', linestyle='-', label='Solar Farm Power Output')
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

# Example: Simulate a solar farm over 24 hours
solar_farm_simulation(hours=24)