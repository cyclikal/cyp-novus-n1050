# cyp-novus-n1050

##### Cyckei Plugin Package, Reads Temperatures from Novus N1050 PID
Intended to work with [Cyckei](https://github.com/cyclikal/cyckei), the Keithley battery cycler for Python 3.

---

## About the Novus N1050 Plugin
The Novus N1050 plugin gets temperature data from Novus N1050 PIDS.
Requires a USB type C connection.

## About Cyckei Plugins
The Cyckei plugin infrastructure was developed to allow data from other instruments to be accessible to Cyckei.
The system uses a two-part structure: a loading system and set of parent classes within Cyckei, and additional packages that meet certain standards to provide accurate data to Cyckei.
When properly set up, the ability to select certain plugins will appear in the Cyckei client, and data will be meshed into Cyckei's usual output files.

See below for installation details for this specific plugin, and details about Cyckei's plugin systems within the [Cyckei documentation](https://docs.cyclikal.com/projects/cyckei/en/stable/plugins.html).

# Installation

#### Requirements
The Novus N1050 plugin interfaces with the PID via a USB connection, and thus requires no adapters. The USB to serial adapter is built into the Novus N1050 PID.

It is recommended that the plugin, as well as Cyckei, are installed in a python [virtual environment](https://docs.python.org/3/tutorial/venv.html). To be accessed, the plugin must be in the same environment as Cyckei.

#### Package Install
To install, clone the github repository, change to the directory and install the python package:

    git clone https://github.com/cyclikal/cyp-mettler-ag204.git
    cd ./cyp-novus-n1050
    python setup.py install

#### Configuration
After installing the plugin you must add configuration so that Cyckei can setup and use the plugin correctly.
To do so, add the following entry to the ``plugins`` list Cyckei's main ``config.json``.

    {
        "name": "novus-n1050",
        "enabled": true,
        "sources": [
            {
              "port": "COM6",
              "meta": null
            }
        ]
    }

``port`` refers to the port of the serial interface that a given scale is connected to. ``meta`` can be left at ``null`` and is not currently referenced.

#### Usage
Once installed and configured the sources specified on ``config.json`` should appear in the Cyckei client interface as dropdown options. A source can be assigned to any channel, and data from the plugin will be appended to the end of Cyckei's cycling data.
A header will be written with the data file specifying which data entries are generated by Cyckei, the plugin, etc.

To check what sources were initialized click ``plugins`` in the dropdown menu.