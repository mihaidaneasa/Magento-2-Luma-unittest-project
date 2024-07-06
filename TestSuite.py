import unittest
import HtmlTestRunner

from createAccountTests import CreateAccountTests
from singInTests import SingInTests
from webElementsTests import WebElementsTests
from myAccountTests import MyAccount
from shopingCartTests import CartTests


class TestSuite(unittest.TestCase):

    def test_suite(self):

        tests_to_run = unittest.TestSuite()

        tests_to_run.addTests([
            unittest.defaultTestLoader.loadTestsFromTestCase(CreateAccountTests),
            unittest.defaultTestLoader.loadTestsFromTestCase(SingInTests),
            unittest.defaultTestLoader.loadTestsFromTestCase(WebElementsTests),
            unittest.defaultTestLoader.loadTestsFromTestCase(MyAccount),
            unittest.defaultTestLoader.loadTestsFromTestCase(CartTests)
        ])

        runner = HtmlTestRunner.HTMLTestRunner(
            combine_reports=True,
            report_title='Magento2 Luma',
            report_name='Magento Luma tests result'
        )

        runner.run(tests_to_run)


