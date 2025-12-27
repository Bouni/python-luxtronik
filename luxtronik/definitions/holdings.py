"""
Constant list containing all 'holdings' definitions
used by the smart home interface (SHI) of the Luxtronik controller.

Unlike the setting registers, these SHI register are volatile and intended for
communication with smart home systems. 'Holding' registers are readable
and writable and are used to control the heat pump externally.

NOTE: Data fields that span multiple registers are typically in big-endian/MSB-first order.
"""
from typing import Final

from luxtronik.datatypes import (
    CelsiusUInt16,
    ControlMode,
    KelvinInt16,
    LevelMode,
    LockMode,
    LpcMode,
    OnOffMode,
    PowerLimit,
    Unknown,
)

# Offset which must be added to the holding indices
# to obtain the correct address of the data fields
HOLDINGS_OFFSET: Final = 10000

HOLDINGS_DEFINITIONS_LIST: Final = [
    {
        "index": 0,
        "count": 1,
        "names": ["heating_mode"],
        "type": ControlMode,
        "writeable": True,
        "datatype": "UINT16",
        "unit": "enum",
        "default": 0,
        "range": {"min": 0, "max": 3},
        "since": "3.90.1",
        "description": "Configuration for heating operation \
0: no influence \
1: Heating setpoint \
2: Heating offset \
3: Heating level"
    },
    {
        "index": 1,
        "count": 1,
        "names": ["heating_setpoint"],
        "type": CelsiusUInt16,
        "writeable": True,
        "datatype": "UINT16",
        "unit": "°C/10",
        "default": 350,
        "range": {"min": 150, "max": 750},
        "since": "3.90.1",
        "description": "Overrides the current return temperature setpoint (tRL) for heating. \
Value may be limited by heat pump controller settings. \
Requires heating_mode = setpoint to apply."
    },
    {
        "index": 2,
        "count": 1,
        "names": ["heating_offset"],
        "type": KelvinInt16,
        "writeable": True,
        "datatype": "INT16",
        "unit": "K/10",
        "default": 0,
        "range": {"min": -200, "max": 200},
        "since": "3.90.1",
        "description": "Offset applied to the current return temperature setpoint (tRL) for heating. \
Requires heating_mode = offset to apply."
    },
    {
        "index": 3,
        "count": 1,
        "names": ["heating_level"],
        "type": LevelMode,
        "writeable": True,
        "since": "3.92.0",
        "description": "Increase or decrease the heating temperature " \
            "using the SHI offset settings.",
    },
    {
        "index": 5,
        "count": 1,
        "names": ["hot_water_mode", "dhw_mode"],
        "type": ControlMode,
        "writeable": True,
        "datatype": "UINT16",
        "unit": "enum",
        "default": 0,
        "range": {"min": 0, "max": 3},
        "since": "3.90.1",
        "description": "Configuration for domestic hot water operation \
0: no influence \
1: DHW setpoint \
2: DHW offset \
3: DHW level"
    },
    {
        "index": 6,
        "count": 1,
        "names": ["hot_water_setpoint", "dhw_setpoint"],
        "type": CelsiusUInt16,
        "writeable": True,
        "datatype": "UINT16",
        "unit": "°C/10",
        "default": 400,
        "range": {"min": 300, "max": 750},
        "since": "3.90.1",
        "description": "Overrides the current DHW setpoint. \
Value may be limited by heat pump controller settings. \
Requires dhw_mode = setpoint to apply."
    },
    {
        "index": 7,
        "count": 1,
        "names": ["hot_water_offset", "dhw_offset"],
        "type": KelvinInt16,
        "writeable": True,
        "datatype": "INT16",
        "unit": "K/10",
        "default": 0,
        "range": {"min": -200, "max": 200},
        "since": "3.90.1",
        "description": "Offset applied to the current DHW setpoint. \
Requires dhw_mode = offset to apply."
    },
    {
        "index": 8,
        "count": 1,
        "names": ["hot_water_level", "dhw_level"],
        "type": LevelMode,
        "writeable": True,
        "since": "3.92.0",
        "description": "Increase or decrease the hot water temperature " \
            "using the SHI offset settings.",
    },
    {
        "index": 10,
        "count": 1,
        "names": ["mc1_heat_mode"],
        "type": ControlMode,
        "writeable": True,
        "datatype": "UINT16",
        "unit": "enum",
        "default": 0,
        "range": {"min": 0, "max": 3},
        "since": "3.90.1",
        "description": "Configuration for mixing circuit 1 heating operation \
0: no influence \
1: Heating setpoint \
2: Heating offset \
3: Heating level"
    },
    {
        "index": 11,
        "count": 1,
        "names": ["mc1_heat_setpoint"],
        "type": CelsiusUInt16,
        "writeable": True,
        "datatype": "UINT16",
        "unit": "°C/10",
        "default": 350,
        "range": {"min": 200, "max": 650},
        "since": "3.90.1",
        "description": "Overrides the current flow temperature for mixing circuit 1 heating. \
Value may be limited by heat pump controller settings. \
Requires mc1_heat_mode = setpoint to apply."
    },
    {
        "index": 12,
        "count": 1,
        "names": ["mc1_heat_offset"],
        "type": KelvinInt16,
        "writeable": True,
        "datatype": "INT16",
        "unit": "K/10",
        "default": 0,
        "range": {"min": -50, "max": 50},
        "since": "3.90.1",
        "description": "Offset applied to the current flow temperature for mixing circuit 1 heating. \
Requires mc1_heat_mode = offset to apply."
    },
    {
        "index": 13,
        "count": 1,
        "names": ["mc1_heat_level"],
        "type": LevelMode,
        "writeable": True,
        "since": "3.92.0",
        "description": "Increase or decrease the mixing circuit 1 temperature " \
            "using the SHI offset settings.",
    },
    {
        "index": 15,
        "count": 1,
        "names": ["mc1_cool_mode"],
        "type": ControlMode,
        "writeable": True,
        "datatype": "UINT16",
        "unit": "enum",
        "default": 0,
        "range": {"min": 0, "max": 3},
        "since": "3.90.1",
        "description": "Configuration for mixing circuit 1 cooling operation \
0: no influence \
1: Cooling setpoint \
2: Cooling offset \
3: Cooling level"
    },
    {
        "index": 16,
        "count": 1,
        "names": ["mc1_cool_setpoint"],
        "type": CelsiusUInt16,
        "writeable": True,
        "datatype": "UINT16",
        "unit": "°C/10",
        "default": 200,
        "range": {"min": 50, "max": 250},
        "since": "3.90.1",
        "description": "Overrides the current flow temperature for mixing circuit 1 cooling. \
Value may be limited by heat pump controller settings. \
Requires mc1_cool_mode = setpoint to apply."
    },
    {
        "index": 17,
        "count": 1,
        "names": ["mc1_cool_offset"],
        "type": KelvinInt16,
        "writeable": True,
        "datatype": "INT16",
        "unit": "K/10",
        "default": 0,
        "range": {"min": -50, "max": 50},
        "since": "3.90.1",
        "description": "Offset applied to the current flow temperature for mixing circuit 1 cooling. \
Requires mc1_cool_mode = offset to apply."
    },
    {
        "index": 20,
        "count": 1,
        "names": ["mc2_heat_mode"],
        "type": ControlMode,
        "writeable": True,
        "datatype": "UINT16",
        "unit": "enum",
        "default": 0,
        "range": {"min": 0, "max": 3},
        "since": "3.90.1",
        "description": "Configuration for mixing circuit 2 heating operation \
0: no influence \
1: Heating setpoint \
2: Heating offset \
3: Heating level"
    },
    {
        "index": 21,
        "count": 1,
        "names": ["mc2_heat_setpoint"],
        "type": CelsiusUInt16,
        "writeable": True,
        "datatype": "UINT16",
        "unit": "°C/10",
        "default": 350,
        "range": {"min": 200, "max": 650},
        "since": "3.90.1",
        "description": "Overrides the current flow temperature for mixing circuit 2 heating. \
Value may be limited by heat pump controller settings. \
Requires mc2_heat_mode = setpoint to apply."
    },
    {
        "index": 22,
        "count": 1,
        "names": ["mc2_heat_offset"],
        "type": KelvinInt16,
        "writeable": True,
        "datatype": "INT16",
        "unit": "K/10",
        "default": 0,
        "range": {"min": -50, "max": 50},
        "since": "3.90.1",
        "description": "Offset applied to the current flow temperature for mixing circuit 2 heating. \
Requires mc2_heat_mode = offset to apply."
    },
    {
        "index": 23,
        "count": 1,
        "names": ["mc2_heat_level"],
        "type": LevelMode,
        "writeable": True,
        "since": "3.92.0",
        "description": "Increase or decrease the mixing circuit 2 temperature " \
            "using the SHI offset settings.",
    },
    {
        "index": 25,
        "count": 1,
        "names": ["mc2_cool_mode"],
        "type": ControlMode,
        "writeable": True,
        "datatype": "UINT16",
        "unit": "enum",
        "default": 0,
        "range": {"min": 0, "max": 3},
        "since": "3.90.1",
        "description": "Configuration for mixing circuit 2 cooling operation \
0: no influence \
1: Cooling setpoint \
2: Cooling offset \
3: Cooling level"
    },
    {
        "index": 26,
        "count": 1,
        "names": ["mc2_cool_setpoint"],
        "type": CelsiusUInt16,
        "writeable": True,
        "datatype": "UINT16",
        "unit": "°C/10",
        "default": 200,
        "range": {"min": 50, "max": 250},
        "since": "3.90.1",
        "description": "Overrides the current flow temperature for mixing circuit 2 cooling. \
Value may be limited by heat pump controller settings. \
Requires mc2_cool_mode = setpoint to apply."
    },
    {
        "index": 27,
        "count": 1,
        "names": ["mc2_cool_offset"],
        "type": KelvinInt16,
        "writeable": True,
        "datatype": "INT16",
        "unit": "K/10",
        "default": 0,
        "range": {"min": -50, "max": 50},
        "since": "3.90.1",
        "description": "Offset applied to the current flow temperature for mixing circuit 2 cooling. \
Requires mc2_cool_mode = offset to apply."
    },
    {
        "index": 30,
        "count": 1,
        "names": ["mc3_heat_mode"],
        "type": ControlMode,
        "writeable": True,
        "datatype": "UINT16",
        "unit": "enum",
        "default": 0,
        "range": {"min": 0, "max": 3},
        "since": "3.90.1",
        "description": "Configuration for mixing circuit 3 heating operation \
0: no influence \
1: Heating setpoint \
2: Heating offset \
3: Heating level"
    },
    {
        "index": 31,
        "count": 1,
        "names": ["mc3_heat_setpoint"],
        "type": CelsiusUInt16,
        "writeable": True,
        "datatype": "UINT16",
        "unit": "°C/10",
        "default": 350,
        "range": {"min": 200, "max": 650},
        "since": "3.90.1",
        "description": "Overrides the current flow temperature for mixing circuit 3 heating. \
Value may be limited by heat pump controller settings. \
Requires mc3_heat_mode = setpoint to apply."
    },
    {
        "index": 32,
        "count": 1,
        "names": ["mc3_heat_offset"],
        "type": KelvinInt16,
        "writeable": True,
        "datatype": "INT16",
        "unit": "K/10",
        "default": 0,
        "range": {"min": -50, "max": 50},
        "since": "3.90.1",
        "description": "Offset applied to the current flow temperature for mixing circuit 3 heating. \
Requires mc3_heat_mode = offset to apply."
    },
    {
        "index": 33,
        "count": 1,
        "names": ["mc3_heat_level"],
        "type": LevelMode,
        "writeable": True,
        "since": "3.92.0",
        "description": "Increase or decrease the mixing circuit 3 temperature " \
            "using the SHI offset settings.",
    },
    {
        "index": 35,
        "count": 1,
        "names": ["mc3_cool_mode"],
        "type": ControlMode,
        "writeable": True,
        "datatype": "UINT16",
        "unit": "enum",
        "default": 0,
        "range": {"min": 0, "max": 3},
        "since": "3.90.1",
        "description": "Configuration for mixing circuit 3 cooling operation \
0: no influence \
1: Cooling setpoint \
2: Cooling offset \
3: Cooling level"
    },
    {
        "index": 36,
        "count": 1,
        "names": ["mc3_cool_setpoint"],
        "type": CelsiusUInt16,
        "writeable": True,
        "datatype": "UINT16",
        "unit": "°C/10",
        "default": 200,
        "range": {"min": 50, "max": 250},
        "since": "3.90.1",
        "description": "Overrides the current flow temperature for mixing circuit 3 cooling. \
Value may be limited by heat pump controller settings. \
Requires mc3_cool_mode = setpoint to apply."
    },
    {
        "index": 37,
        "count": 1,
        "names": ["mc3_cool_offset"],
        "type": KelvinInt16,
        "writeable": True,
        "datatype": "INT16",
        "unit": "K/10",
        "default": 0,
        "range": {"min": -50, "max": 50},
        "since": "3.90.1",
        "description": "Offset applied to the current flow temperature for mixing circuit 3 cooling. \
Requires mc3_cool_mode = offset to apply."
    },
    {
        "index": 40,
        "count": 1,
        "names": ["lpc_mode"],
        "type": LpcMode,
        "writeable": True,
        "datatype": "UINT16",
        "unit": "enum",
        "default": 0,
        "range": {"min": 0, "max": 2},
        "since": "3.90.1",
        "description": "Configuration for limitation of power consumption: \
0: no power limitation (normal operation) \
Setpoint values are achieved with heat pump performance curve \
1: Soft limitation (recommended for PV surplus) \
Power recommendation for heat pump, i.e., heat pump attempts to \
limit power demand according to data point pc_limit \
If the actual value deviates too much from the setpoint (hysteresis), \
the heat pump ignores the PC Limit power specification. \
2: Hard limitation (recommended only for §14a EnWG). \
The heat pump limits the power consumption according to pc_limit regardless of hysteresis. \
Hard limitation may reduce comfort."
    },
    {
        "index": 41,
        "count": 1,
        "names": ["pc_limit"],
        "type": PowerLimit,
        "writeable": True,
        "datatype": "UINT16",
        "unit": "kW/10",
        "default": 300,
        "range": {"min": 0, "max": 300},
        "since": "3.90.1",
        "description": "Maximum allowed power consumption of the heat pump. \
Requires lpc_mode to be set accordingly."
    },
    {
        "index": 50,
        "count": 1,
        "names": ["lock_heating"],
        "type": LockMode,
        "writeable": True,
        "since": "3.92.0",
        "description": "Lock state for the heating function",
    },
    {
        "index": 51,
        "count": 1,
        "names": ["lock_hot_water"],
        "type": LockMode,
        "writeable": True,
        "since": "3.92.0",
        "description": "Lock state for the hot water system",
    },
    {
        "index": 52,
        "count": 1,
        "names": ["lock_cooling"],
        "type": LockMode,
        "writeable": True,
        "datatype": "UINT16",
        "unit": "bool",
        "default": 0,
        "range": {"min": 0, "max": 1},
        "since": "3.90.1",
        "description": "Cooling operation lock. \
0: normal operation \
1: lock passive and active cooling. \
Frequent switching may cause wear on heat pump and hydraulic components."
    },
    {
        "index": 53,
        "count": 1,
        "names": ["lock_swimming_pool"],
        "type": LockMode,
        "writeable": True,
        "datatype": "UINT16",
        "unit": "bool",
        "default": 0,
        "range": {"min": 0, "max": 1},
        "since": "3.90.1",
        "description": "Swimming pool heating lock. \
0: normal operation \
1: lock pool heating. \
Frequent switching may cause wear on heat pump and hydraulic components."
    },
    {
        "index": 60,
        "count": 1,
        "names": ["unknown_holding_60"],
        "type": Unknown,
        "writeable": False,
        "since": "3.92.1",
        "description": "TODO: Function unknown – requires further analysis",
    },
    {
        "index": 65,
        "count": 1,
        "names": ["heat_overall_mode"],
        "type": ControlMode,
        "writeable": True,
        "since": "3.92.0",
        "description": "Operating mode of all heating functions (no setpoint available)",
    },
    {
        "index": 66,
        "count": 1,
        "names": ["heat_overall_offset"],
        "type": KelvinInt16,
        "writeable": True,
        "datatype": "INT16",
        "range": {"min": -200, "max": 200},
        "since": "3.92.0",
        "description": "Temperature correction in Kelvin " \
            "for all heating functions",
    },
    {
        "index": 67,
        "count": 1,
        "names": ["heat_overall_level"],
        "type": LevelMode,
        "writeable": True,
        "since": "3.92.0",
        "description": "Increase or decrease all heating temperatures " \
            "using the SHI offset settings.",
    },
    {
        "index": 70,
        "count": 1,
        "names": ["circulation"],
        "type": OnOffMode,
        "writeable": True,
        "since": "3.92.0",
        "description": "When set to ON, the circulation pump is activated, but only if no time schedule is configured for it.",
    },
    {
        "index": 71,
        "count": 1,
        "names": ["hot_water_extra"],
        "type": OnOffMode,
        "writeable": True,
        "since": "3.92.0",
        "description": "When set to ON, the hot water heating is activated and will run until the maximum temperature is reached.",
    },
]
