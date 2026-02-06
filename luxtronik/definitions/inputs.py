"""
Constant list containing all 'inputs' definitions
used by the smart home interface (SHI) of the Luxtronik controller.

Unlike the setting registers, these SHI register are volatile and intended for
communication with smart home systems. 'Input' register are read-only
and are used for display or to control other devices.

NOTES:
- If there are multiple definitions for an index, the newest and
preferred one should be inserted as the last one in the same index.
- Data fields that span multiple registers are typically in big-endian/MSB-first order.
"""

from typing import Final

from luxtronik.datatypes import (
    Bool,
    BufferType,
    CelsiusInt16,
    CelsiusUInt16,
    Energy,
    Errorcode,
    FullVersion,
    HeatPumpStatus,
    Minutes,
    ModeStatus,
    OnOffMode,
    OperationMode,
    PowerKW,
    Unknown,
)

# Offset which must be added to the input indices
# to obtain the correct address of the data fields
INPUTS_OFFSET: Final = 10000
INPUTS_DEFAULT_DATA_TYPE: Final = 'INT16'

INPUTS_DEFINITIONS_LIST: Final = [
    {
        "index": 0,
        "count": 1,
        "names": ["heatpump_vd1_status"],
        "type": Bool,
        "writeable": False,
        "datatype": "UINT16",
        "bit_offset": 0,
        "bit_count": 1,
        "unit": "boolean",
        "since": "3.90.1",
        "description": "Indicates whether VD1 is running"
    },
    {
        "index": 0,
        "count": 1,
        "names": ["heatpump_vd2_status"],
        "type": Bool,
        "writeable": False,
        "datatype": "UINT16",
        "bit_offset": 1,
        "bit_count": 1,
        "unit": "boolean",
        "since": "3.90.1",
        "description": "Indicates whether VD2 is running"
    },
    {
        "index": 0,
        "count": 1,
        "names": ["heatpump_zwe1_status"],
        "type": Bool,
        "writeable": False,
        "datatype": "UINT16",
        "bit_offset": 2,
        "bit_count": 1,
        "unit": "boolean",
        "since": "3.90.1",
        "description": "Indicates whether ZWE1 is running"
    },
    {
        "index": 0,
        "count": 1,
        "names": ["heatpump_zwe2_status"],
        "type": Bool,
        "writeable": False,
        "datatype": "UINT16",
        "bit_offset": 3,
        "bit_count": 1,
        "unit": "boolean",
        "since": "3.90.1",
        "description": "Indicates whether ZWE2 is running"
    },
    {
        "index": 0,
        "count": 1,
        "names": ["heatpump_zwe3_status"],
        "type": Bool,
        "writeable": False,
        "datatype": "UINT16",
        "bit_offset": 4,
        "bit_count": 1,
        "unit": "boolean",
        "since": "3.90.1",
        "description": "Indicates whether ZWE3 is running"
    },
    {
        "index": 0,
        "count": 1,
        "names": ["heatpump_status"],
        "type": HeatPumpStatus,
        "writeable": False,
        "datatype": "UINT16",
        "unit": "bitmask",
        "since": "3.90.1",
        "description": (
            "Heat pump status bitmask:\n"
            "1: VD1\n"
            "2: VD2\n"
            "4: ZWE1\n"
            "8: ZWE2\n"
            "16: ZWE3\n"
            "0: Heat pump inactive\n"
            ">0: Heat pump or auxiliary heater active"
        )
    },
    {
        "index": 2,
        "count": 1,
        "names": ["operation_mode"],
        "type": OperationMode,
        "writeable": False,
        "datatype": "UINT16",
        "unit": "enum",
        "default": 5,
        "range": {"min": 0, "max": 7},
        "since": "3.90.1",
        "description": (
            "Operating mode status:\n"
            "0: Heating\n"
            "1: DHW heating\n"
            "2: Pool heating / Solar\n"
            "3: Utility lockout\n"
            "4: Defrost\n"
            "5: No demand\n"
            "6: Not used\n"
            "7: Cooling"
        )
    },
    {
        "index": 3,
        "count": 1,
        "names": ["heating_status"],
        "type": ModeStatus,
        "writeable": False,
        "datatype": "UINT16",
        "unit": "enum",
        "range": {"min": 0, "max": 3},
        "since": "3.90.1",
        "description": (
            "Heating status:\n"
            "0: Off\n"
            "1: No demand\n"
            "2: Demand\n"
            "3: Active"
        )
    },
    {
        "index": 4,
        "count": 1,
        "names": ["hot_water_status", "dhw_status"],
        "type": ModeStatus,
        "writeable": False,
        "datatype": "UINT16",
        "unit": "enum",
        "range": {"min": 0, "max": 3},
        "since": "3.90.1",
        "description": (
            "DHW status:\n"
            "0: Off\n"
            "1: No demand\n"
            "2: Demand\n"
            "3: Active"
        )
    },
    {
        "index": 6,
        "count": 1,
        "names": ["cooling_status"],
        "type": ModeStatus,
        "writeable": False,
        "datatype": "UINT16",
        "unit": "enum",
        "range": {"min": 0, "max": 3},
        "since": "3.90.1",
        "description": (
            "Cooling status:\n"
            "0: Off\n"
            "1: No demand\n"
            "2: Demand\n"
            "3: Active"
        )
    },
    {
        "index": 7,
        "count": 1,
        "names": ["pool_heating_status"],
        "type": ModeStatus,
        "writeable": False,
        "datatype": "UINT16",
        "unit": "enum",
        "range": {"min": 0, "max": 3},
        "since": "3.90.1",
        "description": (
            "Pool heating / Solar status:\n"
            "0: Off\n"
            "1: No demand\n"
            "2: Demand\n"
            "3: Active"
        )
    },
    {
        "index": 100,
        "count": 1,
        "names": ["return_line_temp"],
        "type": CelsiusUInt16,
        "writeable": False,
        "datatype": "UINT16",
        "unit": "°C/10",
        "since": "3.90.1",
        "description": "Current return line temperature",
    },
    {
        "index": 101,
        "count": 1,
        "names": ["return_line_target"],
        "type": CelsiusUInt16,
        "writeable": False,
        "datatype": "UINT16",
        "unit": "°C/10",
        "since": "3.90.1",
        "description": "Target return line temperature",
    },
    {
        "index": 102,
        "count": 1,
        "names": ["return_line_ext"],
        "type": CelsiusUInt16,
        "writeable": False,
        "datatype": "UINT16",
        "unit": "°C/10",
        "since": "3.90.1",
        "description": "Current value of the external return temperature sensor",
    },
    {
        "index": 103,
        "count": 1,
        "names": ["return_line_limit"],
        "type": CelsiusInt16,
        "writeable": False,
        "datatype": "INT16",
        "unit": "°C/10",
        "since": "3.90.1",
        "description": "Maximum allowed return line temperature",
    },
    {
        "index": 104,
        "count": 1,
        "names": ["return_line_min_target"],
        "type": CelsiusInt16,
        "writeable": False,
        "datatype": "INT16",
        "unit": "°C/10",
        "since": "3.90.1",
        "description": "Minimum target return line temperature",
    },
    {
        "index": 105,
        "count": 1,
        "names": ["flow_line_temp"],
        "type": CelsiusUInt16,
        "writeable": False,
        "datatype": "UINT16",
        "unit": "°C/10",
        "since": "3.90.1",
        "description": "Current flow line temperature",
    },
    {
        "index": 106,
        "count": 1,
        "names": ["room_temperature"],
        "type": CelsiusInt16,
        "writeable": False,
        "datatype": "INT16",
        "unit": "°C/10",
        "since": "3.90.1",
        "description": (
            "Current room temperature. "
            "Requires accessory RBE+ room control unit."
        )
    },
    {
        "index": 107,
        "count": 1,
        "names": ["heating_limit"],
        "type": CelsiusInt16,
        "writeable": False,
        "datatype": "INT16",
        "unit": "°C/10",
        "since": "3.90.1",
        "description": (
            "Heating limit temperature. "
            "If undershot (heating curve setpoint - hysteresis), soft-limit power control is ignored."
        )
    },
    {
        "index": 108,
        "count": 1,
        "names": ["outside_temp"],
        "type": CelsiusInt16,
        "writeable": False,
        "datatype": "INT16",
        "unit": "°C/10",
        "since": "3.90.1",
        "description": "Measured outdoor temperature",
    },
    {
        "index": 109,
        "count": 1,
        "names": ["outside_temp_average"],
        "type": CelsiusInt16,
        "writeable": False,
        "datatype": "INT16",
        "unit": "°C/10",
        "since": "3.92.0",
        "description": "Average outdoor temperature",
    },
    {
        "index": 110,
        "count": 1,
        "names": ["heat_source_input"],
        "type": CelsiusInt16,
        "writeable": False,
        "datatype": "INT16",
        "unit": "°C/10",
        "since": "3.92.0",
        "description": "Heat source input temperature",
    },
    {
        "index": 111,
        "count": 1,
        "names": ["heat_source_output"],
        "type": CelsiusInt16,
        "writeable": False,
        "datatype": "INT16",
        "unit": "°C/10",
        "since": "3.92.0",
        "description": "Heat source output temperature",
    },
    {
        "index": 112,
        "count": 1,
        "names": ["max_flow_temp"],
        "type": CelsiusUInt16,
        "writeable": False,
        "since": "3.92.0",
        "description": "Maximum flow temperature",
    },
    {
        "index": 113,
        "count": 1,
        "names": ["unknown_input_113"],
        "type": Unknown,
        "writeable": False,
        "since": "3.92.0",
        "description": "TODO: Function unknown – requires further analysis",
    },
    {
        "index": 120,
        "count": 1,
        "names": ["hot_water_temp", "dhw_temp"],
        "type": CelsiusInt16,
        "writeable": False,
        "datatype": "INT16",
        "unit": "°C/10",
        "since": "3.90.1",
        "description": "Current hot water temperature",
    },
    {
        "index": 121,
        "count": 1,
        "names": ["hot_water_target", "dhw_target"],
        "type": CelsiusUInt16,
        "writeable": False,
        "datatype": "UINT16",
        "unit": "°C/10",
        "since": "3.90.1",
        "description": "Target hot water temperature",
    },
    {
        "index": 122,
        "count": 1,
        "names": ["hot_water_min", "dhw_min"],
        "type": CelsiusInt16,
        "writeable": False,
        "datatype": "INT16",
        "unit": "°C/10",
        "since": "3.90.1",
        "description": "Minimum adjustable hot water temperature",
    },
    {
        "index": 123,
        "count": 1,
        "names": ["hot_water_max", "dhw_max"],
        "type": CelsiusInt16,
        "writeable": False,
        "datatype": "INT16",
        "unit": "°C/10",
        "since": "3.90.1",
        "description": "Maximum adjustable hot water temperature",
    },
    {
        "index": 124,
        "count": 1,
        "names": ["hot_water_limit", "dhw_limit"],
        "type": CelsiusInt16,
        "writeable": False,
        "datatype": "INT16",
        "unit": "°C/10",
        "since": "3.90.1",
        "description": (
            "DHW limit temperature. "
            "If undershot (desired regulation value), soft-limit power control is ignored."
        )
    },
    {
        "index": 140,
        "count": 1,
        "names": ["mc1_temp"],
        "type": CelsiusInt16,
        "writeable": False,
        "datatype": "INT16",
        "unit": "°C/10",
        "since": "3.90.1",
        "description": "Current flow temperature of mixing circuit 1",
    },
    {
        "index": 141,
        "count": 1,
        "names": ["mc1_target"],
        "type": CelsiusInt16,
        "writeable": False,
        "datatype": "INT16",
        "unit": "°C/10",
        "since": "3.90.1",
        "description": "Desired target temperature of mixing circuit 1",
    },
    {
        "index": 142,
        "count": 1,
        "names": ["mc1_min"],
        "type": CelsiusInt16,
        "writeable": False,
        "datatype": "INT16",
        "unit": "°C/10",
        "since": "3.90.1",
        "description": "Minimum temperature of mixing circuit 1",
    },
    {
        "index": 143,
        "count": 1,
        "names": ["mc1_max"],
        "type": CelsiusInt16,
        "writeable": False,
        "datatype": "INT16",
        "unit": "°C/10",
        "since": "3.90.1",
        "description": "Maximum temperature of mixing circuit 1",
    },
    {
        "index": 150,
        "count": 1,
        "names": ["mc2_temp"],
        "type": CelsiusInt16,
        "writeable": False,
        "datatype": "INT16",
        "unit": "°C/10",
        "since": "3.90.1",
        "description": "Current flow temperature of mixing circuit 2",
    },
    {
        "index": 151,
        "count": 1,
        "names": ["mc2_target"],
        "type": CelsiusInt16,
        "writeable": False,
        "datatype": "INT16",
        "unit": "°C/10",
        "since": "3.90.1",
        "description": "Desired target temperature of mixing circuit 2",
    },
    {
        "index": 152,
        "count": 1,
        "names": ["mc2_min"],
        "type": CelsiusInt16,
        "writeable": False,
        "datatype": "INT16",
        "unit": "°C/10",
        "since": "3.90.1",
        "description": "Minimum temperature of mixing circuit 2",
    },
    {
        "index": 153,
        "count": 1,
        "names": ["mc2_max"],
        "type": CelsiusInt16,
        "writeable": False,
        "datatype": "INT16",
        "unit": "°C/10",
        "since": "3.90.1",
        "description": "Maximum temperature of mixing circuit 2",
    },
    {
        "index": 160,
        "count": 1,
        "names": ["mc3_temp"],
        "type": CelsiusInt16,
        "writeable": False,
        "datatype": "INT16",
        "unit": "°C/10",
        "since": "3.90.1",
        "description": "Current flow temperature of mixing circuit 3",
    },
    {
        "index": 161,
        "count": 1,
        "names": ["mc3_target"],
        "type": CelsiusInt16,
        "writeable": False,
        "datatype": "INT16",
        "unit": "°C/10",
        "since": "3.90.1",
        "description": "Desired target temperature of mixing circuit 3",
    },
    {
        "index": 162,
        "count": 1,
        "names": ["mc3_min"],
        "type": CelsiusInt16,
        "writeable": False,
        "datatype": "INT16",
        "unit": "°C/10",
        "since": "3.90.1",
        "description": "Minimum temperature of mixing circuit 3",
    },
    {
        "index": 163,
        "count": 1,
        "names": ["mc3_max"],
        "type": CelsiusInt16,
        "writeable": False,
        "datatype": "INT16",
        "unit": "°C/10",
        "since": "3.90.1",
        "description": "Maximum temperature of mixing circuit 3",
    },
    {
        "index": 201,
        "count": 1,
        "names": ["error_number"],
        "type": Errorcode,
        "writeable": False,
        "datatype": "UINT16",
        "since": "3.90.1",
        "description": (
            "Current error number:\n"
            "0: no error\n"
            "X: error code."
        )
    },
    {
        "index": 202,
        "count": 1,
        "names": ["buffer_type"],
        "type": BufferType,
        "writeable": False,
        "datatype": "UINT16",
        "range": {"min": 0, "max": 2},
        "since": "3.90.1",
        "description": (
            "Buffer tank configuration:\n"
            "0: series buffer\n"
            "1: separation buffer\n"
            "2: multifunction buffer."
        )
    },
    {
        "index": 203,
        "count": 1,
        "names": ["min_off_time"],
        "type": Minutes,
        "writeable": False,
        "datatype": "UINT16",
        "unit": "minute",
        "since": "3.90.1",
        "description": "Minimum off-time before heat pump may restart."
    },
    {
        "index": 204,
        "count": 1,
        "names": ["min_run_time"],
        "type": Minutes,
        "writeable": False,
        "datatype": "UINT16",
        "unit": "minute",
        "since": "3.90.1",
        "description": "Minimum runtime of the heat pump."
    },
    {
        "index": 205,
        "count": 1,
        "names": ["cooling_configured"],
        "type": OnOffMode,
        "writeable": False,
        "datatype": "UINT16",
        "unit": "bool",
        "range": {"min": 0, "max": 1},
        "since": "3.90.1",
        "description": (
            "Indicates whether cooling mode is configured:\n"
            "0: no\n"
            "1: yes."
        )
    },
    {
        "index": 206,
        "count": 1,
        "names": ["pool_heating_configured"],
        "type": OnOffMode,
        "writeable": False,
        "datatype": "UINT16",
        "unit": "bool",
        "range": {"min": 0, "max": 1},
        "since": "3.90.1",
        "description": (
            "Indicates whether pool heating is configured:\n"
            "0: no\n"
            "1: yes."
        )
    },
    {
        "index": 207,
        "count": 1,
        "names": ["cooling_release"],
        "type": OnOffMode,
        "writeable": False,
        "datatype": "UINT16",
        "unit": "bool",
        "range": {"min": 0, "max": 1},
        "since": "3.90.1",
        "description": (
            "Cooling release condition fulfilled:\n"
            "0: no\n"
            "1: yes.\n"
            "Cooling release only valid if cooling is enabled (see cooling_configured)."
        )
    },
    {
        "index": 300,
        "count": 1,
        "names": ["heating_power_actual"],
        "type": PowerKW,
        "writeable": False,
        "datatype": "INT16",
        "unit": "kW/10",
        "since": "3.90.1",
        "description": "Current heating power."
    },
    {
        "index": 301,
        "count": 1,
        "names": ["electric_power_actual"],
        "type": PowerKW,
        "writeable": False,
        "datatype": "UINT16",
        "unit": "kW/10",
        "since": "3.90.1",
        "description": "Current electrical power consumption."
    },
    {
        "index": 302,
        "count": 1,
        "names": ["electric_power_min_predicted"],
        "type": PowerKW,
        "writeable": False,
        "datatype": "UINT16",
        "unit": "kW/10",
        "since": "3.90.1",
        "description": "Minimum predicted electrical power consumption."
    },
    {
        "index": 310,
        "count": 2,
        "names": ["electric_energy_total"],
        "type": Energy,
        "writeable": False,
        "datatype": "INT32",
        "unit": "kWh/10",
        "since": "3.90.1",
        "description": "Total electrical energy consumption (all modes)."
    },
    {
        "index": 312,
        "count": 2,
        "names": ["electric_energy_heating"],
        "type": Energy,
        "writeable": False,
        "datatype": "INT32",
        "unit": "kWh/10",
        "since": "3.90.1",
        "description": "Total electrical energy consumption for heating."
    },
    {
        "index": 314,
        "count": 2,
        "names": ["electric_energy_dhw"],
        "type": Energy,
        "writeable": False,
        "datatype": "INT32",
        "unit": "kWh/10",
        "since": "3.90.1",
        "description": "Total electrical energy consumption for DHW."
    },
    {
        "index": 316,
        "count": 2,
        "names": ["electric_energy_cooling"],
        "type": Energy,
        "writeable": False,
        "datatype": "INT32",
        "unit": "kWh/10",
        "since": "3.90.1",
        "description": "Total electrical energy consumption for cooling."
    },
    {
        "index": 318,
        "count": 2,
        "names": ["electric_energy_pool"],
        "type": Energy,
        "writeable": False,
        "datatype": "INT32",
        "unit": "kWh/10",
        "since": "3.90.1",
        "description": "Total electrical energy consumption for pool heating / solar."
    },
    {
        "index": 320,
        "count": 2,
        "names": ["thermal_energy_total"],
        "type": Energy,
        "writeable": False,
        "datatype": "INT32",
        "unit": "kWh/10",
        "since": "3.92.0",
        "description": "Total thermal energy production (all modes)."
    },
    {
        "index": 322,
        "count": 2,
        "names": ["thermal_energy_heating"],
        "type": Energy,
        "writeable": False,
        "datatype": "INT32",
        "unit": "kWh/10",
        "since": "3.92.0",
        "description": "Total thermal energy production for heating."
    },
    {
        "index": 324,
        "count": 2,
        "names": ["thermal_energy_dhw"],
        "type": Energy,
        "writeable": False,
        "datatype": "INT32",
        "unit": "kWh/10",
        "since": "3.92.0",
        "description": "Total thermal energy production for DHW."
    },
    {
        "index": 326,
        "count": 2,
        "names": ["thermal_energy_cooling"],
        "type": Energy,
        "writeable": False,
        "datatype": "INT32",
        "unit": "kWh/10",
        "since": "3.92.0",
        "description": "Total thermal energy production for cooling."
    },
    {
        "index": 328,
        "count": 2,
        "names": ["thermal_energy_pool"],
        "type": Energy,
        "writeable": False,
        "datatype": "INT32",
        "unit": "kWh/10",
        "since": "3.92.0",
        "description": "Total thermal energy production for pool heating / solar."
    },
    {
        "index": 350,
        "count": 1,
        "names": ["unknown_input_350"],
        "type": Unknown,
        "writeable": False,
        "since": "3.92.0",
        "description": "TODO: Function unknown – requires further analysis",
    },
    {
        "index": 351,
        "count": 1,
        "names": ["unknown_input_351"],
        "type": Unknown,
        "writeable": False,
        "since": "3.92.0",
        "description": "TODO: Function unknown – requires further analysis",
    },
    {
        "index": 352,
        "count": 1,
        "names": ["unknown_input_352"],
        "type": Unknown,
        "writeable": False,
        "since": "3.92.0",
        "description": "TODO: Function unknown – requires further analysis",
    },
    {
        "index": 353,
        "count": 1,
        "names": ["unknown_input_353"],
        "type": Unknown,
        "writeable": False,
        "since": "3.92.0",
        "description": "TODO: Function unknown – requires further analysis",
    },
    {
        "index": 354,
        "count": 1,
        "names": ["unknown_input_354"],
        "type": Unknown,
        "writeable": False,
        "since": "3.92.0",
        "description": "TODO: Function unknown – requires further analysis",
    },
    {
        "index": 355,
        "count": 1,
        "names": ["unknown_input_355"],
        "type": Unknown,
        "writeable": False,
        "since": "3.92.0",
        "description": "TODO: Function unknown – requires further analysis",
    },
    {
        "index": 356,
        "count": 1,
        "names": ["unknown_input_356"],
        "type": Unknown,
        "writeable": False,
        "since": "3.92.0",
        "description": "TODO: Function unknown – requires further analysis",
    },
    {
        "index": 360,
        "count": 1,
        "names": ["unknown_input_360"],
        "type": Unknown,
        "writeable": False,
        "since": "3.92.0",
        "description": "TODO: Function unknown – requires further analysis",
    },
    {
        "index": 361,
        "count": 1,
        "names": ["unknown_input_361"],
        "type": Unknown,
        "writeable": False,
        "since": "3.92.0",
        "description": "TODO: Function unknown – requires further analysis",
    },
    {
        "index": 400,
        "count": 3,
        "names": ["version"],
        "type": FullVersion,
        "writeable": False,
        "since": "3.90.1",
        "description": "Full firmware version information",
    },
    {
        "index": 404,
        "count": 1,
        "names": ["unknown_input_404"],
        "type": Unknown,
        "writeable": False,
        "since": "3.92.0",
        "description": "TODO: Function unknown – requires further analysis",
    },
    {
        "index": 405,
        "count": 1,
        "names": ["unknown_input_405"],
        "type": Unknown,
        "writeable": False,
        "since": "3.92.0",
        "description": "TODO: Function unknown – requires further analysis",
    },
    {
        "index": 406,
        "count": 1,
        "names": ["unknown_input_406"],
        "type": Unknown,
        "writeable": False,
        "since": "3.92.0",
        "description": "TODO: Function unknown – requires further analysis",
    },
    {
        "index": 407,
        "count": 1,
        "names": ["unknown_input_407"],
        "type": Unknown,
        "writeable": False,
        "since": "3.92.0",
        "description": "TODO: Function unknown – requires further analysis",
    },
    {
        "index": 408,
        "count": 1,
        "names": ["unknown_input_408"],
        "type": Unknown,
        "writeable": False,
        "since": "3.92.0",
        "description": "TODO: Function unknown – requires further analysis",
    },
    {
        "index": 409,
        "count": 1,
        "names": ["unknown_input_409"],
        "type": Unknown,
        "writeable": False,
        "since": "3.92.0",
        "description": "TODO: Function unknown – requires further analysis",
    },
    {
        "index": 410,
        "count": 1,
        "names": ["unknown_input_410"],
        "type": Unknown,
        "writeable": False,
        "since": "3.92.0",
        "description": "TODO: Function unknown – requires further analysis",
    },
    {
        "index": 411,
        "count": 1,
        "names": ["unknown_input_411"],
        "type": Unknown,
        "writeable": False,
        "since": "3.92.0",
        "description": "TODO: Function unknown – requires further analysis",
    },
    {
        "index": 412,
        "count": 1,
        "names": ["unknown_input_412"],
        "type": Unknown,
        "writeable": False,
        "since": "3.92.0",
        "description": "TODO: Function unknown – requires further analysis",
    },
    {
        "index": 413,
        "count": 1,
        "names": ["unknown_input_413"],
        "type": Unknown,
        "writeable": False,
        "since": "3.92.0",
        "description": "TODO: Function unknown – requires further analysis",
    },
    {
        "index": 416,
        "count": 1,
        "names": ["unknown_input_416"],
        "type": Unknown,
        "writeable": False,
        "since": "3.92.0",
        "description": "TODO: Function unknown – requires further analysis",
    },
    {
        "index": 417,
        "count": 1,
        "names": ["unknown_input_417"],
        "type": Unknown,
        "writeable": False,
        "since": "3.92.0",
        "description": "TODO: Function unknown – requires further analysis",
    },
    {
        "index": 500,
        "count": 1,
        "names": ["unknown_input_500"],
        "type": Unknown,
        "writeable": False,
        "since": "3.92.0",
        "description": "TODO: Function unknown – requires further analysis",
    },
    {
        "index": 501,
        "count": 1,
        "names": ["unknown_input_501"],
        "type": Unknown,
        "writeable": False,
        "since": "3.92.0",
        "description": "TODO: Function unknown – requires further analysis",
    },
    {
        "index": 502,
        "count": 1,
        "names": ["unknown_input_502"],
        "type": Unknown,
        "writeable": False,
        "since": "3.92.0",
        "description": "TODO: Function unknown – requires further analysis",
    },
]
