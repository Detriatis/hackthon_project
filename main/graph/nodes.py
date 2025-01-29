class Node(): 
    def __init__(self, node_id): 
        self.node_id = node_id 
        self.connections = []


class SinkNode(Node): 
    def __init__(self, node_id, demand_profile, lcoe_requirement):
        """
        Represents a power demand location (e.g., city, town).
        
        :param name: Name of the sink
        :param demand_profile: A list or function representing hourly power demand (MW)
        :param lcoe_requirement: Minimum required Levelized Cost of Electricity ($/MWh)
        """
        super.__init__(node_id) 
        self.demand_profile = demand_profile
        self.lcoe_requirement = lcoe_requirement
    
    def get_demand(self, hour):
        """Returns power demand at a specific hour."""
        return self.demand_profile[hour] if isinstance(self.demand_profile, list) else self.demand_profile(hour)
    

class SourceNode(Node):
    def __init__(self, node_id, power_output, dispatchability, co2_per_mw, ramp_up_time, capital_cost, lcoe, deployment_time):
        """
        Base class for energy sources.
        
        :param name: Name of the source
        :param power_output: Function or list representing hourly power output (MW)
        :param dispatchability: Value between 0-1 indicating how flexible the source is
        :param co2_per_mw: CO2 emissions per MW generated
        :param ramp_up_time: Function defining ramp-up time behavior
        :param capital_cost: Initial investment cost
        :param lcoe: Levelized Cost of Electricity ($/MWh)
        :param deployment_time: Time required to deploy the 
        """
        super.__init__(node_id)
        self.power_output = power_output
        self.dispatchability = dispatchability
        self.co2_per_mw = co2_per_mw
        self.ramp_up_time = ramp_up_time
        self.capital_cost = capital_cost
        self.lcoe = lcoe
        self.deployment_time = deployment_time
    
    def get_power_output(self, hour):
        """Returns power output at a specific hour."""
        return self.power_output[hour] if isinstance(self.power_output, list) else self.power_output(hour)


class Solar(SourceNode):
    def __init__(self, name, power_output, capital_cost, lcoe):
        super().__init__(name, power_output, dispatchability=0, co2_per_mw=0, ramp_up_time=lambda x: 0, 
                         capital_cost=capital_cost, lcoe=lcoe, deployment_time=2)


class Wind(SourceNode):
    def __init__(self, name, power_output, capital_cost, lcoe):
        super().__init__(name, power_output, dispatchability=0.2, co2_per_mw=0, ramp_up_time=lambda x: 0, 
                         capital_cost=capital_cost, lcoe=lcoe, deployment_time=3)


class Gas(SourceNode):
    def __init__(self, name, power_output, co2_per_mw, ramp_up_time, capital_cost, lcoe):
        super().__init__(name, power_output, dispatchability=1, co2_per_mw=co2_per_mw, ramp_up_time=ramp_up_time, 
                         capital_cost=capital_cost, lcoe=lcoe, deployment_time=1)

