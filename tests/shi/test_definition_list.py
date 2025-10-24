import re

from luxtronik.datatypes import Base
from luxtronik.definitions.holdings import HOLDINGS_DEFINITIONS_LIST
from luxtronik.definitions.inputs import INPUTS_DEFINITIONS_LIST
from luxtronik.shi.common import parse_version

KEY_IDX = "index"
KEY_COUNT = "count"
KEY_NAMES = "names"
KEY_TYPE = "type"
KEY_WRT = "writeable"
KEY_SINCE = "since"
KEY_UNTIL = "until"
KEY_DESC = "description"


class RunTestDefinitionList:

    # override this
    definitions = None

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

            # data_type
            if KEY_TYPE in definition:
                assert issubclass(definition[KEY_TYPE], Base), \
                    f"{KEY_TYPE} must be inherit from 'Base': {definition}"

            # writeable
            if KEY_WRT in definition:
                assert isinstance(definition[KEY_WRT], bool), \
                    f"{KEY_WRT} must be of type 'bool': {definition}"

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
                assert sanitized == name, \
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

    def test_data_type(self):
        for definition in self.definitions:
            if KEY_TYPE in definition:
                data_type = definition.get(KEY_TYPE, Base)
                assert data_type is not None, \
                    f"Type must be set: {definition}"

    def test_since(self):
        for definition in self.definitions:
            if KEY_SINCE in definition:
                since = definition.get(KEY_SINCE, "")
                parsed = parse_version(since)
                assert parsed is not None, \
                    f"Since must be a valid version instead of {since}: {definition}"

    def test_until(self):
        for definition in self.definitions:
            if KEY_UNTIL in definition:
                until = definition.get(KEY_UNTIL, "")
                parsed = parse_version(until)
                assert parsed is not None, \
                    f"Until must be a valid version instead of {until}: {definition}"

###############################################################################
# Tests
###############################################################################

class TestHoldingsDefinitionList(RunTestDefinitionList):

    definitions = HOLDINGS_DEFINITIONS_LIST


class TestInputsDefinitionList(RunTestDefinitionList):

    definitions = INPUTS_DEFINITIONS_LIST