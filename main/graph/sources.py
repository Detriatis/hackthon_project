# sources.py

class Source:
    def __init__(self, name, power_output, dispatchability, co2_per_mw, ramp_up_time, capital_cost, lcoe, deployment_time):
        """
        Base class for energy sources.
        
        :param name: Name of the source
        :param power_output: Function or list representing hourly power output (MW)
        :param dispatchability: Value between 0-1 indicating how flexible the source is
        :param co2_per_mw: CO2 emissions per MW generated
        :param ramp_up_time: Function defining ramp-up time behavior
        :param capital_cost: Initial investment cost
        :param lcoe: Levelized Cost of Electricity ($/MWh)
        :param deployment_time: Time required to deploy the source
        """
        self.name = name
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


class Solar(Source):
    def __init__(self, name, power_output, capital_cost, lcoe):
        super().__init__(name, power_output, dispatchability=0, co2_per_mw=0, ramp_up_time=lambda x: 0, 
                         capital_cost=capital_cost, lcoe=lcoe, deployment_time=2)


class Wind(Source):
    def __init__(self, name, power_output, capital_cost, lcoe):
        super().__init__(name, power_output, dispatchability=0.2, co2_per_mw=0, ramp_up_time=lambda x: 0, 
                         capital_cost=capital_cost, lcoe=lcoe, deployment_time=3)


class Gas(Source):
    def __init__(self, name, power_output, co2_per_mw, ramp_up_time, capital_cost, lcoe):
        super().__init__(name, power_output, dispatchability=1, co2_per_mw=co2_per_mw, ramp_up_time=ramp_up_time, 
                         capital_cost=capital_cost, lcoe=lcoe, deployment_time=1)

