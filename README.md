# luxtronik

python-luxtronik is a Python library that allows you to interact with a
Luxtronik heat pump controller programmatically. This enables you to read
values from the heat pump and write values back to the heat pump, thus
influencing its behaviour.

## BACKGROUND

Luxtronik is a heat pump control system developed by Alpha Innotec that is used
by several manufactures. Essentially it is the part of the heat pump system
that the user can interact with locally via display and setting dial.

This library uses a TCP socket that is exposed via network (typically on port
8889). Values can be read from and written to the heat pump, essentially making
it controllable from within a Python program.

This allows you, for example, to change the temperature settings of your heat
pump or get current temperature values from the heat pump, similar to what you
can do when controlling the heat pump locally on-site.

This TCP socket is meant to be used by the vendor to control the heat pump
via various mobile apps and desktop applications.

Unfortunately there is no official documentation of this API, and how to
interact with it. As such, the **implementation is heavily based on reverse
engineering**.

## INSTALLATION

This library can be installed via pip by issuing the following command:

```shell
pip install luxtronik
```

Afterwards the module can be used like any other Python module, i.e. it can
be imported via `import luxtronik` from your Python scripts.

## DOCUMENTATION

There is no automatically rendered documentation of this library available yet,
so you'll have to fall back to use the source code itself as documentation. It
can be found in the [luxtronik](luxtronik/) directory.

## EXAMPLE USAGE

### READING VALUES FROM THE HEAT PUMP

The following example reads in data from the heat pump:

```python
from luxtronik import Luxtronik

l = Luxtronik('192.168.1.23', 8889)
calculations, parameters, visibilities = l.read()

t_forerun = calculations.get("ID_WEB_Temperatur_TVL")

# alternatively get also works with numerical ID values

t_forerun = calculations.get(10)

print(t_forerun) # this returns the temperature value of the forerun, 22.7 for example
print(t_forerun.unit) # gives you the unit of the value if known, °C for example

# calculations holds measurement values
# check https://github.com/Bouni/luxtronik/blob/master/luxtronik/calculations.py for values you might need

# parameters holds parameter values
# check https://github.com/Bouni/luxtronik/blob/master/luxtronik/parameters.py for values you might need

# visibilitys holds visibility values, the function of visibilities is not clear at this point
# check https://github.com/Bouni/luxtronik/blob/master/luxtronik/visibilities.py for values you might need
```

### SCRIPTS AND COMMAND LINE INTERFACE (CLI)

Once installed, the luxtronik package provides several scripts that can be used
to interact with your heatpump. Those scripts can be invoked like regular
commands from the command line.

### DISCOVERY OF AVAILABLE HEATPUMPS WITHIN THE NETWORK

Heat pumps can be discovered in a network by sending broadcast packages that the Luxtronik controller will reply to. This can be done with the `discover` sub command in the following way:

```sh
luxtronik discover
```



```sh
1 heatpump(s) reported back                                                                                                                                                                                      │
Heat pump #0 -> IP address: 192.168.178.123 port: 8889
```

### DUMP ALL DATA

To get all data available you can either use the CLI:

```sh
luxtronik dump 192.168.178.123 8889
```

or call the script that comes with the python package:

```python
PYTHONPATH=. ./scripts/dump_luxtronik.py 192.168.178.123 8889
```

The output of this script can be used to backup all values (e.g. before
modifying them) and to get a better understanding about parameters (e.g. by
looking for differences when comparing the output after doing some changes
locally, etc.).

You'll get a long list of all data, like this (truncated):

```txt
================================================================================                                                                                                                                 │
                                   Parameter                                                                                                                                                                     │
================================================================================                                                                                                                                 │
Number: 0     Name: ID_Transfert_LuxNet                                          Type: Unknown              Value: 0                                                                                             │
Number: 1     Name: ID_Einst_WK_akt                                              Type: Celsius              Value: 1.0                                                                                           │
Number: 2     Name: ID_Einst_BWS_akt                                             Type: Celsius              Value: 50.0                                                                                          │
Number: 3     Name: ID_Ba_Hz_akt                                                 Type: HeatingMode          Value: Off                                                                                           │
Number: 4     Name: ID_Ba_Bw_akt                                                 Type: HotWaterMode         Value: Automatic                                                                                     │
Number: 5     Name: ID_Ba_Al_akt                                                 Type: Unknown              Value: 4                                                                                             │
Number: 6     Name: ID_SU_FrkdHz                                                 Type: Unknown              Value: 1167609600                                                                                    │
Number: 7     Name: ID_SU_FrkdBw                                                 Type: Unknown              Value: 1167609600                                                                                    │
Number: 8     Name: ID_SU_FrkdAl                                                 Type: Unknown              Value: 0                                                                                             │
Number: 9     Name: ID_Einst_HReg_akt                                            Type: Unknown              Value: 0                                                                                             │
Number: 10    Name: ID_Einst_HzHwMAt_akt                                         Type: Unknown              Value: -200                                                                                          │
Number: 11    Name: ID_Einst_HzHwHKE_akt                                         Type: Celsius              Value: 33.0                                                                                          │
Number: 12    Name: ID_Einst_HzHKRANH_akt                                        Type: Celsius              Value: 22.0                                                                                          │
Number: 13    Name: ID_Einst_HzHKRABS_akt                                        Type: Celsius              Value: 0.0                                                                                           │
Number: 14    Name: ID_Einst_HzMK1E_akt                                          Type: Unknown              Value: 330                                                                                           │
Number: 15    Name: ID_Einst_HzMK1ANH_akt                                        Type: Unknown              Value: 220                                                                                           │
Number: 16    Name: ID_Einst_HzMK1ABS_akt                                        Type: Unknown              Value: 0
...
```

### SHOW CHANGES

To get all values that change live diplayed you can either use the CLI:

```sh
luxtronik changes 192.168.178.123 8889
```

or call the script that comes with the python package:

```python
PYTHONPATH=. ./scripts/dump_changes.py 192.168.178.123 8889
```

You'll get a list of all values as they change:

```txt
================================================================================                                                                                                                                 │
calc: Number: 15    Name: ID_WEB_Temperatur_TA                                         Value: 27.2 -> 27.0                                                                                                       │
calc: Number: 73    Name: ID_WEB_Time_VDStd_akt                                        Value: 47189 -> 47192                                                                                                     │
calc: Number: 75    Name: ID_WEB_Time_HRW_akt                                          Value: 353732 -> 353735                                                                                                   │
calc: Number: 134   Name: ID_WEB_AktuelleTimeStamp                                     Value: 2023-07-12 11:47:43 -> 2023-07-12 11:47:46                                                                         │
calc: Number: 20    Name: ID_WEB_Temperatur_TWA                                        Value: 24.8 -> reverted                                                                                                   │
calc: Number: 178   Name: ID_WEB_LIN_UH                                                Value: 3.1 -> reverted                                                                                                    │
calc: Number: 180   Name: ID_WEB_LIN_HD                                                Value: 15.46 -> reverted                                                                                                  │
calc: Number: 181   Name: ID_WEB_LIN_ND                                                Value: 15.67 -> reverted                                                                                                  │
calc: Number: 232   Name: Vapourisation_Temperature                                    Value: 25.2 -> reverted                                                                                                   │
calc: Number: 233   Name: Liquefaction_Temperature                                     Value: 24.8 -> reverted                                                                                                   │
calc: Number: 10    Name: ID_WEB_Temperatur_TVL                                        Value: 32.7 -> 32.8                                                                                                       │
calc: Number: 13    Name: ID_WEB_Temperatur_TRL_ext                                    Value: 26.2 -> 26.1
```

### WRITING VALUES TO HEAT PUMP

The following example writes data to the heat pump:

```python
from luxtronik import Luxtronik, Parameters

l = Luxtronik('192.168.1.23', 8889)

parameters = Parameters()
heating_mode = parameters.set("ID_Ba_Hz_akt", "Party")
l.write(parameters)

# If you're not sure what values to write, you can get all available options:

print(parameters.get("ID_Ba_Hz_akt").options()) # returns a list of possible values to write, ['Automatic', 'Second heatsource', 'Party', 'Holidays', 'Off'] for example
```

**NOTE:** Writing values to the heat pump is particulary dangerous as this is
an undocumented API. By default a safe guard is in place, which will prevent
writing parameters that are not (yet) understood.

You can disable that safeguard by passing `safe=False` to the Luxtronik class
during initialization:

```python
from luxtronik import Luxtronik

l = Luxtronik('192.168.1.23', 8889, safe=False)
```

## CONTRIBUTION

The source code is maintained using git and lives in a dedicated
[GitHub repository][github-repo].

Contributions are, of course, highly welcome.

Besides providing improvements to the code itself, there is also help needed in
other areas, in particular the documentation as well as understanding the
parameters that are provided by the heat pump. Also reporting bugs and/or
submitting feature requests via the [issue tracker][issue-tracker] is helpful.

The fastest way to provide improvements to the code is is to use
[pull requests][pull-request-doc].

## LICENSE

> Permission is hereby granted, free of charge, to any person obtaining a
> copy of this software and associated documentation files (the “Software”),
> to deal in the Software without restriction, including without limitation
> the rights to use, copy, modify, merge, publish, distribute, sublicense,
> and/or sell copies of the Software, and to permit persons to whom the
> Software is furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in
> all copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
> THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
> LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
> FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
> DEALINGS IN THE SOFTWARE.

[github-repo]: https://github.com/Bouni/python-luxtronik
[issue-tracker]: https://github.com/Bouni/python-luxtronik/issues
[pull-request-doc]: https://docs.github.com/articles/about-pull-requests
