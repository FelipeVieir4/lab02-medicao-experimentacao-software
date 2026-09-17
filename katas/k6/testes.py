import codewars_test as test
from solution import encode, decode


@test.describe("Fixed Tests")
def fixed_tests():
    @test.it("Basic Test Cases")
    def basic_test_cases():
        test.assert_equals(encode('hello'), 'h2ll4')
        test.assert_equals(encode('How are you today?'), 'H4w 1r2 y45 t4d1y?')
        test.assert_equals(encode('This is an encoding test.'), 'Th3s 3s 1n 2nc4d3ng t2st.')
        test.assert_equals(decode('h2ll4'), 'hello')
