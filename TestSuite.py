import unittest
import HtmlTestRunner

from createAccountTests import CreateAccountTests
from cartTests import CartTests
from singInTests import SingInTests
from webElementsTests import WebElementsTests

class TestSuite(unittest.TestCase):

    def test_suite(self):

        tests_to_run = unittest.TestSuite()

        tests_to_run.addTests([
            unittest.defaultTestLoader.loadTestsFromTestCase(CreateAccountTests),
            unittest.defaultTestLoader.loadTestsFromTestCase(CartTests),
            unittest.defaultTestLoader.loadTestsFromTestCase(SingInTests),
            unittest.defaultTestLoader.loadTestsFromTestCase(WebElementsTests)
        ])

        runner = HtmlTestRunner.HTMLTestRunner(
            combine_reports=True,
            report_title='Magento2 Luma',
            report_name='Magento Luma tests result'
        )

        runner.run(tests_to_run)


