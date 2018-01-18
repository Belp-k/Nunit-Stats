class AssemblyGenerator(object):
    """Generates a matrix representing the data extracted from a
    NUnit test assembly report.
    Each line is as follows:
    Fixture name; Test name; Test duration
    """

    def __init__(self, assembly: "A NUnitTestAssembly"):
        self._assembly = assembly

    def generate_matrix(self):
        matrix = [["Fixture name", "Test name", "Test duration"], []]
        for fixture in self._assembly.fixtures:
            for (j, test) in enumerate(fixture.tests):
                line = [fixture.name, test.name, test.duration]
                matrix.append(line)
        return matrix

    def get_name(self):
        return self._assembly.name
