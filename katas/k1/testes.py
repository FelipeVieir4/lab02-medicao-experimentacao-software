import codewars_test as test
from solution import connect_four_place


@test.describe("Fixed Tests")
def fixed_tests():
	@test.it("Basic Test Cases")
	def basic_test_cases():
		test.assert_equals(
			connect_four_place([0, 1, 2, 5, 6]),
			[
				['-', '-', '-', '-', '-', '-', '-'],
				['-', '-', '-', '-', '-', '-', '-'],
				['-', '-', '-', '-', '-', '-', '-'],
				['-', '-', '-', '-', '-', '-', '-'],
				['-', '-', '-', '-', '-', '-', '-'],
				['Y', 'R', 'Y', '-', '-', 'R', 'Y'],
			],
		)
		test.assert_equals(
			connect_four_place([0, 1, 2, 5, 6, 2, 0, 0]),
			[
				['-', '-', '-', '-', '-', '-', '-'],
				['-', '-', '-', '-', '-', '-', '-'],
				['-', '-', '-', '-', '-', '-', '-'],
				['R', '-', '-', '-', '-', '-', '-'],
				['Y', '-', 'R', '-', '-', '-', '-'],
				['Y', 'R', 'Y', '-', '-', 'R', 'Y'],
			],
		)
