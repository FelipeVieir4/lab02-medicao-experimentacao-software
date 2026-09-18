import codewars_test as test
from solution import to_nato


@test.describe("Basic Tests")
def basic_tests():
	@test.it("Basic Test Cases")
	def basic_test_cases():
		test.assert_equals(
			to_nato('If you can read'),
			"India Foxtrot Yankee Oscar Uniform Charlie Alfa November Romeo Echo Alfa Delta",
		)
		test.assert_equals(
			to_nato('Did not see that coming'),
			"Delta India Delta November Oscar Tango Sierra Echo Echo Tango Hotel Alfa Tango Charlie Oscar Mike India November Golf",
		)
		test.assert_equals(to_nato('.d?d!'), '. Delta ? Delta !')
