<!-- markdownlint-disable MD013 -->
# Smart-Home-Interface

## Introduction

© Guzz-T, 2025. The smart home interface is licensed under the terms specified in the repository's license file. Please refer to the LICENSE for details.

This source code provides an interface for the temporary control of a Luxtronik heat pump controller. All data accessed or modified through this interface is volatile and will be reset upon system restart — unlike configuration values, which are persistent. The interface is designed to interact with the controller in a lightweight and flexible way, making it suitable for short-term adjustments or testing scenarios.

Not every function can be explained in detail or even listed in the readme file. Please refer to the function documentation for further information. The examples are intended to illustrate the typical use of the interface.

## Table of Content

1. [Common Usage](#common-usage)
    1. [Available Data](#available-data)
    2. [Creation](#creation)
    3. [Read](#read)
    4. [Write](#write)
    5. [Collect](#collect)
2. [Using aliases](#using-aliases)
3. [Alternative use cases](#alternative-use-cases)
    1. [Latest or specific version](#latest-or-specific-version)
    2. [Trial-and-error mode](#trial-and-error-mode)
4. [Customization](#customization)
5. [Implementation Details](#implementation-details)

## Common Usage

The functionality available depends on the firmware version of the luxtronik controller. Since different versions support different features, it is important to know which version is in use. In standard usage, the interface automatically detects the firmware version, streamlining setup and ensure compatibility.

Because of this version-dependent behavior, data objects should always be created through the provided interface methods. While it is technically possible to instantiate these objects directly via their constructors, doing so is error-prone and cumbersome. The interface handles version-specific quirks and ensures that the objects are initialized correctly, making it the safer and more convenient approach.

Alternatively, users may choose to manually specify a firmware version or operate the interface in a trial-and-error mode. This can be useful for exploring undocumented features or working with custom setups. For more details, refer to the section titled **"Alternative use cases"**.

### Available Data

The interface provides access to two distinct types of data: *holdings* and *inputs*. Holdings are writable values that allow configuration settings to be modified or overridden, and in some cases, enable additional features. These values can also be read back, enabling verification of changes or inspection of current settings. If a holding has not yet been explicitly written, it will contain a default value as defined by the controller.

Inputs, in contrast, represent read-only values that reflect the current operational state of the system. They provide insight into live metrics such as temperatures, operating modes, and system status, but cannot be altered through the interface.

In both *holdings* and *inputs*, a single *holding* or *input* are referred to as data fields. Each field represents a logical unit of information, and in some cases, multiple raw values are grouped together to form a single, higher-level field — for example, when a value spans multiple registers or requires interpretation. Alongside the interface itself, a comprehensive list of all data fields ever discovered is maintained. This catalog serves as a reference for developers and users alike, offering insight into the full range of known data and their structure.

It’s worth noting that while certain functions may be supported by the firmware, they can be disabled by the active configuration. In such cases, the interface will not return any data for the affected fields. Instead, it will yield `None`, indicating that the feature is currently inactive or unavailable.

### Creation

To begin using the interface, it must first be instantiated. During this step, the communication method is selected — currently, only Modbus-TCP is supported. Once initialized, the interface automatically reads the firmware version from the Luxtronik controller and configures itself accordingly. This ensures that all subsequent operations are aligned with the capabilities and structure of the detected version, providing a reliable foundation for interacting with the system.

```python
from luxtronik.shi import create_modbus_tcp

# Use the default values for all arguments except the IP address
shi = create_modbus_tcp('your.lux.ip.addr')
```

### Read

Data fields can be accessed individually or grouped together as data vectors for more efficient reading. This allows users to retrieve multiple related values in a single operation, improving performance and simplifying code. In addition to individual vectors, the interface also provides a data vector collection — a container that holds an instance of all available data vectors. This collection can be passed around and reused, making it easier to manage and access structured data sets.

The examples provided in this chapter focus on reading *inputs*, which represent live system values. However, the same principles apply to *holdings* as well, allowing for consistent usage patterns across both read-only and writable data types.

**Read all fields together:**

Recommendation if only one data vector is to be used:

```python
# First create the data vector (once) that contains all data fields
inputs = shi.create_inputs()
# ... and afterwards read the data into those fields
shi.read_inputs(inputs)
print(inputs)
```

Recommendation if all data vectors are to be used:

```python
# First create the data vector collection (once) that contains
# all supported data vectors which contains all data fields
data = shi.create_data()
# ... and afterwards read the data into those fields
shi.read(data)
print(data.inputs)
```

Create a new data vector for each read operation:

```python
# Create the data vector and read the fields
inputs = shi.read_inputs()
print(inputs)
```

Create a new data vector collection for each read operation:

```python
# Create the data vector collection and read the fields
data = shi.read()
# or ...
data = shi.read_data()
print(data.inputs)
```

**Read a single field:**

For single queries, the (newly created) field is returned.

```python
# Read field by name
op_mode = shi.read_input('operation_mode')
# ... or register index (index 2 is 'operation_mode')
op_mode = shi.read_input(2)
# ... or first create the field (once)
op_mode = shi.create_input('operation_mode')
shi.read_input(op_mode)
# ... or use the definition of the field
op_mode_def = shi.get_input('operation_mode')
op_mode = shi.read_input(op_mode_def)
print(op_mode)
```

**Read a subset:**

It is also possible to read only a selected subset of data fields together. To do this, a new, empty data vector must first be created. The desired fields can then be added to this vector individually. Once all relevant fields have been included, the vector can be read in a single operation, allowing for efficient and targeted data access tailored to specific use cases.

```python
# Create (once) an empty data vector
inputs = shi.create_empty_inputs()
# ..., add the desired data fields
op_mode = inputs.add('operation_mode')
# ...
# Afterwards read the data into those fields
shi.read_inputs(inputs)
print(op_mode)
# (index 2 is 'operation_mode')
print(inputs.get(2))
print(inputs['operation_mode'])
```

### Write

Just like reading, writing to data fields can be done individually or in grouped form using data vectors. This allows multiple configuration values to be updated in a single operation. Only fields for which the user has updated the value are written.

**Write all (updated by the user) fields together:**

Recommendation if only one data vector is to be used:

```python
# First create the data vector (once) that contains all data fields
holdings = shi.create_holdings()
# ..., set the user data
holdings['heating_mode'] = 'Setpoint'
# ... and then write the data from these fields
success = shi.write_holdings(holdings)
```

Recommendation if all data vectors are to be used:

```python
# First create the data vector collection (once) that contains
# all supported data vectors which contains all data fields
data = shi.create_data()
# ..., set the user data
holdings.set('heating_mode', 'Setpoint')
# ... and then write the data from these fields
success = shi.write(data)
# or ...
success = shi.write_data(data)
```

On writing, an empty data vector can also be created and filled, but this generates the same data transfer as above.

```python
# Create (once) an empty data vector
holdings = shi.create_empty_holdings()
# ..., add the desired data fields (index 0 is 'heating_mode')
heating_mode = holdings.add(0)
# ..., set the user data
heating_mode.value = 'Setpoint'
# ... and then write the data from these fields
success = shi.write_holdings(holdings)
```

### Collect

In addition to standard read and write operations, the interface also offers *collect* variants of these functions. A collect operation behaves like a read or write, but without triggering any communication with the controller. Instead, it prepares the data structures internally by collecting all valid fields.

This is particularly useful for inspecting or staging data before transmission, validating field selections, or building reusable data blocks in advance. All read and write capabilities are mirrored in their collect counterparts, ensuring consistent behavior and structure across both modes of operation.

Each valid collect operation schedules at least one transmission to the controller. While the collect itself does not initiate communication, it prepares the necessary data for a future read or write. When the actual transmission is triggered, all scheduled operations are executed together within the same connection session. This bundling ensures efficient communication and minimizes overhead, especially when working with multiple data vectors or fields.

```python
# Collect a write to activate the hot water lock
shi.collect_holding_for_write('lock_hot_water', True)
# Collect all data fields within "holdings_for_heating"
# to write first and then read back afterwards
shi.collect_holdings(holdings_for_heating)
# Collect all data fields within "inputs_for_heating" to read them
shi.collect_inputs(inputs_for_heating)
# Trigger communication
success = shi.send()
```

Attention:

It is technically possible to collect the same instance of a data field multiple times. However, this practice is discouraged, as it can lead to ambiguous behavior. During a write operation, the value is not extracted from the field until the actual transmission occurs. Similarly, during a read, the results are written into the field’s single memory location multiple times. If the same field is collected multiple times, the last value assigned before transmission will take precedence and overwrite any previous ones. To ensure clarity and avoid unintended side effects, each field should be collected only once per transmission, or using multiple instances of the same data field. This ensures that each collected field maintains its own memory space and avoids conflicts during read or write operations. By using distinct field objects, values can be managed independently, and the outcome of each transmission remains predictable and clearly scoped.

## Using aliases

Instead of the predefined names, any (hashable) values can also be used.
However, these must be registered beforehand. This also makes it possible
to "overwrite" existing names or register indices.

There are two ways to register:

**global:**

The aliases are registered in the `LuxtronikDefinitionsList`. They are then available in every newly created data vector.

```python
from luxtronik.shi import create_modbus_tcp

shi = create_modbus_tcp('your.lux.ip.addr')
shi.inputs.register_alias(input_definition_to_alias, any_hashable_alias)

data = shi.read()
print(data.inputs[any_hashable_alias].value)
```

**local:**

The aliases can also only be registered in a specific data vector.

```python
from luxtronik.shi import create_modbus_tcp

shi = create_modbus_tcp('your.lux.ip.addr')

data = shi.read()
data.holdings.register_alias(holding_definition_to_alias, any_hashable_alias)

print(data.holdings[any_hashable_alias].value)
```

## Alternative use cases

### Latest or specific version

It is possible to create the data vector/data object yourself,
but there is no guarantee that the fields they contains
will match the current firmware version of the controller.

Use a specific versions:

```python
from luxtronik.shi import create_modbus_tcp
from luxtronik.shi.holdings import Holdings

shi = create_modbus_tcp('your.lux.ip.addr', version="3.92.0")
holdings = Holdings("3.92.0")
shi.read_holdings(holdings)

# inputs is created with version "3.92.0"
inputs = shi.read_inputs()
```

The special tag "latest" is used to generate the interface
using the latest supported version:

```python
from shi import create_modbus_tcp

shi = create_modbus_tcp('your.lux.ip.addr', version="latest")
```

### Trial-and-error mode

If you pass `None’ as the version, you set the interface to trial-and-error mode.
This means that no attempt is made to bundle read or write accesses,
but that all available fields/definitions are read or written individually (possibly twice).
Errors will occur, but as many operations as possible will be attempted.

```python
from luxtronik.shi import create_modbus_tcp
from luxtronik.shi.interface import LuxtronikSmartHomeData

shi = create_modbus_tcp('your.lux.ip.addr', version=None)

data = LuxtronikSmartHomeData(version=None)
shi.read(data)

holdings = shi.create_holdings()
holdings[1].value = 22.0
holdings[2].value =  5.0
success = shi.write_holdings(holdings)
```

## Customization

**Safe / non-safe:**

Only data fields with a known and verified function are marked as writable by default. This precaution helps prevent unintended changes and ensures that write operations target safe and well-understood parameters. When performing a write or preparing a data vector for writing, a `safe` flag can be used to control how strictly this classification is enforced. If the flag is set, the interface will only write to fields that are both marked as writable and considered safe. Fields that are not writable will be skipped. If the flag is not set, the interface will attempt to write to all fields that carries user data in the vector, regardless of their classification — this includes fields that are not marked as writable and those whose safety is uncertain. This flexibility is particularly useful for testing or exploring undocumented functionality.

```python
shi.write_holding('heating_mode', 'Setpoint', safe=False)
```

**Custom definitions:**

If you discover a new field or want to experiment with one that isn’t yet part of the standard definitions, you can add it manually to your local configuration. If you're confident in its behavior and purpose, please consider reporting it so it can be reviewed and potentially included in future versions of the interface. Since this is not the norm, there is currently no convenient function that allows for easier definition.

```python
shi.inputs.add({
    "index": 5,
    "count": 2,
    "names": "foo"
})
```

## Implementation Details

### Definition vs. field

- **Definition**:
  A definition describes a data field. This includes, among other things,
  the register index where to find the related raw data,
  the number of required registers, the usable names
  and meta-information about the appropriate controller version.

- **Field**:
  A field contains the data that has been read or is to be written
  and makes the raw data available in a user-friendly format.

### Register vs. fields vs. data-blocks

- **Register**:
  A single 16‑bit word addressable by an index.
  Registers are the atomic unit of transfer.

- **Field**:
  Logically related registers. A field can comprise
  one register or several consecutive registers.

- **Data Block**:
  A contiguous address range containing one or more fields.
  Data blocks are used to perform bulk read or write operations in a
  single sequential transfer to minimize communication overhead.

```json
Index
      +------------+      +------------+      +------------+
0x00  | Register 0 |      | Field 0    |      | Data block |
      +------------+      +------------+      +            +
0x01  | Register 1 |      | Field 1    |      |            |
      +------------+      +            +      +            +
0x02  | Register 2 |      |            |      |            |
      +------------+      +------------+      +------------+
0x03  Register 3 do not exist

0x04  Register 4 do not exist
      +------------+      +------------+      +------------+
0x05  | Register 5 |      | Field 5    |      | Data block |
      +------------+      +            +      +            +
0x06  | Register 6 |      |            |      |            |
      +------------+      +------------+      +------------+
0x07  Register 7 do not exist

0x08  Register 8 do not exist
      +------------+      +------------+      +------------+
0x09  | Register 9 |      | Field 9    |      | Data block |
      +------------+      +------------+      +------------+
...
```

### Available definition vs. version-dependent definition

- **Available definitions**:
  All definitions contained in the `LuxtronikDefinitionsList` are designated
  with the term "available definitions". This includes all definitions ever used.

- **Version-dependent definitions**:
  The definitions themselves may contain version information specifying
  in which version the described field is included. This is used to
  determine a subset that matches a specific firmware version of the controller.
  Fields without version information are always included.
  Note: If the desired version is "None",
  all "available" are considered as "version-dependent".

```json
Available:
- {index: 0, since: 1.0, until: 2.9}
- {index: 1, since: 2.2            }
- {index: 4,             until: 1.5}
- {index: 5, since: 2.4, until: 3.0}
- {index: 6, since: 1.3            }
- {index: 8,                       }
- {index: 9,             until: 2.0}

Version-dependent on v0.3:
- {index: 4,             until: 1.5}
- {index: 8,                       }
- {index: 9,             until: 2.0}

Version-dependent on v1.1:
- {index: 0, since: 1.0, until: 2.9}
- {index: 4,             until: 1.5}
- {index: 8,                       }
- {index: 9,             until: 2.0}

Version-dependent on v2.6:
- {index: 0, since: 1.0, until: 2.9}
- {index: 1, since: 2.2            }
- {index: 5, since: 2.4, until: 3.0}
- {index: 6, since: 1.3            }
- {index: 8,                       }

Version-dependent on v3.2:
- {index: 1, since: 2.2            }
- {index: 6, since: 1.3            }
- {index: 8,                       }

Version-dependent on None:
- {index: 0, since: 1.0, until: 2.9}
- {index: 1, since: 2.2            }
- {index: 4,             until: 1.5}
- {index: 5, since: 2.4, until: 3.0}
- {index: 6, since: 1.3            }
- {index: 8,                       }
- {index: 9,             until: 2.0}
```

### Data-blocks vs. telegrams

- **Data-blocks**:
  A data block bundles all fields that can be read or written together.
  However, when writing, only fields for which the user has set data are bundled.
  The resulting address space can be read with a single telegram,
  or the contiguous raw data can be written with a single telegram.

- **Telegrams**:
  A telegram defines a read or write operation to be performed.
  Several telegrams can be handled in one transmission.

<!-- markdownlint-enable MD013 -->