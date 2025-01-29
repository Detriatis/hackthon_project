# connections.py

class Connection:
    def __init__(self, source, sink, efficiency):
        """
        Represents a connection between a source and a sink.
        
        :param source: Source object
        :param sink: Sink object
        :param efficiency: Transmission efficiency (0-1)
        """
        self.source = source
        self.sink = sink
        self.efficiency = efficiency
    
    def transmit_power(self, hour):
        """Computes actual power delivered from source to sink at a given hour."""
        generated_power = self.source.get_power_output(hour)
        return generated_power * self.efficiency
