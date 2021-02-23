import minimalmodbus
import datetime
import time
import json
from cyckei.plugins import cyp_base

pv_config = json.loads(
    """{
      "name": "Novus N1050 PV",
      "module": "novus_n1050",
      "enabled": true,
      "sources": [
          {
            "port": "COM5",
            "meta": "PV"
          }
      ]
    }"""
)

sv_config = json.loads(
    """
    {
      "name": "Novus N1050 SV",
      "module": "novus_n1050",
      "enabled": true,
      "sources": [
          {
            "port": "COM5",
            "meta": "SV"
          }
      ]
    }
    """
)

class PluginController(cyp_base.BaseController):
    def __init__(self, sources):
        for pid in sources:
            if pid["meta"] == "PV":
                super().__init__(
                    "novus-n1050-pv",
                    "Gets set and measured temp data from Novus 1050 PID."
                )
            else:
                super().__init__(
                    "novus-n1050-sv",
                    "Gets set and measured temp data from Novus 1050 PID."
                )
                 
        # Create a PicoChannel object for each Device
        self.sources = self.load_sources(sources)

        self.logger.info(f"Connected {len(self.sources)} Novus 1050 PID(s)")

        # List of names to declare to Cyckei
        self.names = []
        for source in self.sources:
            self.names.append(str(source))

    def load_sources(self, config_sources):
        """
        Searches for available sources, and establishes source objects.
        Returns
        -------
        Dictionary of sources in format "name": SourceObject.
        """
        sources = {}
        for pid in config_sources:
            if pid["meta"] == "PV":
                pid = NovusN1050LoggerPV(self.logger, PORT=pid["port"])
            else:
                pid = NovusN1050LoggerSV(self.logger, PORT=pid["port"])
            sources[pid.name] = pid

        return sources

class NovusN1050LoggerPV(object):
    def __init__(self,
                 logger,
                 TIMEFORMAT='%Y-%m-%d %H:%M:%S.%f',
                 PORT=None,
                 NAME=None,
                 maxi=100000000000,
                 verbosity=1, delay_in_sec = 30):

        timestamp_start = time.time()
        date_start = datetime.datetime.fromtimestamp(timestamp_start)
        date_start_str = date_start.strftime(TIMEFORMAT)         
        self.options = {
            'description': 'Logfile of data. Header is JSON, data is CSV',
            'date_start': date_start_str,
            'time_format': TIMEFORMAT,
            'timestamp': timestamp_start,
            'data_columns': [
                {'index': 0,
                 'name': 'time',
                 'unit': 'seconds',
                 'description': 'time elapsed in seconds since date_start'},
                {'index': 1,
                 'name': 'PV',
                 'unit': 'C',
                 'description': 'instantaneous setvalue in celcius'}],
            'name': NAME,
            'port': PORT,
            'verbosity': verbosity,
            'delay': delay_in_sec
        }
        self.read_time = 0
        self.pv = 0
        self.logger = logger
        self.set_instrument()
        self.name = f"PV NovusN1050 {PORT}"
        
    
    def set_instrument(self):
        try:
            # port name, slave address (in decimal)
            self.instrument = minimalmodbus.Instrument(self.options['port'], 1)
            self.instrument.close_port_after_each_call = True
        except Exception as e:
            if self.options['verbosity'] > 0:
                self.logger.error('Could not load NovusN1050 PV: %s' % e)
                self.instrument = None

    def read(self):
        '''
        Opens a connection with PID.
        Requests return value using command.
        Parses the PID's response.
        Returns the temp(s) in C.
        Parameters:
            command:
                command string determines what to be read
        Returns:
            temp:
                either a float or a dict of floats
        '''
        self.logger.debug(f"Retrieving ProcessValue from Novus N1050")
        
        if (time.time() - self.read_time) >= self.options['delay']:
            try:
                self.pv = self.instrument.read_register(1, 0)
                self.logger.debug(f"Got ProcessValue of {self.pv} from Novus N1050")
                self.read_time = time.time()
                return self.pv

            except Exception as e:
                if self.options['verbosity'] > 0:
                    self.logger.error('Could not get NovusN1050 data: %s' % e)
                    return None
        else:
            self.logger.debug(f"Got ProcessValue of {self.pv} from Novus N1050 less than {self.options['delay']} seconds ago")
            return self.pv

class NovusN1050LoggerSV(object):
    def __init__(self,
                 logger, 
                 TIMEFORMAT='%Y-%m-%d %H:%M:%S.%f',
                 PORT=None,
                 NAME=None,
                 maxi=100000000000,
                 verbosity=1,
                 delay_in_sec = 30):
        
        timestamp_start = time.time()
        date_start = datetime.datetime.fromtimestamp(timestamp_start)
        date_start_str = date_start.strftime(TIMEFORMAT)
        self.options = {
            'description': 'Logfile of data. Header is JSON, data is CSV',
            'date_start': date_start_str,
            'time_format': TIMEFORMAT,
            'timestamp': timestamp_start,
            'data_columns': [
                {'index': 0,
                 'name': 'time',
                 'unit': 'seconds',
                 'description': 'time elapsed in seconds since date_start'},
                {'index': 1,
                 'name': 'SV',
                 'unit': 'C',
                 'description': 'instantaneous setvalue in celcius'}],
            'name': NAME,
            'port': PORT,
            'verbosity': verbosity,
            'delay': delay_in_sec,
        }
        self.read_time = 0
        self.sv = 0
        self.logger = logger
        self.set_instrument()
        self.name = f"SV NovusN1050 {PORT}"
        

    def set_instrument(self):
        try:
            # port name, slave address (in decimal)
            self.instrument = minimalmodbus.Instrument(self.options['port'], 1)
            self.instrument.close_port_after_each_call = True
        except Exception as e:
            if self.options['verbosity'] > 0:
                self.logger.error('Could not load NovusN1050 SV: %s' % e)
                self.instrument = None

    def read(self):
        '''
        Opens a connection with PID.
        Requests return value using command.
        Parses the PID's response.
        Returns the temp(s) in C.
        Parameters:
            command:
                command string determines what to be read
        Returns:
            temp:
                either a float or a dict of floats
        '''
        self.logger.debug(f"Retrieving SetValue from Novus N1050")
        if self.instrument == None:
            self.set_instrument()
        
        if (time.time() - self.read_time) >= self.options['delay']:
            try:
                self.sv = self.instrument.read_register(0, 1)
                self.logger.debug(f"Got SetValue of {self.sv} from Novus N1050")
                self.read_time = time.time()
                return self.sv

            except Exception as e:
                if self.options['verbosity'] > 0:
                    self.logger.error('Could not get NovusN1050 data: %s' % e)
                    return None
        else:
            self.logger.debug(f"Got SetValue of {self.sv} from Novus N1050 less than {self.options['delay']} seconds ago")
            return self.sv


if __name__ == "__main__":
    sources = pv_config["sources"]
    sources.append(sv_config["sources"])
    controller = PluginController(sources)
    print(cyp_base.read_all(controller))