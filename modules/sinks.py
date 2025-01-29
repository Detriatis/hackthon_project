# sinks.py

class Sink:
    def __init__(self, name, demand_profile, lcoe_requirement):
        """
        Represents a power demand location (e.g., city, town).
        
        :param name: Name of the sink
        :param demand_profile: A list or function representing hourly power demand (MW)
        :param lcoe_requirement: Minimum required Levelized Cost of Electricity ($/MWh)
        """
        self.name = name
        self.demand_profile = demand_profile
        self.lcoe_requirement = lcoe_requirement
    
    def get_demand(self, hour):
        """Returns power demand at a specific hour."""
        return self.demand_profile[hour] if isinstance(self.demand_profile, list) else self.demand_profile(hour)
