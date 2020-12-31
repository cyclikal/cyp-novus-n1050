import minimalmodbus
import datetime
import time
import json
from cyckei.plugins import cyp_base

# port name, slave address (in decimal)
instrument = minimalmodbus.Instrument('COM5', 1)

default_config = json.loads(
    """
    {
        "name": "novus_n1050",
        "enabled": true,
        "sources": [
            {
              "port": "COM5",
              "meta": "PV"
            }
        ]
    }
    """
)

class PluginController(cyp_base.BaseController):
    def __init__(self, sources):
        super().__init__(
            "novus-n1050",
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
                 verbosity=1):

        self.name = f"PV NovusN1050 {PORT}"
        self.logger = logger
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
            'verbosity': verbosity
            }

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
        try:
            t = instrument.read_register(1, 1)
            self.logger.debug(f"Got ProcessValue of {t} from Novus N1050")
            return t

        except Exception as e:
            if self.options['verbosity'] > 0:
                self.logger.error('Could not get NovusN1050 PV data: %s' % e)
                return None

class NovusN1050LoggerSV(object):
    def __init__(self,
                 logger,
                 TIMEFORMAT='%Y-%m-%d %H:%M:%S.%f',
                 PORT=None,
                 NAME=None,
                 maxi=100000000000,
                 verbosity=1):

        self.name = f"SV NovusN1050 {PORT}"
        self.logger = logger
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
            'verbosity': verbosity
            }

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
        try:
            t = instrument.read_register(0, 1)
            print(t)
            self.logger.debug(f"Got SetValue of {t} from Novus N1050")
            return t

        except Exception as e:
            if self.options['verbosity'] > 0:
                self.logger.error('Could not get NovusN1050 data: %s' % e)
                return None


if __name__ == "__main__":
    sources = default_config["sources"]
    controller = PluginController(sources)
    print(cyp_base.read_all(controller))