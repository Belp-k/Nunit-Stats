from nunit_test import NUnitTest
from nunit_test_fixture import NUnitTestFixture
from nunit_test_assembly import NUnitTestAssembly

import xml.etree.ElementTree as ET
import sys


class NUnitXmlReader(object):
    """XML reader to retrieve the list of NUnit test assemblies of a given NUnit report.
    """

    def __init__(self, filename: str):
        try:
            tree = ET.parse(filename)
        except:
            print(filename, "is not a valid XML file")
            sys.exit(1)

        self._root = tree.getroot()

    def _get_element_name(self, element: "An ElementTree node") -> str:
        return element.attrib.get("name")

    def _get_element_duration_in_ms(self, element: "An ElementTree node") -> int:
        # Durations are expressed in seconds in NUnit test report
        return round(float(element.attrib.get("duration")) * 1000)

    # Retrieves all test assemblies from the parsed NUnit test report
    # return    : the ElementTree list of found test assemblies
    def _get_assemblies(self) -> list:
        # All 'test-suite' nodes of type 'Assembly'
        return self._root.findall(".//test-suite/[@type='Assembly']")

    # Retrieves all test fixtures from the input test suite as an ElementTree node
    # arg       : the ElementTree note of a test suite
    # return    : the ElementTree list of found test fixtures
    def _get_fixtures(self, suite: "A test-suite node of type Assembly") -> list:
        # All 'test-suite' nodes of type 'TestFixture'
        return suite.findall(".//test-suite/[@type='TestFixture']")

    # Retrieves all tests from the input text fixture as an ElementTree node
    # arg       : the ElementTree note of a test fixture
    # return    : the ElementTree list of found tests
    def _get_tests(self, fixture: "A test-suite node of type TestFixture") -> list:
        return fixture.findall(".//test-case")

    # Builds a list of NUnitTest objects
    # arg       : the ElementTree list of tests
    # return    : the NUnitTest list
    def _build_nunit_tests(self, tests: list) -> list:
        nunit_tests = []
        for test in tests:
            test_name = self._get_element_name(test)
            test_order = tests.index(test) + 1
            test_duration_ms = self._get_element_duration_in_ms(test)

            nunit_tests.append(NUnitTest(test_name, test_order, test_duration_ms))
        return nunit_tests

    # Builds a list of NUnitTestFixture objects
    # arg       : the ElementTree list of test fixtures
    # return    : the NUnitTestFixture list
    def _build_nunit_test_fixtures(self, fixtures: list) -> list:
        nunit_test_fixtures = []
        for fixture in fixtures:
            fixture_name = self._get_element_name(fixture)
            fixture_order = fixtures.index(fixture) + 1
            fixture_duration = self._get_element_duration_in_ms(fixture)

            parsed_tests = self._get_tests(fixture)
            test_cases = self._build_nunit_tests(parsed_tests)

            nunit_test_fixtures.append(NUnitTestFixture(fixture_name, fixture_order, fixture_duration, test_cases))
        return nunit_test_fixtures

    # Builds a list of NUnitTestAssembly objects
    # return    : the NUnitTestAssembly list
    def build_nunit_test_assemblies(self) -> list:
        assemblies = self._get_assemblies()
        nunit_test_assemblies = []
        for assembly in assemblies:
            assembly_name = self._get_element_name(assembly)
            assembly_duration = self._get_element_duration_in_ms(assembly)

            parsed_fixtures = self._get_fixtures(assembly)
            fixtures = self._build_nunit_test_fixtures(parsed_fixtures)

            nunit_test_assemblies.append(NUnitTestAssembly(assembly_name, assembly_duration, fixtures))
        return nunit_test_assemblies
