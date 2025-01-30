import numpy as np
import matplotlib.pyplot as plt

"""Each function in supply files generates a random farm size within real-life limits with UK params.
Idea is to import these functions and use them to generate x farms/generators in main code"""

# Function to generate a skewed random number of turbines, favoring higher values
def skewed_random(low, high, skew_factor=0.65):
    return int(low + (high - low) * np.random.beta(skew_factor * 5, (1 - skew_factor) * 5))

# Onshore wind turbine: Siemens SWT-2.3-93
# More details: https://www.thewindpower.net/turbine_en_22_siemens_swt-2.3-93.php
# Rated Power: 2.3 MW, Rotor Diameter: 93m, Cut-in Speed: 3.5 m/s, Cut-out Speed: 25 m/s

def turbine_power_output_onshore(hours=24):
    """Calculate the hourly power output and cost of an onshore wind farm."""
    num_turbines = skewed_random(20, 150)
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
        
        cost_outputs[i] = (power_outputs[i] / 1000) * maintenance_cost_per_mwh
    
    power_outputs *= num_turbines
    cost_outputs *= num_turbines
    
    return num_turbines, wind_speeds, power_outputs, cost_outputs, capital_cost

# Offshore wind turbine: Siemens SWT-3.6-120
# More details: https://www.thewindpower.net/turbine_en_79_siemens_swt-3.6-120.php
# Rated Power: 3.6 MW, Rotor Diameter: 120m, Cut-in Speed: 3.5 m/s, Cut-out Speed: 25 m/s

def turbine_power_output_offshore(hours=24):
    """Calculate the hourly power output and cost of an offshore wind farm."""
    num_turbines = skewed_random(10, 200)
    wind_speeds = np.clip(np.random.normal(9, 2, hours), 0, None)  # Offshore avg wind speed slightly higher
    power_outputs = np.zeros(hours)
    cost_outputs = np.zeros(hours)
    
    capital_cost = num_turbines * 1_500_000  # Example: $1.5M per turbine
    maintenance_cost_per_mwh = 15  # Example: $15 per MWh
    
    for i in range(hours):
        if wind_speeds[i] < 3.5:
            power_outputs[i] = 0
        elif wind_speeds[i] >= 25:
            power_outputs[i] = 0
        elif wind_speeds[i] >= 14:
            power_outputs[i] = 3600
        else:
            power_outputs[i] = (3600 / 14**3) * wind_speeds[i]**3
        
        cost_outputs[i] = (power_outputs[i] / 1000) * maintenance_cost_per_mwh
    
    power_outputs *= num_turbines
    cost_outputs *= num_turbines
    
    return num_turbines, wind_speeds, power_outputs, cost_outputs, capital_cost

def wind_farm_output(hours=24, offshore=False):
    """Calculate and plot the hourly power output and cost of a wind farm."""
    if offshore:
        num_turbines, wind_speeds, power_outputs, cost_outputs, capital_cost = turbine_power_output_offshore(hours)
        title = f'Hourly Power Output for {num_turbines} Turbine Offshore Farm'
    else:
        num_turbines, wind_speeds, power_outputs, cost_outputs, capital_cost = turbine_power_output_onshore(hours)
        title = f'Hourly Power Output for {num_turbines} Turbine Onshore Wind farms'
    
    # Plot the power output over time
    plt.figure(figsize=(10, 5))
    plt.plot(range(hours), power_outputs, marker='o', linestyle='-', label='Wind Farm Power Output')
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

# Example: Simulate an onshore wind farm over 24 hours
wind_farm_output(hours=24, offshore=False)

# Example: Simulate an offshore wind farm over 24 hours
wind_farm_output(hours=24, offshore=True)