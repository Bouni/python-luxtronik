from luxtronik import LuxtronikAllData, Luxtronik


class FakeLuxtronik(Luxtronik):

    def __init__(self):
        LuxtronikAllData.__init__(self)
        for idx, field in self.parameters:
            field.raw = idx
        for idx, field in self.calculations:
            field.raw = idx
        for idx, field in self.visibilities:
            field.raw = idx