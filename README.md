# Luxtronik

python-luxtronik is a library that allow you to interact with a Luxtronik heatpump controller.

## Example
```
from luxtronik import Luxtronik

l = Luxtronik('192.168.1.23', 8889)
l.get_data()
```

You'll get a huge dict as result with already parsed and converted data.

```
l.set_data("ID_Einst_BWS_akt", 48)
```

Sets the hot-water target temperature to 48 degrees Celsius.
