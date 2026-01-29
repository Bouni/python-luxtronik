
from luxtronik import (
  Parameters,
  Calculations,
  Visibilities,
  LuxtronikSocketInterface,
)


class TestLuxtronikSocketInterface:

    def test_parse(self):
        lux = LuxtronikSocketInterface('host')
        parameters = Parameters()
        calculations = Calculations()
        visibilities = Visibilities()

        n = 2000
        t = list(range(0, n + 1))

        lux._parse(parameters, t)
        p = parameters.get(n)
        assert p.name == f"unknown_parameter_{n}"
        assert p.raw == n

        lux._parse(calculations, t)
        c = calculations.get(n)
        assert c.name == f"unknown_calculation_{n}"
        assert c.raw == n

        lux._parse(visibilities, t)
        v = visibilities.get(n)
        assert v.name == f"unknown_visibility_{n}"
        assert v.raw == n

        n = 10
        t = list(range(0, n + 1))

        lux._parse(parameters, t)
        for definition, field in parameters.data.pairs():
            if definition.index > n:
                assert field.raw is None

        lux._parse(calculations, t)
        for definition, field in calculations.data.pairs():
            if definition.index > n:
                assert field.raw is None

        lux._parse(visibilities, t)
        for definition, field in visibilities.data.pairs():
            if definition.index > n:
                assert field.raw is None