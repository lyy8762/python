import unittest
from HTMLTestRunner import HTMLTestRunner


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)


if __name__ == '__main__':
    testunit=unittest.TestSuite()
    #testunit.addTest(element("MyTestCase"))
    testunit.addTest(MyTestCase('test_something'))
    filename="C:/Users/lyy/Desktop/Learning/python/unittest/xxx.html"
    fp=file(filename,'wb')
    runner =HTMLTestRunner.HTMLTestRunner(stream=fp,title='Report_title',description='Report_description')
    runner.run(testunit)
