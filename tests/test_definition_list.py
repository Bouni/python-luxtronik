import re

from luxtronik.common import parse_version
from luxtronik.datatypes import Base
from luxtronik.definitions import LuxtronikDefinition
from luxtronik.definitions.calculations import CALCULATIONS_DEFINITIONS_LIST
from luxtronik.definitions.holdings import HOLDINGS_DEFINITIONS_LIST
from luxtronik.definitions.inputs import INPUTS_DEFINITIONS_LIST
from luxtronik.definitions.parameters import PARAMETERS_DEFINITIONS_LIST
from luxtronik.definitions.visibilities import VISIBILITIES_DEFINITIONS_LIST


KEY_IDX = "index"
KEY_COUNT = "count"
KEY_NAMES = "names"
KEY_TYPE = "type"
KEY_WRT = "writeable"
KEY_DATATYPE = "datatype"
KEY_UNIT = "unit"
KEY_DEFAULT = "default"
KEY_RANGE = "range"
KEY_MIN = "min"
KEY_MAX = "max"
KEY_SINCE = "since"
KEY_UNTIL = "until"
KEY_DESC = "description"


class RunTestDefinitionList:

    # override this
    definitions = None

    # use True for SHI and false for CFI
    do_lower_case_test = True

    def get_names(self, definition):
        names = definition.get(KEY_NAMES, [])
        if isinstance(names, str):
            names = [names]
        return names

    def test_structure(self):
        for definition in self.definitions:

            # index
            assert KEY_IDX in definition, \
                f"{KEY_IDX} not defined: {definition}"
            assert isinstance(definition[KEY_IDX], int), \
                f"{KEY_IDX} must be of type 'int': {definition}"

            # count
            if KEY_COUNT in definition:
                assert isinstance(definition[KEY_COUNT], int), \
                    f"{KEY_COUNT} must be of type 'int': {definition}"

            # names
            if KEY_NAMES in definition:
                assert isinstance(definition[KEY_NAMES], list) \
                        or isinstance(definition[KEY_NAMES], str), \
                    f"{KEY_NAMES} must be of type 'list' or 'str': {definition}"
                if isinstance(definition[KEY_NAMES], list):
                    for name in definition[KEY_NAMES]:
                        assert isinstance(name, str), f"Entry of {KEY_NAMES} " \
                            f"must be of type 'int': {definition}"

            # field_type
            if KEY_TYPE in definition:
                assert issubclass(definition[KEY_TYPE], Base), \
                    f"{KEY_TYPE} must be inherit from 'Base': {definition}"

            # writeable
            if KEY_WRT in definition:
                assert isinstance(definition[KEY_WRT], bool), \
                    f"{KEY_WRT} must be of type 'bool': {definition}"

            # data type
            if KEY_DATATYPE in definition:
                assert isinstance(definition[KEY_DATATYPE], str), \
                    f"{KEY_DATATYPE} must be of type 'str': {definition}"

            # unit
            if KEY_UNIT in definition:
                assert isinstance(definition[KEY_UNIT], str), \
                    f"{KEY_UNIT} must be of type 'str': {definition}"

            # default (raw value)
            if KEY_DEFAULT in definition:
                assert isinstance(definition[KEY_DEFAULT], int), \
                    f"{KEY_DEFAULT} must be of type 'int': {definition}"

            # range (raw value)
            if KEY_RANGE in definition:
                assert isinstance(definition[KEY_RANGE], dict), \
                    f"{KEY_RANGE} must be of type 'dict': {definition}"

            # range - min (raw value)
            if KEY_RANGE in definition and KEY_MIN in definition[KEY_RANGE]:
                assert isinstance(definition[KEY_RANGE][KEY_MIN], int), \
                    f"{KEY_MIN} must be of type 'int': {definition}"

            # range - max (raw value)
            if KEY_RANGE in definition and KEY_MAX in definition[KEY_RANGE]:
                assert isinstance(definition[KEY_RANGE][KEY_MAX], int), \
                    f"{KEY_MAX} must be of type 'int': {definition}"

            # since
            if KEY_SINCE in definition:
                assert isinstance(definition[KEY_SINCE], str), \
                    f"{KEY_SINCE} must be of type 'str': {definition}"

            # until
            if KEY_UNTIL in definition:
                assert isinstance(definition[KEY_UNTIL], str), \
                    f"{KEY_UNTIL} must be of type 'str': {definition}"

            # description
            if KEY_DESC in definition:
                assert isinstance(definition[KEY_DESC], str), \
                    f"{KEY_DESC} must be of type 'str': {definition}"

    def test_index(self):
        for definition in self.definitions:
            idx = definition.get(KEY_IDX, 0)
            assert idx >= 0, \
            f"The index must be greater or equal than zero: {definition}"

    def test_index_ascending(self):
        prev = self.definitions[0]

        for definition in self.definitions:
            prev_idx = prev.get(KEY_IDX, -1)
            this_idx = definition.get(KEY_IDX, 0)
            assert prev_idx <= this_idx, \
                "The definitions must be arranged in ascending order. " \
                "This allows us to avoid sorting them afterwards." \
                f"this  = {definition}" \
                f"other = {prev}"
            prev = definition

    def test_count(self):
        for definition in self.definitions:
            count = definition.get(KEY_COUNT, 1)
            assert count > 0, \
                f"Count field must be greater than zero: {definition}"

    def test_name_valid(self):
        for definition in self.definitions:
            names = self.get_names(definition)
            for name in names:
                sanitized = re.sub(r"[^a-z0-9_]", "", name)
                assert not self.do_lower_case_test or sanitized == name, \
                    f"The name may only contain a-z0-9_ {definition}"
                assert sanitized != "", \
                    f"Name must not be empty. {definition}"
                try:
                    int(name)
                    assert False, "Name must not be a number."
                except Exception:
                    pass

    def test_name_unique(self):
        length = len(self.definitions)

        for i in range(length):
            i_def = self.definitions[i]
            i_names = self.get_names(i_def)
            for j in range(i + 1, length):
                j_def = self.definitions[j]
                j_names = self.get_names(j_def)
                for i_name in i_names:
                    for j_name in j_names:
                        assert i_name!= j_name, \
                            "All names of the same type must be unique. " \
                            f"this  = {i_def}" \
                            f"other = {j_def}"

    def test_field_type(self):
        for definition in self.definitions:
            field_type = definition.get(KEY_TYPE, None)
            assert issubclass(field_type, Base), \
                f"Type must be set: {definition}"

    def test_data_type(self):
        for definition in self.definitions:
            if KEY_DATATYPE in definition:
                data_type = definition[KEY_DATATYPE]
                assert data_type in LuxtronikDefinition.VALID_DATA_TYPES, \
                    f"Datatype must be set correctly: {definition}"

    def test_since(self):
        for definition in self.definitions:
            if KEY_SINCE in definition:
                since = definition[KEY_SINCE]
                parsed = parse_version(since)
                assert parsed is not None, \
                    f"Since must be a valid version instead of {since}: {definition}"

    def test_until(self):
        for definition in self.definitions:
            if KEY_UNTIL in definition:
                until = definition[KEY_UNTIL]
                parsed = parse_version(until)
                assert parsed is not None, \
                    f"Until must be a valid version instead of {until}: {definition}"

###############################################################################
# Tests
###############################################################################

class TestCalculationsDefinitionList(RunTestDefinitionList):

    definitions = CALCULATIONS_DEFINITIONS_LIST
    do_lower_case_test = False


class TestHoldingsDefinitionList(RunTestDefinitionList):

    definitions = HOLDINGS_DEFINITIONS_LIST
    do_lower_case_test = True


class TestInputsDefinitionList(RunTestDefinitionList):

    definitions = INPUTS_DEFINITIONS_LIST
    do_lower_case_test = True


class TestParametersDefinitionList(RunTestDefinitionList):

    definitions = PARAMETERS_DEFINITIONS_LIST
    do_lower_case_test = False


class TestVisibilitiesDefinitionList(RunTestDefinitionList):

    definitions = VISIBILITIES_DEFINITIONS_LIST
    do_lower_case_test = False