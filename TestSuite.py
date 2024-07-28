import unittest
import HtmlTestRunner

from tests.createAccountTests import CreateAccountTests
from tests.singInTests import SingInTests
from tests.searchAndFilterProductsTests import SearchAndFilterProducts
from tests.myAccountTests import MyAccount
from tests.shoppingCartTests import CartTests

class TestSuite(unittest.TestCase):

    def test_suite(self):

        tests_to_run = unittest.TestSuite()

        tests_to_run.addTests([
            unittest.defaultTestLoader.loadTestsFromTestCase(CreateAccountTests),
            unittest.defaultTestLoader.loadTestsFromTestCase(SingInTests),
            unittest.defaultTestLoader.loadTestsFromTestCase(SearchAndFilterProducts),
            unittest.defaultTestLoader.loadTestsFromTestCase(MyAccount),
            unittest.defaultTestLoader.loadTestsFromTestCase(CartTests)
        ])

        runner = HtmlTestRunner.HTMLTestRunner(
            combine_reports=True,
            report_title='Magento2 Luma',
            report_name='Magento Luma tests result'
        )

        runner.run(tests_to_run)