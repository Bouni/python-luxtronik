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

In order to dump all known values from the Luxtronik controller, you can use
the `dump-luxtronik.py` script in the following way:

```python
PYTHONPATH=. ./scripts/dump-luxtronik.py 192.168.1.5
```

The output of this script can be used to backup all values (e.g. before
modifying them) and to get a better understanding about parameters (e.g. by
looking for differences when comparing the output after doing some changes
locally, etc.).

Alternatively, you can use the `dump-changes.py` script to output only changed values:

```python
PYTHONPATH=. ./scripts/dump-changes.py 192.168.1.5
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

print(parameters.get("ID_Ba_Hz_akt").options) # returns a list of possible values to write, ['Automatic', 'Second heatsource', 'Party', 'Holidays', 'Off'] for example
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
