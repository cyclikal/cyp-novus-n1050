import minimalmodbus
# port name, slave address (in decimal)
instrument = minimalmodbus.Instrument('COM6', 1)

## Read temperature (PV = ProcessValue, SV = SetValue) ##
# Registernumber, number of decimals
sv = instrument.read_register(0, 1)
pv = instrument.read_register(1, 1)

print(f"{pv=}°C, {sv=}°C")
