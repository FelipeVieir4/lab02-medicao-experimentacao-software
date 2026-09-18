import codewars_test as test

try:
	from solution import nbMonths as nb_months
except ImportError:
	from solution import nb_months


@test.describe("Fixed Tests")
def fixed_tests():
	@test.it("Basic Test Cases")
	def basic_test_cases():
		test.assert_equals(nb_months(2000, 8000, 1000, 1.5), [6, 766])
		test.assert_equals(nb_months(12000, 8000, 1000, 1.5), [0, 4000])
		test.assert_equals(nb_months(8000, 12000, 500, 1), [8, 597])
		test.assert_equals(nb_months(18000, 32000, 1500, 1.25), [8, 332])
		test.assert_equals(nb_months(7500, 32000, 300, 1.55), [25, 122])
