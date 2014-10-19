from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebdriver
import unittest
import sys


class ExampleTestCase(unittest.TestCase):

    def setUp(self):
        self.driver = ChromeWebdriver()

    def test_example(self):
        self.driver.get("http://www.google.com")
        self.assertEqual(self.driver.title, "Google")

    def tearDown(self):
        self.driver.quit()