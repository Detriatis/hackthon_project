"""
Test docstring (module-level).
This module contains various node definitions for an energy network.
"""
import numpy as np 

class Node:
    """
    A basic node in the energy network.

    Parameters
    ----------
    node_id : Hashable
        A unique identifier for the node.

    Attributes
    ----------
    node_id : Hashable
        The node's identifier.
    connections : list
        A list of connections leading from this node to other nodes.
    connections_ids : list 
        A list of the connected nodes by node_id 
    """

    def __init__(self, node_id):
        self.node_id = node_id
        self.connections = []
        self.connections_ids = [] 

    def set_connection(self, connection, node_id): 
        """
        Set the connection and connection_ids attribute of a node.

        Parameters
        ----------
        connection : Connection
            A connection object which defines the coefficient between two
            connected nodes.
        node_id : Hashable
            A unique identifier for the node being connected to.
        
        """
        self.connections.append(connection) 
        self.connections_ids.append(node_id)


class SinkNode(Node):
    """
    Represents a power demand location (e.g., city, town).

    Parameters
    ----------
    node_id : Hashable
        A unique identifier for the sink node.
    demand_profile : list or callable
        Hourly power demand (MW). If a list, indexed by hour;
        if callable, called with an hour integer as the argument.
    lcoe_requirement : float
        Minimum required Levelized Cost of Electricity ($/MWh).
    """

    def __init__(self, node_id, demand_profile, lcoe_requirement):
        super().__init__(node_id)
        self.demand_profile = demand_profile
        self.lcoe_requirement = lcoe_requirement

    def get_demand(self, hour):
        """
        Returns the power demand at a specified hour.

        Parameters
        ----------
        hour : int
            The hour of interest (e.g., 0 = midnight, 1 = 1 AM, etc.).

        Returns
        -------
        float
            The demand in MW at the given hour.
        """
        if isinstance(self.demand_profile, list):
            return self.demand_profile[hour]
        else:
            return self.demand_profile(hour)


class SourceNode(Node):
    """
    Base class for energy sources.

    Parameters
    ----------
    node_id : Hashable
        A unique identifier for the source node.
    power_output : list or callable
        Hourly power output (MW). If a list, indexed by hour;
        if callable, called with an hour integer as the argument.
    dispatchability : float
        A value in [0, 1] indicating how flexible the source is in adjusting output.
    co2_per_mw : float
        CO2 emissions per MW generated.
    ramp_up_time : callable
        A function defining how quickly the source can ramp up to full capacity.
    capital_cost : float
        Initial investment cost of the source.
    lcoe : float
        Levelized Cost of Electricity ($/MWh).
    deployment_time : int or float
        Time (in some unit, e.g., years) required to deploy the source.
    """

    def __init__(self, node_id, power_output, dispatchability, co2_per_mw,
                 ramp_up_time, capital_cost, lcoe, deployment_time):
        super().__init__(node_id)
        self.power_output = power_output
        self.dispatchability = dispatchability
        self.co2_per_mw = co2_per_mw
        self.ramp_up_time = ramp_up_time
        self.capital_cost = capital_cost
        self.lcoe = lcoe
        self.deployment_time = deployment_time

    def get_power_output(self, hour):
        """
        Returns the power output at a specified hour.

        Parameters
        ----------
        hour : int
            The hour for which to retrieve output.

        Returns
        -------
        float
            The power output (MW) at the given hour.
        """
        if isinstance(self.power_output, list):
            return self.power_output[hour]
        else:
            return self.power_output(hour) 
        


class Solar(SourceNode):
    """
    A solar power source node.

    Parameters
    ----------
    name : Hashable
        A unique identifier for the solar node.
    power_output : list or callable
        Hourly power output (MW) specific to solar production.
    capital_cost : float
        Initial investment cost for the solar installation.
    lcoe : float
        Levelized Cost of Electricity ($/MWh) for solar.
    """
    def __init__(self, name, power_output, capital_cost, lcoe):
        super().__init__(name, power_output,
                         dispatchability=0,
                         co2_per_mw=0,
                         ramp_up_time=lambda x: 0,
                         capital_cost=capital_cost,
                         lcoe=lcoe,
                         deployment_time=2)


class Wind(SourceNode):
    """
    A wind power source node.

    Parameters
    ----------
    name : Hashable
        A unique identifier for the wind node.
    power_output : list or callable
        Hourly power output (MW) specific to wind production.
    capital_cost : float
        Initial investment cost for the wind installation.
    lcoe : float
        Levelized Cost of Electricity ($/MWh) for wind.
    """
    def __init__(self, name, power_output, capital_cost, lcoe):
        super().__init__(name, power_output,
                         dispatchability=0.2,
                         co2_per_mw=0,
                         ramp_up_time=lambda x: 0,
                         capital_cost=capital_cost,
                         lcoe=lcoe,
                         deployment_time=3)


class Gas(SourceNode):
    """
    A gas-powered source node.

    Parameters
    ----------
    name : Hashable
        A unique identifier for the gas node.
    power_output : list or callable
        Hourly power output (MW) for gas generation.
    co2_per_mw : float
        CO2 emissions per MW generated by gas.
    ramp_up_time : callable
        A function defining how quickly the gas source can ramp up to full capacity.
    capital_cost : float
        Initial investment cost for the gas installation.
    lcoe : float
        Levelized Cost of Electricity ($/MWh) for gas.
    """
    def __init__(self, name, power_output, co2_per_mw, ramp_up_time,
                 capital_cost, lcoe):
        super().__init__(name, power_output,
                         dispatchability=1,
                         co2_per_mw=co2_per_mw,
                         ramp_up_time=ramp_up_time,
                         capital_cost=capital_cost,
                         lcoe=lcoe,
                         deployment_time=1)
