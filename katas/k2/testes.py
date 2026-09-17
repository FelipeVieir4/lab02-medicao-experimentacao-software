import codewars_test as test
from solution import balance


@test.describe("Fixed Tests")
def fixed_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        test.assert_equals(balance("","") , "Balance")
        test.assert_equals(balance("!!","??") , "Right")
        test.assert_equals(balance("!??","?!!") , "Left")
        test.assert_equals(balance("!?!!","?!?") , "Left")
        test.assert_equals(balance("!!???!????","??!!?!!!!!!!") , "Balance")
