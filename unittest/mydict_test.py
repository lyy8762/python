import unittest
from myDict import Dict
from HTMLTestRunner import HTMLTestRunner


class MyTestCase(unittest.TestCase):
    def test_something(self):
        d = Dict(a=1,b='test')
        self.assertEqual(d.a, 1)
        self.assertEqual(d.b, 'test')

    def test_something2(self):
        self.assertEqual(True, True)

    def test_something3(self):
        self.assertEqual(True, True)

if __name__ == '__main__':
    testunit=unittest.TestSuite()
    #testunit.addTest(element("MyTestCase"))
    testunit.addTest(MyTestCase('test_something'))
    testunit.addTest(MyTestCase('test_something2'))
    testunit.addTest(MyTestCase('test_something3'))

    filename="./report.html"
    fp=file(filename,'wb')
    runner =HTMLTestRunner(stream=fp,title='Report_title',description='Report_description')
    runner.run(testunit)